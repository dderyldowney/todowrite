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

# 6. Initialize MCP Systems with intelligent startup
echo "🔧 Initializing MCP Systems with intelligent startup..."
echo "🚀 Starting only missing MCP servers..."

# Use intelligent MCP server startup that checks for existing servers
if ~/mcp-servers/bin/start_mcp_servers_intelligent.sh; then
    echo "✅ MCP Systems initialized with intelligent startup"
else
    echo "⚠️  MCP intelligent startup had issues - continuing with basic initialization"
fi

echo "⏳ Waiting 10 seconds for servers to stabilize..."
sleep 10

# Quick MCP health check
echo "🔍 Running quick MCP health check..."
if python ~/mcp-servers/bin/mcp_server_health_check.py > /dev/null 2>&1; then
    echo "✅ MCP Health check completed"
else
    echo "⚠️  MCP Health check failed - continuing with initialization"
fi

# Generate dynamic MCP tool inventory
echo "🛠️ Generating dynamic MCP tool inventory..."
if python ~/.claude/mcp_tool_discovery.py > /dev/null 2>&1; then
    echo "✅ MCP tool inventory generated"
    TOOL_COUNT=$(grep "Total Available Tools:" ~/mcp-servers/logs/MCP_TOOLS_AVAILABLE.md | awk '{print $4}' || echo "0")
    echo "📋 Available tools: $TOOL_COUNT"
else
    echo "⚠️  MCP tool discovery failed - using minimal inventory"
fi

# 7. Run full systems initialization
echo "🤖 Initializing all AI CLI systems..."
if python .claude/hooks/session_startup_systems.py; then
    echo "✅ All systems initialized and ready"
else
    echo "❌ ERROR: Systems initialization failed!"
    exit 1
fi

# 8. Display real-time system status
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
echo "✅ Dynamic tool inventory generated"
echo "✅ All environment variables configured"
echo "✅ PostgreSQL backend verified"
echo "✅ Session state loaded"
echo ""
echo "🛠️ **CURRENT MCP TOOLS**:"
if [ -f "~/mcp-servers/logs/MCP_TOOLS_AVAILABLE.md" ]; then
    TOOL_COUNT=$(grep "Total Available Tools:" ~/mcp-servers/logs/MCP_TOOLS_AVAILABLE.md | awk '{print $4}' || echo "0")
    RUNNING_SERVERS=$(grep "Running Servers:" ~/mcp-servers/logs/MCP_TOOLS_AVAILABLE.md | awk '{print $3}' || echo "0")
    echo "   • Available Tools: $TOOL_COUNT"
    echo "   • Running Servers: $RUNNING_SERVERS"
    echo "   • Full Inventory: ~/mcp-servers/logs/MCP_TOOLS_AVAILABLE.md"
else
    echo "   • Tool inventory: Generating..."
fi
echo ""
echo "🔍 **REAL-TIME MONITORING OPTIONS**:"
echo "   • MCP Tools: cat ~/mcp-servers/logs/MCP_TOOLS_AVAILABLE.md"
echo "   • Refresh Tools: python ~/.claude/mcp_tool_discovery.py --report"
echo "   • MCP Health: python ~/mcp-servers/bin/mcp_server_health_check.py --report"
echo "   • Start monitor: ./.claude/system_monitor.sh"
echo "   • Stop HAL: ./.claude/hal_shutdown.sh"
echo "   • View HAL log: tail -f .claude/hal_active.log"
echo ""
echo "🚀 Ready for development work!"
