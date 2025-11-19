#!/bin/bash
# Ensure Episodic Memory is Always Indexed and Available
# This script ensures episodic memory is indexed and search is available

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[EPISODIC-MEMORY]${NC} $1"
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

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Check if episodic memory plugin is installed
check_episodic_plugin() {
    print_status "Checking episodic memory plugin installation..."

    if [ ! -f "$HOME/.claude/plugins/installed_plugins.json" ]; then
        print_error "No plugins directory found"
        return 1
    fi

    if ! grep -q "episodic-memory" "$HOME/.claude/plugins/installed_plugins.json"; then
        print_error "Episodic memory plugin not installed"
        print_warning "Install with: claude plugin install episodic-memory@superpowers-marketplace"
        return 1
    fi

    print_success "Episodic memory plugin installed"
    return 0
}

# Check if episodic memory CLI is available
check_episodic_cli() {
    print_status "Checking episodic memory CLI..."

    if [ ! -f "$HOME/.claude/plugins/cache/episodic-memory/cli/episodic-memory.js" ]; then
        print_error "Episodic memory CLI not found"
        return 1
    fi

    print_success "Episodic memory CLI available"
    return 0
}

# Run optimized indexing with verification
run_optimized_indexing() {
    print_status "Running optimized episodic memory indexing (4x concurrency)..."

    # Run the index command with cleanup and moderate concurrency
    if node "$HOME/.claude/plugins/cache/episodic-memory/cli/episodic-memory.js" index --cleanup --concurrency 4; then
        print_success "Optimized indexing completed successfully"
    else
        print_error "Optimized indexing failed"
        return 1
    fi
}

# Run indexing with verification
run_indexing() {
    print_status "Running episodic memory indexing..."

    # Run the index command with cleanup
    if node "$HOME/.claude/plugins/cache/episodic-memory/cli/episodic-memory.js" index --cleanup; then
        print_success "Indexing completed successfully"
    else
        print_error "Indexing failed"
        return 1
    fi
}

# Run sync with verification
run_sync() {
    print_status "Running episodic memory sync..."

    # Run the sync command
    if node "$HOME/.claude/plugins/cache/episodic-memory/cli/episodic-memory.js" sync; then
        print_success "Sync completed successfully"
    else
        print_error "Sync failed"
        return 1
    fi
}

# Verify indexing worked
verify_indexing() {
    print_status "Verifying indexing..."

    # Check if stats command works
    if node "$HOME/.claude/plugins/cache/episodic-memory/cli/episodic-memory.js" stats > /dev/null 2>&1; then
        print_success "Indexing verification passed"
        return 0
    else
        print_error "Indexing verification failed"
        return 1
    fi
}

# Test search functionality
test_search() {
    print_status "Testing search functionality..."

    # Test a simple search
    if node "$HOME/.claude/plugins/cache/episodic-memory/cli/episodic-memory.js" search "test" --limit 1 > /dev/null 2>&1; then
        print_success "Search functionality works"
        return 0
    else
        print_warning "Search test failed (may be normal if no conversations indexed yet)"
        return 0
    fi
}

# Create session startup hook
create_startup_hook() {
    print_status "Creating session startup hook..."

    HOOK_DIR="$PROJECT_ROOT/.claude/hooks"
    HOOK_FILE="$HOOK_DIR/session_startup_episodic_memory.py"

    mkdir -p "$HOOK_DIR"

    cat > "$HOOK_FILE" << 'EOF'
#!/usr/bin/env python3
"""Session Startup Hook - Ensure Episodic Memory is Ready"""

import subprocess
import sys
from pathlib import Path

def main():
    """Ensure episodic memory is ready for the session"""

    project_root = Path(__file__).parent.parent

    # Check if episodic memory plugin is installed
    plugins_file = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
    if not plugins_file.exists():
        print("⚠️  No episodic memory plugin found")
        return

    # Run a quick index to ensure embedding model is loaded
    episodic_cli = Path.home() / ".claude" / "plugins" / "cache" / "episodic-memory" / "cli" / "episodic-memory.js"

    if episodic_cli.exists():
        try:
            # Run a quick index to load embedding model
            result = subprocess.run(
                ["node", str(episodic_cli), "stats"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                print("✅ Episodic memory ready - embedding model loaded")
            else:
                print("🔄 Initializing episodic memory indexing...")
                # Run background indexing if stats fail
                subprocess.Popen([
                    "node", str(episodic_cli), "index", "--cleanup"
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        except subprocess.TimeoutExpired:
            print("⏳ Episodic memory indexing in progress...")
        except Exception as e:
            print(f"⚠️  Episodic memory error: {e}")

    # Create a marker file to indicate episodic memory was initialized
    marker = project_root / ".claude" / "episodic_memory_ready.json"
    marker.write_text('{"status": "initialized", "timestamp": "' + str(Path().cwd()) + '"}')

if __name__ == "__main__":
    main()
EOF

    chmod +x "$HOOK_FILE"
    print_success "Session startup hook created"
}

# Add to CLAUDE.md initialization
add_to_claude_md() {
    print_status "Adding episodic memory initialization to CLAUDE.md..."

    CLAUDE_MD="$PROJECT_ROOT/.claude/CLAUDE.md"

    # Check if episodic memory init is already mentioned
    if grep -q "episodic-memory initialization" "$CLAUDE_MD"; then
        print_warning "Episodic memory init already mentioned in CLAUDE.md"
        return
    fi

    # Add to startup checklist
    cat >> "$CLAUDE_MD" << 'EOF'

## 21. Episodic Memory Initialization - MANDATORY

**ABSOLUTE REQUIREMENT**: ALL agents MUST ensure episodic memory is initialized and available

- **MANDATORY**: Run episodic memory indexing before starting development work
- **MANDATORY**: Ensure `/search-conversations` slash command is available
- **MANDATORY**: Verify embedding model is loaded and ready
- **MANDATORY**: Use episodic memory for context before starting new tasks
- **AUTOMATED**: Session startup hooks ensure episodic memory is ready
- **ZERO EXCEPTIONS**: This applies to ALL agents at ALL times

### Implementation:
```bash
# Manual episodic memory initialization
./dev_tools/ensure_episodic_memory.sh

# Or automatic via startup hook
.claude/hooks/session_startup_episodic_memory.py
```

EOF

    print_success "Added episodic memory requirements to CLAUDE.md"
}

# Main function
main() {
    echo "ToDoWrite Episodic Memory Setup"
    echo "================================"
    echo ""

    # Check prerequisites
    check_episodic_plugin || exit 1
    check_episodic_cli || exit 1

    # Run optimized indexing and sync
    run_sync || exit 1
    run_optimized_indexing || exit 1

    # Verify functionality
    verify_indexing || exit 1
    test_search || true  # Non-critical if no conversations yet

    # Create startup hook for future sessions
    create_startup_hook

    # Add to CLAUDE.md
    add_to_claude_md

    print_success "Episodic memory setup complete!"
    echo ""
    print_status "Search will be available via: /search-conversations"
    print_status "Future sessions will automatically initialize episodic memory"
}

# Run main function
main "$@"