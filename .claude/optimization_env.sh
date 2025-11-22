#!/bin/bash
# ToDoWrite Token Optimization Environment Variables
# Source this file to enable mandatory token optimizations
# Usage: source .claude/optimization_env.sh

# Core Token Optimization Settings
export CLAUDE_MAX_TOKENS=40000
export MAX_ALLOWED_TOKENS=40000

# HAL Preprocessing (MANDATORY)
export HAL_PREPROCESSING_MANDATORY=true
export HAL_PREPROCESSING_ENABLED=true

# CLI Tools (MANDATORY)
export CLI_TOOLS_MANDATORY=true
export READ_TOOL_RESTRICTED=true
export EDIT_TOOL_RESTRICTED=true

# Package Context (auto-detected if not set)
detect_package_context() {
    local cwd="$(pwd)"
    if [[ "$cwd" == *"/lib_package/"* ]]; then
        echo "lib_package"
    elif [[ "$cwd" == *"/cli_package/"* ]]; then
        echo "cli_package"
    elif [[ "$cwd" == *"/web_package/"* ]]; then
        echo "web_package"
    else
        echo "root"
    fi
}

export PACKAGE_CONTEXT="${PACKAGE_CONTEXT:-$(detect_package_context)}"

# Adaptive Limits based on package context
case "$PACKAGE_CONTEXT" in
    "lib_package")
        export MAX_FILES=150
        export MAX_CONTEXT_CHARS=3000
        export CONTEXT_LINES=5
        ;;
    "cli_package")
        export MAX_FILES=100
        export MAX_CONTEXT_CHARS=2000
        export CONTEXT_LINES=3
        ;;
    "web_package")
        export MAX_FILES=120
        export MAX_CONTEXT_CHARS=2500
        export CONTEXT_LINES=4
        ;;
    *)
        export MAX_FILES=100
        export MAX_CONTEXT_CHARS=2000
        export CONTEXT_LINES=3
        ;;
esac

# Cache directories
export HAL_CACHE_DIR="$HOME/.token_optimized_cache"
mkdir -p "$HAL_CACHE_DIR"

# Function to verify optimizations are active
verify_optimization() {
    local missing_vars=()

    [[ "$CLAUDE_MAX_TOKENS" == "40000" ]] || missing_vars+=("CLAUDE_MAX_TOKENS")
    [[ "$MAX_ALLOWED_TOKENS" == "40000" ]] || missing_vars+=("MAX_ALLOWED_TOKENS")
    [[ "$HAL_PREPROCESSING_MANDATORY" == "true" ]] || missing_vars+=("HAL_PREPROCESSING_MANDATORY")
    [[ "$CLI_TOOLS_MANDATORY" == "true" ]] || missing_vars+=("CLI_TOOLS_MANDATORY")

    if [[ ${#missing_vars[@]} -eq 0 ]]; then
        echo "✅ All token optimizations are properly enabled"
        echo "🎯 Package Context: $PACKAGE_CONTEXT"
        echo "📊 Max Tokens: $CLAUDE_MAX_TOKENS"
        echo "📁 Max Files: $MAX_FILES"
        echo "📝 Max Context Chars: $MAX_CONTEXT_CHARS"
        return 0
    else
        echo "❌ Missing optimizations: ${missing_vars[*]}"
        return 1
    fi
}

# Function to run optimizations automatically
apply_optimizations() {
    echo "🔧 Applying token optimizations..."
    python "$(dirname "${BASH_SOURCE[0]}")/mandatory_token_optimization.py"
    verify_optimization
}

# Aliases for commonly used CLI tools (promote over internal tools)
if [[ "$CLI_TOOLS_MANDATORY" == "true" ]]; then
    # File reading preferences
    alias readfile='cat'
    alias readhead='head'
    alias readtail='tail'
    alias readless='less'

    # File searching preferences
    alias search='grep -r'
    alias findfiles='find . -name'

    # File editing preferences
    alias quickedit='sed -i'
    alias batchedit='awk'
fi

# Show status when sourced
echo "🚀 ToDoWrite Token Optimization Environment Loaded"
echo "📦 Package Context: $PACKAGE_CONTEXT"
echo "📊 Max Tokens: $CLAUDE_MAX_TOKENS"
echo "🔧 HAL Preprocessing: $HAL_PREPROCESSING_MANDATORY"
echo "⚡ CLI Tools: $CLI_TOOLS_MANDATORY"
echo ""
echo "💡 Run 'verify_optimization' to check status"
echo "💡 Run 'apply_optimizations' to reapply settings"
