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

    def __init__(self, player_factory=None):
        """Initialize the playback manager."""
        self.state = PlaybackState.STOPPED
        self.current_file: Optional[str] = None
        self.player: Optional[vlc.MediaPlayer] = None
        self.playback_thread: Optional[threading.Thread] = None
        self.display: Optional[PlaybackDisplay] = None
        self._player_factory = player_factory or (vlc.MediaPlayer if vlc else None)
        self._generation = 0
        self.history: list[str] = []
        
        # Control flags
        self._stop_requested = False
        self._pause_requested = False
        self._next_requested = False
        self._restart_requested = False
        
        # Callbacks for queue management
        self.on_playback_complete: Optional[Callable[[], None]] = None
        self.on_next_requested: Optional[Callable[[], Optional[str]]] = None
        self.on_previous_requested: Optional[Callable[[], Optional[str]]] = None
        
        # Lock for thread-safe state access
        self._lock = threading.Lock()

    def play(self, filename: str, full_length: bool = True, show_ui: bool = True) -> None:
        """Start playing a file in background thread.
        
        Args:
            filename: Path to audio file
            full_length: If True, play entire file; if False, play for 3 seconds
            show_ui: If True, display fancy playback UI
        """
        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            return

        if self._player_factory is None:
            print("python-vlc is not installed; cannot play audio.")
            # Keep the asynchronous contract even when the optional backend
            # is unavailable, so callers can safely inspect/join the worker.
            self.playback_thread = threading.Thread(target=lambda: None, daemon=True)
            self.playback_thread.start()
            return

        with self._lock:
            # Stop any currently playing track
            if self.state in (PlaybackState.PLAYING, PlaybackState.PAUSED):
                if self.current_file and self.current_file != filename:
                    self.history.append(self.current_file)
                self._stop_playback_internal()

            self.current_file = filename
            self.state = PlaybackState.PLAYING
            self._generation += 1
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
        generation = self._generation
        self.playback_thread = threading.Thread(
            target=self._playback_worker,
            args=(filename, full_length, show_ui, generation),
            daemon=True
        )
        self.playback_thread.start()

    def stop(self) -> None:
        """Stop current playback."""
        with self._lock:
            if self.state in (PlaybackState.PLAYING, PlaybackState.PAUSED):
                self._stop_requested = True
                self._stop_playback_internal()
                print("\n[Playback stopped]")

    def pause(self) -> None:
        """Pause current playback."""
        with self._lock:
            if self.state == PlaybackState.PLAYING:
                if self.player and hasattr(self.player, "pause"):
                    self.player.pause()
                self._pause_requested = True
                self.state = PlaybackState.PAUSED
                print("\n[Playback paused]")

    def resume(self) -> None:
        """Resume paused playback."""
        with self._lock:
            if self.state == PlaybackState.PAUSED:
                if self.player and hasattr(self.player, "play"):
                    self.player.play()
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
        with self._lock:
            if self.state not in (PlaybackState.PLAYING, PlaybackState.PAUSED):
                return
            callback = self.on_previous_requested
            previous = None if callback else (self.history.pop() if self.history else None)
        if callback:
            previous = callback()
        if previous:
            self.play(previous)
        else:
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

    def _playback_worker(
        self, filename: str, full_length: bool, show_ui: bool, generation: int
    ) -> None:
        """Background worker thread for playback.
        
        This function runs in a separate thread and can be interrupted
        by control commands.
        """
        try:
            duration = self._get_duration(filename) if full_length else 3.0
            
            # Create and start player
            self.player = self._player_factory(filename)
            self.player.play()
            
            start_time = time.time()
            
            # Main playback loop with responsive control checking
            while time.time() - start_time < duration:
                with self._lock:
                    if generation != self._generation:
                        return
                    # Check for stop/next requests
                    if self._stop_requested:
                        self._stop_playback_internal()
                        return
                    
                    next_requested = self._next_requested
                    if next_requested:
                        self._stop_playback_internal()
                        self._next_requested = False
                        next_callback = self.on_next_requested
                    else:
                        next_callback = None
                    if next_requested and not next_callback:
                        return
                    
                    if self._restart_requested:
                        self._stop_playback_internal()
                        self.player = self._player_factory(filename)
                        self.player.play()
                        start_time = time.time()
                        self._restart_requested = False

                if next_callback:
                    next_file = next_callback()
                    if next_file:
                        self.play(next_file, full_length, show_ui)
                    return
                
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
                if generation == self._generation:
                    self.state = PlaybackState.STOPPED
            
            if show_ui and self.display:
                self.display.print_playback_complete()
            
            if self.on_playback_complete:
                self.on_playback_complete()
                
        except Exception as e:
            print(f"Playback error: {e}")
            with self._lock:
                if generation == self._generation:
                    self.state = PlaybackState.STOPPED

    def shutdown(self, timeout: float = 2.0) -> None:
        """Stop playback and wait briefly for the worker to exit."""
        self.stop()
        thread = self.playback_thread
        if thread and thread is not threading.current_thread():
            thread.join(timeout)
        with self._lock:
            self.player = None
            self.current_file = None
            self.state = PlaybackState.STOPPED
