# soundfile_analyzer

**A small, local-first command-line tool for finding, previewing, and playing a DJ
set.** It also includes optional audio metadata, visualization, filtering, and
effect commands.

## What it does

- Interactive DJ console with playback controls and a persistent queue
- Full-track playback or quick three-second previews
- Track metadata and audio-file listings
- Waveform, spectrogram, and frequency visualizations
- Optional filters and effects for preparing files
- Scriptable commands for queueing and playback

The primary workflow is `dj`; the other commands are preparation and inspection
tools rather than separate applications.

## Requirements

- Linux with Python 3.11 or newer
- VLC installed and available on `PATH` for playback
- A supported audio file such as WAV, MP3, FLAC, or OGG

On Debian/Ubuntu:

```bash
sudo apt install vlc
```

## Install

From a checkout:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
```

For development and tests:

```bash
python -m pip install -r requirements.txt
```

The install creates the `soundfile-analyzer` command. You can also use
`python -m src.runner` directly from the repository.

## Start a set

Launch the interactive console:

```bash
soundfile-analyzer dj
```

To index a music folder immediately:

```bash
soundfile-analyzer dj --library ~/Music
```

Typical first-set workflow:

```text
dj> add /music/intro.wav
dj> add "/music/long filename.mp3"
dj> queue
dj> queue next
dj> find house
dj> pause
dj> resume
dj> next
dj> status
dj> exit
```

The queue is stored outside the repository by default. Use `--queue PATH` when
you want a portable queue file next to a set or need separate queues:

```bash
soundfile-analyzer dj --queue ./my-set.json
```

### Interactive commands

| Command | Purpose |
| --- | --- |
| `play FILE` | Play a full track immediately |
| `demo FILE` | Preview a track for three seconds |
| `pause` / `resume` | Pause or continue the current track |
| `stop` | Stop playback |
| `next` | Skip to the next queued track |
| `previous` | Return to the previous track when history is available |
| `restart` | Restart the current track |
| `add FILE` | Add a track to the queue |
| `queue` | Show the current and upcoming tracks |
| `queue next` | Start the next queued track |
| `queue clear` | Clear upcoming tracks |
| `scan FOLDER` | Index supported audio files recursively |
| `find TEXT` | Search indexed title, artist, album, or path |
| `status` | Show playback and queue status |
| `help` / `exit` | Show help or leave DJ mode |

Paths containing spaces should be quoted. Missing files and playback failures
are reported without terminating the console.

The library index is intentionally lightweight and rebuilt when `scan` is run;
it does not copy or modify music files. Search results show the original path so
they can be passed directly to `play` or `add`.

## One-shot commands

```bash
soundfile-analyzer list --dir ~/Music
soundfile-analyzer info ~/Music/track.mp3
soundfile-analyzer play ~/Music/track.mp3
soundfile-analyzer play ~/Music/track.mp3 --demo
soundfile-analyzer queue add ~/Music/next.mp3
soundfile-analyzer queue show
soundfile-analyzer queue next
soundfile-analyzer visualize ~/Music/track.wav --waveform --spectrogram
```

Run `soundfile-analyzer --help` and the command-specific `--help` flags for
the complete option list.

## Analysis and preparation

The analyzer is intentionally secondary to the DJ workflow:

- `info` reads duration, bitrate, sample rate, channels, and embedded tags.
- `visualize` writes waveform, spectrogram, and frequency images to
  `./artifacts/`.
- `apply-filter` and `apply-effect` write processed audio to temporary output
  files.

These commands can require more CPU and memory than playback. Run them before a
set rather than during a live performance.

## Deliberately deferred

The current lean release does not attempt beat matching, time-stretching, cue
points, crossfading, normalization, or a full-screen terminal UI. Those features
need backend-specific testing and should be added only after the dependable
queue/library workflow is in regular use. Keeping them out of the live path
also keeps installation and failure recovery simple.

## Development

```bash
python -m pip install -e ".[dev]"
python -m compileall -q src tests
python -m ruff check src tests
python -m build
python -m pytest -q
```

Playback tests use the real command and queue interfaces but do not require an
audio device. VLC/device smoke tests should be run manually on the target Linux
machine. GitHub Actions runs the same compile, lint, build, and test checks for
pushes and pull requests.

## License

See [LICENSE](LICENSE).
