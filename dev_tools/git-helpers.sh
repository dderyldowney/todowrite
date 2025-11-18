#!/bin/bash
# ToDoWrite Git Helper Scripts
# Helper functions for proper branch workflow

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_usage() {
    echo "ToDoWrite Git Helper Scripts"
    echo ""
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  start-branch <type> <description>  Start a new feature branch"
    echo "  finish-branch                       Prepare branch for PR"
    echo "  sync-develop                        Sync with develop branch"
    echo "  status                              Show branch status"
    echo "  clean                               Clean up merged branches"
    echo "  help                                Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 start-branch feature user-authentication"
    echo "  $0 start-branch fix cli-version-sync"
    echo "  $0 start-branch refactor cleanup-legacy-code"
}

validate_branch_type() {
    local type="$1"
    local valid_types=("feature" "fix" "refactor" "docs" "test" "build" "chore")

    for valid_type in "${valid_types[@]}"; do
        if [[ "$type" == "$valid_type" ]]; then
            return 0
        fi
    done

    echo -e "${RED}Error: Invalid branch type '$type'${NC}"
    echo "Valid types: ${valid_types[*]}"
    return 1
}

start_branch() {
    local type="$1"
    local description="$2"

    if [[ -z "$type" || -z "$description" ]]; then
        echo -e "${RED}Error: Both type and description required${NC}"
        echo "Usage: $0 start-branch <type> <description>"
        return 1
    fi

    validate_branch_type "$type" || return 1

    # Clean up description (replace spaces with hyphens, lowercase)
    local clean_desc=$(echo "$description" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
    local branch_name="$type/$clean_desc"

    echo -e "${BLUE}Starting new branch: $branch_name${NC}"

    # Update develop first
    echo -e "${YELLOW}Updating develop branch...${NC}"
    git checkout develop
    git pull origin develop

    # Create new branch
    echo -e "${YELLOW}Creating branch: $branch_name${NC}"
    git checkout -b "$branch_name"

    echo -e "${GREEN}✅ Branch '$branch_name' created and ready for work!${NC}"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "1. Make your changes"
    echo "2. Commit frequently with conventional commits"
    echo "3. Run '$0 finish-branch' when ready for PR"
}

finish_branch() {
    local current_branch=$(git branch --show-current)

    if [[ "$current_branch" == "develop" || "$current_branch" == "main" ]]; then
        echo -e "${RED}Error: Cannot finish main branch. Use feature branches.${NC}"
        return 1
    fi

    echo -e "${BLUE}Finishing branch: $current_branch${NC}"

    # Sync with develop
    echo -e "${YELLOW}Syncing with develop...${NC}"
    git checkout develop
    git pull origin develop

    # Rebase current branch
    echo -e "${YELLOW}Rebasing $current_branch onto develop...${NC}"
    git checkout "$current_branch"
    git rebase develop

    # Run tests
    echo -e "${YELLOW}Running tests and quality checks...${NC}"
    if ./dev_tools/build.sh dev; then
        echo -e "${GREEN}✅ All checks passed!${NC}"
    else
        echo -e "${RED}❌ Tests failed. Please fix issues before PR.${NC}"
        return 1
    fi

    # Push branch
    echo -e "${YELLOW}Pushing branch to remote...${NC}"
    git push origin "$current_branch" --force-with-lease

    echo -e "${GREEN}✅ Branch '$current_branch' ready for PR!${NC}"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "1. Create PR targeting 'develop' branch"
    echo "2. Wait for code review"
    echo "3. Merge and delete branch when approved"
}

sync_develop() {
    echo -e "${BLUE}Syncing with develop branch...${NC}"

    local current_branch=$(git branch --show-current)

    if [[ "$current_branch" != "develop" ]]; then
        echo -e "${YELLOW}Stashing current changes...${NC}"
        git stash push -m "Auto-stash before sync"
    fi

    git checkout develop
    git pull origin develop

    if [[ "$current_branch" != "develop" ]]; then
        echo -e "${YELLOW}Returning to branch: $current_branch${NC}"
        git checkout "$current_branch"

        echo -e "${YELLOW}Rebasing onto develop...${NC}"
        git rebase develop

        echo -e "${YELLOW}Restoring stashed changes...${NC}"
        git stash pop
    fi

    echo -e "${GREEN}✅ Synced with latest develop${NC}"
}

show_status() {
    local current_branch=$(git branch --show-current)
    local branch_status=$(git status --porcelain --branch)

    echo -e "${BLUE}Branch Status:${NC}"
    echo "Current branch: ${GREEN}$current_branch${NC}"
    echo "$branch_status"
    echo ""

    if [[ "$current_branch" != "develop" && "$current_branch" != "main" ]]; then
        echo -e "${YELLOW}Feature branch differences with develop:${NC}"
        git log --oneline develop..$current_branch | head -5
        echo ""
    fi

    echo -e "${BLUE}Recent commits on current branch:${NC}"
    git log --oneline -5
}

clean_branches() {
    echo -e "${BLUE}Cleaning up merged branches...${NC}"

    # Update develop
    git checkout develop
    git pull origin develop

    # Remove merged local branches (except main and develop)
    local merged_branches=$(git branch --merged develop | grep -v "^\*" | grep -v "develop" | grep -v "main" | sed 's/^[ ]*//')

    if [[ -n "$merged_branches" ]]; then
        echo -e "${YELLOW}Removing merged branches:${NC}"
        echo "$merged_branches"
        echo "$merged_branches" | xargs git branch -d
        echo -e "${GREEN}✅ Merged branches cleaned up${NC}"
    else
        echo -e "${GREEN}✅ No merged branches to clean${NC}"
    fi

    # Prune remote branches
    echo -e "${YELLOW}Pruning remote branches...${NC}"
    git remote prune origin

    echo -e "${GREEN}✅ Branch cleanup complete${NC}"
}

# Main command handling
case "${1:-}" in
    start-branch)
        start_branch "$2" "$3"
        ;;
    finish-branch)
        finish_branch
        ;;
    sync-develop)
        sync_develop
        ;;
    status)
        show_status
        ;;
    clean)
        clean_branches
        ;;
    help|--help|-h)
        print_usage
        ;;
    *)
        echo -e "${RED}Error: Unknown command '${1:-}'${NC}"
        echo ""
        print_usage
        exit 1
        ;;
esac
