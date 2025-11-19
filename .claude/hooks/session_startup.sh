#!/bin/bash
# Session startup hook - Enforces CLAUDE.md rules for ALL sessions

echo "🚀 Running session startup enforcement..."

# 1. Set required environment variables
export PYTHONPATH="lib_package/src:cli_package/src"

# PostgreSQL is now the preferred development backend
# The setup_postgresql_development.py script will configure the correct URL
# export TODOWRITE_DATABASE_URL will be set by the PostgreSQL setup script

# CRITICAL: Set project-specific episodic memory database path
export EPISODIC_MEMORY_DB_PATH=".claude/episodic_memory.db"
echo "📍 Project episodic memory database: $EPISODIC_MEMORY_DB_PATH"

# 2. Activate virtual environment if not already active
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "📦 Activating virtual environment..."
    source "$PWD/.venv/bin/activate"
fi

# 3. Initialize PostgreSQL development environment
echo "🐳 Initializing PostgreSQL development environment..."
python .claude/hooks/setup_postgresql_development.py

# Source PostgreSQL environment if created
if [ -f ".claude/postgresql_env.sh" ]; then
    echo "🔧 Loading PostgreSQL environment..."
    source .claude/postgresql_env.sh
fi

# Source episodic memory environment if created
if [ -f ".claude/episodic_memory_env.sh" ]; then
    echo "🧠 Loading episodic memory PostgreSQL environment..."
    source .claude/episodic_memory_env.sh
fi

# 4. Run comprehensive session initialization
echo "🔧 Initializing session with comprehensive enforcement..."
python .claude/hooks/session_initialization.py

# 5. Run permanent enforcement activation (CRITICAL: runs after every /clear)
echo "🔒 Activating permanent code quality enforcement..."
python .claude/autorun.py

# 6. Run AI CLI systems verification
echo "🤖 Verifying AI CLI systems..."
python .claude/hooks/session_startup_systems.py

# 7. Initialize episodic memory
echo "🧠 Initializing episodic memory..."
python .claude/hooks/session_startup_episodic_memory.py

echo "✅ Session startup enforcement complete - All systems ready"
