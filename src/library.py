"""Small, local music-library index for the interactive DJ console."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from mutagen import File as MutagenFile
from mutagen import MutagenError


SUPPORTED_EXTENSIONS = frozenset({".flac", ".mp3", ".ogg", ".wav", ".m4a", ".aac"})


@dataclass(frozen=True)
class Track:
    path: str
    title: str
    artist: str = ""
    album: str = ""
    duration: float | None = None

    @property
    def label(self) -> str:
        artist = f"{self.artist} - " if self.artist else ""
        return f"{artist}{self.title}"


def _tag_value(tags, key: str) -> str:
    value = tags.get(key) if tags else None
    if isinstance(value, (list, tuple)):
        value = value[0] if value else None
    return str(value) if value else ""


def read_track(path: Path) -> Track:
    """Read DJ-facing metadata, falling back to the filename."""
    title = path.stem
    artist = album = ""
    duration = None
    try:
        audio = MutagenFile(path)
        if audio is not None:
            title = _tag_value(audio.tags, "title") or title
            artist = _tag_value(audio.tags, "artist")
            album = _tag_value(audio.tags, "album")
            duration = getattr(audio.info, "length", None)
    except (OSError, TypeError, ValueError, MutagenError):
        pass
    return Track(str(path), title, artist, album, duration)


def scan_folder(folder: str | Path, recursive: bool = True) -> list[Track]:
    """Scan a folder for supported audio files in stable path order."""
    root = Path(folder).expanduser()
    paths: Iterable[Path] = root.rglob("*") if recursive else root.glob("*")
    return [
        read_track(path)
        for path in sorted(paths, key=lambda item: str(item).lower())
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]


def search_tracks(tracks: Iterable[Track], query: str) -> list[Track]:
    """Search title, artist, album, and path case-insensitively."""
    needle = query.casefold().strip()
    if not needle:
        return list(tracks)
    return [
        track
        for track in tracks
        if needle in " ".join(
            (track.title, track.artist, track.album, track.path)
        ).casefold()
    ]
