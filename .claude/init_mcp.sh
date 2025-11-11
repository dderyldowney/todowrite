#!/bin/bash
# MCP Initialization Script - Ensures episodic memory is available for EVERY session
echo "🔧 Initializing episodic memory MCP for ToDoWrite project..."

# Set episodic memory CLI path
export EPISODIC_MEMORY_CLI_PATH="$HOME/.claude/plugins/cache/episodic-memory/cli"

# Add to PATH
export PATH="$EPISODIC_MEMORY_CLI_PATH:$PATH"

# Create project-local symlinks for reliable access
ln -sf "$EPISODIC_MEMORY_CLI_PATH/episodic-memory" ./.claude/episodic-memory-cli 2>/dev/null || true
ln -sf "$EPISODIC_MEMORY_CLI_PATH/search-conversations" ./.claude/search-conversations-cli 2>/dev/null || true
ln -sf "$EPISODIC_MEMORY_CLI_PATH/index-conversations" ./.claude/index-conversations-cli 2>/dev/null || true

# Verify tools are accessible
if [[ -f "$EPISODIC_MEMORY_CLI_PATH/episodic-memory" ]]; then
    echo "✅ Episodic memory CLI tools available"
    echo "   - episodic-memory: $(which episodic-memory 2>/dev/null || echo "$EPISODIC_MEMORY_CLI_PATH/episodic-memory")"
    echo "   - search-conversations: $(which search-conversations 2>/dev/null || echo "$EPISODIC_MEMORY_CLI_PATH/search-conversations")"
else
    echo "⚠️  Episodic memory CLI tools not found at expected location"
fi

# Set environment variables for pagination safety
export EPISODIC_MEMORY_PAGINATION_ENABLED=true
export EPISODIC_MEMORY_MAX_RESULTS=50
export EPISODIC_MEMORY_USE_OFFSET_LIMIT=true

echo "🚀 MCP episodic memory initialized with pagination safety"
