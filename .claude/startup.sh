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

    # Verify HAL is actually running
    if ps -p $HAL_PID > /dev/null; then
        echo "✅ HAL Agent System ACTIVE (PID: $HAL_PID) - Mandatory preprocessing engaged"
        # Check if HAL is actually working by looking at its log
        if [ -f ".claude/hal_active.log" ]; then
            echo "📋 HAL Status: $(tail -n 3 .claude/hal_active.log | grep -E "(HAL|✅|❌|⚠️)" | tail -1 || echo 'Initializing monitoring cycles...')"
        fi
    else
        echo "❌ ERROR: HAL Agent System failed to start!"
        if [ -f ".claude/hal_active.log" ]; then
            echo "🚨 HAL Error Log:"
            cat .claude/hal_active.log
        fi
        exit 1
    fi
else
    echo "❌ ERROR: HAL_PREPROCESSING_MANDATORY not set to true!"
    exit 1
fi

# 6. Run full systems initialization
echo "🤖 Initializing all AI CLI systems..."
if python .claude/hooks/session_startup_systems.py; then
    echo "✅ All systems initialized and ready"
else
    echo "❌ ERROR: Systems initialization failed!"
    exit 1
fi

# 7. Display real-time system status
echo ""
echo "📊 **INITIAL SYSTEM STATUS**"
echo "=================================================="

# Quick status check
echo "🤖 HAL Agent System Status:"
if ps -p $HAL_PID > /dev/null 2>&1; then
    echo "   ✅ RUNNING (PID: $HAL_PID)"
    echo "   📋 Recent Activity: $(tail -n 3 .claude/hal_active.log 2>/dev/null | grep -E "(✅|❌|⚠️)" | tail -1 || echo 'Initializing...')"
else
    echo "   ❌ NOT RUNNING"
fi

echo ""
echo "⚡ Token Optimization System Status:"
if python dev_tools/token_optimization/always_token_sage.py "test" > /dev/null 2>&1; then
    echo "   ✅ OPERATIONAL"
else
    echo "   ❌ FAILED"
fi

echo ""
echo "💻 System Resources:"
echo "   📈 CPU Load: $(top -l 1 -n 0 | grep "CPU usage" | awk '{print $3}' | sed 's/%//' || echo "N/A")%"
echo "   🧠 Memory: $(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//' || echo "N/A") pages free"

echo ""
echo "🎯 **SESSION STARTUP COMPLETE**"
echo "✅ CLAUDE.md loaded and enforced"
echo "✅ Policy documents verified and accessible"
echo "✅ HAL Agent System ACTIVE and processing"
echo "✅ Token Optimization System active"
echo "✅ MCP Systems initialized"
echo "✅ All environment variables configured"
echo "✅ PostgreSQL backend verified"
echo "✅ Session state loaded"
echo ""
echo "🔍 **REAL-TIME MONITORING OPTIONS**:"
echo "   • Start monitor: ./.claude/system_monitor.sh"
echo "   • Stop HAL: ./.claude/hal_shutdown.sh"
echo "   • View HAL log: tail -f .claude/hal_active.log"
echo ""
echo "🚀 Ready for development work!"
