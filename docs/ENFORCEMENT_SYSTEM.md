# ToDoWrite Quality Enforcement System

This document provides a comprehensive overview of the quality enforcement system that ensures code quality, security, and development best practices across the ToDoWrite monorepo.

## 🔧 Overview

The ToDoWrite project uses a multi-layered quality enforcement system that integrates seamlessly with the development workflow. The system is designed to be automatic, comprehensive, and educational while minimizing developer friction.

## 📁 Enforcement System Architecture

```
.claude/                                    # Claude Code development environment
├── agent_registry.json                    # Central agent configuration
├── comprehensive_quality_enforcement.json # Quality enforcement configuration
├── conventional_commits_enforcement.json  # Commit message enforcement
├── semantic_scoping_*.json               # Semantic scope enforcement
├── tdd_workflow.json                     # Test-driven development workflow
├── skills_testing_*.json                 # Skills testing workflow
├── workflow_enforcement.json             # Development workflow enforcement
├── token_optimization_config.json        # AI token optimization
├── permanent_code_quality_enforcement.json # Permanent quality gates
└── [30+ additional enforcement configs]  # Various quality configurations

.hooks/                                   # Custom quality enforcement hooks
├── red-green-refactor-enforcer.py        # TDD methodology enforcement
├── alembic-enforcer.py                   # Database migration validation
├── test-cleanup-enforcer.py              # Test artifact management
├── tmp-file-enforcer.py                  # Hardcoded temp file prevention
└── token-optimizer.py                    # Token usage optimization

.pre-commit-config.yaml                  # Pre-commit hook configuration
.pyproject.toml                          # Project-wide tool configuration
```

## 🎯 Semantic Scoping System

### Configuration Files
- **`.claude/semantic_scoping_awareness.json`**: Defines semantic scopes and patterns
- **`.claude/semantic_scoping_enforcement.json`**: Enforces scope usage in commits
- **`.claude/agent_registry.json`**: Contains monorepo package definitions

### Available Semantic Scopes

| Scope | Description | File Patterns | Example Usage |
|-------|-------------|---------------|---------------|
| `lib` | Core todowrite library functionality | `lib_package/`, `src/todowrite/` | `feat(lib): add hierarchical task relationships` |
| `cli` | Command-line interface and CLI tools | `cli_package/`, `src/todowrite_cli/` | `fix(cli): resolve argument parsing bug` |
| `web` | Web interface and API endpoints | `web_package/`, `src/todowrite_web/` | `feat(web): implement real-time task updates` |
| `tests` | Test suite and testing infrastructure | `tests/`, `test_`, `_test.py` | `test(lib): add comprehensive integration tests` |
| `docs` | Documentation and guides | `docs/`, `*.md`, `README*` | `docs(readme): update installation instructions` |
| `build` | Build system, packaging, and deployment | `pyproject.toml`, `Makefile`, `Dockerfile` | `build(lib): update packaging configuration` |
| `config` | Configuration files and settings | `.pre-commit-config.yaml`, `.env*`, `.claude/` | `feat(config): add semantic scoping validation` |
| `ci` | Continuous integration and deployment | `.github/`, `.gitlab-ci.yml` | `ci(github): add automated testing workflow` |
| `deps` | Dependencies and requirements | `requirements*`, `uv.lock`, `poetry.lock` | `deps(lib): upgrade SQLAlchemy to latest` |

### Enforcement Features
- **Automatic Scope Detection**: Based on changed files
- **Format Validation**: `<type>(scope): description` format required
- **Pattern Matching**: Intelligent file-to-scope mapping
- **Cross-Agent Consistency**: Enforced across all AI agents
- **Error Prevention**: Helpful suggestions and corrections

## 🚦 Conventional Commits Enforcement

### Configuration File
- **`.claude/conventional_commits_enforcement.json`**: Commit message rules and validation

### Supported Commit Types
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test additions or modifications
- `build`: Build system changes
- `ci`: CI/CD changes
- `chore`: Maintenance tasks
- `revert`: Revert previous changes

### Enforcement Hooks
- **Commit Message Validation**: Enforces format compliance
- **Scope Validation**: Requires semantic scoping
- **Length Limits**: Subject line max 72 characters
- **Capitalization**: Subject must start with lowercase
- **No Period**: Subject line should not end with period

## 🧪 Test-Driven Development Enforcement

### Configuration Files
- **`.claude/tdd_workflow.json`**: TDD methodology configuration
- **`.hooks/red-green-refactor-enforcer.py`**: Red-Green-Refactor methodology enforcement

### TDD Methodology Phases

#### 🔴 RED Phase
- Write failing test before production code
- Watch test fail for correct reason
- Test should fail because feature doesn't exist
- **Forbidden**: Writing production code before test

#### 🟢 GREEN Phase
- Write minimal code to make test pass
- All tests must pass with clean output
- No extra features beyond test requirements
- **Forbidden**: Over-engineering or adding features beyond test

