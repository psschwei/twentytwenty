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
cd twentytwenty
uv sync
uv run twentytwenty
```

### Install with pip
```bash
git clone <repository-url>
cd twentytwenty
pip install -e .
twentytwenty
```

### Pre-built Binary

Build a standalone binary that can run without Python installed:

```bash
# Build binary with desktop integration
uv run python build.py

# Install as desktop application (Linux)
uv run python build.py --install
```

After installation, you can find "Twenty Twenty" in your applications menu.

### From Source

To run directly from source code:

```bash
cd twentytwenty
uv sync
uv run twentytwenty
```

## Usage

1. **Start the application** - Run `uv run twentytwenty`
2. **Start timer** - Left-click or right-click the eye icon in your system tray, select "Start Timer"
3. **Take breaks** - When notified, look at something 20 feet away for 20 seconds
4. **Restart timer** - After each break, manually start the next 20-minute timer

### Tray Icon

The tray icon shows:
- **Green numbers** - More than 10 minutes remaining
- **Orange numbers** - 5-10 minutes remaining
- **Red numbers** - Less than 5 minutes remaining

## Development

### Technologies Used

- **Python 3.11+** - Core language
- **PyQt5** - Cross-platform GUI framework
- **uv** - Modern Python package and dependency management

### Project Structure
```
├── twentytwenty.py    # Main application
├── build.py           # Build script for creating binaries
├── pyproject.toml     # Project configuration
├── uv.lock            # Dependency lock file
├── .python-version    # Python version specification
├── .gitignore         # Git ignore rules
├── LICENSE            # MIT license
└── README.md          # This file
```

### Running in Debug Mode
For testing and development, you can run the application in debug mode:

```bash
# Using uv (recommended)
uv run twentytwenty --debug

# Using direct Python execution
uv run python twentytwenty.py --debug
```

Debug mode enables:
- **1-second timer intervals** instead of 20-minute intervals (for faster testing)
- **Detailed logging output** showing all debug messages
- **Enhanced development visibility** into timer operations

## Building Binaries

The project includes a comprehensive build script that creates standalone binaries and desktop integration files.

### Build Options

```bash
# Basic binary build
uv run python build.py

# Build and install as desktop application (Linux)
uv run python build.py --install

# Create directory distribution instead of single file
uv run python build.py --dir

# Build with console window (useful for debugging)
uv run python build.py --console
```

### Build Outputs

The build process creates:

- **Binary**: `dist/twentytwenty` - Standalone executable (~49MB)
- **Desktop file**: `twentytwenty.desktop` - Linux application menu entry
- **Icon**: `twentytwenty.png` - Application icon

### Desktop Integration (Linux)

When using `--install`, the application is installed to:
- Binary: `~/.local/bin/twentytwenty`
- Desktop entry: `~/.local/share/applications/twentytwenty.desktop`
- Icon: `~/.local/share/icons/twentytwenty.png`

After installation, "Twenty Twenty" appears in your applications menu under Utilities/Health.

## Development

This project uses modern Python tooling:

- **uv** for dependency management and virtual environments
- **PyQt5** for the GUI framework
- **PyInstaller** for binary creation
- **Python 3.11+** as the minimum required version

### Setting Up Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd twentytwenty

# Install dependencies
uv sync

# Run in development mode
uv run twentytwenty --debug

# Or run directly with Python
uv run python twentytwenty.py --debug
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please feel free to submit issues and pull requests.