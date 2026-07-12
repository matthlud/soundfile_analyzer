# soundfile_analyzer

Comprehensive audio analysis and DJ-style playback system. Features visualization, real-time playback with progress tracking, filtering, queue management, and audio effects.

![Docu1](/docs/equipment_desk_1920s.jpeg)

## Requirements

- **Python 3.13 or newer**

## Installation

### 1. Install Python 3.13+

Ensure you have Python 3.13 or newer installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

To check your Python version:
```bash
python3 --version
```

### 2. Create a Virtual Environment

A virtual environment isolates project dependencies from your system Python. Create one using `venv`:

```bash
python3 -m venv soundfile_analyzer_venv
```

This creates a `soundfile_analyzer_venv/` directory in your project.

### 3. Activate the Virtual Environment

**On Linux/macOS:**
```bash
source soundfile_analyzer_venv/bin/activate
```

**On Windows (PowerShell):**
```bash
soundfile_analyzer_venv\Scripts\Activate.ps1
```

**On Windows (cmd):**
```bash
soundfile_analyzer_venv\Scripts\activate.bat
```

Your command prompt should now show `(soundfile_analyzer_venv)` prefix, indicating the virtual environment is active.

### 4. Install Dependencies

With the virtual environment activated, install project dependencies:

```bash
pip install -r requirements.txt
```

### 5. Deactivate Virtual Environment

When finished working, deactivate the virtual environment:
```bash
deactivate
```

## Directory Layout

```
soundfile_analyzer/
├── .github/              # GitHub configuration and workflows
├── .vscode/              # VS Code settings and extensions
├── artifacts/            # Generated output files (spectrograms, waveforms, etc.)
├── docs/                 # Documentation and reference images
├── src/                  # Source code
├── tests/                # Unit tests
├── .gitignore            # Git ignore rules
├── .flake8               # Flake8 linter configuration
├── LICENSE               # License file
├── README.md             # This file
├── requirements.txt      # Python dependencies
└── TODO                  # Development todo list
```

### Directory Descriptions

- **.github/** - GitHub-specific configuration, including workflows for CI/CD
- **.vscode/** - VS Code workspace settings and recommended extensions
- **artifacts/** - Output directory for generated visualizations and processed audio files
- **docs/** - Documentation, including images and reference materials
- **src/** - Main source code for the audio analyzer application
- **tests/** - Automated tests for validating functionality

## Runner CLI

A comprehensive command-line interface for audio analysis and DJ operations available at `src/runner.py`.

### Commands

#### Listing and Info
- `runner list [-d DIR]` - List audio files in directory (defaults to src/tests/)
- `runner info FILE` - Show metadata and file information

#### Visualization
- `runner visualize FILE [--waveform] [--spectrogram] [--frequency]` - Create visual artifacts in ./artifacts/

#### Playback
- `runner play FILE [--full-length] [--demo]` - Play audio file
  - `--full-length` - Play entire file (default)
  - `--demo` - Play only 3 seconds for preview

#### Queue Management
- `runner queue add FILE` - Add file to persistent queue
- `runner queue show` - Display full queue with current item highlighted
- `runner queue list` - List queue items
- `runner queue next [--full-length] [--demo]` - Play next queued item

#### Filtering
- `runner apply-filter FILE --filter {lowpass,highpass,notch} [--cutoff N] [--q Q]` - Apply frequency filter

#### Effects
- `runner apply-effect FILE --effect {fader,reverb} [--gain N] [--delay MS] [--decay N] [--repeats N]` - Apply DJ effects

### Enhanced Playback Features

#### Full-Length Playback
Audio files now play in their entirety by default. Use `--demo` to preview just 3 seconds.

**Examples:**
```bash
# Play full song (default)
python runner.py play /path/to/song.wav

# Play only 3 seconds for preview
python runner.py play /path/to/song.wav --demo
```

#### Real-Time Playback Display
Console shows live progress with formatted time and percentage:

**Now Playing Header:**
```
============================================================
▶ NOW PLAYING
============================================================
File: song.wav
Duration: 3:45
============================================================
```

**Real-Time Progress Bar:**
```
Progress: [████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 1:45/3:45 46.7%
```

Features:
- Filled █ and empty ░ indicators showing progress
- Current time and total duration (MM:SS format)
- Percentage completion
- Color-coded output for visibility
- Real-time updates every 100ms
- UTF-8 symbols for visual appeal (▶, ✓, █, ░, 🎵)

**Completion Message:**
```
============================================================
✓ Playback complete!
============================================================
```

#### Enhanced Queue Display
Visualize your queue with current item highlighted:

```
============================================================
🎵 PLAYBACK QUEUE
============================================================
► current_song.wav (NOW PLAYING)

Upcoming:
  1. next_song_1.wav
  2. next_song_2.wav
  3. next_song_3.wav
============================================================
```

Features:
- Current item marked with ▶ indicator
- Numbered queue items
- Automatic truncation for large queues (shows first 10 + count of remaining)
- Color-coded for easy reading
- Persistent storage to `queue.json` at repository root

### Usage Examples

**Example 1: Play a Single Song**
```bash
cd src
python runner.py play ../samples/music.wav
```

Output:
```
============================================================
▶ NOW PLAYING
============================================================
File: music.wav
Duration: 4:32
============================================================

Progress: [████████████████████████████████░░░░░░░░░] 3:15/4:32 69.2%
```

**Example 2: Queue Multiple Songs**
```bash
# Add songs to queue
python runner.py queue add song1.wav
python runner.py queue add song2.wav
python runner.py queue add song3.wav

# View queue
python runner.py queue show

# Play next song with full-length playback and UI
python runner.py queue next
```

**Example 3: Demo Mode Preview**
```bash
# Quick 3-second preview
python runner.py play song.wav --demo
```

### Running the CLI

From the repository root:
```bash
python -m src.runner <command> [options]
```

Or from src directory:
```bash
python runner.py <command> [options]
```

Run tests with `pytest` from the repo root:
```bash
pytest tests/ -v
```

### Dependencies

Core features require:
- librosa - Audio analysis
- soundfile - Audio I/O
- scipy - Signal processing
- python-vlc - Audio playback
- colorama - Console colors

See `requirements.txt` for complete dependency list.

## License

See [LICENSE](LICENSE) file for details.
