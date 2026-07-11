"""Top-level runner CLI for soundfile_analyzer."""

from __future__ import annotations

import argparse
import os

from file_handler import FileHandler
from player import Player

# Optional components implemented in this feature set
# These modules were added: filters.py, fileinfos.py, visualization.py, queue.py, deck.py, effects.py
try:
    from filters import LowpassFilter, HighpassFilter, NotchFilter
    from playback_queue import PlaybackQueue
    from deck import Deck
    from fileinfos import FileInfos
    from visualization import Visualization
    from effects import Fader, Reverb
except Exception:
    # If optional modules are missing, CLI will still expose basic functionality
    LowpassFilter = HighpassFilter = NotchFilter = None
    PlaybackQueue = None
    Deck = None
    FileInfos = None
    Visualization = None
    Fader = Reverb = None


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="runner", description="Soundfile DJ runner CLI")
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list", help="List audio files in directory")
    p_list.add_argument("--dir", "-d", default=os.path.join(os.path.dirname(__file__), "tests"))

    p_info = sub.add_parser("info", help="Show file information")
    p_info.add_argument("file")

    p_visual = sub.add_parser("visualize", help="Create visualizations")
    p_visual.add_argument("file")
    p_visual.add_argument("--waveform", action="store_true")
    p_visual.add_argument("--spectrogram", action="store_true")
    p_visual.add_argument("--frequency", action="store_true")

    p_play = sub.add_parser("play", help="Play a file (short demo)")
    p_play.add_argument("file")

    p_queue = sub.add_parser("queue", help="Queue operations")
    qsub = p_queue.add_subparsers(dest="qcmd")
    qadd = qsub.add_parser("add")
    qadd.add_argument("file")
    qnext = qsub.add_parser("next")

    p_filter = sub.add_parser("apply-filter", help="Apply filter to a file and write a temp file")
    p_filter.add_argument("file")
    p_filter.add_argument("--filter", choices=["lowpass", "highpass", "notch"], required=True)
    p_filter.add_argument("--cutoff", type=float, default=1000.0)
    p_filter.add_argument("--q", type=float, default=30.0)

    p_effect = sub.add_parser("apply-effect", help="Apply DJ effect (fader or reverb) to a file and write a temp file")
    p_effect.add_argument("file")
    p_effect.add_argument("--effect", choices=["fader", "reverb"], required=True)
    p_effect.add_argument("--gain", type=float, default=1.0)
    p_effect.add_argument("--delay", type=float, default=50.0, help="delay in ms for reverb")
    p_effect.add_argument("--decay", type=float, default=0.5, help="decay factor for reverb")
    p_effect.add_argument("--repeats", type=int, default=5, help="number of repeats for reverb")

    args = parser.parse_args(argv)

    # persistent queue stored at repository root (one level above src)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    queue_file = os.path.join(project_root, "queue.json")
    q = PlaybackQueue(queue_file) if PlaybackQueue is not None else None

    if args.cmd == "list":
        files = FileInfos.list_files(args.dir) if FileInfos is not None else FileHandler(args.dir, "").print_files()
        if isinstance(files, list):
            for f in files:
                print(f)
        return

    if args.cmd == "info":
        path = args.file
        if not os.path.isabs(path):
            # allow either an absolute path or a path relative to repo root
            path = os.path.join(os.path.dirname(__file__), path)
        dirname, fname = os.path.split(path)
        if FileInfos is None:
            print("FileInfos not available in this installation")
            return
        fi = FileInfos(dirname, fname)
        fi.print_info()
        return

    if args.cmd == "visualize":
        if Visualization is None:
            print("Visualization feature not available")
            return
        viz = Visualization(args.file)
        if args.waveform:
            viz.waveform()
        if args.spectrogram:
            viz.spectrogram()
        if args.frequency:
            viz.frequency()
        if not (args.waveform or args.spectrogram or args.frequency):
            viz.waveform()
            viz.spectrogram()
            viz.frequency()
        print("Saved visualizations to ./artifacts")
        return

    if args.cmd == "play":
        p = Player(args.file)
        p.play_forward()
        return

    if args.cmd == "queue":
        if q is None:
            print("Queue feature not available")
            return
        if args.qcmd == "add":
            q.add(args.file)
            print("Added to queue:", args.file)
        elif args.qcmd == "next":
            nxt = q.next()
            if nxt:
                print("Next in queue:", nxt)
                p = Player(nxt)
                p.play_forward()
            else:
                print("Queue is empty")
        return

    if args.cmd == "apply-filter":
        if Deck is None or LowpassFilter is None:
            print("Filtering feature not available")
            return
        deck = Deck(args.file)
        # load sample rate to construct filters
        import librosa
        _, sr = librosa.load(args.file, sr=None)
        if args.filter == "lowpass":
            f = LowpassFilter(cutoff_hz=args.cutoff, sr=sr)
        elif args.filter == "highpass":
            f = HighpassFilter(cutoff_hz=args.cutoff, sr=sr)
        else:
            f = NotchFilter(freq_hz=args.cutoff, sr=sr, q=args.q)
        newfile = deck.apply_filter(f)
        print("Filtered file written to:", newfile)
        return

    if args.cmd == "apply-effect":
        if Deck is None or Fader is None:
            print("Effects feature not available")
            return
        deck = Deck(args.file)
        import librosa
        _, sr = librosa.load(args.file, sr=None)
        if args.effect == "fader":
            eff = Fader(gain=args.gain)
        else:
            eff = Reverb(delay_ms=args.delay, decay=args.decay, repeats=args.repeats)
        newfile = deck.apply_effect(eff)
        print("Effect applied; output:", newfile)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
