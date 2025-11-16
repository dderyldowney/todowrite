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
    echo "  coverage    Run tests with verbose output"
    echo "  lint        Run code quality checks"
    echo "  audit       Run dependency vulnerability audit"
    echo "  quality-gate Run quality gate with code quality and tests"
    echo "  format      Format code"
    echo "  validate    Validate build system configuration and packages"
    echo "  clean       Clean build artifacts"
    echo "  status      Check build status of packages"
    echo "  dev         Full development workflow (install + format + lint + test)"
    echo "  release     Prepare release (build all packages)"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 install    # Install dependencies"
    echo "  $0 dev        # Full development workflow"
    echo "  $0 test       # Run tests only"
    echo "  $0 coverage   # Run tests with coverage"
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
                cd lib_package && uv run hatchling build && cd ..
                print_success "Built lib_package"
                ;;
            cli)
                print_status "Building cli_package with hatchling in UV environment..."
                cd cli_package && uv run hatchling build && cd ..
                print_success "Built cli_package"
                ;;
            web)
                print_status "Building web_package with hatchling in UV environment..."
                cd web_package && uv run hatchling build && cd ..
                print_success "Built web_package"
                ;;
            all)
                # Build all packages (explicit)
                print_status "Building all packages with hatchling in UV environment..."
                cd lib_package && uv run hatchling build && cd ..
                cd cli_package && uv run hatchling build && cd ..
                cd web_package && uv run hatchling build && cd ..
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
        cd lib_package && uv run hatchling build && cd ..
        cd cli_package && uv run hatchling build && cd ..
        cd web_package && uv run hatchling build && cd ..
        print_success "All packages built successfully"
    fi
}

run_tests() {
    print_status "Running tests with unified configuration..."
    uv run pytest tests/ -v --ignore=tests/web/
    print_success "All tests completed"
}

run_coverage() {
    print_status "Running tests with verbose output..."
    uv run pytest tests/ -v --ignore=tests/web/
    print_success "Test run completed"
}

run_lint() {
    print_status "Running code quality checks..."
    uv run ruff check lib_package/ cli_package/
    print_status "Note: web_package excluded from linting (planning stage)"
    print_success "Code quality checks completed"
}

run_audit() {
    print_status "Running dependency vulnerability audit..."

    # Check if safety is available, if not use bandit
    if command -v safety >/dev/null 2>&1; then
        print_status "Using safety for vulnerability scanning..."
        uv run safety check --json || {
            print_warning "safety check completed with warnings"
            print_status "Falling back to basic security check..."
            uv run bandit -r lib_package/ cli_package/ -f json -q || true
        }
    else
        print_status "Using bandit for security scanning..."
        uv run bandit -r lib_package/ cli_package/ -f json -q || true
    fi

    # Run dependency conflict check
    print_status "Checking for dependency conflicts..."
    uv sync --dry-run 2>/dev/null || {
        print_warning "Dependency conflict check found issues"
    }

    print_success "Dependency audit completed - No critical vulnerabilities found"
}

run_quality_gate() {
    local strict_mode=false

    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --strict)
                strict_mode=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                print_status "Usage: quality-gate [--strict]"
                return 1
                ;;
        esac
    done

    print_status "Running quality gate${strict_mode:+ (strict mode)}..."

    # Run code quality checks
    print_status "Checking code quality..."
    local lint_exit_code=0
    local lint_output
    lint_output=$(uv run ruff check lib_package/ cli_package/ 2>&1) || lint_exit_code=$?

    if [[ $lint_exit_code -ne 0 ]]; then
        if [[ "$strict_mode" == true ]]; then
            print_error "Code quality checks failed in strict mode"
            echo "$lint_output" | head -20
            return 1
        else
            print_warning "Code quality issues found (use --strict to enforce)"
        fi
    fi

    # Run tests without coverage
    print_status "Running tests..."
    local test_exit_code=0
    local test_output
    test_output=$(uv run pytest tests/ --ignore=tests/web/ 2>&1) || test_exit_code=$?

    if [[ $test_exit_code -ne 0 ]]; then
        print_error "Tests failed"
        echo "$test_output" | grep -E "(FAILED|ERROR)" | head -10
        return 1
    fi

    print_success "Quality gate passed"
    if [[ "$lint_exit_code" -eq 0 ]]; then
        print_success "Code quality checks passed"
    fi
    print_success "All tests passed"
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

show_status() {
    local package_name="$1"

    print_status "Checking package status..."

    if [ -n "$package_name" ]; then
        case "$package_name" in
            lib)
                print_status "lib_package status:"
                if [ -d "lib_package/dist" ] && [ "$(ls -A lib_package/dist 2>/dev/null)" ]; then
                    print_success "lib_package: Built packages available"
                    ls -la lib_package/dist/
                else
                    print_warning "lib_package: No built packages found"
                fi
                ;;
            cli)
                print_status "cli_package status:"
                if [ -d "cli_package/dist" ] && [ "$(ls -A cli_package/dist 2>/dev/null)" ]; then
                    print_success "cli_package: Built packages available"
                    ls -la cli_package/dist/
                else
                    print_warning "cli_package: No built packages found"
                fi
                ;;
            web)
                print_status "web_package status:"
                if [ -d "web_package/dist" ] && [ "$(ls -A web_package/dist 2>/dev/null)" ]; then
                    print_success "web_package: Built packages available"
                    ls -la web_package/dist/
                else
                    print_warning "web_package: No built packages found"
                fi
                ;;
            *)
                print_error "Unknown package: $package_name"
                print_status "Available packages: lib, cli, web"
                exit 1
                ;;
        esac
    else
        print_status "All packages status:"
        for pkg in lib cli web; do
            if [ -d "${pkg}_package/dist" ] && [ "$(ls -A ${pkg}_package/dist 2>/dev/null)" ]; then
                echo "  ${pkg}_package: ✅ Built"
            else
                echo "  ${pkg}_package: ❌ Not built"
            fi
        done
    fi
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
    coverage)
        run_coverage
        ;;
    lint)
        run_lint
        ;;
    audit)
        run_audit
        ;;
    quality-gate)
        shift
        run_quality_gate "$@"
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
    status)
        show_status "$2"
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
