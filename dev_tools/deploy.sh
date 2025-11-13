#!/bin/bash
# ToDoWrite Monorepo Deployment Script
# Uses hatchling for builds and twine for PyPI/TestPyPI deployments

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
    echo -e "${BLUE}[DEPLOY]${NC} $1"
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
    echo "ToDoWrite Monorepo Deployment Script"
    echo "Uses UV environment + hatchling for builds and twine for deployments"
    echo ""
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  build               Build all packages using hatchling in UV environment"
    echo "  testpypi            Deploy to TestPyPI"
    echo "  pypi                Deploy to PyPI (main branch only)"
    echo "  auto-deploy         Deploy to TestPyPI, then PyPI (main branch only)"
    echo "  testpypi-single     Deploy single package to TestPyPI"
    echo "  pypi-single         Deploy single package to PyPI (main branch only)"
    echo "  check               Check packages before deployment"
    echo "  clean               Clean build artifacts"
    echo "  help                Show this help message"
    echo ""
    echo "Options for single package deployment:"
    echo "  lib                 Deploy lib_package (todowrite)"
    echo "  cli                 Deploy cli_package (todowrite_cli)"
    echo "  web                 Deploy web_package (todowrite_web)"
    echo ""
    echo "Environment Variables:"
    echo "  TWINE_USERNAME      PyPI/TestPyPI username (default: __token__)"
    echo "  TWINE_PASSWORD      PyPI/TestPyPI password/token"
    echo "  TEST_PYPI_REPO_URL  TestPyPI repository URL"
    echo ""
    echo "Examples:"
    echo "  $0 build                           # Build all packages"
    echo "  $0 testpypi                        # Deploy to TestPyPI"
    echo "  $0 auto-deploy                     # Deploy to TestPyPI, then PyPI (main branch)"
    echo "  $0 pypi-single lib                # Deploy lib package to PyPI"
    echo "  TWINE_PASSWORD=token $0 testpypi  # Deploy with token"
}

# Function to clean build artifacts
clean_build() {
    print_status "Cleaning build artifacts..."
    rm -rf lib_package/dist/ cli_package/dist/ web_package/dist/
    rm -rf lib_package/build/ cli_package/build/ web_package/build/
    rm -f .coverage coverage.xml
    rm -rf htmlcov/ .pytest_cache/ .ruff_cache/
    print_success "Build artifacts cleaned"
}

# Function to build all packages using hatchling in UV environment
build_all_packages() {
    print_status "Building all packages using hatchling in UV environment..."

    print_status "Building todowrite (lib_package)..."
    uv run python -m build lib_package/

    print_status "Building todowrite_cli (cli_package)..."
    uv run python -m build cli_package/

    print_status "Building todowrite_web (web_package)..."
    uv run python -m build web_package/

    print_success "All packages built successfully with hatchling in UV environment"
}

# Function to check packages before deployment
check_packages() {
    print_status "Checking packages before deployment..."

    # Check if dist directories exist and have files
    for pkg in lib_package cli_package web_package; do
        if [ ! -d "$pkg/dist" ]; then
            print_error "Distribution directory not found: $pkg/dist"
            print_status "Run './dev_tools/build.sh build' first"
            exit 1
        fi

        if [ -z "$(ls -A $pkg/dist/)" ]; then
            print_error "No distribution files found in: $pkg/dist"
            print_status "Run './dev_tools/build.sh build' first"
            exit 1
        fi
    done

    print_success "All package checks passed"
}

# Function to check if on main branch
check_main_branch() {
    local current_branch
    current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

    if [ "$current_branch" != "main" ]; then
        print_error "PyPI deployment is only allowed from main branch. Current branch: $current_branch"
        print_status "Switch to main branch or use TestPyPI deployment"
        exit 1
    fi

    print_status "Confirmed on main branch - PyPI deployment allowed"
}

# Function to deploy all packages to specified repository
deploy_all_packages() {
    local repo_url="$1"
    local repo_name="$2"

    print_status "Deploying all packages to $repo_name..."

    check_packages

    for pkg in lib_package cli_package web_package; do
        print_status "Deploying $pkg to $repo_name..."
        cd "$pkg"

        # Use twine to upload
        if [ -n "$repo_url" ]; then
            twine upload --repository-url "$repo_url" dist/*
        else
            twine upload dist/*
        fi

        cd ..
        print_success "$pkg deployed to $repo_name"
    done

    print_success "All packages deployed to $repo_name successfully"
}

# Function to deploy to TestPyPI then optionally to PyPI
deploy_with_test_first() {
    print_status "Starting deployment workflow: TestPyPI first, then PyPI (main branch only)"

    # First deploy to TestPyPI
    print_status "Step 1: Deploying to TestPyPI..."
    deploy_all_packages "${TEST_PYPI_REPO_URL:-https://test.pypi.org/legacy/}" "TestPyPI"

    # Check if we should also deploy to PyPI
    if [ "$1" = "--pypi-after" ]; then
        print_status "Step 2: Deploying to PyPI after TestPyPI success..."
        check_main_branch
        deploy_all_packages "" "PyPI"
        print_success "Deployment complete: TestPyPI + PyPI"
    else
        print_status "TestPyPI deployment completed. Use --pypi-after flag to also deploy to PyPI from main branch"
    fi
}

# Function to deploy single package
deploy_single_package() {
    local pkg_name="$1"
    local repo_url="$2"
    local repo_name="$3"

    case "$pkg_name" in
        lib)
            pkg_dir="lib_package"
            ;;
        cli)
            pkg_dir="cli_package"
            ;;
        web)
            pkg_dir="web_package"
            ;;
        *)
            print_error "Unknown package: $pkg_name"
            print_status "Use 'lib', 'cli', or 'web'"
            exit 1
            ;;
    esac

    print_status "Deploying $pkg_name package ($pkg_dir) to $repo_name..."

    if [ ! -d "$pkg_dir/dist" ] || [ -z "$(ls -A $pkg_dir/dist/)" ]; then
        print_error "No distribution files found for $pkg_name"
        print_status "Run './dev_tools/build.sh build' first"
        exit 1
    fi

    cd "$pkg_dir"

    if [ -n "$repo_url" ]; then
        twine upload --repository-url "$repo_url" dist/*
    else
        twine upload dist/*
    fi

    cd ..
    print_success "$pkg_name package deployed to $repo_name successfully"
}

# Main script logic
case "${1:-help}" in
    build)
        clean_build
        build_all_packages
        ;;
    check)
        check_packages
        ;;
    testpypi)
        deploy_with_test_first
        ;;
    pypi)
        deploy_all_packages "" "PyPI"
        ;;
    auto-deploy)
        deploy_with_test_first --pypi-after
        ;;
    testpypi-single)
        if [ -z "$2" ]; then
            print_error "Package name required for single deployment"
            show_usage
            exit 1
        fi
        deploy_single_package "$2" "${TEST_PYPI_REPO_URL:-https://test.pypi.org/legacy/}" "TestPyPI"
        ;;
    pypi-single)
        if [ -z "$2" ]; then
            print_error "Package name required for single deployment"
            show_usage
            exit 1
        fi
        deploy_single_package "$2" "" "PyPI"
        ;;
    clean)
        clean_build
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
