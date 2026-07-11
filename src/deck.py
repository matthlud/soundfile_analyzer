"""Deck abstraction: load a file and apply filters/effects producing a temporary file."""
from __future__ import annotations

import librosa
import soundfile as sf
import tempfile
import os


class Deck:
    def __init__(self, filename: str | None = None):
        self.filename = filename

    def load(self, filename: str) -> None:
        self.filename = filename

    def apply_filter(self, filter_instance) -> str:
        if not self.filename:
            raise ValueError("No file loaded in deck")
        samples, sr = librosa.load(self.filename, sr=None)
        filtered = filter_instance.apply(samples)
        suffix = os.path.splitext(self.filename)[1] or ".wav"
        tf = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        sf.write(tf.name, filtered, sr)
        self.filename = tf.name
        return self.filename

    def apply_effect(self, effect_instance) -> str:
        """Apply a generic effect (supports apply(samples, sr)) and write a temp file.

        The effect may accept either (samples) or (samples, sr). Both are tried.
        """
        if not self.filename:
            raise ValueError("No file loaded in deck")
        samples, sr = librosa.load(self.filename, sr=None)
        try:
            processed = effect_instance.apply(samples, sr)
        except TypeError:
            processed = effect_instance.apply(samples)
        suffix = os.path.splitext(self.filename)[1] or ".wav"
        tf = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        sf.write(tf.name, processed, sr)
        self.filename = tf.name
        return self.filename
