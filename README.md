# soundfile_analyzer

Evaluation of soundfiles (visualization, playback, filtering, cutting, etc.)

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

A top-level command-line runner is available at src/runner.py which exposes common DJ-style operations:

- runner list [-d DIR] : list audio files in DIR (defaults to src/tests or tests/).
- runner info FILE : show metadata for FILE.
- runner visualize FILE [--waveform] [--spectrogram] [--frequency] : create visual artifacts in ./artifacts/.
- runner play FILE : play a file (requires python-vlc).
- runner queue add FILE : add FILE to a persistent queue (queue.json at repo root).
- runner queue next : pop and play the next file from the queue.
- runner apply-filter FILE --filter {lowpass,highpass,notch} [--cutoff N] [--q Q] : apply a filter and write a temporary output file.

Run the CLI from the repository root using:

```bash
python -m src.runner <command> [options]
```

Requirements for these features: librosa, soundfile, scipy, python-vlc (for playback). Run tests with `pytest` from the repo root.

## License

See [LICENSE](LICENSE) file for details.
