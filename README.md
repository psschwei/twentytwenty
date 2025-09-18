# 20-20-20 Eye Break Timer

A cross-platform desktop application that implements the 20-20-20 rule to help prevent eye strain from computer use.

## What is the 20-20-20 Rule?

The 20-20-20 rule is a simple guideline to reduce eye strain:
- Every **20 minutes**, take a **20-second break**
- Look at something **20 feet away** (across the room or out a window)

This helps relax your eye muscles and reduce digital eye strain from prolonged screen time.

## Features

- **System tray integration** - Runs quietly in the background
- **Visual countdown** - Tray icon shows minutes remaining
- **Gentle notifications** - Non-intrusive break reminders
- **Guided breaks** - 20-second countdown with instructions
- **Manual control** - Start/stop timer as needed
- **Cross-platform** - Works on Linux, Windows, and macOS

## Installation

### Requirements
- Python 3.11+
- PyQt5
- Desktop environment with system tray support (Linux, Windows, macOS)

### Install with uv (recommended)
```bash
git clone <repository-url>
cd 20-20-20
uv sync
uv run twentytwenty
```

### Install with pip
```bash
git clone <repository-url>
cd 20-20-20
pip install -e .
twentytwenty
```

### Pre-built Packages

Download pre-built packages from the [Releases](https://github.com/YOUR_USERNAME/twentytwenty/releases) page:

**Linux:**
- `.rpm` - For Fedora, RHEL, SUSE
- `.deb` - For Ubuntu, Debian

**Windows:**
- `.exe` - Standalone executable
- `.msi` - Windows installer

**macOS:**
- `.app` - Application bundle
- `.dmg` - Disk image installer

## Usage

1. **Start the application** - Run `twentytwenty` or `uv run twentytwenty`
2. **Start timer** - Left-click or right-click the eye icon in your system tray, select "Start Timer"
3. **Take breaks** - When notified, look at something 20 feet away for 20 seconds
4. **Restart timer** - After each break, manually start the next 20-minute timer

### Tray Icon

The tray icon shows:
- **Green numbers** - More than 10 minutes remaining
- **Orange numbers** - 5-10 minutes remaining
- **Red numbers** - Less than 5 minutes remaining

## Development

Built with:
- **Python 3.11+**
- **PyQt5** - GUI framework
- **uv** - Modern Python package management

### Project Structure
```
├── twentytwenty.py    # Main application
├── pyproject.toml     # Project configuration
└── README.md          # This file
```

### Running in Debug Mode
For testing and development, you can run the application in debug mode:

```bash
# Using uv (recommended)
uv run twentytwenty --debug

# Using direct Python execution
python3 twentytwenty.py --debug
```

Debug mode enables:
- **1-second timer intervals** instead of 20-minute intervals (for faster testing)
- **Detailed logging output** showing all debug messages
- **Enhanced development visibility** into timer operations

## Building from Source

### Local Building

Use the build scripts to create packages locally:

```bash
# Build for current platform
python build.py

# Build for specific platform
python build.py --platform linux    # RPM and DEB
python build.py --platform windows  # EXE and MSI
python build.py --platform macos    # APP and DMG

# Build specific format
python build.py --platform linux --format rpm
python build.py --platform windows --format exe

# List available targets
python build.py --list
```

### Requirements for Building

**Linux (RPM):** `rpm-build`, `python3-dev`
**Linux (DEB):** `build-essential`, `debhelper`, `dh-python`
**Windows:** `pyinstaller`, `cx_Freeze` (optional)
**macOS:** `pyinstaller`, Xcode command line tools

### GitHub Actions

Packages are automatically built for all platforms on:
- Push to main/develop branches
- Pull requests
- Tagged releases (creates GitHub release with packages)

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please feel free to submit issues and pull requests.