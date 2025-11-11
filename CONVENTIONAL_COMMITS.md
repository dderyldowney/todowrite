# Conventional Commits Configuration for ToDoWrite

This project enforces Conventional Commit messages through pre-commit hooks.

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types

- **feat**: New feature for the user
- **fix**: Bug fix for the user
- **docs**: Documentation changes
- **style**: Formatting, missing semi colons, etc. (no code change)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvements
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Maintenance tasks, dependency updates, etc.
- **revert**: Revert previous commit

## Scopes

Valid scopes for this project:
- **lib**: Core library (todowrite package)
- **cli**: Command-line interface (todowrite-cli package)
- **web**: Web interface (todowrite-web package)
- **tests**: Test suite and testing infrastructure
- **docs**: Documentation
- **build**: Build system and packaging
- **config**: Configuration files and settings

## Examples

### Good commits

```
feat(lib): add hierarchical task relationship support

Add parent-child relationships between tasks to support
project planning and task dependencies.

Implements #123

feat(cli): implement task export to JSON format

Users can now export their tasks to JSON for integration
with other tools and workflows.

fix(web): resolve authentication timeout issue

Authentication was timing out after 5 minutes, causing
users to be logged out unexpectedly.

fixes #145

test(lib): add comprehensive coverage for task validation

Add unit tests for all task validation rules and edge cases.
Covers #156-#160.

docs(readme): update installation instructions for Python 3.12

Reflect the new Python 3.12 requirement and updated
installation process using uv.

refactor(cli): simplify command argument parsing

Remove duplicate argument parsing logic and consolidate
into a single reusable function.

chore(deps): update ruff to v0.7.0

Includes latest formatting improvements and bug fixes.
```

### Bad commits (will be rejected)

```
# Missing type
"Add new feature"

# Missing scope
"feat: add new feature"

# Lowercase subject
"feat(lib): add new feature"

# Too long subject
"feat(lib): implement comprehensive hierarchical task management system with full database support"

# Vague description
"fix(lib): fix stuff"

# Missing required scope
"feat: add database support"
```

## Enforcement Rules

- **Type is required**: Must be one of the valid types
- **Scope is required**: Must be one of the valid scopes
- **Subject is required**: Must be capitalized and no longer than 72 characters
- **Body lines**: Max 72 characters per line
- **No period at end**: Subject should not end with a period

## Testing

To test commit messages without committing:

```bash
# Test a valid commit message
echo "feat(lib): add new feature" | git commit-msg-hook -

# Test an invalid commit message
echo "bad commit message" | git commit-msg-hook -
```

## Integration

This configuration integrates with:
- **Pre-commit hooks**: Automatically validate commit messages
- **Gitlint**: Additional commit message validation
- **Semantic versioning**: Can be used for automated version bumps
- **Changelog generation**: Can be used to generate CHANGELOG.md
