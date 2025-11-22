#!/bin/bash
# Auto-start Docker MCP Gateway with comprehensive MCP server suite
# Source environment variables (especially Context7 API key)
source ~/.env

echo "🚀 Starting Docker MCP Gateway with full server suite..."
echo "📚 Context7 API Key: ${CONTEXT7_API_KEY:0:15}..."
echo ""

# Start the MCP Gateway with all configured servers
docker mcp gateway run --servers context7,docker,github-official,git,filesystem,postgres,SQLite,hugging-face,playwright --log-calls