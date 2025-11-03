#!/bin/bash
# Publish script for ToDoWrite packages
# Usage: ./scripts/publish.sh [test|prod] [clean]

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

# Default to test repository
REPOSITORY=${1:-test}
CLEAN_BUILD=""

# Parse arguments
if [ "$2" = "clean" ]; then
    CLEAN_BUILD="clean"
fi

# Validate repository argument
if [ "$REPOSITORY" != "test" ] && [ "$REPOSITORY" != "prod" ]; then
    print_error "Invalid repository: $REPOSITORY"
    echo "Usage: $0 [test|prod] [clean]"
    exit 1
fi

# Check if we're in the project root
if [ ! -f "pyproject.toml" ] || [ ! -d "lib_package" ] || [ ! -d "cli_package" ]; then
    print_error "Must be run from the project root directory"
    exit 1
fi

# Function to check if twine is installed
check_twine() {
    if ! command -v twine &> /dev/null; then
        print_error "twine is not installed. Install it with: pip install twine"
        exit 1
    fi
}

# Function to check package integrity with twine
check_package() {
    local package_dir=$1
    local package_name=$2

    print_status "Checking $package_name package integrity..."

    cd "$package_dir"

    if twine check dist/*; then
        print_success "$package_name package integrity verified"
    else
        print_error "Package integrity check failed for $package_name"
        exit 1
    fi

    cd - > /dev/null
}

# Function to upload to repository
upload_package() {
    local package_dir=$1
    local package_name=$2
    local repo_flag=""

    if [ "$REPOSITORY" = "test" ]; then
        repo_flag="--repository testpypi"
        print_status "Uploading $package_name to TestPyPI..."
    else
        print_status "Uploading $package_name to PyPI..."
    fi

    cd "$package_dir"

    if twine upload $repo_flag dist/*; then
        print_success "$package_name uploaded successfully"
    else
        print_error "Failed to upload $package_name"
        exit 1
    fi

    cd - > /dev/null
}

# Function to confirm upload
confirm_upload() {
    if [ "$REPOSITORY" = "prod" ]; then
        echo
        print_warning "You are about to upload to PRODUCTION PyPI!"
        echo "This will make the packages publicly available."
        echo
        read -p "Are you sure you want to continue? (yes/no): " confirm
        if [ "$confirm" != "yes" ]; then
            print_status "Upload cancelled"
            exit 0
        fi
    fi
}

# Function to show repository info
show_repo_info() {
    if [ "$REPOSITORY" = "test" ]; then
        print_status "Publishing to TestPyPI"
        echo "Repository URL: https://test.pypi.org/"
        echo "Packages will be available at:"
        echo "  - https://test.pypi.org/project/todowrite/"
        echo "  - https://test.pypi.org/project/todowrite-cli/"
    else
        print_status "Publishing to Production PyPI"
        echo "Repository URL: https://pypi.org/"
        echo "Packages will be available at:"
        echo "  - https://pypi.org/project/todowrite/"
        echo "  - https://pypi.org/project/todowrite-cli/"
    fi
    echo
}

# Main publish process
main() {
    print_status "Starting ToDoWrite package publish process..."

    # Show repository information
    show_repo_info

    # Confirm upload
    confirm_upload

    # Check prerequisites
    check_twine

    # Build packages first
    print_status "Building packages..."
    if ./scripts/build.sh $CLEAN_BUILD; then
        print_success "Packages built successfully"
    else
        print_error "Failed to build packages"
        exit 1
    fi

    # Check package integrity
    check_package "lib_package" "todowrite"
    check_package "cli_package" "todowrite-cli"

    # Upload packages
    upload_package "lib_package" "todowrite"
    upload_package "cli_package" "todowrite-cli"

    print_success "Publish process completed successfully!"

    # Show installation instructions
    echo
    print_status "Installation instructions:"

    if [ "$REPOSITORY" = "test" ]; then
        echo "# Install from TestPyPI"
        echo "pip install --index-url https://test.pypi.org/simple/ todowrite"
        echo "pip install --index-url https://test.pypi.org/simple/ todowrite-cli"
    else
        echo "# Install from PyPI"
        echo "pip install todowrite"
        echo "pip install todowrite-cli"
    fi

    echo
    print_success "All done! 🚀"
}

# Show usage
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "Usage: $0 [test|prod] [clean]"
    echo ""
    echo "Publish ToDoWrite packages using Twine"
    echo ""
    echo "Arguments:"
    echo "  test     Publish to TestPyPI (default)"
    echo "  prod     Publish to production PyPI"
    echo "  clean    Clean build artifacts before building"
    echo ""
    echo "Options:"
    echo "  -h       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0               # Build and publish to TestPyPI"
    echo "  $0 prod          # Build and publish to PyPI"
    echo "  $0 test clean    # Clean, build, and publish to TestPyPI"
    echo "  $0 prod clean    # Clean, build, and publish to PyPI"
    exit 0
fi

# Run main function
main "$@"