#### 🔄 REFACTOR Phase
- Clean up code while keeping tests green
- Remove duplication and improve design
- Tests must remain green throughout refactoring
- **Forbidden**: Adding new behavior during refactoring

### Quality Gates
- **Zero Mocking Policy**: Only real implementations allowed
- **Test Coverage**: 80% minimum coverage requirement
- **Real Implementation Testing**: All tests use actual implementations
- **TDD Compliance**: Enforced Red-Green-Refactor methodology

## 🔍 Security Analysis

### Tools and Configuration
- **Bandit**: Security vulnerability scanning (configured in `pyproject.toml`)
- **Detect-Secrets**: Secret detection and prevention
- **Ruff Security**: Built-in security rules and analysis

### Security Enforcement
- **Vulnerability Scanning**: Automated security analysis on all Python files
- **Secret Detection**: Prevents API keys, passwords, tokens from being committed
- **Subprocess Validation**: All subprocess calls secured with proper validation
- **Dependency Scanning**: Automated checks for vulnerable dependencies

### Configuration Files
- **`.secrets.baseline`**: Secret detection baseline
- **`pyproject.toml`**: Bandit configuration and excludes
- **`.pre-commit-config.yaml`**: Security hooks integration

## 📊 Code Quality Enforcement

### Tools and Configuration
- **Ruff**: Comprehensive Python linting, formatting, and type checking
- **Pre-commit Hooks**: Automated quality checks before commits
- **Type Annotations**: Static type checking with comprehensive coverage

### Ruff Configuration
```toml
[tool.ruff]
line-length = 100
target-version = "py312"
select = [
    "E", "W",  # pycodestyle
    "F",       # pyflakes
    "I",       # isort
    "B",       # flake8-bugbear
    "C4",      # flake8-comprehensions
    "UP",      # pyupgrade
    "RUF",     # Ruff-specific rules
    "S",       # flake8-bandit (security)
    "SIM",     # flake8-simplify
    "ARG",     # flake8-unused-arguments
    "TCH",     # type-checking
    "ANN",     # type annotations
    "PLC0415", # import-outside-top-level
    "E402",    # module-import-not-at-top
]
```

### Quality Features
- **Automatic Formatting**: Consistent code style across all files
- **Import Sorting**: Organized and optimized imports
- **Type Checking**: Comprehensive static type analysis
- **Security Analysis**: Built-in vulnerability detection
- **Performance Analysis**: Code performance optimization suggestions
- **Complexity Analysis**: Maintainable code complexity limits

## 🗃️ Database Migration Enforcement

### Tools and Configuration
- **Alembic**: Database migration management
- **`.hooks/alembic-enforcer.py`**: Migration validation hook
- **`alembic.ini`**: Migration configuration

### Enforcement Features
- **Migration Validation**: Ensures all migrations are properly created
- **Database Consistency**: Validates migration scripts across environments
- **Schema Drift Detection**: Prevents manual schema modifications
- **Migration History**: Maintains complete migration audit trail

### Configuration Files
- **`alembic.ini`**: Alembic configuration
- **`alembic/env.py`**: Migration environment setup
- **`alembic/versions/`**: Migration version files

## ⚡ Token Optimization

### Tools and Configuration
- **`.hooks/token-optimizer.py`**: AI token usage optimization
- **`.claude/token_optimization_config.json`**: Optimization rules and thresholds

### Optimization Features
- **Redundant Comment Removal**: Eliminates unnecessary documentation
- **Verbose Docstring Simplification**: Optimizes documentation length
- **Unused Import Detection**: Removes unused imports and dependencies
- **Code Structure Optimization**: Improves code organization for AI efficiency
- **Token Usage Analysis**: Provides efficiency metrics and suggestions

### Quality Thresholds
- **Token Inefficiency**: 15% threshold for optimization alerts
- **Code Complexity**: Maximum complexity limits enforced
- **File Size**: 1MB maximum file size limits

## 🧹 Test Artifact Management

### Tools and Configuration
- **`.hooks/test-cleanup-enforcer.py`**: Test artifact cleanup enforcement
- **`.claude/test_cleanup_config.json`**: Cleanup rules and policies

### Management Features
- **Automatic Cleanup**: Removes test artifacts after completion
- **Coverage Report Management**: Optimizes coverage report storage
- **Temporary File Cleanup**: Prevents temporary file accumulation
- **Database Cleanup**: Removes test databases and schemas

## 🔒 Hardcoded Value Prevention

### Tools and Configuration
- **`.hooks/tmp-file-enforcer.py`**: Hardcoded temporary file prevention
- **`.claude/tmp_file_enforcement_config.json`**: Temporary file usage policies

### Prevention Features
- **Hardcoded `/tmp` Detection**: Prevents hardcoded temporary directory usage
- **Secure Alternatives**: Enforces use of proper temporary file APIs
- **Cross-Platform Compatibility**: Ensures portable temporary file handling
- **Security Validation**: Prevents temporary file security vulnerabilities

## 🔄 Permanent Enforcement

