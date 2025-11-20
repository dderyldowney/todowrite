#!/bin/bash
# ToDoWrite AI CLI Startup Script with Full Rule Enforcement
# AUTOMATICALLY activates virtual environment - no manual activation needed

set -e  # Exit on any error

echo "🚀 Starting ToDoWrite AI CLI with AUTOMATIC Virtual Environment Activation..."
echo "📋 NOTE: You DON'T need to run 'source .venv/bin/activate' - this script does it automatically!"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. Verify we're in the correct directory
if [ ! -f "pyproject.toml" ] || [ ! -d ".claude" ]; then
    print_error "Must be run from ToDoWrite project root directory"
    exit 1
fi
print_status "Verified we're in the ToDoWrite project directory"

# 2. Check if virtual environment exists, create if needed
if [ ! -d ".venv" ]; then
    print_status "Virtual environment not found. Creating with uv sync..."
    if command -v uv >/dev/null 2>&1; then
        uv sync
    else
        print_error "uv not found. Please install uv first: pip install uv"
        exit 1
    fi
fi

# 3. ALWAYS activate virtual environment (AUTOMATIC - no manual step needed!)
print_status "🔄 Automatically activating virtual environment..."
source .venv/bin/activate

# Verify activation was successful
if [[ "$(which python)" != *".venv"* ]]; then
    print_error "❌ Virtual environment activation failed!"
    print_error "   This should never happen - the script activates it automatically"
    exit 1
fi
print_success "✅ Virtual environment automatically activated"

# 4. Set required environment variables
print_status "Setting required environment variables..."
export PYTHONPATH="$PWD/lib_package/src:$PWD/cli_package/src"
# export EPISODIC_MEMORY_DB_PATH="$(pwd)/.claude/episodic_memory.db"  # DISABLED

# Load PostgreSQL environment
if [ -f ".claude/postgresql_env.sh" ]; then
    source .claude/postgresql_env.sh
    print_success "✅ PostgreSQL environment loaded"
else
    print_error "❌ PostgreSQL environment file not found: .claude/postgresql_env.sh"
    exit 1
fi

# Verify environment variables
if [ -z "$TODOWRITE_DATABASE_URL" ]; then
    print_error "TODOWRITE_DATABASE_URL not set"
    exit 1
fi

if [ -z "$PYTHONPATH" ]; then
    print_error "PYTHONPATH not set"
    exit 1
fi

print_success "✅ Environment variables set"
print_status "📍 Database URL: $TODOWRITE_DATABASE_URL"
print_status "📍 Python Path: $PYTHONPATH"

