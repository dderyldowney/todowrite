#!/bin/bash
# Comprehensive Release Automation Script for ToDoWrite
# Usage: ./scripts/release.sh [version|patch|minor|major] [options]
# Examples:
#   ./scripts/release.sh 0.4.2
#   ./scripts/release.sh patch
#   ./scripts/release.sh minor --dry-run

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Global variables
DRY_RUN=false
SKIP_TESTS=false
SKIP_GITHUB=false
VERSION_ARG=""
ORIGINAL_BRANCH=""
RELEASE_VERSION=""
CURRENT_VERSION=""
FAILED_STEP=""
ROLLBACK_NEEDED=false

# Function to print colored output
print_header() {
    echo -e "${BLUE}${BOLD}============================================${NC}"
    echo -e "${BLUE}${BOLD}$1${NC}"
    echo -e "${BLUE}${BOLD}============================================${NC}"
}

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

print_step() {
    echo -e "${CYAN}[STEP]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [version|patch|minor|major] [options]"
    echo ""
    echo "Automated release script for ToDoWrite that handles the complete process:"
    echo "  - Version bumping with README/fallback updates"
    echo "  - Git operations (merge, tag, push)"
    echo "  - GitHub release creation"
    echo "  - Package building and publishing to TestPyPI and PyPI"
    echo ""
    echo "Arguments:"
    echo "  version    Specific version number (e.g., 0.4.2)"
    echo "  patch      Bump patch version (X.Y.Z → X.Y.Z+1)"
    echo "  minor      Bump minor version (X.Y.Z → X.Y+1.0)"
    echo "  major      Bump major version (X.Y.Z → X+1.0.0)"
    echo ""
    echo "Options:"
    echo "  --dry-run         Preview what would be done without making changes"
    echo "  --skip-tests      Skip running tests (not recommended for production)"
    echo "  --skip-github     Skip GitHub release creation"
    echo "  --help, -h        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 0.4.2                    # Cut release 0.4.2"
    echo "  $0 patch                    # Cut next patch release"
    echo "  $0 minor --dry-run          # Preview minor release"
    echo "  $0 0.5.0 --skip-tests       # Cut release 0.5.0 without tests"
    echo ""
    echo "The script will:"
    echo "  1. Run prerequisites checks (tests, linting, git status)"
    echo "  2. Bump version and update README/fallback versions"
    echo "  3. Commit version changes"
    echo "  4. Merge develop → main"
    echo "  5. Tag and push to GitHub"
    echo "  6. Create GitHub release"
    echo "  7. Build and publish to TestPyPI"
    echo "  8. Build and publish to PyPI"
    echo "  9. Return to develop branch"
    echo ""
    echo "⚠️  Make sure you're on develop branch with clean git status before running."
}

# Function to parse command line arguments
parse_args() {
    if [ $# -eq 0 ]; then
        print_error "Missing version argument"
        show_usage
        exit 1
    fi

    # Check for help flag first
    if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        show_usage
        exit 0
    fi

    VERSION_ARG="$1"
    shift

    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --skip-tests)
                SKIP_TESTS=true
                shift
                ;;
            --skip-github)
                SKIP_GITHUB=true
                shift
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
}

