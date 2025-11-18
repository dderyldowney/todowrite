# Claude Code Powered Development Workflow

This document describes the comprehensive development workflow powered by Claude Code for the ToDoWrite monorepo, including quality enforcement, semantic scoping, and AI-assisted development practices.

## 🤖 Overview

The ToDoWrite project leverages Claude Code's advanced capabilities to create a sophisticated development environment that ensures code quality, consistency, and developer productivity through automated enforcement and AI assistance.

## 🏗️ Development Environment Setup

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite

# Install development environment
uv sync --dev

# Install pre-commit hooks
pre-commit install

# Initialize Claude Code environment
python .claude/autorun.py
```

### Claude Code Configuration

The project uses a hierarchical Claude Code configuration:

```
.claude/                                    # Root configuration (applies to all packages)
├── agent_registry.json                    # Central agent configuration
├── comprehensive_quality_enforcement.json # Quality enforcement rules
├── semantic_scoping_*.json               # Semantic scoping system
├── conventional_commits_*.json           # Commit message enforcement
├── tdd_workflow.json                     # Test-driven development workflow
├── skills_testing_*.json                 # Skills testing workflow
├── workflow_enforcement.json             # Development workflow enforcement
├── permanent_code_quality_*.json         # Permanent quality gates
└── autorun.py                           # Automatic setup script

web_package/src/todowrite_web/.claude/     # Independent web development environment
└── agent_registry.json                  # Web-specific configuration
```

## 🎯 Semantic Scoping Workflow

### Understanding Semantic Scopes

The project uses semantic scoping to provide context-aware development:

| Scope | Description | When to Use | Example |
|-------|-------------|-------------|---------|
| `lib` | Core library functionality | Working on `lib_package/` | `feat(lib): add hierarchical task relationships` |
| `cli` | Command-line interface | Working on `cli_package/` | `fix(cli): resolve argument parsing bug` |
| `web` | Web application | Working on `web_package/` | `feat(web): implement real-time task updates` |
| `tests` | Test suite | Writing or modifying tests | `test(lib): add comprehensive integration tests` |
| `docs` | Documentation | Updating documentation | `docs(readme): update installation instructions` |
| `build` | Build system | Modifying build configuration | `build(lib): update packaging configuration` |
| `config` | Configuration | Changing project configuration | `feat(config): add semantic scoping validation` |
| `ci` | Continuous integration | Updating CI/CD pipelines | `ci(github): add automated testing workflow` |
| `deps` | Dependencies | Updating project dependencies | `deps(lib): upgrade SQLAlchemy to latest` |

### Automatic Scope Detection

Claude Code automatically detects the appropriate scope based on:

1. **File Patterns**: Each scope has defined file patterns
2. **Directory Structure**: Package locations determine scope
3. **Changed Files**: Git diff analysis identifies affected areas
4. **Context Awareness**: Development context influences scope selection

### Commit Message Format

All commits must follow the conventional commits format with semantic scoping:

```
<type>(scope): description

[optional body]

[optional footer(s)]
```

**Examples:**
- `feat(lib): add hierarchical task relationships`
- `fix(cli): resolve authentication timeout issue`
- `test(web): add comprehensive coverage for user interface`
- `docs(config): update development environment settings`

## 🧪 Test-Driven Development Workflow

### Red-Green-Refactor Methodology

The project enforces strict TDD methodology through automated hooks:

#### 🔴 RED Phase - Write Failing Test
```python
# test_example.py
def test_new_feature_should_fail_initially():
    """Test that new feature fails before implementation."""
    result = some_new_function()
    assert result == "expected_value"  # This will fail initially
```

**Rules:**
- Write test BEFORE production code
- Watch test FAIL for correct reason
- Test should fail because feature doesn't exist
- **Forbidden**: Writing production code before test

#### 🟢 GREEN Phase - Make Test Pass
```python
# implementation.py
def some_new_function():
    """Minimal implementation to make test pass."""
    return "expected_value"  # Simplest possible implementation
```

**Rules:**
- Write MINIMAL code to make test pass
- All tests must pass with clean output
- No extra features beyond test requirements
- **Forbidden**: Over-engineering or adding extra features

#### 🔄 REFACTOR Phase - Clean Up Code
```python
# implementation.py (refactored)
def some_new_function():
    """Improved implementation while maintaining test passing."""
    if not hasattr(some_new_function, '_cached'):
        some_new_function._cached = "expected_value"
    return some_new_function._cached
