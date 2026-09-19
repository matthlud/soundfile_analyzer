import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from library import search_tracks, scan_folder


def test_scan_folder_finds_supported_files_recursively(tmp_path):
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "ambient.flac").write_bytes(b"not-a-valid-audio-file")
    (tmp_path / "song.wav").write_bytes(b"not-a-valid-audio-file")
    (tmp_path / "notes.txt").write_text("ignore")

    tracks = scan_folder(tmp_path)

    assert [track.title for track in tracks] == ["ambient", "song"]


def test_search_tracks_matches_metadata_and_path(tmp_path):
    (tmp_path / "house anthem.mp3").write_bytes(b"not-a-valid-audio-file")
    tracks = scan_folder(tmp_path)

    assert len(search_tracks(tracks, "HOUSE")) == 1
    assert search_tracks(tracks, "missing") == []
