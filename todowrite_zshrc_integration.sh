#!/usr/bin/env zsh
#
# ToDoWrite Zsh Integration
# ================================
#
# This file contains the shell integration logic for ToDoWrite's database architecture.
#
# To enable ToDoWrite's automatic database detection and loading:
#
# 1. Add this line to your ~/.zshrc:
#    source /path/to/todowrite/todowrite_zshrc_integration.sh
#
# 2. Or copy the contents below into your ~/.zshrc directly
#
# 3. Reload your shell with: source ~/.zshrc
#
# Architecture Overview:
# ===================
#
# Database Naming Convention:
# - Development: ~/dbs/{project}_{project}_development.db (collaborative planning)
# - Production:  ~/dbs/{project}_{project}_production.db  (end user deployments)
# - Testing:     $project_root/tmp/todowrite_todowrite_testing.db (tests only)
#
# Directory Structure:
# - $project_root: Monorepo root (contains lib_package, cli_package, web_package)
# - $package_root: Individual package directories
#
# Priority System:
# 1. Testing database (EXPLICIT USE ONLY by tests)
# 2. Development database (auto-loaded for collaborative work)
# 3. Production database (auto-loaded in production areas only)

# Function to check if directory is a test/development area
is_test_or_dev_area() {
    local current_dir="$1"
    local full_path="$2"

    # Primary check: current directory name
    case "$current_dir" in
        *test*|*tmp*|*dev*|development|build|dist|spec|coverage)
            return 0
            ;;
    esac

    # Secondary check: parent directories in the path
    if [[ "$full_path" == *"/tests/"* ]] || [[ "$full_path" == *"/test/"* ]] || [[ "$full_path" == *"/spec/"* ]] || [[ "$full_path" == *"/tmp/"* ]] || [[ "$full_path" == *"/dev/"* ]] || [[ "$full_path" == *"/development/"* ]]; then
        return 0
    fi

    # Special case: path starts with /tmp (directly in tmp)
    if [[ "$full_path" == "/tmp/"* ]]; then
        return 0
    fi

    # No test patterns found - this is a production area
    return 1
}

# Function to find project root (monorepo root) by looking for characteristic package structure
find_project_root() {
    local search_dir="$PWD"

    # Search up the directory tree for project root (contains lib_package, cli_package, web_package)
    while [[ "$search_dir" != "/" ]]; do
        if [[ -d "$search_dir/lib_package" && -d "$search_dir/cli_package" && -d "$search_dir/web_package" ]]; then
            echo "$search_dir"
            return 0
        fi
        search_dir="$(dirname "$search_dir")"
    done

    # If not found, return current directory (fallback for non-monorepo projects)
    echo "$PWD"
    return 1
}

# Function to get project name from project root (monorepo root)
get_project_name() {
    local project_root="$(find_project_root)"
    local project_name="$(basename "$project_root")"
    echo "$project_name"
}

# Function to check for todowrite database using correct project-specific naming
load_todowrite_db() {
    # Clear any existing todowrite database URL
    unset TODOWRITE_DATABASE_URL

    # Get current project name
    local project_name="$(get_project_name)"
    local dev_db_name="${project_name}_${project_name}_development.db"
    local prod_db_name="${project_name}_${project_name}_production.db"

    # Priority 1: Project-specific development database in ~/dbs/ (for collaborative work)
    if [[ -f "$HOME/dbs/$dev_db_name" ]]; then
        export TODOWRITE_DATABASE_URL="sqlite:///$HOME/dbs/$dev_db_name"
        echo "🗂️  ToDoWrite DEV DB: $dev_db_name (collaborative project: $project_name)"
        return 0
    fi

    # Priority 2: Project-specific production database in ~/dbs/ (only if not in test/dev area)
    if [[ -f "$HOME/dbs/$prod_db_name" ]]; then
        if is_test_or_dev_area "$(basename "$PWD")" "$PWD"; then
            echo "⚠️  Production database not available in test/development areas"
            return 1
        else
            export TODOWRITE_DATABASE_URL="sqlite:///$HOME/dbs/$prod_db_name"
            echo "🗂️  ToDoWrite PROD DB: $prod_db_name (project: $project_name)"
            return 0
        fi
    fi

    # NOTE: Testing database ($PWD/tmp/todowrite_todowrite_testing.db) is for TESTS ONLY
    # Do NOT auto-load it for general project work to avoid test data contamination

    echo "ℹ️  No project database found for '$project_name'"
    echo "   → Create development: TODOWRITE_DATABASE_URL=sqlite:///$HOME/dbs/$dev_db_name"
    echo "   → For tests only: TODOWRITE_DATABASE_URL=sqlite:///$PWD/tmp/todowrite_todowrite_testing.db"
    return 1
}

# Function to manually reload todowrite database
reload_todowrite() {
    load_todowrite_db
    if [[ -n "$TODOWRITE_DATABASE_URL" ]]; then
        echo "✅ Loaded: $TODOWRITE_DATABASE_URL"
    else
        echo "❌ No todowrite database found in current directory tree"
    fi
}

