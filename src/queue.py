"""Simple persistent playback queue."""
from __future__ import annotations

import os
import json


class PlaybackQueue:
    def __init__(self, storage_file: str | None = None):
        if storage_file is None:
            storage_file = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "queue.json")
            )
        self.storage_file = storage_file
        self._queue: list[str] = []
        self._load()

    def _load(self) -> None:
        try:
            with open(self.storage_file, "r") as f:
                self._queue = json.load(f)
        except Exception:
            self._queue = []

    def _save(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
            with open(self.storage_file, "w") as f:
                json.dump(self._queue, f)
        except Exception:
            pass

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
