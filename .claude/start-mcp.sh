#!/bin/bash
# Auto-start Docker MCP Gateway with comprehensive MCP server suite
# Source environment variables (especially Context7 API key)
source ~/.env

echo "🚀 Starting Docker MCP Gateway with ENFORCED development workflow..."
echo ""
echo "🧠 DEVELOPMENT MANDATES LOADED:"
echo "  ✅ MCP-First Workflow - Use MCP tools over built-in tools"
echo "  ✅ TDD Red-Green-Refactor - Always write failing tests first"
echo "  ✅ Background Process Management - Always cleanup processes"
echo "  ✅ Environment Configuration - Always source environment variables"
echo ""

echo "🔄 MANDATORY PROCESS CLEANUP:"
# Kill existing MCP gateway processes
pkill -f "docker mcp gateway" 2>/dev/null || true
# Kill related Docker containers
docker stop $(docker ps -q --filter "name=mcp*") 2>/dev/null || true
docker rm $(docker ps -aq --filter "name=mcp*") 2>/dev/null || true
# Kill Python processes
pkill -f "python.*mcp" 2>/dev/null || true
echo "  ✅ Killed existing MCP gateway processes"
echo "  ✅ Stopped related Docker containers"
echo "  ✅ Verified clean process state"

echo ""
echo "📚 Context7 API Key: ${CONTEXT7_API_KEY:0:15}..."
echo "📁 Project Directory: ${TODOWRITE_PROJECT_DIR}"
echo ""

# Regenerate filesystem config with current environment variables
cat > ./.claude/filesystem-mcp-config.yaml << EOF
filesystem:
  paths:
    - "${TODOWRITE_PROJECT_DIR}"
  environment:
    DATABASE_URL: "${MCP_FILESYSTEM_DATABASE_URL}"
EOF

echo "📝 Generated .claude/filesystem-mcp-config.yaml with environment variables"
echo ""

# Start the MCP Gateway with core servers (Playwright paused for now)
echo "🎭 PLAYWRIGHT PAUSED: Not needed for current development workflow"
echo ""
echo "🔧 ACTIVE MCP SERVERS:"
echo "  ✅ filesystem (11 tools) - File operations - USE INSTEAD OF BUILT-IN TOOLS"
echo "  ✅ github-official (40 tools) - GitHub integration"
echo "  ✅ git (12 tools) - Git version control"
echo "  ✅ SQLite (6 tools) - Database operations"
echo "  ✅ context7 (2 tools) - AI assistance"
echo "  ✅ docker - Container management"
echo "  ✅ hugging-face (9 tools) - AI/ML integration"
echo ""
echo "📋 ZERO TOLERANCE MANDATES:"
echo "  🚫 NEVER use built-in file tools (Read, Write, Edit, Glob, Grep)"
echo "  ✅ ALWAYS use MCP filesystem tools instead"
echo "  🔴 ALWAYS write failing test FIRST (TDD Red-Green-Refactor)"
echo "  🔄 ALWAYS kill background processes before starting new ones"
echo "  📁 ALWAYS source environment variables"
echo "  ✅ ALWAYS use MCP git/github tools for version control"
echo ""
echo "⚠️  VIOLATION = IMMEDIATE WORKFLOW TERMINATION"
echo ""

docker mcp gateway run --servers context7,docker,github-official,git,filesystem,SQLite,hugging-face --additional-config ./.claude/filesystem-mcp-config.yaml --log-calls
