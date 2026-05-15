"""Fileinfos module

Provides a Fileinfos class that extracts basic file and audio metadata.
"""
from __future__ import annotations

import os
import mimetypes
from typing import Optional, Dict, Any

try:
    import soundfile as sf
except Exception:  # pragma: no cover - runtime import
    sf = None

try:
    from mutagen import File as MutagenFile
except Exception:  # pragma: no cover - runtime import
    MutagenFile = None


class Fileinfos:
    """Extracts metadata for a file (audio-focused).

    Methods return None when the information is not available.
    """

    def __init__(self, path: str) -> None:
        self.path = str(path)
        self._exists: bool = os.path.exists(self.path)

        # basic
        self.size: Optional[int] = None
        self.format: Optional[str] = None
        self.mime: Optional[str] = None

        # audio-specific
        self.samplerate: Optional[int] = None
        self.channels: Optional[int] = None
        self.frames: Optional[int] = None
        self.duration: Optional[float] = None
        self.bitrate: Optional[int] = None

        if self._exists:
            self._load()

    def _load(self) -> None:
        try:
            self.size = os.path.getsize(self.path)
        except Exception:
            self.size = None

        self.format = os.path.splitext(self.path)[1].lower().lstrip('.') or None
        self.mime = mimetypes.guess_type(self.path)[0]

        # Try soundfile first for reliable samplerate/channels/frames
        if sf is not None:
            try:
                info = sf.info(self.path)
                # soundfile.Info has samplerate, channels and frames
                self.samplerate = int(info.samplerate) if getattr(info, "samplerate", None) else None
                self.channels = int(info.channels) if getattr(info, "channels", None) else None
                try:
                    self.frames = int(info.frames)
                except Exception:
                    self.frames = None
                if self.frames and self.samplerate:
                    self.duration = float(self.frames) / float(self.samplerate)
            except Exception:
                # not an audio file soundfile can read
                pass

        # Mutagen fallback (good for mp3 and some containers) to get length/bitrate
        if MutagenFile is not None:
            try:
                mf = MutagenFile(self.path)
                if mf is not None and hasattr(mf, "info"):
                    length = getattr(mf.info, "length", None)
                    if length is not None:
                        self.duration = float(length)
                    bitrate = getattr(mf.info, "bitrate", None)
                    if bitrate is not None:
                        # mutagen reports bitrate in bits/s for many formats
                        try:
                            self.bitrate = int(bitrate)
                        except Exception:
                            self.bitrate = None

                    # Some mutagen backends expose sample_rate/channels
                    sr = getattr(mf.info, "sample_rate", None)
                    if sr is not None and self.samplerate is None:
                        self.samplerate = int(sr)
                    ch = getattr(mf.info, "channels", None)
                    if ch is not None and self.channels is None:
                        self.channels = int(ch)
            except Exception:
                pass

    def exists(self) -> bool:
        return self._exists

    def get_size_bytes(self) -> Optional[int]:
        return self.size

    def get_size_human(self) -> Optional[str]:
        if self.size is None:
            return None
        s = float(self.size)
        for unit in ("B", "KB", "MB", "GB", "TB"):
            if s < 1024.0:
                # show 1 decimal place
                return f"{s:.1f}{unit}"
            s /= 1024.0
        return f"{s:.1f}PB"

    def get_samplerate(self) -> Optional[int]:
        return self.samplerate

    def get_channels(self) -> Optional[int]:
        return self.channels

    def get_frames(self) -> Optional[int]:
        return self.frames

    def get_duration(self) -> Optional[float]:
        return self.duration

    def get_bitrate(self) -> Optional[int]:
        return self.bitrate

    def get_format(self) -> Optional[str]:
        return self.format or (self.mime.split('/')[1] if self.mime and '/' in self.mime else None)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "exists": self._exists,
            "size": self.size,
            "size_human": self.get_size_human(),
            "format": self.get_format(),
            "mime": self.mime,
            "samplerate": self.samplerate,
            "channels": self.channels,
            "frames": self.frames,
            "duration": self.duration,
            "bitrate": self.bitrate,
        }

    def print_info(self) -> None:
        """Pretty-print file information to stdout."""
        d = self.as_dict()
        for k, v in d.items():
            print(f"{k}: {v}")


__all__ = ["Fileinfos"]
