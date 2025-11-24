#!/bin/bash
# Real-time System Monitor - Monitors HAL and Token Optimization with auto-restart

# Configuration
HAL_CHECK_INTERVAL=15  # Check every 15 seconds
TOKEN_CHECK_INTERVAL=20  # Check every 20 seconds
MAX_RESTART_ATTEMPTS=3
RESTART_COOLDOWN=30  # Seconds between restart attempts

# State tracking
HAL_RESTART_COUNT=0
TOKEN_RESTART_COUNT=0
LAST_HAL_RESTART=0
LAST_TOKEN_RESTART=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log_status() {
    echo "[$(date '+%H:%M:%S')] $1"
}

log_success() {
    echo -e "${GREEN}[$(date '+%H:%M:%S')] ✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%H:%M:%S')] ⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}[$(date '+%H:%M:%S')] ❌ $1${NC}"
}

log_info() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')] ℹ️  $1${NC}"
}

# Check HAL Agent System status
check_hal_status() {
    local hal_pid_file=".claude/hal_active.pid"

    if [[ -f "$hal_pid_file" ]]; then
        local hal_pid=$(cat "$hal_pid_file")
        if ps -p "$hal_pid" > /dev/null 2>&1; then
            # Check if HAL process is actually responsive
            local hal_log=".claude/hal_active.log"
            if [[ -f "$hal_log" ]]; then
                local last_activity=$(tail -n 5 "$hal_log" 2>/dev/null | grep -c "HAL" || echo "0")
                if [[ "$last_activity" -gt 0 ]]; then
                    return 0  # HAL is healthy
                fi
            fi
            return 1  # HAL process exists but not responding
        else
            return 2  # HAL process is dead
        fi
    else
        return 3  # HAL PID file missing
    fi
}

# Check Token Optimization System status
check_token_status() {
    # Test token optimization system with a quick check
    local test_output
    test_output=$(python dev_tools/token_optimization/always_token_sage.py "test" 2>&1 | head -n 1)
    if [[ $? -eq 0 && -n "$test_output" ]]; then
        return 0  # Token system is healthy
    else
        return 1  # Token system failed
    fi
}

# Restart HAL Agent System
restart_hal() {
    local current_time=$(date +%s)
    local time_since_restart=$((current_time - LAST_HAL_RESTART))

    if [[ $time_since_restart -lt $RESTART_COOLDOWN ]]; then
        log_warning "HAL restart cooldown active ($((RESTART_COOLDOWN - time_since_restart))s remaining)"
        return 1
    fi

    if [[ $HAL_RESTART_COUNT -ge $MAX_RESTART_ATTEMPTS ]]; then
        log_error "HAL maximum restart attempts ($MAX_RESTART_ATTEMPTS) reached!"
        return 2
    fi

    log_warning "Restarting HAL Agent System (attempt $((HAL_RESTART_COUNT + 1))/$MAX_RESTART_ATTEMPTS)"

    # Stop existing HAL if running
    if [[ -f ".claude/hal_active.pid" ]]; then
        local old_pid=$(cat .claude/hal_active.pid)
        if ps -p "$old_pid" > /dev/null 2>&1; then
            kill "$old_pid" 2>/dev/null
            sleep 2
            kill -9 "$old_pid" 2>/dev/null
        fi
        rm -f ".claude/hal_active.pid"
    fi

    # Start HAL monitor
    nohup .claude/hal_active_monitor.sh > .claude/hal_active.log 2>&1 &
    local new_pid=$!
    echo $new_pid > .claude/hal_active.pid

    # Wait and verify
    sleep 5
    if ps -p "$new_pid" > /dev/null 2>&1; then
        log_success "HAL Agent System restarted successfully (PID: $new_pid)"
        HAL_RESTART_COUNT=$((HAL_RESTART_COUNT + 1))
        LAST_HAL_RESTART=$(date +%s)
        return 0
    else
        log_error "HAL Agent System restart failed!"
        return 3
    fi
}

