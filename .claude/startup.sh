#!/bin/bash
# MANDATORY STARTUP SEQUENCE - MUST RUN ON EVERY SESSION START
# This script ensures all systems are properly initialized

echo "🚀 **STARTING SESSION - LOADING ALL CONFIGURATION**"
echo "=================================================="

# 1. Source environment variables
echo "📋 Loading environment variables..."
if [ -f ".env.dev" ]; then
    source .env.dev
    echo "✅ Development environment variables loaded"
else
    echo "❌ ERROR: .env.dev file not found!"
    exit 1
fi

# 2. Activate virtual environment
echo "🐍 Activating virtual environment..."
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ ERROR: .venv directory not found!"
    exit 1
fi

# 3. Set PYTHONPATH
echo "🛠️  Setting Python paths..."
export PYTHONPATH="lib_package/src:cli_package/src"
echo "✅ Python paths configured"

# 4. Run startup enforcement (loads CLAUDE.md and verifies policy documents)
echo "📋 Running startup enforcement (CLAUDE.md + Policy Documents)..."
if python .claude/startup_enforcement.py; then
    echo "✅ CLAUDE.md and all policy documents loaded"
else
    echo "❌ ERROR: Startup enforcement failed!"
    exit 1
fi

# 5. Start HAL Agent System (MANDATORY ACTIVE PREPROCESSING)
echo "🤖 Starting HAL Agent System (Mandatory Active Preprocessing)..."
if [ "$HAL_PREPROCESSING_MANDATORY" = "true" ]; then
    # Start HAL continuous monitoring for active preprocessing
    nohup .claude/hal_active_monitor.sh > .claude/hal_active.log 2>&1 &
    HAL_PID=$!
    echo $HAL_PID > .claude/hal_active.pid
    sleep 5  # Give HAL monitor time to initialize and run first cycle

    # Verify HAL is running
    if ps -p $HAL_PID > /dev/null; then
        echo "✅ HAL Agent System ACTIVE (PID: $HAL_PID) - Mandatory preprocessing engaged"
        echo "📋 HAL Status: $(tail -n 1 .claude/hal_active.log 2>/dev/null || echo 'Initializing...')"
    else
        echo "❌ ERROR: HAL Agent System failed to start!"
        exit 1
    fi
else
    echo "⚠️  HAL preprocessing not mandatory - bypassing active monitoring"
fi

# 6. Initialize Development Systems
echo "🔧 Initializing Development Systems..."

# Verify PostgreSQL connectivity
echo "📋 Verifying PostgreSQL connectivity..."
if docker exec todowrite-postgres psql -U todowrite_user -d todowrite -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ PostgreSQL accessible"
else
    echo "❌ ERROR: PostgreSQL not accessible!"
    exit 1
fi

# Initialize and verify ToDoWrite database
echo "📋 Initializing ToDoWrite database..."
if python .claude/todowrite_database_manager.py --init > /dev/null 2>&1; then
    echo "✅ ToDoWrite database initialized"
else
    echo "⚠️  ToDoWrite database initialization encountered issues (may be already initialized)"
fi

# Verify session state
echo "📋 Verifying session state..."
if python .claude/session_manager.py --summary > /dev/null 2>&1; then
    echo "✅ Session state loaded"
else
    echo "⚠️  Session state loading encountered issues"
fi

echo ""
echo "✅ **STARTUP SEQUENCE COMPLETE**"
echo "📋 Ready for development work"
echo ""