```

**Rules:**
- Clean up code while keeping tests green
- Remove duplication and improve design
- Tests must remain green throughout refactoring
- **Forbidden**: Adding new behavior during refactoring

### TDD Enforcement Features

- **Automated Validation**: Hooks enforce TDD compliance
- **Zero Mocking Policy**: Only real implementations allowed
- **Test Coverage Requirements**: Minimum coverage thresholds enforced
- **Real Implementation Testing**: All tests must use actual implementations

## 🔒 Quality Assurance Workflow

### Pre-commit Quality Gates

All commits go through comprehensive quality checks:

```bash
# Automatic quality checks run before each commit
pre-commit run --all-files
```

### Quality Enforcement Tools

#### Code Quality (Ruff)
- **Linting**: Comprehensive code analysis
- **Formatting**: Consistent code style
- **Import Sorting**: Organized imports
- **Type Checking**: Static type analysis
- **Security Analysis**: Built-in vulnerability detection

#### Security Analysis (Bandit)
- **Vulnerability Scanning**: Automated security analysis
- **Subprocess Validation**: Secure subprocess call handling
- **Dependency Security**: Vulnerable dependency detection

#### Secret Detection (Detect-Secrets)
- **Credential Prevention**: Blocks API keys, passwords, tokens
- **Baseline Management**: Tracks known secrets
- **Pattern Matching**: Advanced secret detection patterns

#### Database Migration Validation (Alembic)
- **Migration Consistency**: Ensures proper migration scripts
- **Schema Drift Prevention**: Blocks manual schema changes
- **Migration History**: Maintains complete audit trail

### Quality Metrics

- **Code Coverage**: Minimum 80% coverage required
- **Security Score**: Zero high-severity vulnerabilities
- **Code Quality**: All Ruff checks must pass
- **Test Quality**: All tests use real implementations

## 🔄 Development Workflow Process

### 1. Session Initialization

```bash
# Start development session
cd todowrite

# Claude Code automatically initializes
# - Loads semantic scoping configuration
# - Activates quality enforcement
# - Sets up development environment
# - Validates project structure
```

### 2. Feature Development

#### Step 1: Planning Phase
```bash
# Claude Code assists with planning
"Plan the implementation of hierarchical task relationships"

# Claude Code will:
# - Analyze requirements
# - Create implementation plan
# - Identify affected components
# - Suggest semantic scope
```

#### Step 2: TDD Implementation
```bash
# Write failing test first
"Create tests for hierarchical task relationships"

# Watch test fail
# Verify failure reason is correct

# Write minimal implementation
"Implement minimal code to make tests pass"

# Verify all tests pass
```

#### Step 3: Refactoring
```bash
# Clean up implementation while tests remain green
"Refactor the hierarchical task relationship code for better maintainability"

# Ensure tests continue to pass
```

### 3. Code Review Process

#### Automated Review
```bash
# Pre-commit hooks provide automated review
pre-commit run --all-files

# Checks performed:
# - Code formatting and style
# - Security vulnerability scanning
# - Type checking
# - Secret detection
# - Database migration validation
# - Test coverage verification
```

#### Claude Code Review
```bash
# Request code review from Claude
"Review the hierarchical task relationship implementation"

# Claude Code will:
# - Analyze code quality
# - Check for security issues
# - Verify test coverage
# - Suggest improvements
# - Validate semantic scoping compliance
```

### 4. Commit Process

#### Semantic Commit Creation
```bash
# Claude Code helps create proper commit messages
"Create a commit for the hierarchical task relationships feature"

# Result: feat(lib): add hierarchical task relationships
```

#### Quality Validation
```bash
# Commit with automatic quality checks
git add .
git commit -m "feat(lib): add hierarchical task relationships"

# Pre-commit hooks validate:
# - Semantic scoping compliance
# - Conventional commit format
# - Code quality standards
# - Security requirements
# - Test coverage
```

## 🎯 Claude Code Skills Integration

### Available Skills

The project integrates several specialized Claude Code skills:

#### Episodic Memory
- **Purpose**: Remembers past conversations and decisions
- **Usage**: `Remember previous hierarchical task management decisions`
- **Benefit**: Avoids repeating mistakes and maintains consistency

#### Test-Driven Development
- **Purpose**: Enforces TDD methodology
- **Usage**: `Implement feature using TDD methodology`
- **Benefit**: Ensures high test coverage and code quality

#### Brainstorming
- **Purpose**: Collaborative idea refinement
- **Usage**: `Brainstorm approaches for hierarchical task visualization`
- **Benefit**: Explores multiple solution approaches

#### Planning
- **Purpose**: Creates detailed implementation plans
- **Usage**: `Plan implementation of new task relationship features`
- **Benefit**: Ensures comprehensive consideration of requirements

### Skill Usage Workflow

```bash
# 1. Remember past decisions
"Remember previous decisions about hierarchical task management"

# 2. Brainstorm solutions
"Brainstorm approaches for implementing task dependencies"

# 3. Create detailed plan
"Plan the implementation of task dependency features"

# 4. Implement with TDD
"Implement task dependencies using test-driven development"

# 5. Review and validate
"Review the task dependency implementation"
```

## 🔧 Configuration Management

### Environment Configuration

The project uses environment-specific configuration:

```bash
# Development environment
export DATABASE_URL="sqlite:///development_todowrite.db"
export DEBUG="true"
export LOG_LEVEL="DEBUG"

