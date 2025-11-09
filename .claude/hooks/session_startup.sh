#!/bin/bash
# Session startup hook that enforces todowrite_cli workflow and token optimization

# Run the Python startup script
python3 ~/.claude/session_startup.py

# Set environment variables for the session
export PYTHONPATH="lib_package/src:cli_package/src"
export TODOWRITE_DATABASE_URL="sqlite:///development_todowrite.db"

# Verify todowrite_cli is working
if ! PYTHONPATH="lib_package/src:cli_package/src" python -m todowrite_cli --version &>/dev/null; then
    echo "⚠️  todowrite_cli test failed - check your PYTHONPATH"
    echo "   Current PYTHONPATH: $PYTHONPATH"
else
    echo "✓ todowrite_cli is ready for use"
fi
