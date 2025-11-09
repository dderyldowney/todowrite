#!/bin/bash
# ruff linting and formatting script for ToDoWrite
# Usage: ./scripts/lint_and_format.sh [check|fix]

set -e  # Exit on any error

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

# Default mode
MODE=${1:-check}

# Check if we're in the project root
if [ ! -f "pyproject.toml" ] || [ ! -d "lib_package" ] || [ ! -d "cli_package" ]; then
    print_error "Must be run from the project root directory"
    exit 1
fi

# Check if ruff is available
if ! command -v ruff &> /dev/null; then
    print_error "ruff is not installed. Install it with: pip install ruff"
    exit 1
fi

print_status "Running ruff in ${MODE} mode..."

# Function to run ruff on a directory
run_ruff() {
    local target_dir=$1
    local mode=$2

    print_status "Checking $target_dir..."

    if [ "$mode" = "fix" ]; then
        # Fix issues and format
        if ruff check "$target_dir" --fix && ruff format "$target_dir"; then
            print_success "$target_dir: Issues fixed and formatted"
        else
            print_error "$target_dir: Failed to fix issues"
            return 1
        fi
    else
        # Check only (don't modify files)
        if ruff check "$target_dir" && ruff format "$target_dir" --check; then
            print_success "$target_dir: No issues found"
        else
            print_warning "$target_dir: Issues found (run with 'fix' to auto-correct)"
            return 1
        fi
    fi
}

# Main process
main() {
    local has_issues=0

    print_status "Starting ruff linting and formatting..."

    # Check lib_package
    if ! run_ruff "lib_package" "$MODE"; then
        has_issues=1
    fi

    # Check cli_package
    if ! run_ruff "cli_package" "$MODE"; then
        has_issues=1
    fi

    # Check web_package if it exists
    if [ -d "web_package" ]; then
        print_status "Checking web_package..."
        # Check backend
        if [ -d "web_package/backend" ]; then
            if ! run_ruff "web_package/backend" "$MODE"; then
                has_issues=1
            fi
        fi

        # Check frontend Python files (scripts, tests, etc.)
        if [ -d "web_package/frontend" ]; then
            # Find and check Python files in frontend
            frontend_py_files=$(find web_package/frontend -name "*.py" -type f 2>/dev/null || true)
            if [ -n "$frontend_py_files" ]; then
                if ! run_ruff "web_package/frontend" "$MODE"; then
                    has_issues=1
                fi
            fi
        fi
    fi

    # Check scripts
    if [ -d "scripts" ]; then
        if ! run_ruff "scripts" "$MODE"; then
            has_issues=1
        fi
    fi

    # Check root Python files
    root_py_files=$(find . -maxdepth 1 -name "*.py" -type f 2>/dev/null || true)
    if [ -n "$root_py_files" ]; then
        print_status "Checking root Python files..."
        if ! run_ruff "." "$MODE"; then
            has_issues=1
        fi
    fi

    # Final result
    if [ $has_issues -eq 0 ]; then
        print_success "All files passed ruff checks!"
        if [ "$MODE" = "fix" ]; then
            print_status "Files have been formatted and linted"
        fi
    else
        if [ "$MODE" = "check" ]; then
            print_error "Some files have ruff issues. Run with 'fix' to auto-correct"
            print_status "Or run: ruff check . --fix && ruff format ."
        else
            print_error "Some files still have issues after auto-correction"
        fi
        exit 1
    fi
}

# Show usage
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "Usage: $0 [check|fix]"
    echo ""
    echo "Run ruff linting and formatting on ToDoWrite codebase"
    echo ""
    echo "Arguments:"
    echo "  check    Check for issues (default, doesn't modify files)"
    echo "  fix      Auto-fix issues and format files"
    echo "  -h       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0              # Check for issues"
    echo "  $0 check        # Check for issues (explicit)"
    echo "  $0 fix          # Auto-fix and format"
    echo ""
    echo "Note: ruff replaces black, isort, flake8, bandit, and pyright"
    exit 0
fi

# Validate mode argument
if [ "$1" != "" ] && [ "$1" != "check" ] && [ "$1" != "fix" ]; then
    print_error "Invalid argument: $1"
    print_status "Use 'check' or 'fix', or run with -h for help"
    exit 1
fi

# Run main function
main "$MODE"
