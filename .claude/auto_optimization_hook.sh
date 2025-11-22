#!/bin/bash
# Auto-optimization hook for shell integration
# Add to ~/.zshrc or ~/.bashrc:

# ToDoWrite Auto-Optimization Hook
# Automatically sources token optimizations when entering the project directory

_todowrite_optimization_hook() {
    # Get current directory
    local current_dir="$(pwd)"

    # Check if we're in the ToDoWrite project
    if [[ -f "$current_dir/.claude/optimization_env.sh" ]]; then
        # Source the optimization environment if not already loaded
        if [[ "$CLAUDE_MAX_TOKENS" != "40000" ]]; then
            source "$current_dir/.claude/optimization_env.sh"
            echo "🔧 Auto-enabled token optimizations for ToDoWrite"
        fi
    elif [[ "$current_dir" == *"todowrite"* ]]; then
        # Check if we've left the project but still have optimizations loaded
        if [[ "$CLAUDE_MAX_TOKENS" == "40000" ]]; then
            echo "ℹ️  ToDoWrite optimizations still loaded (run 'deactivate_todowrite_optimizations' to disable)"
        fi
    fi
}

# Function to deactivate optimizations
deactivate_todowrite_optimizations() {
    unset CLAUDE_MAX_TOKENS MAX_ALLOWED_TOKENS HAL_PREPROCESSING_MANDATORY
    unset CLI_TOOLS_MANDATORY READ_TOOL_RESTRICTED EDIT_TOOL_RESTRICTED
    unset PACKAGE_CONTEXT MAX_FILES MAX_CONTEXT_CHARS CONTEXT_LINES
    unset -f verify_optimization apply_optimizations
    echo "🔌 ToDoWrite optimizations deactivated"
}

# Add to PROMPT_COMMAND for bash or precmd for zsh
if [[ -n "$BASH_VERSION" ]]; then
    # Bash
    if [[ -z "$PROMPT_COMMAND" ]]; then
        PROMPT_COMMAND="_todowrite_optimization_hook"
    else
        PROMPT_COMMAND="_todowrite_optimization_hook; $PROMPT_COMMAND"
    fi
elif [[ -n "$ZSH_VERSION" ]]; then
    # Zsh
    autoload -U add-zsh-hook
    add-zsh-hook precmd _todowrite_optimization_hook
fi

echo "✅ ToDoWrite auto-optimization hook loaded"
echo "💡 Add this to your ~/.zshrc or ~/.bashrc:"
echo "   source $(pwd)/.claude/auto_optimization_hook.sh"
