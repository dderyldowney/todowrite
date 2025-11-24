#!/bin/bash
# HAL Status Component for Statusline

hal_status() {
    # Only show HAL status if we're in the todowrite project
    if [[ ! -f ".claude/startup.sh" ]]; then
        return 0
    fi

    # Check HAL status
    if [[ -f ".claude/hal_active.pid" ]]; then
        local hal_pid=$(cat ".claude/hal_active.pid" 2>/dev/null)
        if [[ -n "$hal_pid" ]] && ps -p "$hal_pid" > /dev/null 2>&1; then
            # HAL is running
            echo "%F{green}✓ HAL%f"
        else
            # HAL PID exists but process is dead
            echo "%F{red}✗ HAL%f"
        fi
    else
        # No HAL PID file
        echo "%F{red}✗ HAL%f"
    fi
}

# Token optimization status with savings count
token_status() {
    # Only show if we're in the todowrite project
    if [[ ! -f ".claude/startup.sh" ]]; then
        return 0
    fi

    # Quick token system test
    if ! python dev_tools/token_optimization/always_token_sage.py "test" > /dev/null 2>&1; then
        echo "%F{red}✗ TOK%f"
        return
    fi

    # Calculate total tokens saved from log files
    local total_saved=0
    if [[ -f ".claude/token_usage.log" ]]; then
        while IFS=: read -r timestamp tokens; do
            if [[ -n "$tokens" && "$tokens" =~ ^[0-9]+$ ]]; then
                ((total_saved += tokens))
            fi
        done < .claude/token_usage.log
    fi

    if [[ -f ".claude/token_usage 2.log" ]]; then
        while IFS=: read -r timestamp tokens; do
            if [[ -n "$tokens" && "$tokens" =~ ^[0-9]+$ ]]; then
                ((total_saved += tokens))
            fi
        done < .claude/token_usage 2.log
    fi

    # Display with savings count
    if [[ $total_saved -gt 0 ]]; then
        echo "%F{green}$total_saved T/S%f"
    else
        echo "%F{green}✓ TOK%f"
    fi
}

# Combined todowrite status
todowrite_status() {
    # Only show if we're in the todowrite project
    if [[ ! -f ".claude/startup.sh" ]]; then
        return 0
    fi

    local hal=$(hal_status)
    local token=$(token_status)
    echo "[$hal $token]"
}
