#!/bin/bash
# ToDoWrite AI CLI Startup Script with Full Rule Enforcement

set -e  # Exit on any error

echo "🚀 Starting ToDoWrite AI CLI with CLAUDE.md Rule Enforcement..."

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

# 2. Activate virtual environment
if [ ! -d ".venv" ]; then
    print_error "Virtual environment not found. Run: uv sync"
    exit 1
fi

print_status "Activating virtual environment..."
source .venv/bin/activate

# Verify activation
if [[ "$(which python)" != *".venv"* ]]; then
    print_error "Virtual environment activation failed"
    exit 1
fi
print_success "Virtual environment activated"

# 3. Set required environment variables
print_status "Setting required environment variables..."
export TODOWRITE_DATABASE_URL="sqlite:///$HOME/dbs/todowrite_development.db"
export PYTHONPATH="$PWD/lib_package/src:$PWD/cli_package/src"
export EPISODIC_MEMORY_DB_PATH="$(pwd)/.claude/episodic_memory.db"

# Verify environment variables
if [ -z "$TODOWRITE_DATABASE_URL" ]; then
    print_error "TODOWRITE_DATABASE_URL not set"
    exit 1
fi

if [ -z "$PYTHONPATH" ]; then
    print_error "PYTHONPATH not set"
    exit 1
fi

print_success "Environment variables set"
print_status "Database URL: $TODOWRITE_DATABASE_URL"
print_status "Python Path: $PYTHONPATH"

# 4. Verify database exists
if [ ! -f "$HOME/dbs/todowrite_development.db" ]; then
    print_warning "Development database not found at $HOME/dbs/todowrite_development.db"
    print_status "You may need to initialize it with: python .claude/auto_init_todowrite_models.py"
fi

# 5. Run startup enforcement (MANDATORY)
print_status "Running CLAUDE.md rule enforcement..."
if ! python .claude/startup_enforcement.py; then
    print_error "CLAUDE.md rule enforcement failed - cannot start AI CLI"
    print_status "Please fix the reported violations and retry"
    exit 1
fi
print_success "All CLAUDE.md rules verified"

# 6. Initialize episodic memory
print_status "Initializing episodic memory..."
if [ -f "./dev_tools/ensure_episodic_memory.sh" ]; then
    ./dev_tools/ensure_episodic_memory.sh
else
    print_warning "Episodic memory initialization script not found"
fi

# 7. Initialize ToDoWrite Models API
print_status "Initializing ToDoWrite Models API..."
if [ -f ".claude/auto_init_todowrite_models.py" ]; then
    python .claude/auto_init_todowrite_models.py
else
    print_warning "ToDoWrite Models initialization script not found"
fi

# 8. Start Claude Code
print_success "All verifications complete - Starting AI CLI..."
echo ""
echo -e "${GREEN}✅ AI CLI is now ready with full CLAUDE.md enforcement${NC}"
echo -e "${BLUE}📍 Environment:${NC}"
echo -e "   • Virtual Environment: Active"
echo -e "   • Database: $TODOWRITE_DATABASE_URL"
echo -e "   • Python Path: $PYTHONPATH"
echo -e "   • Episodic Memory: $EPISODIC_MEMORY_DB_PATH"
echo ""

# Start Claude Code with the provided arguments
exec claude "$@"