# Production environment
export DATABASE_URL="postgresql://user:pass@localhost/todowrite"  # pragma: allowlist secret
export DEBUG="false"
export LOG_LEVEL="INFO"
```

### Package Configuration

Each package has specific configuration:

#### lib_package (Core Library)
```python
# Library configuration
TODOWRITE_DEFAULT_STORAGE = "sqlite"
TODOWRITE_SCHEMA_VALIDATION = True
TODOWRITE_TYPE_CHECKING = True
```

#### cli_package (CLI Interface)
```python
# CLI configuration
TODOWRITE_CLI_COLORS = True
TODOWRITE_CLI_PROGRESS_BARS = True
TODOWRITE_CLI_TABLE_FORMAT = "fancy_grid"
```

#### web_package (Web Application)
```python
# Web application configuration
TODOWRITE_WEB_HOST = "0.0.0.0"
TODOWRITE_WEB_PORT = 8000
TODOWRITE_WEB_DEBUG = False
TODOWRITE_WEB_CORS_ORIGINS = ["http://localhost:3000"]
```

## 📊 Workflow Monitoring

### Quality Metrics Dashboard

Monitor development quality through automated metrics:

```bash
# Check quality status
python .claude/hooks/session_initialization.py

# View semantic scoping status
cat .claude/agent_registry.json | jq '.claude-code.semantic_scoping_aware'

# Check test coverage
pytest --cov=src/todowrite --cov-report=term-missing

# Verify security status
bandit -r . -f json
```

### Development Analytics

Track development progress and patterns:

- **Commit Quality**: Semantic scoping compliance rate
- **Code Quality**: Ruff compliance scores
- **Test Coverage**: Coverage percentages across packages
- **Security Status**: Vulnerability counts and severity
- **Development Velocity**: Commit frequency and patterns

## 🚀 Advanced Workflow Features

### Multi-Package Development

When working across multiple packages:

```bash
# 1. Understand package relationships
"Explain the relationship between lib_package and cli_package"

# 2. Plan cross-package changes
"Plan changes that affect both core library and CLI"

# 3. Implement with package awareness
"Update library interface and CLI integration"

# 4. Test across packages
"Run integration tests covering library and CLI"
```

### Database Migration Workflow

When making database changes:

```bash
# 1. Create migration
"Create Alembic migration for new task relationship fields"

# 2. Validate migration
python .hooks/alembic-enforcer.py --check

# 3. Test migration
# Test migration on development database

# 4. Apply and verify
# Apply migration and verify functionality
```

### Performance Optimization

When optimizing performance:

```bash
# 1. Analyze performance
"Analyze performance bottlenecks in hierarchical task queries"

# 2. Plan optimizations
"Plan database query optimizations for task hierarchies"

# 3. Implement optimizations
"Implement query optimizations with proper testing"

# 4. Validate improvements
"Verify performance improvements meet requirements"
```

## 🔍 Troubleshooting

### Common Issues

#### Quality Enforcement Failures
```bash
# Check what failed
pre-commit run --all-files

# Fix common issues
ruff check . --fix
ruff format .
```

#### Semantic Scoping Issues
```bash
# Check scope configuration
cat .claude/semantic_scoping_awareness.json

# Validate scope usage
python .hooks/semantic-scope-validator.py --help
```

#### TDD Compliance Issues
```bash
# Check TDD compliance
python .hooks/red-green-refactor-enforcer.py --help

# Verify test coverage
pytest --cov=src/todowrite --cov-fail-under=80
```

### Getting Help

```bash
# Claude Code assistance
"Help me debug the quality enforcement failures"

# Check configuration
cat .claude/comprehensive_quality_enforcement.json

# Verify setup
python .claude/autorun.py
```

## 📈 Best Practices

### Development Practices

1. **Always Use Semantic Scoping**: Ensure all commits use proper semantic scopes
2. **Follow TDD Methodology**: Write tests before implementation
3. **Maintain High Test Coverage**: Keep coverage above 80%
4. **Use Real Implementations**: Avoid mocking in tests
5. **Follow Security Best Practices**: Use secure coding patterns
6. **Keep Documentation Updated**: Update docs with code changes

### Workflow Practices

1. **Start with Episodic Memory**: Remember past decisions before starting
2. **Use Brainstorming for Complex Problems**: Explore multiple approaches
3. **Create Detailed Plans**: Use planning skill for complex features
4. **Implement with TDD**: Follow red-green-refactor methodology
5. **Review and Refactor**: Continuously improve code quality
6. **Commit Frequently**: Make small, focused commits with proper semantic scoping

### Quality Practices

1. **Let Automation Help**: Trust quality enforcement tools
2. **Fix Issues Promptly**: Address quality feedback immediately
3. **Maintain Consistency**: Follow established patterns and conventions
4. **Document Decisions**: Keep track of important architectural decisions
5. **Collaborate Effectively**: Use Claude Code for collaborative development

---

This comprehensive development workflow ensures that ToDoWrite maintains high code quality, security standards, and development best practices while providing an efficient and enjoyable development experience powered by Claude Code.