# Pre-command hook to catch database creation attempts (PROJECT-SPECIFIC)
todowrite_preexec() {
    local cmd="$1"

    # Look for patterns that might create databases
    if [[ "$cmd" == *"todowrite"* ]]; then
        if [[ "$cmd" == *"create"* ]] || [[ "$cmd" == *"init"* ]] || [[ "$cmd" == *"migrate"* ]]; then
            if [[ -z "$TODOWRITE_DATABASE_URL" ]]; then
                local project_name="$(get_project_name)"
                local dev_db_name="${project_name}_${project_name}_development.db"
                echo "⚠️  WARNING: todowrite command without explicit database"
                echo "   → For project development: TODOWRITE_DATABASE_URL=sqlite:///$HOME/dbs/$dev_db_name"
                echo "   → For tests only: TODOWRITE_DATABASE_URL=sqlite:///$PWD/tmp/todowrite_todowrite_testing.db"
                echo "   → Use 'reload_todowrite' to auto-detect project database"
                echo "   → TESTING DATABASE IS FOR TESTS ONLY - DO NOT USE FOR PROJECT WORK"
            fi
        fi
    fi
}

# Function to enforce database naming conventions (WARNINGS ONLY)
enforce_todowrite_conventions() {
    local search_dir="$PWD"

    # Search current directory for improperly named database files
    if [[ -f "$search_dir/development_todowrite.db" ]]; then
        echo "⚠️  WARNING: development_todowrite.db found - should use ~/dbs/todowrite_todowrite_development.db"
        echo "   → Use 'mv development_todowrite.db ~/dbs/todowrite_todowrite_development.db' to fix"
    elif [[ -f "$search_dir/todowrite.db" && "$search_dir" != "$HOME/dbs" ]]; then
        echo "⚠️  WARNING: todowrite.db found in wrong location"
        echo "   → Should use ~/dbs/todowrite_todowrite_development.db or ~/dbs/todowrite_todowrite_production.db"
        echo "   → Or move to ~/dbs/ directory if this is meant to be a production database"
    fi
}

# Function to report on todowrite database naming violations (WARNING ONLY)
cleanup_todowrite_databases() {
    local count=0

    echo "🔍 Scanning for todowrite database naming violations..."

    # Find and report incorrectly named database files
    find "$PWD" -name "*.db" -type f 2>/dev/null | while read -r db_file; do
        local dir_path="$(dirname "$db_file")"
        local dir_name="$(basename "$dir_path")"
        local db_name="$(basename "$db_file")"

        # Check for violations: old naming patterns or wrong locations
        if [[ "$db_name" == "development_todowrite.db" ]] ||
           [[ "$db_name" == "todowrite.db" && "$dir_path" != "$HOME/dbs" ]]; then
            echo "⚠️  VIOLATION FOUND: $db_file"
            if [[ "$dir_name" == "tmp" ]]; then
                echo "   → Should be renamed to: todowrite_todowrite_testing.db"
            else
                echo "   → Should use ~/dbs/todowrite_todowrite_development.db or ~/dbs/todowrite_todowrite_production.db"
            fi
            count=$((count + 1))
        fi
    done

    echo ""
    echo "📋 Proper database locations:"
    echo "   • Development: ~/dbs/todowrite_todowrite_development.db"
    echo "   • Production:  ~/dbs/todowrite_todowrite_production.db"
    echo "   • Testing:     \$PROJECT_ROOT/tmp/todowrite_todowrite_testing.db"
    echo "   • No files were automatically modified"
}

# Function to show current environment and violations
show_todowrite_status() {
    echo "Current directory: $PWD"

    # Check for violations first
    local has_violation=0
    if [[ -f "development_todowrite.db" ]]; then
        echo "❌ VIOLATION: development_todowrite.db found - should use ~/dbs/todowrite_todowrite_development.db"
        has_violation=1
    elif [[ -f "todowrite.db" && "$PWD" != "$HOME/dbs" ]]; then
        echo "❌ VIOLATION: todowrite.db found in wrong location - should use ~/dbs/todowrite_todowrite_development.db"
        has_violation=1
    fi

    # Show database status
    if [[ -n "$TODOWRITE_DATABASE_URL" ]]; then
        echo "✅ ToDoWrite DB loaded: $TODOWRITE_DATABASE_URL"
    else
        if [[ $has_violation -eq 1 ]]; then
            echo "⚠️  Database loading blocked due to naming violations"
        else
            echo "❌ No ToDoWrite database found"
        fi
    fi

    # Final status summary
    if [[ $has_violation -eq 0 ]]; then
        echo "✅ No database naming violations"
    fi
}

# Hook into directory changes for enforcement
autoload -U add-zsh-hook
add-zsh-hook chpwd load_todowrite_db
add-zsh-hook chpwd enforce_todowrite_conventions
add-zsh-hook preexec todowrite_preexec

# Load database for current session and enforce conventions
load_todowrite_db
enforce_todowrite_conventions

echo "✅ ToDoWrite shell integration loaded"
echo "   • Auto-loading project databases on directory change"
echo "   • Enforcing proper database naming conventions"
echo "   • Use 'reload_todowrite' to manually reload database"
echo "   • Use 'show_todowrite_status' to check current status"
echo "   • Use 'cleanup_todowrite_databases' to find naming violations"