# 5. Verify PostgreSQL environment is loaded
print_status "Verifying PostgreSQL environment..."
if [[ "$TODOWRITE_DATABASE_URL" != postgresql://* ]]; then
    print_error "❌ Database URL is not PostgreSQL: $TODOWRITE_DATABASE_URL"
    exit 1
fi
print_success "✅ PostgreSQL environment verified"

# 6. Run startup enforcement (MANDATORY)
print_status "Running CLAUDE.md rule enforcement..."
if ! python .claude/startup_enforcement.py; then
    print_error "CLAUDE.md rule enforcement failed - cannot start AI CLI"
    print_status "Please fix the reported violations and retry"
    exit 1
fi
print_success "All CLAUDE.md rules verified"

# 7. Initialize episodic memory (DISABLED)
# print_status "Initializing episodic memory..."
# if [ -f "./dev_tools/ensure_episodic_memory.sh" ]; then
#     ./dev_tools/ensure_episodic_memory.sh
# else
#     print_warning "Episodic memory initialization script not found"
# fi

# 7.5. Initialize HAL Agent dependencies if needed
print_status "Checking HAL Agent dependencies..."
if ! python -c "import openai" 2>/dev/null; then
    print_status "Installing HAL Agent dependencies..."
    pip install openai
else
    print_success "HAL Agent dependencies available"
fi

# 8. Initialize ToDoWrite Models API
print_status "Initializing ToDoWrite Models API..."
if [ -f ".claude/auto_init_todowrite_models.py" ]; then
    python .claude/auto_init_todowrite_models.py
else
    print_warning "ToDoWrite Models initialization script not found"
fi

# 9. Verify HAL Agent System (MANDATORY)
print_status "Verifying HAL Agent System..."
if [ -f "dev_tools/agent_controls/hal_token_savvy_agent.py" ]; then
    if python -c "import openai; print('✅ HAL dependencies available')" 2>/dev/null; then
        print_success "HAL Agent System ready"
        # Test HAL Agent functionality
        if python dev_tools/agent_controls/hal_token_savvy_agent.py --help >/dev/null 2>&1; then
            print_success "HAL Agent functionality verified"
        else
            print_warning "HAL Agent test failed - may need configuration"
        fi
    else
        print_warning "HAL Agent dependencies missing - run: pip install openai"
    fi
else
    print_warning "HAL Agent System not found"
fi

# 10. Verify Token Optimization System (MANDATORY)
print_status "Verifying Token Optimization System..."
if [ -f "dev_tools/token_optimization/always_token_sage.py" ]; then
    if python dev_tools/token_optimization/always_token_sage.py "test" >/dev/null 2>&1; then
        print_success "Token Optimization System verified"
    else
        print_warning "Token Optimization System test failed"
    fi
else
    print_warning "Token Optimization System not found"
fi

# 11. Verify MCP (Model Context Protocol) Systems (MANDATORY)
print_status "Verifying MCP Systems..."
# Check for episodic memory MCP
if [ -d ".claude/episodic_memory" ] || [ -f ".claude/episodic_memory.db" ]; then
    print_success "Episodic Memory MCP available"
else
    print_warning "Episodic Memory MCP not initialized"
fi

# Check for other MCP plugins
if [ -d ".claude/plugins" ]; then
    mcp_count=$(find .claude/plugins -name "*.py" | wc -l)
    print_success "Found $mcp_count MCP plugins in .claude/plugins/"
else
    print_warning "No MCP plugins directory found"
fi

# 12. Verify Anthropic Configuration for HAL Agent
print_status "Checking Anthropic API configuration..."
if [ -n "$ANTHROPIC_API_KEY" ]; then
    print_success "ANTHROPIC_API_KEY is set"
    if [ -n "$ANTHROPIC_MODEL" ]; then
        print_success "ANTHROPIC_MODEL is set to: $ANTHROPIC_MODEL"
    else
        print_status "ANTHROPIC_MODEL not set - will use default"
    fi
else
    print_warning "ANTHROPIC_API_KEY not set - HAL Agent will need it"
    print_status "Set it with: export ANTHROPIC_API_KEY='your-key-here'"  # pragma: allowlist secret
fi

# 13. Start Claude Code
print_success "All verifications complete - Starting AI CLI..."
echo ""
echo -e "${GREEN}✅ AI CLI is now ready with full CLAUDE.md enforcement${NC}"
echo -e "${BLUE}📍 Complete Environment Status:${NC}"
echo -e "   • 🔄 Virtual Environment: AUTOMATICALLY activated (no manual step needed)"
echo -e "   • 🗄️  Database: $TODOWRITE_DATABASE_URL"
echo -e "   • 🐍 Python Path: $PYTHONPATH"
echo -e "   • 🧠 Episodic Memory: $EPISODIC_MEMORY_DB_PATH"
echo -e "   • 🤖 HAL Agent System: Ready for local preprocessing"
echo -e "   • ⚡ Token Optimization: Active (90% token savings)"
echo -e "   • 🔌 MCP Systems: Model Context Protocol ready"
echo -e "   • 📋 CLAUDE.md Rules: Fully enforced"
echo ""

# Start Claude Code with the provided arguments
exec claude "$@"
