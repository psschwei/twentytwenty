#!/bin/bash
# Convenience wrapper for the Python build script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run the Python build orchestrator
python3 "$SCRIPT_DIR/build.py" "$@"