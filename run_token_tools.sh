#!/bin/bash

# Token optimization tools launcher script
# This script provides backward compatibility for running token optimization tools

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Add dev_tools to Python path
export PYTHONPATH="$SCRIPT_DIR/dev_tools:$PYTHONPATH"

# Function to run a token optimization tool
run_tool() {
    local tool_name="$1"
    shift

    echo "🚀 Running token optimization tool: $tool_name"

    if [[ -f "$SCRIPT_DIR/dev_tools/token_optimization/${tool_name}.py" ]]; then
        python3 "$SCRIPT_DIR/dev_tools/token_optimization/${tool_name}.py" "$@"
    else
        echo "❌ Tool not found: $tool_name"
        echo "Available tools:"
        ls "$SCRIPT_DIR/dev_tools/token_optimization/" | grep -E "\.py$" | sed 's/\.py$//'
        exit 1
    fi
}

# Function to run an agent control tool
run_agent_tool() {
    local tool_name="$1"
    shift

    echo "🤖 Running agent control tool: $tool_name"

    if [[ -f "$SCRIPT_DIR/dev_tools/agent_controls/${tool_name}.py" ]]; then
        python3 "$SCRIPT_DIR/dev_tools/agent_controls/${tool_name}.py" "$@"
    else
        echo "❌ Agent tool not found: $tool_name"
        echo "Available agent tools:"
        ls "$SCRIPT_DIR/dev_tools/agent_controls/" | grep -E "\.py$" | sed 's/\.py$//'
        exit 1
    fi
}

# Main execution logic
case "$1" in
    "token_optimized_agent"|"always_token_sage"|"auto_agent")
        run_tool "$@"
        ;;
    "hal_agent_loop"|"hal_token_savvy_agent")
        run_agent_tool "$@"
        ;;
    "list")
        echo "📋 Available token optimization tools:"
        ls "$SCRIPT_DIR/dev_tools/token_optimization/" | grep -E "\.py$" | sed 's/\.py$//'
        echo ""
        echo "🤖 Available agent control tools:"
        ls "$SCRIPT_DIR/dev_tools/agent_controls/" | grep -E "\.py$" | sed 's/\.py$//'
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 <tool_name> [arguments]"
        echo ""
        echo "Token Optimization Tools:"
        echo "  $0 token_optimized_agent [args]     - Run token optimized agent"
        echo "  $0 always_token_sage [args]         - Run always token sage"
        echo "  $0 auto_agent [args]               - Run auto agent"
        echo ""
        echo "Agent Control Tools:"
        echo "  $0 hal_agent_loop [args]            - Run HAL agent loop"
        echo "  $0 hal_token_savvy_agent [args]     - Run HAL token savvy agent"
        echo ""
        echo "Other Commands:"
        echo "  $0 list                            - List all available tools"
        echo "  $0 help                            - Show this help message"
        ;;
    "")
        echo "❌ No tool specified. Use '$0 help' for usage information."
        exit 1
    ;;
    *)
        echo "❌ Unknown tool: $1"
        echo "Use '$0 list' to see available tools or '$0 help' for usage information."
        exit 1
        ;;
esac
