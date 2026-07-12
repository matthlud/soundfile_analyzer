"""Background playback manager with responsive console and control commands.

Enables playing audio in a background thread while keeping the console
responsive for issuing control commands (play, stop, next, restart, etc).
"""

from __future__ import annotations

import threading
import time
import os
from enum import Enum
from typing import Optional, Callable

try:
    import vlc
except ImportError:
    vlc = None

try:
    import librosa
except ImportError:
    librosa = None

PlaybackDisplay = None
try:
    from .playback_ui import PlaybackDisplay
except ImportError:
    try:
        from playback_ui import PlaybackDisplay
    except ImportError:
        PlaybackDisplay = None


class PlaybackState(Enum):
    """Enumeration of playback states."""
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"


class PlaybackManager:
    """Manages background audio playback with console control commands.
    
    Handles:
    - Background playback in a separate thread
    - Console responsiveness for control commands
    - Playback state management (play, pause, stop, next, restart, previous)
    - Real-time progress display
    """

    def __init__(self):
        """Initialize the playback manager."""
        self.state = PlaybackState.STOPPED
        self.current_file: Optional[str] = None
        self.player: Optional[vlc.MediaPlayer] = None
        self.playback_thread: Optional[threading.Thread] = None
        self.display: Optional[PlaybackDisplay] = None
        
        # Control flags
        self._stop_requested = False
        self._pause_requested = False
        self._next_requested = False
        self._restart_requested = False
        
        # Callbacks for queue management
        self.on_playback_complete: Optional[Callable[[], None]] = None
        self.on_next_requested: Optional[Callable[[], Optional[str]]] = None
        
        # Lock for thread-safe state access
        self._lock = threading.Lock()

    def play(self, filename: str, full_length: bool = True, show_ui: bool = True) -> None:
        """Start playing a file in background thread.
        
        Args:
            filename: Path to audio file
            full_length: If True, play entire file; if False, play for 3 seconds
            show_ui: If True, display fancy playback UI
        """
        if vlc is None:
            print("python-vlc is not installed; cannot play audio.")
            return

        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            return

        with self._lock:
            # Stop any currently playing track
            if self.state == PlaybackState.PLAYING:
                self._stop_playback_internal()

            self.current_file = filename
            self.state = PlaybackState.PLAYING
            self._stop_requested = False
            self._pause_requested = False
            self._next_requested = False
            self._restart_requested = False

        # Create display
        if show_ui:
            self.display = PlaybackDisplay(filename)
            self.display.print_now_playing()
        else:
            print(f"Playing: {filename}")

        # Start playback thread
        self.playback_thread = threading.Thread(
            target=self._playback_worker,
            args=(filename, full_length, show_ui),
            daemon=True
        )
        self.playback_thread.start()

    def stop(self) -> None:
        """Stop current playback."""
        with self._lock:
            if self.state in (PlaybackState.PLAYING, PlaybackState.PAUSED):
                self._stop_requested = True
                print("\n[Playback stopped]")

    def pause(self) -> None:
        """Pause current playback."""
        with self._lock:
            if self.state == PlaybackState.PLAYING:
                self._pause_requested = True
                self.state = PlaybackState.PAUSED
                print("\n[Playback paused]")

    def resume(self) -> None:
        """Resume paused playback."""
        with self._lock:
            if self.state == PlaybackState.PAUSED:
                self._pause_requested = False
                self.state = PlaybackState.PLAYING
                print("\n[Playback resumed]")

    def next(self) -> None:
        """Skip to next track."""
        with self._lock:
            if self.state in (PlaybackState.PLAYING, PlaybackState.PAUSED):
                self._next_requested = True
                print("\n[Skipping to next track]")

    def restart(self) -> None:
        """Restart current track from beginning."""
        with self._lock:
            if self.state in (PlaybackState.PLAYING, PlaybackState.PAUSED):
                self._restart_requested = True
                print("\n[Restarting track]")

    def previous(self) -> None:
        """Go to previous track (restart current or queue previous)."""
        if self.on_next_requested:
            # For now, just restart current track
            self.restart()

    def get_status(self) -> dict:
        """Get current playback status."""
        with self._lock:
            return {
                "state": self.state.value,
                "current_file": self.current_file,
                "is_playing": self.state == PlaybackState.PLAYING,
            }

    def wait_for_completion(self, timeout: Optional[float] = None) -> bool:
        """Wait for playback to complete.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if playback completed, False if timeout
        """
        if self.playback_thread and self.playback_thread.is_alive():
            self.playback_thread.join(timeout)
            return not self.playback_thread.is_alive()
        return True

    def _stop_playback_internal(self) -> None:
        """Internal method to stop playback (must be called with lock held)."""
        if self.player:
            try:
                self.player.stop()
            except Exception:
                pass
        self.state = PlaybackState.STOPPED

    def _get_duration(self, filename: str) -> float:
        """Get audio duration in seconds."""
        if librosa is None:
            return 0.0
        try:
            y, sr = librosa.load(filename, sr=None)
            return len(y) / sr
        except Exception:
            return 0.0

    def _playback_worker(self, filename: str, full_length: bool, show_ui: bool) -> None:
        """Background worker thread for playback.
        
        This function runs in a separate thread and can be interrupted
        by control commands.
        """
        try:
            duration = self._get_duration(filename) if full_length else 3.0
            
            # Create and start player
            self.player = vlc.MediaPlayer(filename)
            self.player.play()
            
            start_time = time.time()
            
            # Main playback loop with responsive control checking
            while time.time() - start_time < duration:
                with self._lock:
                    # Check for stop/next requests
                    if self._stop_requested:
                        self._stop_playback_internal()
                        return
                    
                    if self._next_requested:
                        self._stop_playback_internal()
                        self._next_requested = False
                        # Call callback to get next track
                        if self.on_next_requested:
                            next_file = self.on_next_requested()
                            if next_file:
                                # Play next track recursively
                                self.play(next_file, full_length, show_ui)
                        return
                    
                    if self._restart_requested:
                        self._stop_playback_internal()
                        self.player = vlc.MediaPlayer(filename)
                        self.player.play()
                        start_time = time.time()
                        self._restart_requested = False
                
                # Update display
                if show_ui and self.display:
                    elapsed = time.time() - start_time
                    self.display.print_progress_bar(elapsed, duration)
                
                # Sleep briefly to allow responsive control checking
                time.sleep(0.1)
            
            # Playback complete
            if self.player:
                self.player.stop()
            
            with self._lock:
                self.state = PlaybackState.STOPPED
            
            if show_ui and self.display:
                self.display.print_playback_complete()
            
            if self.on_playback_complete:
                self.on_playback_complete()
                
        except Exception as e:
            print(f"Playback error: {e}")
            with self._lock:
                self.state = PlaybackState.STOPPED
