#!/bin/bash
# Build script for ToDoWrite packages using Hatchling
# Usage: ./scripts/build.sh [clean]

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

# Check if we're in the project root
if [ ! -f "pyproject.toml" ] || [ ! -d "lib_package" ] || [ ! -d "cli_package" ]; then
    print_error "Must be run from the project root directory"
    exit 1
fi

# Function to build a package
build_package() {
    local package_dir=$1
    local package_name=$2

    print_status "Building $package_name package..."

    cd "$package_dir"

    # Clean if requested
    if [ "$1" = "clean" ]; then
        print_status "Cleaning previous build artifacts..."
        rm -rf dist/ build/ *.egg-info/
    fi

    # Build with hatchling
    if python -m hatchling build; then
        print_success "$package_name built successfully"

        # Show built artifacts
        if [ -d "dist" ]; then
            print_status "Built artifacts:"
            ls -la dist/
        fi
    else
        print_error "Failed to build $package_name"
        exit 1
    fi

    cd - > /dev/null
}

# Function to verify build artifacts
verify_artifacts() {
    print_status "Verifying build artifacts..."

    # Get current version from VERSION file
    local version=$(cat VERSION | tr -d '\n')

    # Check library package
    if [ ! -f "lib_package/dist/todowrite-${version}-py3-none-any.whl" ]; then
        print_error "Library package wheel not found (expected: todowrite-${version}-py3-none-any.whl)"
        exit 1
    fi

    if [ ! -f "lib_package/dist/todowrite-${version}.tar.gz" ]; then
        print_error "Library package sdist not found (expected: todowrite-${version}.tar.gz)"
        exit 1
    fi

    # Check CLI package
    if [ ! -f "cli_package/dist/todowrite_cli-${version}-py3-none-any.whl" ]; then
        print_error "CLI package wheel not found (expected: todowrite_cli-${version}-py3-none-any.whl)"
        exit 1
    fi

    if [ ! -f "cli_package/dist/todowrite_cli-${version}.tar.gz" ]; then
        print_error "CLI package sdist not found (expected: todowrite_cli-${version}.tar.gz)"
        exit 1
    fi

    print_success "All build artifacts verified"
}

# Main build process
main() {
    print_status "Starting ToDoWrite package build process..."

    # Clean if requested
    if [ "$1" = "clean" ]; then
        print_warning "Cleaning all build artifacts..."
        rm -rf lib_package/dist/ lib_package/build/
        rm -rf cli_package/dist/ cli_package/build/
        # Remove egg-info directories if they exist (avoid glob errors)
        find lib_package -name "*.egg-info" -type d -exec rm -rf {} + 2>/dev/null || true
        find cli_package -name "*.egg-info" -type d -exec rm -rf {} + 2>/dev/null || true
        print_success "Clean completed"
    fi

    # Build library package
    build_package "lib_package" "todowrite"

    # Build CLI package
    build_package "cli_package" "todowrite-cli"

    # Verify artifacts
    verify_artifacts

    print_success "Build process completed successfully!"
    print_status "Ready for publishing with twine"
}

# Show usage
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "Usage: $0 [clean]"
    echo ""
    echo "Build ToDoWrite packages using Hatchling"
    echo ""
    echo "Options:"
    echo "  clean    Clean previous build artifacts before building"
    echo "  -h       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0              # Build packages"
    echo "  $0 clean        # Clean and build packages"
    exit 0
fi

# Run main function with all arguments
main "$@"
