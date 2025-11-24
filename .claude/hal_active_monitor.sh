#!/bin/bash
# HAL Active Monitor - Keeps HAL running in continuous preprocessing mode

echo "🤖 Starting HAL Active Monitor - Continuous Preprocessing Mode"

# Ensure we're in the project directory
cd "$(dirname "$0")/.."

# Main HAL monitoring loop
while true; do
    echo "🔄 HAL Monitoring Cycle - $(date)"

    # Run HAL status check to keep it active and processing
    python dev_tools/agent_controls/hal_token_savvy_agent.py \
        --provider anthropic \
        --model sonnet \
        --goal "Status check and preprocessing monitoring - verify system health and await preprocessing tasks" \
        --context 1000 \
        --chars 5000 \
        2>&1 | grep -E "(HAL|✅|❌|⚠️|🤖)" | tail -5

    echo "💤 HAL monitoring pause - 30 seconds"
    sleep 30
done
