"""Fancy console UI for playback status and queue display."""

from __future__ import annotations

import os
import sys
from typing import Optional
from datetime import timedelta

try:
    from colorama import Fore, Back, Style, init as colorama_init
except ImportError:
    colorama_init = None
    Fore = Back = Style = None

try:
    import librosa
except ImportError:
    librosa = None


def format_time(seconds: float) -> str:
    """Convert seconds to MM:SS format."""
    td = timedelta(seconds=int(seconds))
    return f"{td.seconds // 60}:{td.seconds % 60:02d}"


class PlaybackDisplay:
    """Handle fancy console display for playback status."""

    def __init__(self, filename: str):
        self.filename = filename
        self.duration = self._get_duration()
        if colorama_init:
            colorama_init(autoreset=True)

    def _get_duration(self) -> float:
        """Get audio duration in seconds."""
        if librosa is None:
            return 0.0
        try:
            y, sr = librosa.load(self.filename, sr=None)
            return len(y) / sr
        except Exception:
            return 0.0

    def print_now_playing(self) -> None:
        """Print a fancy now playing header."""
        filename = os.path.basename(self.filename)
        duration_str = format_time(self.duration) if self.duration > 0 else "?:??"

        if Fore:
            print(f"\n{Fore.CYAN}{'=' * 60}")
            print(f"{Fore.GREEN}▶ {Fore.YELLOW}NOW PLAYING{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'=' * 60}")
            print(f"{Fore.WHITE}File: {Fore.MAGENTA}{filename}")
            print(f"{Fore.WHITE}Duration: {Fore.CYAN}{duration_str}")
            print(f"{Fore.CYAN}{'=' * 60}\n")
        else:
            print(f"\n{'=' * 60}")
            print(f"▶ NOW PLAYING")
            print(f"{'=' * 60}")
            print(f"File: {filename}")
            print(f"Duration: {duration_str}")
            print(f"{'=' * 60}\n")

    def print_simple_status(self, elapsed: float, total: float) -> None:
        """Print simple playback status."""
        elapsed_str = format_time(elapsed)
        total_str = format_time(total) if total > 0 else "?:??"

        if Fore:
            print(f"{Fore.GREEN}Playing: {Fore.CYAN}{elapsed_str}/{Fore.MAGENTA}{total_str}",
                  end="\r", file=sys.stdout)
        else:
            print(f"Playing: {elapsed_str}/{total_str}", end="\r", file=sys.stdout)

    def print_progress_bar(self, elapsed: float, total: float, width: int = 50) -> None:
        """Print a fancy progress bar with color."""
        if total <= 0:
            return

        percent = min(elapsed / total, 1.0)
        filled = int(width * percent)
        bar = "█" * filled + "░" * (width - filled)
        elapsed_str = format_time(elapsed)
        total_str = format_time(total)
        percent_str = f"{percent * 100:.1f}%"

        if Fore:
            print(f"{Fore.YELLOW}Progress: [{Fore.GREEN}{bar}{Fore.YELLOW}] "
                  f"{Fore.CYAN}{elapsed_str}/{total_str} {Fore.MAGENTA}{percent_str}",
                  end="\r", file=sys.stdout)
        else:
            print(f"Progress: [{bar}] {elapsed_str}/{total_str} {percent_str}",
                  end="\r", file=sys.stdout)

    def print_playback_complete(self) -> None:
        """Print completion message."""
        if Fore:
            print(f"\n{Fore.GREEN}{'=' * 60}")
            print(f"{Fore.GREEN}✓ Playback complete!")
            print(f"{Fore.GREEN}{'=' * 60}\n")
        else:
            print(f"\n{'=' * 60}")
            print(f"✓ Playback complete!")
            print(f"{'=' * 60}\n")


class QueueDisplay:
    """Handle fancy console display for queue."""

    @staticmethod
    def print_queue(current_item: Optional[str], queue_items: list[str]) -> None:
        """Print the current queue with current item highlighted."""
        if not queue_items and not current_item:
            if Fore:
                print(f"{Fore.YELLOW}Queue is empty")
            else:
                print("Queue is empty")
            return

        if Fore:
            print(f"\n{Fore.CYAN}{'=' * 60}")
            print(f"{Fore.GREEN}🎵 PLAYBACK QUEUE{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'=' * 60}")

            # Current playing
            if current_item:
                current_name = os.path.basename(current_item)
                print(f"{Fore.GREEN}► {Fore.YELLOW}{current_name} {Fore.GREEN}(NOW PLAYING)")
            else:
                print(f"{Fore.YELLOW}(No item currently playing)")

            # Upcoming queue
            if queue_items:
                print(f"\n{Fore.CYAN}Upcoming:")
                for i, item in enumerate(queue_items[:10], 1):
                    item_name = os.path.basename(item)
                    print(f"  {Fore.MAGENTA}{i}. {Fore.WHITE}{item_name}")
                if len(queue_items) > 10:
                    print(f"  {Fore.YELLOW}... and {len(queue_items) - 10} more items")
            else:
                print(f"{Fore.YELLOW}\n(No items in queue)")

            print(f"{Fore.CYAN}{'=' * 60}\n")
        else:
            print(f"\n{'=' * 60}")
            print(f"🎵 PLAYBACK QUEUE")
            print(f"{'=' * 60}")

            if current_item:
                current_name = os.path.basename(current_item)
                print(f"► {current_name} (NOW PLAYING)")
            else:
                print(f"(No item currently playing)")

            if queue_items:
                print(f"\nUpcoming:")
                for i, item in enumerate(queue_items[:10], 1):
                    item_name = os.path.basename(item)
                    print(f"  {i}. {item_name}")
                if len(queue_items) > 10:
                    print(f"  ... and {len(queue_items) - 10} more items")
            else:
                print(f"\n(No items in queue)")

            print(f"{'=' * 60}\n")
