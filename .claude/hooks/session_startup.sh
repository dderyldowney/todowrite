#!/bin/bash
# Session startup hook - Enforces CLAUDE.md rules for ALL sessions

echo "🚀 Running session startup enforcement..."

# 1. Set required environment variables
export PYTHONPATH="$PWD/lib_package/src:$PWD/cli_package/src"
export TODOWRITE_DATABASE_URL="sqlite:///$HOME/dbs/todowrite_development.db"

# 2. Activate virtual environment if not already active
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "📦 Activating virtual environment..."
    source "$PWD/.venv/bin/activate"
fi

# 3. Run comprehensive session initialization
echo "🔧 Initializing session with comprehensive enforcement..."
python .claude/hooks/session_initialization.py

# 4. Run AI CLI systems verification
echo "🤖 Verifying AI CLI systems..."
python .claude/hooks/session_startup_systems.py

# 5. Initialize episodic memory
echo "🧠 Initializing episodic memory..."
python .claude/hooks/session_startup_episodic_memory.py

echo "✅ Session startup enforcement complete - All systems ready"
