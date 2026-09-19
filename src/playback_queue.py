"""Simple persistent playback queue."""
from __future__ import annotations

import os
import json
try:
    from platformdirs import user_data_dir
except ImportError:
    user_data_dir = None


class QueuePersistenceError(RuntimeError):
    """Raised when the persistent queue cannot be read or written."""


class PlaybackQueue:
    def __init__(self, storage_file: str | None = None):
        if storage_file is None:
            if user_data_dir:
                storage_file = os.path.join(
                    user_data_dir("soundfile-analyzer"), "queue.json"
                )
            else:
                storage_file = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "..", "queue.json")
                )
        self.storage_file = storage_file
        self._queue: list[str] = []
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.storage_file):
            self._queue = []
            return
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                value = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            raise QueuePersistenceError(
                f"Unable to load playback queue '{self.storage_file}': {exc}"
            ) from exc
        if not isinstance(value, list) or not all(
            isinstance(item, str) for item in value
        ):
            raise QueuePersistenceError(
                f"Invalid playback queue '{self.storage_file}': expected a list of paths"
            )
        self._queue = value

    def _save(self) -> None:
        try:
            directory = os.path.dirname(os.path.abspath(self.storage_file))
            os.makedirs(directory, exist_ok=True)
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(self._queue, f)
        except (OSError, TypeError, ValueError) as exc:
            raise QueuePersistenceError(
                f"Unable to save playback queue '{self.storage_file}': {exc}"
            ) from exc

    def add(self, filepath: str) -> None:
        self._queue.append(filepath)
        self._save()

    def next(self) -> str | None:
        if not self._queue:
            return None
        item = self._queue.pop(0)
        self._save()
        return item

    def current(self) -> str | None:
        return self._queue[0] if self._queue else None

    def list(self) -> list[str]:
        return list(self._queue)

    def clear(self) -> None:
        self._queue = []
        self._save()

    def remove(self, index: int) -> str:
        """Remove and return an item by zero-based index."""
        try:
            item = self._queue.pop(index)
        except IndexError as exc:
            raise IndexError(f"Queue index out of range: {index}") from exc
        self._save()
        return item

    def move(self, source: int, destination: int) -> None:
        """Move an item by zero-based indexes."""
        if not 0 <= source < len(self._queue):
            raise IndexError(f"Queue index out of range: {source}")
        if not 0 <= destination < len(self._queue):
            raise IndexError(f"Queue index out of range: {destination}")
        item = self._queue.pop(source)
        self._queue.insert(destination, item)
        self._save()
