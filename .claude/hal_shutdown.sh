#!/bin/bash
# HAL Shutdown Script - Properly stops active HAL Agent System

echo "🛑 Shutting down HAL Agent System..."

# Check if HAL PID file exists
if [ -f ".claude/hal_active.pid" ]; then
    HAL_PID=$(cat .claude/hal_active.pid)

    # Check if process is still running
    if ps -p $HAL_PID > /dev/null 2>&1; then
        echo "🔄 Stopping HAL process (PID: $HAL_PID)..."
        kill $HAL_PID

        # Wait for graceful shutdown
        sleep 2

        # Force kill if still running
        if ps -p $HAL_PID > /dev/null 2>&1; then
            echo "⚡ Force stopping HAL process..."
            kill -9 $HAL_PID
            sleep 1
        fi

        echo "✅ HAL Agent System stopped"
    else
        echo "⚠️  HAL process not running (stale PID file)"
    fi

    # Clean up PID file
    rm -f .claude/hal_active.pid
else
    echo "⚠️  No HAL PID file found - HAL may not be running"
fi

# Clean up log file if desired
# rm -f .claude/hal_active.log

echo "✅ HAL shutdown complete"