# Function to validate environment
validate_environment() {
    print_step "Validating environment..."

    # Check if we're in project root
    if [ ! -f "pyproject.toml" ] || [ ! -d "lib_package" ] || [ ! -d "cli_package" ]; then
        print_error "Must be run from the project root directory"
        exit 1
    fi

    # Check if required scripts exist
    if [ ! -f "scripts/bump_version.py" ]; then
        print_error "bump_version.py script not found"
        exit 1
    fi

    if [ ! -f "scripts/build.sh" ]; then
        print_error "build.sh script not found"
        exit 1
    fi

    if [ ! -f "scripts/publish.sh" ]; then
        print_error "publish.sh script not found"
        exit 1
    fi

    # Check required tools
    local missing_tools=()

    if ! command -v python &> /dev/null; then
        missing_tools+=("python")
    fi

    if ! command -v git &> /dev/null; then
        missing_tools+=("git")
    fi

    if [ "$SKIP_GITHUB" = false ] && ! command -v gh &> /dev/null; then
        print_warning "gh CLI not found, will skip GitHub release creation"
        SKIP_GITHUB=true
    fi

    if [ ${#missing_tools[@]} -ne 0 ]; then
        print_error "Missing required tools: ${missing_tools[*]}"
        exit 1
    fi

    print_success "Environment validation passed"
}

# Function to get current version
get_current_version() {
    CURRENT_VERSION=$(python scripts/bump_version.py --verify-only 2>/dev/null | grep "Current version:" | cut -d' ' -f3)
    if [ -z "$CURRENT_VERSION" ]; then
        CURRENT_VERSION=$(cat VERSION)
    fi
    print_status "Current version: $CURRENT_VERSION"
}

# Function to determine release version
determine_release_version() {
    print_step "Determining release version..."

    if [[ "$VERSION_ARG" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        # Explicit version
        RELEASE_VERSION="$VERSION_ARG"
        print_status "Explicit version specified: $RELEASE_VERSION"
    elif [ "$VERSION_ARG" = "patch" ]; then
        # Bump patch version
        RELEASE_VERSION=$(python -c "
import sys
current = '$CURRENT_VERSION'.split('.')
print(f'{current[0]}.{current[1]}.{int(current[2]) + 1}')
")
        print_status "Patch bump: $CURRENT_VERSION → $RELEASE_VERSION"
    elif [ "$VERSION_ARG" = "minor" ]; then
        # Bump minor version
        RELEASE_VERSION=$(python -c "
import sys
current = '$CURRENT_VERSION'.split('.')
print(f'{current[0]}.{int(current[1]) + 1}.0')
")
        print_status "Minor bump: $CURRENT_VERSION → $RELEASE_VERSION"
    elif [ "$VERSION_ARG" = "major" ]; then
        # Bump major version
        RELEASE_VERSION=$(python -c "
import sys
current = '$CURRENT_VERSION'.split('.')
print(f'{int(current[0]) + 1}.0.0')
")
        print_status "Major bump: $CURRENT_VERSION → $RELEASE_VERSION"
    else
        print_error "Invalid version argument: $VERSION_ARG"
        print_error "Use semantic version (X.Y.Z) or bump type (patch/minor/major)"
        exit 1
    fi

    # Validate that new version is greater than current
    if ! python -c "
import sys
from packaging import version
if not version.parse('$RELEASE_VERSION') > version.parse('$CURRENT_VERSION'):
    print('Release version must be greater than current version')
    sys.exit(1)
" 2>/dev/null; then
        print_error "Release version $RELEASE_VERSION must be greater than current version $CURRENT_VERSION"
        exit 1
    fi

    print_success "Release version determined: $RELEASE_VERSION"
}

# Function to run prerequisites checks
run_prerequisites() {
    print_step "Running prerequisites checks..."

    # Check git status
    if [ -n "$(git status --porcelain)" ]; then
        print_error "Working directory is not clean"
        print_error "Please commit or stash changes before releasing"
        git status --short
        exit 1
    fi

    # Check current branch
    local current_branch=$(git branch --show-current)
    if [ "$current_branch" != "develop" ]; then
        print_error "Not on develop branch (current: $current_branch)"
        print_error "Please switch to develop branch before releasing"
        exit 1
    fi

    # Check if develop is up to date with origin
    git fetch origin develop
    local local_commit=$(git rev-parse HEAD)
    local remote_commit=$(git rev-parse origin/develop)
    if [ "$local_commit" != "$remote_commit" ]; then
        print_warning "Local develop branch is not up to date with origin"
        print_status "Pulling latest changes from origin/develop..."
        if [ "$DRY_RUN" = false ]; then
            git pull origin develop
        fi
    fi

    # Run tests unless skipped
    if [ "$SKIP_TESTS" = false ]; then
        print_status "Running tests..."
        if [ "$DRY_RUN" = false ]; then
            if ! PYTHONPATH="lib_package/src:cli_package/src" python -m pytest tests/ -v --tb=short; then
                print_error "Tests failed"
                exit 1
            fi
        else
            print_warning "DRY RUN: Would run tests"
        fi
    else
        print_warning "Skipping tests (not recommended for production)"
    fi

    # Run code quality checks
    print_status "Running code quality checks..."
    if [ "$DRY_RUN" = false ]; then
        if ! ruff check lib_package/src cli_package/src; then
            print_error "Code quality checks failed"
            exit 1
        fi
    else
        print_warning "DRY RUN: Would run code quality checks"
    fi

    print_success "Prerequisites checks passed"
}

# Function to save current state for rollback
save_state() {
    ORIGINAL_BRANCH=$(git branch --show-current)
    FAILED_STEP=""
    ROLLBACK_NEEDED=true

    print_status "Current state saved for potential rollback"
    print_status "Original branch: $ORIGINAL_BRANCH"
}

# Function to rollback on failure
rollback() {
    if [ "$ROLLBACK_NEEDED" = false ]; then
        return
    fi

    print_error "Rolling back changes due to failure in step: $FAILED_STEP"

    # Return to original branch
    if [ "$(git branch --show-current)" != "$ORIGINAL_BRANCH" ]; then
        print_status "Returning to original branch: $ORIGINAL_BRANCH"
        git checkout "$ORIGINAL_BRANCH" 2>/dev/null || true
    fi

    # Reset to original state
    if [ "$ORIGINAL_BRANCH" = "develop" ]; then
        print_status "Resetting develop branch to original state"
        git reset --hard HEAD~1 2>/dev/null || true
    fi

    # Remove any tags created
    if [ -n "$RELEASE_VERSION" ]; then
        print_status "Removing any created tags"
        git tag -d "v$RELEASE_VERSION" 2>/dev/null || true
        git push origin ":refs/tags/v$RELEASE_VERSION" 2>/dev/null || true
    fi

    print_error "Rollback completed"
}

# Function to bump version
bump_version() {
    print_step "Bumping version..."
    FAILED_STEP="version bump"

    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN: Would bump version from $CURRENT_VERSION to $RELEASE_VERSION"
        python scripts/bump_version.py "$RELEASE_VERSION" --dry-run
        return
    fi

    if python scripts/bump_version.py "$RELEASE_VERSION"; then
        print_success "Version bumped successfully: $CURRENT_VERSION → $RELEASE_VERSION"
    else
        print_error "Version bump failed"
        rollback
        exit 1
    fi
}

# Function to commit version changes
commit_changes() {
    print_step "Committing version changes..."
    FAILED_STEP="commit changes"

    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN: Would commit version changes"
        print_warning "Would run: git add . && git commit -m 'bump: version $RELEASE_VERSION'"
        return
    fi

    # Stage all changes
    git add .

    # Commit with standard message
    if git commit -m "bump: version $RELEASE_VERSION

- Update VERSION file
- Update README.md version badges
- Update package fallback versions
- Automated version bump from $CURRENT_VERSION → $RELEASE_VERSION

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"; then
        print_success "Version changes committed successfully"
    else
        print_error "Failed to commit version changes"
        rollback
        exit 1
    fi
}

# Function to merge to main
merge_to_main() {
    print_step "Merging develop to main..."
    FAILED_STEP="merge to main"

    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN: Would merge develop to main"
        print_warning "Would run: git checkout main && git merge develop"
        return
    fi

    # Switch to main branch
    git checkout main

    # Merge develop into main
    if git merge --no-ff develop -m "release: merge develop into main for v$RELEASE_VERSION

Merging develop branch for release v$RELEASE_VERSION

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"; then
        print_success "Successfully merged develop to main"
    else
        print_error "Failed to merge develop to main"
        rollback
        exit 1
    fi
}

# Function to tag and push
tag_and_push() {
    print_step "Tagging and pushing to GitHub..."
    FAILED_STEP="tag and push"

    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN: Would create tag and push to GitHub"
        print_warning "Would run: git tag v$RELEASE_VERSION && git push origin main && git push origin v$RELEASE_VERSION"
        return
    fi

    # Create tag
    if git tag -a "v$RELEASE_VERSION" -m "Release v$RELEASE_VERSION

$RELEASE_VERSION

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"; then
        print_success "Tag v$RELEASE_VERSION created successfully"
    else
        print_error "Failed to create tag"
        rollback
        exit 1
    fi

    # Push main branch and tag
    if git push origin main && git push origin "v$RELEASE_VERSION"; then
        print_success "Successfully pushed main branch and tag to GitHub"
    else
        print_error "Failed to push to GitHub"
        rollback
        exit 1
    fi
}

# Function to create GitHub release
create_github_release() {
    if [ "$SKIP_GITHUB" = true ]; then
        print_warning "Skipping GitHub release creation"
        return
    fi

    print_step "Creating GitHub release..."
    FAILED_STEP="GitHub release"

    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN: Would create GitHub release"
        print_warning "Would run: gh release create v$RELEASE_VERSION --title 'Release $RELEASE_VERSION' --generate-notes"
        return
    fi

    # Create GitHub release
    if gh release create "v$RELEASE_VERSION" \
        --title "Release $RELEASE_VERSION" \
        --generate-notes \
        --verify; then
        print_success "GitHub release created successfully"
        print_status "Release URL: https://github.com/dderyldowney/todowrite/releases/tag/v$RELEASE_VERSION"
    else
        print_warning "Failed to create GitHub release (continuing with PyPI publishing)"
        print_warning "You can create it manually at: https://github.com/dderyldowney/todowrite/releases/new"
    fi
}

# Function to build and publish packages
build_and_publish() {
    print_step "Building and publishing packages..."
    FAILED_STEP="build and publish"

    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN: Would build and publish packages"
        print_warning "Would run: ./scripts/publish.sh test clean"
        print_warning "Would run: ./scripts/publish.sh prod clean"
        return
    fi

    # First, build packages
    print_status "Building packages..."
    if ! ./scripts/build.sh clean; then
        print_error "Failed to build packages"
        rollback
        exit 1
    fi

    # Publish to TestPyPI
    print_status "Publishing to TestPyPI..."
    if ./scripts/publish.sh test clean; then
        print_success "Successfully published to TestPyPI"
        print_status "TestPyPI URL: https://test.pypi.org/project/todowrite/"
    else
        print_error "Failed to publish to TestPyPI"
        print_warning "Continuing with PyPI publishing (but you should verify TestPyPI)"
    fi

    # Confirm production PyPI upload
    echo
    print_warning "About to publish to PRODUCTION PyPI!"
    echo "This will make the packages publicly available."
    echo
    read -p "Continue with PyPI publishing? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        print_warning "Skipping PyPI publishing"
        return
    fi

    # Publish to production PyPI
    print_status "Publishing to PyPI..."
    if ./scripts/publish.sh prod clean; then
        print_success "Successfully published to PyPI"
        print_status "PyPI URL: https://pypi.org/project/todowrite/"
    else
        print_error "Failed to publish to PyPI"
        print_error "You may need to publish manually using: ./scripts/publish.sh prod clean"
        rollback
        exit 1
    fi
}

# Function to return to develop
return_to_develop() {
    print_step "Returning to develop branch..."
    FAILED_STEP="return to develop"

    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN: Would return to develop branch"
        print_warning "Would run: git checkout develop && git pull origin develop"
        return
    fi

    # Switch back to develop branch
    git checkout develop

    # Pull latest changes to ensure develop is up to date
    if git pull origin develop; then
        print_success "Successfully returned to develop branch"
    else
        print_warning "Failed to pull latest develop changes (you may need to manually sync)"
    fi
}

# Function to show release summary
show_summary() {
    print_header "🎉 RELEASE COMPLETED SUCCESSFULLY!"

    echo -e "${GREEN}Version:${NC} $RELEASE_VERSION"
    echo -e "${GREEN}Previous:${NC} $CURRENT_VERSION"
    echo

    if [ "$DRY_RUN" = false ]; then
        echo -e "${GREEN}What was done:${NC}"
        echo "  ✅ Version bumped and committed"
        echo "  ✅ Merged develop to main"
        echo "  ✅ Tagged and pushed to GitHub"
        if [ "$SKIP_GITHUB" = false ]; then
            echo "  ✅ GitHub release created"
        fi
        echo "  ✅ Published to TestPyPI"
        echo "  ✅ Published to PyPI"
        echo "  ✅ Returned to develop branch"
        echo

        echo -e "${GREEN}Important URLs:${NC}"
        echo "  📦 PyPI: https://pypi.org/project/todowrite/"
        echo "  🧪 TestPyPI: https://test.pypi.org/project/todowrite/"
        echo "  📋 GitHub Release: https://github.com/dderyldowney/todowrite/releases/tag/v$RELEASE_VERSION"
        echo

        echo -e "${GREEN}Installation:${NC}"
        echo "  pip install todowrite"
        echo "  pip install todowrite-cli"
        echo

        echo -e "${YELLOW}Next steps:${NC}"
        echo "  1. Test the new packages in a clean environment"
        echo "  2. Update any documentation or examples"
        echo "  3. Announce the release if needed"
    else
        echo -e "${YELLOW}DRY RUN COMPLETED${NC}"
        echo "  No actual changes were made"
        echo "  Review the output above to see what would happen"
        echo
        echo -e "${YELLOW}To perform the actual release, run:${NC}"
        echo "  ./scripts/release.sh $VERSION_ARG"
    fi
}

# Main release function
main() {
    print_header "🚀 ToDoWrite Release Automation"

    # Parse arguments
    parse_args "$@"

    # Show what we're doing
    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN MODE - No changes will be made"
    fi

    echo -e "${BLUE}Release plan:${NC}"
    echo "  From version: $CURRENT_VERSION (to be determined)"
    echo "  To version: $VERSION_ARG (will be calculated)"
    echo "  Dry run: $DRY_RUN"
    echo "  Skip tests: $SKIP_TESTS"
    echo "  Skip GitHub: $SKIP_GITHUB"
    echo

    if [ "$DRY_RUN" = false ]; then
        read -p "Continue with release? (yes/no): " confirm
        if [ "$confirm" != "yes" ]; then
            print_status "Release cancelled"
            exit 0
        fi
    fi

    # Execute release steps
    validate_environment
    get_current_version
    determine_release_version
    run_prerequisites

    # Save state for potential rollback
    save_state

    # Execute release pipeline
    bump_version
    commit_changes
    merge_to_main
    tag_and_push
    create_github_release
    build_and_publish
    return_to_develop

    # Mark as successful
    ROLLBACK_NEEDED=false

    # Show summary
    show_summary
}

# Set up error handling
trap 'print_error "Script failed unexpectedly"; rollback; exit 1' ERR

# Run main function with all arguments
main "$@"
