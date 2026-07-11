"""Visualization wrapper around Analyzer visual outputs."""
from __future__ import annotations

from analyzer import Analyzer


class Visualization:
    def __init__(self, filename: str):
        self.filename = filename
        self._analyzer = Analyzer(filename)

    def waveform(self) -> None:
        self._analyzer.visualize_waveform()

    def spectrogram(self) -> None:
        self._analyzer.visualize_spectrogram()

    def frequency(self) -> None:
        self._analyzer.visualize_frequency()
