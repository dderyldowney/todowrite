#!/bin/bash
# One-time setup for ToDoWrite AI CLI

echo "🚀 ToDoWrite AI CLI - One Time Setup"
echo "=================================="
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ] || [ ! -d ".claude" ]; then
    echo "❌ ERROR: Must be run from ToDoWrite project root directory"
    echo "   Navigate to the ToDoWrite project directory first"
    exit 1
fi

# Make the startup script executable
echo "📋 Making startup script executable..."
chmod +x start-ai-cli.sh

# Create the databases directory if it doesn't exist
echo "📁 Creating databases directory..."
mkdir -p "$HOME/dbs"

# Check if uv is installed
if ! command -v uv >/dev/null 2>&1; then
    echo "⚠️  WARNING: 'uv' not found. Installing..."
    pip install uv
fi

# Sync dependencies (creates .venv if needed)
echo "📦 Installing dependencies..."
uv sync

# Initialize the database if needed
if [ ! -f "$HOME/dbs/todowrite_development.db" ]; then
    echo "🗄️  Initializing ToDoWrite database..."
    source .venv/bin/activate
    python .claude/auto_init_todowrite_models.py
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 FROM NOW ON, just run:"
echo "   ./start-ai-cli.sh ."
echo ""
echo "📝 That's it! No more manual venv activation needed!"
echo "   The script handles everything automatically."
