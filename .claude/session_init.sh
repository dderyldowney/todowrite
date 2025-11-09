#!/bin/bash

# Claude Code Session Initialization Script
# This script is automatically executed by Claude Code CLI at session start

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Get the project root directory
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Initializing Claude Code session for ToDoWrite project..."

# Add dev_tools to Python path for this session
export PYTHONPATH="$PROJECT_ROOT/dev_tools:$PYTHONPATH"

# Set environment variables for token optimization
export CLAUDE_TOKEN_OPTIMIZATION="enabled"
export CLAUDE_DEFAULT_AGENT="token-sage"
export CLAUDE_HAL_AGENTS="enabled"

# Set project root
export TODOWRITE_PROJECT_ROOT="$PROJECT_ROOT"

# Execute Python session startup
python3 "$SCRIPT_DIR/session_startup.py"

echo "✅ Session initialization complete"
