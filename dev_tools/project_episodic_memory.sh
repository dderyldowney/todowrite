#!/bin/bash
# Project-Scoped Episodic Memory Indexer
# Only indexes conversations from the current project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[PROJECT-EPISODIC-MEMORY]${NC} $1"
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

# Get current project directory and name
PROJECT_ROOT="$(pwd)"
PROJECT_NAME="$(basename "$PROJECT_ROOT")"

# Get the current project's Claude conversation directory
# Claude encodes project paths as: -Users-username-path-to-project
ENCODED_PROJECT_PATH=$(echo "$PROJECT_ROOT" | sed 's/^\///' | sed 's/\//-/g')
CLAUDE_PROJECT_DIR="$HOME/.claude/projects/-Users-$ENCODED_PROJECT_PATH"

# Also check if the current working directory project exists
CWD_ENCODED=$(pwd | sed 's/^\///' | sed 's/\//-/g')
CWD_CLAUDE_DIR="$HOME/.claude/projects/-Users-$CWD_ENCODED"

# Use whichever exists
if [ -d "$CLAUDE_PROJECT_DIR" ]; then
    CONVERSATION_DIR="$CLAUDE_PROJECT_DIR"
elif [ -d "$CWD_CLAUDE_DIR" ]; then
    CONVERSATION_DIR="$CWD_CLAUDE_DIR"
else
    CONVERSATION_DIR="$CLAUDE_PROJECT_DIR"  # Default to expected path
fi

print_status "Project: $PROJECT_NAME"
print_status "Project Root: $PROJECT_ROOT"
print_status "Conversation Dir: $CONVERSATION_DIR"

# Check if we're in a Claude-tracked project
if [ ! -d "$CONVERSATION_DIR" ]; then
    print_warning "No Claude conversation directory found for current project"
    print_warning "Starting new project - episodic memory will be empty initially"
    mkdir -p "$CONVERSATION_DIR"
fi

# Set the episodic memory database to be project-specific
export EPISODIC_MEMORY_DB_PATH="$PROJECT_ROOT/.claude/episodic_memory.db"

print_status "Using project-specific database: $EPISODIC_MEMORY_DB_PATH"

# Function to index only current project conversations
index_current_project() {
    print_status "Indexing conversations for current project only..."

    # Check if there are any conversations to index
    if [ ! "$(ls -A "$CONVERSATION_DIR"/*.jsonl 2>/dev/null)" ]; then
        print_warning "No conversations found for current project"
        return 0
    fi

    # Create project-specific archive directory
    ARCHIVE_DIR="$PROJECT_ROOT/.claude/episodic_memory_archive"
    mkdir -p "$ARCHIVE_DIR"

    # Copy only current project conversations to archive
    print_status "Copying project conversations to archive..."
    cp -r "$CONVERSATION_DIR"/* "$ARCHIVE_DIR/" 2>/dev/null || true

    # Run episodic memory index with project-specific archive
    cd "$HOME/.claude/plugins/cache/episodic-memory"
    node cli/episodic-memory.js index --cleanup --concurrency 4

    print_success "Project-specific indexing completed"
}

# Function to search only current project conversations
search_current_project() {
    local query="$1"
    print_status "Searching current project conversations for: $query"

    # Ensure we're using the project-specific database
    export EPISODIC_MEMORY_DB_PATH="$PROJECT_ROOT/.claude/episodic_memory.db"

    cd "$HOME/.claude/plugins/cache/episodic-memory"
    node cli/episodic-memory.js search "$query" --limit 10
}

# Function to show current project stats
show_current_project_stats() {
    print_status "Current project episodic memory statistics:"

    # Ensure we're using the project-specific database
    export EPISODIC_MEMORY_DB_PATH="$PROJECT_ROOT/.claude/episodic_memory.db"

    if [ ! -f "$EPISODIC_MEMORY_DB_PATH" ]; then
        print_warning "No episodic memory database found for current project"
        return 0
    fi

    cd "$HOME/.claude/plugins/cache/episodic-memory"
    node cli/episodic-memory.js stats
}

# Main command handling
case "${1:-}" in
    index)
        index_current_project
        ;;
    search)
        if [[ -z "$2" ]]; then
            print_error "Search query required"
            echo "Usage: $0 search \"your query\""
            exit 1
        fi
        search_current_project "$2"
        ;;
    stats)
        show_current_project_stats
        ;;
    setup)
        print_status "Setting up project-scoped episodic memory..."

        # Create .claude directory if it doesn't exist
        mkdir -p "$PROJECT_ROOT/.claude"

        # Create project-specific session startup hook
        cat > "$PROJECT_ROOT/.claude/hooks/session_startup_project_episodic_memory.py" << 'EOF'
#!/usr/bin/env python3
"""Project-Scoped Episodic Memory Startup Hook"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    """Initialize project-scoped episodic memory for this session"""

    project_root = Path(__file__).parent.parent
    episodic_db = project_root / ".claude" / "episodic_memory.db"

    # Set environment variable for project-specific database
    os.environ["EPISODIC_MEMORY_DB_PATH"] = str(episodic_db)

    print(f"🔍 Project-scoped episodic memory initialized")
    print(f"📁 Database: {episodic_db}")

if __name__ == "__main__":
    main()
EOF

        chmod +x "$PROJECT_ROOT/.claude/hooks/session_startup_project_episodic_memory.py"

        # Create project-specific session end hook
        cat > "$PROJECT_ROOT/.claude/hooks/session_end_project_episodic_memory.py" << 'EOF'
#!/usr/bin/env python3
"""Project-Scoped Episodic Memory Session End Hook"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    """Index current project conversations at session end"""

    project_root = Path(__file__).parent.parent
    script_path = project_root / "dev_tools" / "project_episodic_memory.sh"

    if script_path.exists():
        # Set environment variable for project-specific database
        episodic_db = project_root / ".claude" / "episodic_memory.db"
        os.environ["EPISODIC_MEMORY_DB_PATH"] = str(episodic_db)

        # Run project-specific indexing
        try:
            result = subprocess.run(
                [str(script_path), "index"],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                print("✅ Project episodic memory indexed successfully")
            else:
                print(f"⚠️  Episodic memory indexing issue: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("⏳ Episodic memory indexing timed down...")
        except Exception as e:
            print(f"⚠️  Episodic memory error: {e}")

if __name__ == "__main__":
    main()
EOF

        chmod +x "$PROJECT_ROOT/.claude/hooks/session_end_project_episodic_memory.py"

        print_success "Project-scoped episodic memory hooks created"
        print_status "Commands:"
        print_status "  $0 index    - Index current project conversations"
        print_status "  $0 search   - Search current project conversations"
        print_status "  $0 stats    - Show current project statistics"
        ;;
    help|--help|-h)
        echo "Project-Scoped Episodic Memory"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  index       Index conversations from current project only"
        echo "  search QUERY Search current project conversations"
        echo "  stats       Show current project statistics"
        echo "  setup       Set up project-scoped hooks and configuration"
        echo "  help        Show this help"
        echo ""
        echo "Examples:"
        echo "  $0 index"
        echo "  $0 search 'database connection issues'"
        echo "  $0 stats"
        ;;
    *)
        print_error "Unknown command '${1:-}'"
        echo ""
        print_status "Use '$0 help' to see available commands"
        exit 1
        ;;
esac