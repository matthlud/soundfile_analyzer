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
- `runner play FILE [--full-length] [--demo] [--no-wait]` - Play audio file
  - `--full-length` - Play entire file (default)
  - `--demo` - Play only 3 seconds for preview
  - `--no-wait` - Start playback in background (returns immediately)

#### Playback Controls
- `runner control stop` - Stop current playback
- `runner control pause` - Pause current playback
- `runner control resume` - Resume from pause
- `runner control next` - Skip to next track
- `runner control restart` - Restart current track
- `runner control previous` - Go to previous track
- `runner control status` - Show playback status

#### Interactive DJ Mode
- `runner dj [--queue FILE]` - Launch interactive DJ mode with responsive console
  - `--queue FILE` - Use custom queue file (default: queue.json at repo root)

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

#### Responsive Console with Playback Controls

Keep the console responsive while music is playing! Start playback in background mode and issue control commands without interrupting the currently playing track.

**Background Playback:**
```bash
# Start playback in background
python runner.py play /path/to/song.wav --no-wait

# Console returns immediately; music plays in the background
# Now you can issue control commands:
```

**Playback Control Commands:**

All control commands execute immediately without waiting for current playback to finish:

```bash
# Control playback
python runner.py control stop      # Stop current playback
python runner.py control pause     # Pause playback
python runner.py control resume    # Resume from pause
python runner.py control next      # Skip to next track
python runner.py control restart   # Restart current track from beginning
python runner.py control previous  # Go to previous track
python runner.py control status    # Show current playback status
```

**Workflow Example:**

```bash
# Terminal 1: Start playing a song in background
$ python runner.py play song1.wav --no-wait
Playback started in background. Use 'control status' to check status.

# Terminal 1: Check status while music plays
$ python runner.py control status
State: playing
Playing: True
File: song1.wav

# Terminal 1 or 2: Queue new songs
$ python runner.py queue add song2.wav
$ python runner.py queue add song3.wav

# Terminal 1 or 2: View the queue while music plays
$ python runner.py queue show

# Terminal 1 or 2: Control playback at any time
$ python runner.py control pause   # Pause the current song
$ python runner.py control resume  # Resume playing
$ python runner.py control next    # Skip to next track (song2.wav)
```

**Features:**
- Console remains responsive for all commands
- Background playback thread runs independently
- Multiple control commands can be issued in quick succession
- Thread-safe state management
- Real-time progress display continues while console accepts commands
- Graceful handling of all playback state transitions

#### Interactive DJ Mode (Recommended!)

For the best interactive experience, use DJ mode to keep the console fully responsive while DJing:

```bash
python runner.py dj
```

This launches an interactive prompt where you can type commands freely while music plays. No more waiting for playback to finish - your input goes directly to the prompt!

**DJ Mode Commands:**
```
🎵 dj> play /path/to/song.wav          # Play a file
🎵 dj> demo /path/to/song.wav          # Play 3-second preview
🎵 dj> stop                             # Stop playback
🎵 dj> pause                            # Pause playback
🎵 dj> resume                           # Resume playback
🎵 dj> restart                          # Restart current track
🎵 dj> next                             # Skip to next track
🎵 dj> prev                             # Go to previous track
🎵 dj> status                           # Show playback status
🎵 dj> add /path/to/song.wav            # Add file to queue
🎵 dj> queue                            # Show queue
🎵 dj> queue next                       # Play next queued track
🎵 dj> queue clear                      # Clear the queue
🎵 dj> help                             # Show help
🎵 dj> exit                             # Exit DJ mode
```

**Why DJ Mode?**

DJ Mode provides true interactivity:
- Type commands at `🎵 dj>` prompt while music plays
- Progress bar displays without interfering with your input
- No waiting - commands are instant
- Main thread handles user input, background thread handles playback
- Thread-safe command processing
- Perfect for live DJing scenarios
- Automatic queue advancement on track completion

**DJ Mode Example Workflow:**
```bash
# Start DJ mode
$ python runner.py dj

🎵 dj> play intro.wav
============================================================
▶ NOW PLAYING
============================================================
File: intro.wav
Duration: 0:30
============================================================

Progress: [████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0:10/0:30 33.3%

🎵 dj> queue add next_song.wav    # Add while playing!
Added to queue: next_song.wav

🎵 dj> queue                       # Check queue
============================================================
🎵 PLAYBACK QUEUE
============================================================
► intro.wav (NOW PLAYING)

Upcoming:
  1. next_song.wav
============================================================

🎵 dj> status                      # Check status anytime
▶ Playback Status:
  State: playing
  Playing: True
  File: intro.wav

🎵 dj> pause                       # Pause for announcements
[Playback paused]

🎵 dj> resume                      # Resume after speaking
[Playback resumed]

🎵 dj> exit
Goodbye!
```

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
