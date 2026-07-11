"""FileInfos: helper for file metadata and simple file listings."""
from __future__ import annotations

import os
from mutagen import File as MutagenFile
from typing import Dict, Any


class FileInfos:
    def __init__(self, dirpath: str, filename: str):
        self.dirpath = dirpath
        self.filename = filename
        self.path = os.path.join(dirpath, filename)

    def exists(self) -> bool:
        return os.path.exists(self.path)

    def size(self) -> int | None:
        if not self.exists():
            return None
        return os.path.getsize(self.path)

    def metadata(self) -> Dict[str, Any]:
        if not self.exists():
            return {}
        f = MutagenFile(self.path)
        info: Dict[str, Any] = {}
        if f is not None:
            info["tags"] = dict(f.tags) if f.tags else {}
            try:
                info["length"] = getattr(f.info, "length", None)
                info["bitrate"] = getattr(f.info, "bitrate", None)
                info["sample_rate"] = getattr(f.info, "sample_rate", None)
                info["channels"] = getattr(f.info, "channels", None)
            except Exception:
                pass
        return info

    def print_info(self) -> None:
        print(f"Path: {self.path}")
        meta = self.metadata()
        for k, v in meta.items():
            print(f"{k}: {v}")

    @staticmethod
    def list_files(dirpath: str, extensions=None):
        if extensions is None:
            extensions = [".wav", ".mp3"]
        result = []
        try:
            for entry in os.listdir(dirpath):
                if any(entry.lower().endswith(ext) for ext in extensions):
                    result.append(entry)
        except Exception:
            pass
        return result

