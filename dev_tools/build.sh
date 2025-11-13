#!/bin/bash
# Unified ToDoWrite Monorepo Build Script
# This script provides a simple interface for common build operations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[BUILD]${NC} $1"
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

# Function to show usage
show_usage() {
    echo "ToDoWrite Monorepo Build Script"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  install     Install dependencies (uv sync --group dev)"
    echo "  build       Build all packages (lib, cli, web)"
    echo "  test        Run all tests"
    echo "  lint        Run code quality checks"
    echo "  format      Format code"
    echo "  validate    Validate build system configuration and packages"
    echo "  clean       Clean build artifacts"
    echo "  dev         Full development workflow (install + format + lint + test)"
    echo "  release     Prepare release (build all packages)"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 install    # Install dependencies"
    echo "  $0 dev        # Full development workflow"
    echo "  $0 test       # Run tests only"
}

# Command functions
install_deps() {
    print_status "Installing dependencies with unified build system..."
    uv sync --group dev
    print_success "Dependencies installed successfully"
}

build_packages() {
    local package_name="$1"

    if [ -n "$package_name" ]; then
        # Build specific package
        case "$package_name" in
            lib)
                print_status "Building lib_package with hatchling in UV environment..."
                uv run python -m build lib_package/
                print_success "Built lib_package"
                ;;
            cli)
                print_status "Building cli_package with hatchling in UV environment..."
                uv run python -m build cli_package/
                print_success "Built cli_package"
                ;;
            web)
                print_status "Building web_package with hatchling in UV environment..."
                uv run python -m build web_package/
                print_success "Built web_package"
                ;;
            all)
                # Build all packages (explicit)
                print_status "Building all packages with hatchling in UV environment..."
                uv run python -m build lib_package/
                uv run python -m build cli_package/
                uv run python -m build web_package/
                print_success "Built all packages"
                ;;
            *)
                print_error "Unknown package: $package_name"
                print_status "Available packages: lib, cli, web, all"
                exit 1
                ;;
        esac
    else
        # Build all packages (default)
        print_status "Building all packages with hatchling in UV environment..."
        uv run python -m build lib_package/
        uv run python -m build cli_package/
        uv run python -m build web_package/
        print_success "All packages built successfully"
    fi
}

run_tests() {
    print_status "Running tests with unified configuration..."
    uv run pytest tests/ -v --cov=lib_package/src --cov=cli_package/src --cov-report=term-missing --ignore=tests/web/
    print_success "All tests completed"
}

run_lint() {
    print_status "Running code quality checks..."
    uv run ruff check lib_package/ cli_package/
    print_status "Note: web_package excluded from linting (planning stage)"
    print_success "Code quality checks completed"
}

format_code() {
    print_status "Formatting code..."
    uv run ruff format lib_package/ cli_package/
    print_status "Note: web_package excluded from formatting (planning stage)"
    print_success "Code formatted successfully"
}

validate_build_system() {
    print_status "Validating build system configuration and packages..."

    # Check if UV workspace is configured
    if ! grep -q "\[tool.uv.workspace\]" pyproject.toml; then
        print_error "UV workspace not configured in pyproject.toml"
        exit 1
    fi

    # Check if all packages are in workspace
    if ! grep -q "lib_package" pyproject.toml; then
        print_error "lib_package not found in workspace"
        exit 1
    fi

    if ! grep -q "cli_package" pyproject.toml; then
        print_error "cli_package not found in workspace"
        exit 1
    fi

    if ! grep -q "web_package" pyproject.toml; then
        print_error "web_package not found in workspace"
        exit 1
    fi

    # Check if VERSION file exists
    if [ ! -f "VERSION" ]; then
        print_error "VERSION file not found"
        exit 1
    fi

    # Check if packages reference central VERSION
    if ! grep -q "path = \"../VERSION\"" lib_package/pyproject.toml; then
        print_error "lib_package doesn't reference central VERSION"
        exit 1
    fi

    if ! grep -q "path = \"../VERSION\"" cli_package/pyproject.toml; then
        print_error "cli_package doesn't reference central VERSION"
        exit 1
    fi

    if ! grep -q "path = \"../VERSION\"" web_package/pyproject.toml; then
        print_error "web_package doesn't reference central VERSION"
        exit 1
    fi

    print_success "Build system validation completed successfully"
}

clean_build() {
    print_status "Cleaning build artifacts..."
    rm -rf lib_package/dist/ cli_package/dist/ web_package/dist/
    rm -rf lib_package/build/ cli_package/build/ web_package/build/
    rm -f .coverage coverage.xml
    rm -rf htmlcov/ .pytest_cache/ .ruff_cache/
    print_success "Build artifacts cleaned"
}

dev_workflow() {
    print_status "Running full development workflow..."

    install_deps
    format_code
    run_lint
    run_tests

    print_success "Development workflow completed successfully"
}

prepare_release() {
    print_status "Preparing release..."

    # Clean first
    clean_build

    # Run tests to ensure everything works
    run_tests

    # Build all packages
    build_packages

    print_success "Release preparation completed"
    print_status "Built packages:"
    ls -la lib_package/dist/ cli_package/dist/ web_package/dist/ 2>/dev/null || true
}

# Main script logic
case "${1:-help}" in
    install)
        install_deps
        ;;
    build)
        build_packages "$2"
        ;;
    test)
        run_tests
        ;;
    lint)
        run_lint
        ;;
    format)
        format_code
        ;;
    validate)
        validate_build_system
        ;;
    clean)
        clean_build
        ;;
    dev)
        dev_workflow
        ;;
    release)
        prepare_release
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        print_error "Unknown command: $1"
        show_usage
        exit 1
        ;;
esac
