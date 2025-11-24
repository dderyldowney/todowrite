#!/bin/bash
# Quick Status Check - Fast system health overview

echo "🔍 **QUICK SYSTEM STATUS**"
echo "=================================================="
echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# HAL Status
echo "🤖 HAL Agent System:"
if [[ -f ".claude/hal_active.pid" ]]; then
    hal_pid=$(cat .claude/hal_active.pid)
    if ps -p "$hal_pid" > /dev/null 2>&1; then
        uptime=$(ps -o etime= -p "$hal_pid" 2>/dev/null | tr -d ' ')
        echo "   ✅ RUNNING (PID: $hal_pid, Uptime: $uptime)"
    else
        echo "   ❌ DEAD (PID file exists but process dead)"
    fi
else
    echo "   ❌ NOT RUNNING (no PID file)"
fi

# Token Optimization Status
echo ""
echo "⚡ Token Optimization System:"
if python dev_tools/token_optimization/always_token_sage.py "test" > /dev/null 2>&1; then
    echo "   ✅ OPERATIONAL"
else
    echo "   ❌ FAILED"
fi

# System Resources
echo ""
echo "💻 System Resources:"
cpu_load=$(top -l 1 -n 0 | grep "CPU usage" | awk '{print $3}' | sed 's/%//' || echo "N/A")
mem_free=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//' || echo "N/A")
echo "   📈 CPU Load: ${cpu_load}%"
echo "   🧠 Memory Free: ${mem_free} pages"

# Monitoring Options
echo ""
echo "🔧 **MANAGEMENT OPTIONS**:"
echo "   📊 Real-time Monitor: ./.claude/system_monitor.sh"
echo "   🛑 Stop HAL: ./.claude/hal_shutdown.sh"
echo "   📋 HAL Log: tail -f .claude/hal_active.log"
echo "   🚀 Full Restart: ./.claude/startup.sh"
echo ""
echo "=================================================="
