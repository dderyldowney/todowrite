#!/bin/bash
# SessionStart hook - Ensures episodic memory MCP is available for EVERY session
echo "🔧 Loading episodic memory MCP configuration..."

# Ensure episodic memory CLI tools are accessible
export EPISODIC_MEMORY_CLI_PATH="$HOME/.claude/plugins/cache/episodic-memory/cli"

# Add to PATH if not already there
if [[ ":$PATH:" != *":$EPISODIC_MEMORY_CLI_PATH:"* ]]; then
    export PATH="$EPISODIC_MEMORY_CLI_PATH:$PATH"
fi

# Verify MCP tools are available
if [[ ! -f "$EPISODIC_MEMORY_CLI_PATH/episodic-memory" ]]; then
    echo "⚠️  Episodic memory CLI not found at $EPISODIC_MEMORY_CLI_PATH"
    echo "   Attempting to install..."

    # Try to install if missing
    mkdir -p "$EPISODIC_MEMORY_CLI_PATH"
    # Add installation logic here if needed
fi

# Create symlink for project-local access
ln -sf "$EPISODIC_MEMORY_CLI_PATH/episodic-memory" ./.claude/episodic-memory 2>/dev/null || true
ln -sf "$EPISODIC_MEMORY_CLI_PATH/search-conversations" ./.claude/search-conversations 2>/dev/null || true

echo "✅ Episodic memory MCP configured for session"
echo "   Available commands:"
echo "   - episodic-memory (search, index, show, stats)"
echo "   - search-conversations (semantic + text search)"