# Restart Token Optimization System (placeholder - usually this is just a script, not a daemon)
restart_token() {
    local current_time=$(date +%s)
    local time_since_restart=$((current_time - LAST_TOKEN_RESTART))

    if [[ $time_since_restart -lt $RESTART_COOLDOWN ]]; then
        log_warning "Token system restart cooldown active ($((RESTART_COOLDOWN - time_since_restart))s remaining)"
        return 1
    fi

    if [[ $TOKEN_RESTART_COUNT -ge $MAX_RESTART_ATTEMPTS ]]; then
        log_error "Token system maximum restart attempts ($MAX_RESTART_ATTEMPTS) reached!"
        return 2
    fi

    log_warning "Testing Token Optimization System recovery (attempt $((TOKEN_RESTART_COUNT + 1))/$MAX_RESTART_ATTEMPTS)"

    # For token system, we just test it again since it's not a daemon
    if check_token_status; then
        log_success "Token Optimization System recovered"
        TOKEN_RESTART_COUNT=$((TOKEN_RESTART_COUNT + 1))
        LAST_TOKEN_RESTART=$(date +%s)
        return 0
    else
        log_error "Token Optimization System still failing"
        return 3
    fi
}

# Display system status
display_status() {
    clear
    echo "=================================================="
    echo "🔍 REAL-TIME SYSTEM MONITOR"
    echo "=================================================="
    echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""

    # HAL Status
    echo "🤖 HAL Agent System:"
    if check_hal_status; then
        local hal_pid=$(cat .claude/hal_active.pid 2>/dev/null || echo "unknown")
        local uptime=$(ps -o etime= -p "$hal_pid" 2>/dev/null | tr -d ' ' || echo "unknown")
        log_success "RUNNING (PID: $hal_pid, Uptime: $uptime)"
        echo "   Recent Activity: $(tail -n 3 .claude/hal_active.log 2>/dev/null | grep -E "(✅|❌|⚠️)" | tail -1 || echo "No recent activity")"
    else
        case $? in
            1) log_error "NOT RESPONDING";;
            2) log_error "PROCESS DEAD";;
            3) log_error "PID FILE MISSING";;
            *) log_error "UNKNOWN STATUS";;
        esac
    fi
    echo ""

    # Token Optimization Status
    echo "⚡ Token Optimization System:"
    if check_token_status; then
        log_success "OPERATIONAL"
        echo "   Last Check: Passed"
    else
        log_error "FAILED"
        echo "   Last Check: $(date '+%H:%M:%S')"
    fi
    echo ""

    # Restart Statistics
    echo "📊 Restart Statistics:"
    echo "   HAL Restarts: $HAL_RESTART_COUNT/$MAX_RESTART_ATTEMPTS"
    echo "   Token System Restarts: $TOKEN_RESTART_COUNT/$MAX_RESTART_ATTEMPTS"
    echo ""

    # System Resources
    echo "💻 System Resources:"
    echo "   CPU Load: $(top -l 1 -n 0 | grep "CPU usage" | awk '{print $3}' | sed 's/%//' || echo "N/A")%"
    echo "   Memory: $(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//' || echo "N/A") pages free"
    echo ""

    echo "Press Ctrl+C to stop monitoring"
    echo "=================================================="
}

# Main monitoring loop
main_monitor() {
    log_info "Starting Real-time System Monitor"
    log_info "Check intervals: HAL=${HAL_CHECK_INTERVAL}s, Token=${TOKEN_CHECK_INTERVAL}s"

    local hal_counter=0
    local token_counter=0

    while true; do
        display_status

        # Check HAL status
        hal_counter=$((hal_counter + 1))
        if [[ $hal_counter -ge $((HAL_CHECK_INTERVAL / 5)) ]]; then
            if ! check_hal_status; then
                log_error "HAL Agent System status check failed!"
                restart_hal
            fi
            hal_counter=0
        fi

        # Check Token status
        token_counter=$((token_counter + 1))
        if [[ $token_counter -ge $((TOKEN_CHECK_INTERVAL / 5)) ]]; then
            if ! check_token_status; then
                log_error "Token Optimization System status check failed!"
                restart_token
            fi
            token_counter=0
        fi

        sleep 5  # Update display every 5 seconds
    done
}

# Handle interrupt signal
trap 'log_info "System Monitor stopped"; exit 0' INT TERM

# Start monitoring
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main_monitor
fi
