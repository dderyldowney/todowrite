#!/bin/bash
# Auto-optimization hook for shell integration
# Add to ~/.zshrc or ~/.bashrc:

# ToDoWrite Auto-Optimization Hook
# Automatically sources token optimizations when entering the project directory

_todowrite_optimization_hook() {
    # Only run optimization check once per session or when directory changes
    if [[ "$PWD" != "$_TODOWRITE_LAST_DIR" ]]; then
        local current_dir="$PWD"

        # Check if we're in the ToDoWrite project (must have both marker file AND be in correct directory structure)
        if [[ -f "$current_dir/.claude/optimization_env.sh" && -d "$current_dir/lib_package/src" && -d "$current_dir/cli_package/src" ]]; then
            # Source the optimization environment if not already loaded
            if [[ "$CLAUDE_MAX_TOKENS" != "40000" ]]; then
                source "$current_dir/.claude/optimization_env.sh"
                echo "🔧 Auto-enabled token optimizations for ToDoWrite"
            fi

            # Set proper PYTHONPATH for ToDoWrite project (only if we're in the actual project directory)
            if [[ "$PYTHONPATH" != *"lib_package/src:cli_package/src"* ]]; then
                export PYTHONPATH="lib_package/src:cli_package/src:${PYTHONPATH}"
                echo "📦 Set PYTHONPATH for ToDoWrite project"
            fi

            # Remember we're in ToDoWrite project
            export _TODOWRITE_IN_PROJECT=true

        else
            # We're not in the ToDoWrite project directory, clean up if needed
            if [[ "$_TODOWRITE_IN_PROJECT" == "true" ]]; then
                # Remove ToDoWrite PYTHONPATH when leaving the project
                if [[ "$PYTHONPATH" == *"lib_package/src:cli_package/src"* ]]; then
                    # Remove todowrite PYTHONPATH components
                    export PYTHONPATH="${PYTHONPATH//lib_package\/src:cli_package\/src:/}"
                    export PYTHONPATH="${PYTHONPATH//:lib_package\/src:cli_package\/src/}"
                    echo "📦 Cleared ToDoWrite PYTHONPATH (left project directory)"
                fi
                export _TODOWRITE_IN_PROJECT=false
            fi
        fi

        # Remember current directory to avoid repeated checks
        export _TODOWRITE_LAST_DIR="$PWD"
    fi
}

# Function to deactivate optimizations
deactivate_todowrite_optimizations() {
    unset CLAUDE_MAX_TOKENS MAX_ALLOWED_TOKENS HAL_PREPROCESSING_MANDATORY
    unset CLI_TOOLS_MANDATORY READ_TOOL_RESTRICTED EDIT_TOOL_RESTRICTED
    unset PACKAGE_CONTEXT MAX_FILES MAX_CONTEXT_CHARS CONTEXT_LINES
    unset -f verify_optimization apply_optimizations

    # Remove ToDoWrite PYTHONPATH (keep any existing path components)
    if [[ "$PYTHONPATH" == *"lib_package/src:cli_package/src"* ]]; then
        export PYTHONPATH="${PYTHONPATH//lib_package\/src:cli_package\/src:/}"
        export PYTHONPATH="${PYTHONPATH//:lib_package\/src:cli_package\/src/}"
        echo "📦 Removed ToDoWrite PYTHONPATH"
    fi

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

# Silent loading - no status messages needed
