#!/bin/bash
# SessionStart hook - DISABLED - Episodic memory MCP has been completely disabled
echo "⏸️  Episodic memory MCP configuration: DISABLED"

# Ensure episodic memory CLI tools are accessible (DISABLED)
# export EPISODIC_MEMORY_CLI_PATH="$HOME/.claude/plugins/cache/episodic-memory/cli"

# Add to PATH if not already there (DISABLED)
# if [[ ":$PATH:" != *":$EPISODIC_MEMORY_CLI_PATH:"* ]]; then
#     export PATH="$EPISODIC_MEMORY_CLI_PATH:$PATH"
# fi

# Verify MCP tools are available (DISABLED)
# if [[ ! -f "$EPISODIC_MEMORY_CLI_PATH/episodic-memory" ]]; then
#     echo "⚠️  Episodic memory CLI not found at $EPISODIC_MEMORY_CLI_PATH"
#     echo "   Attempting to install..."
#
#     # Try to install if missing
#     mkdir -p "$EPISODIC_MEMORY_CLI_PATH"
#     # Add installation logic here if needed
# fi

# Create symlink for project-local access (DISABLED)
# ln -sf "$EPISODIC_MEMORY_CLI_PATH/episodic-memory" ./.claude/episodic-memory 2>/dev/null || true
# ln -sf "$EPISODIC_MEMORY_CLI_PATH/search-conversations" ./.claude/search-conversations 2>/dev/null || true

echo "⏸️  Episodic memory MCP: DISABLED"
# echo "   Available commands:"
# echo "   - episodic-memory (search, index, show, stats)"
# echo "   - search-conversations (semantic + text search)"
