"""Interactive DJ mode REPL for responsive console playback control.

Provides a command prompt that stays responsive while music plays in background.
Uses input() in main thread with non-blocking display updates.
"""

from __future__ import annotations

import sys
import threading
import time
from typing import Optional

PlaybackManager = None
PlaybackQueue = None
QueueDisplay = None

try:
    from .playback_manager import PlaybackManager
    from .playback_queue import PlaybackQueue
    from .playback_ui import QueueDisplay
except ImportError:
    try:
        from playback_manager import PlaybackManager
        from playback_queue import PlaybackQueue
        from playback_ui import QueueDisplay
    except ImportError:
        pass


class PlaybackREPL:
    """Interactive REPL for DJ-style playback control.
    
    Runs in main thread accepting commands while PlaybackManager
    plays music in background thread.
    """

    def __init__(self, queue_file: Optional[str] = None):
        """Initialize the REPL.
        
        Args:
            queue_file: Path to persistent queue file
        """
        self.manager = PlaybackManager()
        self.queue = PlaybackQueue(queue_file) if queue_file else None
        self.running = False
        self.current_file: Optional[str] = None
        
        # Set up callbacks
        if self.manager:
            self.manager.on_playback_complete = self._on_playback_complete
            self.manager.on_next_requested = self._on_next_requested

    def _on_playback_complete(self) -> None:
        """Handle playback completion."""
        self.current_file = None
        if self.queue:
            next_file = self.queue.current()
            if next_file:
                print("\n[Playback complete, playing next track...]")
                self._play_file(next_file, full_length=True)
                self.current_file = next_file

    def _on_next_requested(self) -> Optional[str]:
        """Handle next track request."""
        if self.queue:
            nxt = self.queue.next()
            if nxt:
                self.current_file = nxt
                return nxt
        return None

    def _play_file(self, filename: str, full_length: bool = True) -> None:
        """Play a file."""
        try:
            self.current_file = filename
            self.manager.play(filename, full_length=full_length, show_ui=True)
        except Exception as e:
            print(f"Error playing file: {e}")

    def _show_help(self) -> None:
        """Show help message."""
        print("""
╔════════════════════════════════════════════════════════════╗
║                  DJ MODE COMMANDS                          ║
╚════════════════════════════════════════════════════════════╝

PLAYBACK CONTROL:
  play <file>          - Play a file
  demo <file>          - Play 3-second demo
  stop                 - Stop playback
  pause                - Pause playback
  resume               - Resume playback
  restart              - Restart current track
  next                 - Skip to next track
  prev / previous      - Go to previous track
  status               - Show playback status

QUEUE MANAGEMENT:
  add <file>           - Add file to queue
  queue                - Show queue
  queue next           - Play next queued track
  queue clear          - Clear the queue

GENERAL:
  help                 - Show this help
  exit / quit          - Exit DJ mode

""")

    def _show_status(self) -> None:
        """Show current status."""
        if not self.manager:
            print("Playback manager not available")
            return
        
        status = self.manager.get_status()
        print(f"\n▶ Playback Status:")
        print(f"  State: {status['state']}")
        print(f"  Playing: {status['is_playing']}")
        if status['current_file']:
            print(f"  File: {status['current_file']}")
        
        if self.queue:
            current = self.queue.current()
            remaining = self.queue.list()[1:] if self.queue.list() else []
            if current or remaining:
                QueueDisplay.print_queue(current, remaining)

    def run(self) -> None:
        """Run the interactive REPL."""
        self.running = True
        self._show_help()
        
        try:
            while self.running:
                try:
                    # Show prompt
                    command = input("\n🎵 dj> ").strip()
                    
                    if not command:
                        continue
                    
                    self._process_command(command)
                    
                except EOFError:
                    break
                except KeyboardInterrupt:
                    print("\n[Use 'exit' command to quit]")
                    continue
                except Exception as e:
                    print(f"Error: {e}")
                    
        except Exception as e:
            print(f"REPL error: {e}")
        finally:
            self._cleanup()

    def _process_command(self, command: str) -> None:
        """Process a user command.
        
        Args:
            command: The command string to process
        """
        parts = command.split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        # Playback control commands
        if cmd == "play" and args:
            self._play_file(args[0], full_length=True)
        elif cmd == "demo" and args:
            self._play_file(args[0], full_length=False)
        elif cmd == "stop":
            self.manager.stop()
            print("[Stopped]")
        elif cmd == "pause":
            self.manager.pause()
        elif cmd == "resume":
            self.manager.resume()
        elif cmd == "restart":
            self.manager.restart()
            print("[Restarting track]")
        elif cmd == "next":
            self.manager.next()
        elif cmd in ("prev", "previous"):
            self.manager.previous()
        elif cmd == "status":
            self._show_status()
        
        # Queue commands
        elif cmd == "add" and args:
            if self.queue:
                self.queue.add(args[0])
                print(f"Added to queue: {args[0]}")
            else:
                print("Queue not available")
        elif cmd == "queue":
            if args and args[0] == "next":
                if self.queue:
                    nxt = self.queue.next()
                    if nxt:
                        self._play_file(nxt, full_length=True)
                    else:
                        print("Queue is empty")
                else:
                    print("Queue not available")
            elif args and args[0] == "clear":
                if self.queue:
                    self.queue.clear()
                    print("Queue cleared")
            else:
                # Show queue
                if self.queue:
                    current = self.queue.current()
                    remaining = self.queue.list()[1:] if self.queue.list() else []
                    QueueDisplay.print_queue(current, remaining)
                else:
                    print("Queue not available")
        
        # General commands
        elif cmd == "help":
            self._show_help()
        elif cmd in ("exit", "quit"):
            print("Goodbye!")
            self.running = False
        else:
            print(f"Unknown command: {cmd}")
            print("Type 'help' for available commands")

    def _cleanup(self) -> None:
        """Clean up resources."""
        if self.manager:
            self.manager.stop()
