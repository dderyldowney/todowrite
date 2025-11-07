#!/bin/bash

# Document and commit the pending changes
echo "=== ToDoWrite Import Organization Changes ==="
echo ""
echo "Changes Summary:"
echo "- Reorganized imports in CLI main file to ensure core classes are imported first"
echo "- Consolidated and reorganized database model imports in test files"
echo "- Removed unnecessary blank lines between import statements across multiple test files"
echo "- Improved code organization and readability"
echo ""
echo "Files changed:"
echo "- cli_package/src/todowrite_cli/main.py: Import reorganization"
echo "- tests/cli/test_cli.py: Import consolidation"
echo "- tests/cli/test_commands.py: Removed blank line"
echo "- tests/core/test_app.py: Removed blank line"
echo "- tests/database/test_models.py: Removed blank line"
echo "- tests/workflows/test_user_cli_workflows.py: Removed blank line"
echo ""

# Stage the changes
git add -A

# Commit with descriptive message
git commit -m "refactor: reorganize imports and remove whitespace in test files

- Move core imports before grouped imports in CLI main file
- Consolidate database model imports in test files
- Remove unnecessary blank lines between import statements
- Improve import organization for better readability and consistency

These changes improve code organization without affecting functionality.
The import reordering ensures core classes are available before grouped imports,
and the whitespace cleanup makes the test files more consistent."

echo "Changes committed successfully!"

# Push to origin
git push origin develop

echo "Changes pushed to origin/develop"