### Configuration Files
- **`.claude/permanent_code_quality_enforcement.json`**: Permanent quality gates
- **`.claude/autorun.py`**: Automatic enforcement activation
- **`.claude/permanent_enforcement_active`**: Enforcement activation marker

### Permanent Features
- **Session Persistence**: Enforcement survives `/clear` commands
- **Automatic Activation**: Quality gates activate on session start
- **Cross-Session Consistency**: Maintains standards across sessions
- **Zero-Tolerance Violations**: Critical quality gates prevent violations

## 🤖 Claude Code Integration

### Agent Configuration
- **Universal Agent Coverage**: All AI agents subject to enforcement
- **Subagent Coordination**: Consistent enforcement across subagents
- **Code Review Integration**: Quality gates in code review process
- **Planning Agent Compliance**: Standards enforced in planning phase

### Workflow Integration
- **Session Initialization**: Automatic quality setup on session start
- **Context Awareness**: Enforcement adapts to development context
- **Skill Integration**: Quality enforcement integrated with skill usage
- **Memory Integration**: Enforcement learns from project history

## 📋 Enforcement Configuration Files

### Core Configuration Files

| File | Purpose | Key Features |
|------|---------|--------------|
| `.claude/agent_registry.json` | Central agent configuration | Monorepo package definitions, semantic scoping |
| `.claude/comprehensive_quality_enforcement.json` | Quality enforcement configuration | Tool integration, quality gates |
| `.claude/conventional_commits_enforcement.json` | Commit message enforcement | Format validation, scope requirements |
| `.claude/semantic_scoping_awareness.json` | Semantic scope definitions | Scope patterns, file mappings |
| `.claude/semantic_scoping_enforcement.json` | Scope enforcement rules | Validation, error handling |
| `.claude/tdd_workflow.json` | TDD methodology configuration | Red-Green-Refactor phases |
| `.claude/permanent_code_quality_enforcement.json` | Permanent quality gates | Session persistence, zero-tolerance |

### Hook Scripts

| Script | Purpose | Enforcement Type |
|--------|---------|-----------------|
| `.hooks/red-green-refactor-enforcer.py` | TDD methodology enforcement | Development workflow |
| `.hooks/alembic-enforcer.py` | Database migration validation | Database integrity |
| `.hooks/test-cleanup-enforcer.py` | Test artifact management | Clean development |
| `.hooks/tmp-file-enforcer.py` | Hardcoded temp file prevention | Security & portability |
| `.hooks/token-optimizer.py` | Token usage optimization | AI efficiency |

## 🚀 Getting Started with Enforcement

### Initial Setup
```bash
# Clone repository
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite

# Install development environment
uv sync --dev

# Install pre-commit hooks
pre-commit install

# Initialize Claude Code environment
python .claude/autorun.py
```

### Verification Commands
```bash
# Run all quality checks
pre-commit run --all-files

# Check semantic scoping
python .hooks/semantic-scope-validator.py --help

# Run token optimization analysis
python .hooks/token-optimizer.py --analyze

# Verify database migrations
python .hooks/alembic-enforcer.py --check

# Clean test artifacts
python .hooks/test-cleanup-enforcer.py --cleanup
```

### Quality Status Monitoring
```bash
# Check overall quality status
git status  # Shows enforcement status

# Verify enforcement configuration
python .claude/hooks/session_initialization.py

# Check agent registry
cat .claude/agent_registry.json | jq '.claude-code.monorepo_packages'
```

## 📊 Enforcement Metrics

### Quality Metrics Tracked
- **Code Quality**: Ruff compliance score
- **Test Coverage**: Percentage coverage across all packages
- **Security**: Vulnerability count and severity
- **Token Efficiency**: AI token usage optimization
- **Migration Status**: Database migration consistency
- **Documentation**: Documentation completeness and accuracy

### Reporting
- **Real-time Feedback**: Immediate enforcement feedback during development
- **Commit-time Validation**: Comprehensive checks before commits
- **Session Reports**: Quality metrics provided at session end
- **Historical Tracking**: Quality trends over time

## 🔧 Customization and Extension

### Adding New Enforcement Rules
1. Update relevant configuration files in `.claude/`
2. Create or modify hook scripts in `.hooks/`
3. Update pre-commit configuration
4. Test enforcement rules with `pre-commit run --all-files`
5. Update documentation

### Package-Specific Configuration
- **Root Configuration**: Applies to `lib_package` and `cli_package`
- **Web Package**: Independent configuration in `web_package/.claude/`
- **Semantic Scoping**: Universal across all packages
- **Quality Gates**: Consistent enforcement standards

### Integration with External Tools
- **IDE Integration**: Quality enforcement available in IDEs
- **CI/CD Integration**: Automated quality checks in pipelines
- **GitHub Integration**: Quality status in pull requests
- **Monitoring Integration**: Quality metrics in dashboards

---

This comprehensive enforcement system ensures that ToDoWrite maintains high code quality, security standards, and development best practices while providing a smooth and educational development experience.