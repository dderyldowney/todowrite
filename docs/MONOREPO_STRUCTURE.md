# ToDoWrite Monorepo Structure

This document describes the complete structure of the ToDoWrite monorepo, including all packages, their purposes, and their relationships.

## 📁 Repository Overview

ToDoWrite is a hierarchical task management system organized as a monorepo with three main packages:

```
todowrite/
├── lib_package/          # Core library (todowrite)
├── cli_package/          # Command-line interface (todowrite-cli)
├── web_package/          # Web application (todowrite-web)
├── tests/                # Shared test suite
├── docs/                 # Project documentation
├── .claude/              # Claude Code development environment
├── .hooks/               # Quality enforcement hooks
└── [config files]        # Project configuration
```

## 📦 Package Details

### 1. lib_package/ - Core Library
**Package Name**: `todowrite`
**Package Type**: `library`
**Published**: ✅ Yes (PyPI & TestPyPI)
**Version Locked**: With `cli_package`

#### Purpose
The core library providing hierarchical task management functionality with database persistence.

#### Key Features
- 12-layer hierarchical architecture (Goal → Concept → Task → Command)
- Database persistence (SQLite & PostgreSQL)
- Schema validation with JSON Schema
- Import/Export capabilities (JSON & YAML)
- Type safety with Python 3.12+

#### Structure
```
lib_package/
├── src/todowrite/
│   ├── __init__.py           # Public API
│   ├── core/
│   │   ├── app.py           # Main ToDoWrite class
│   │   ├── types.py         # Type definitions
│   │   └── [models/]        # Data models
│   ├── storage/             # Storage backends
│   └── utils/               # Utilities
├── pyproject.toml          # Package configuration
└── README.md               # Package documentation
```

#### Publication
- **PyPI**: https://pypi.org/project/todowrite/
- **TestPyPI**: https://test.pypi.org/project/todowrite/
- **Version**: Synchronized with `todowrite-cli`

---

### 2. cli_package/ - Command-Line Interface
**Package Name**: `todowrite-cli`
**Package Type**: `cli`
**Published**: ✅ Yes (PyPI & TestPyPI)
**Version Locked**: With `lib_package`

#### Purpose
Command-line interface providing full access to ToDoWrite functionality from the terminal.

#### Key Features
- Complete CRUD operations for hierarchical tasks
- Interactive mode with Rich UI
- Batch operations and scripting support
- Configuration management
- Database migration tools

#### Structure
```
cli_package/
├── src/todowrite_cli/
│   ├── __init__.py          # Public API
│   ├── main.py             # CLI entry point
│   ├── commands/           # CLI command implementations
│   ├── config/             # Configuration management
│   └── utils/              # CLI utilities
├── pyproject.toml         # Package configuration
└── README.md              # Package documentation
```

#### Publication
- **PyPI**: https://pypi.org/project/todowrite-cli/
- **TestPyPI**: https://test.pypi.org/project/todowrite-cli/
- **Version**: Synchronized with `todowrite`

---

### 3. web_package/ - Web Application
**Package Name**: `todowrite-web`
**Package Type**: `webapp`
**Published**: ❌ Not yet (in development)
**Versioning**: Independent

#### Purpose
FastAPI-based web application providing a modern interface for ToDoWrite functionality.

#### Key Features
- RESTful API endpoints
- Real-time task updates
- Web-based task management interface
- Database integration
- Authentication and authorization (planned)

#### Architecture
- **Backend**: FastAPI
- **Frontend**: React (planned)
- **Database**: PostgreSQL/SQLite
- **API**: REST with WebSocket support

#### Structure
```
web_package/
├── src/todowrite_web/
│   ├── __init__.py          # Package initialization
│   ├── api/
│   │   ├── backend/
│   │   │   ├── main.py      # FastAPI application
│   │   │   ├── models.py    # Pydantic models
│   │   │   ├── v1/          # API v1 endpoints
│   │   │   └── middleware/  # Custom middleware
│   │   └── frontend/        # Frontend code (planned)
│   ├── database/            # Database models and migrations
│   └── static/              # Static assets
├── pyproject.toml          # Package configuration
├── .claude/                 # Independent development environment
└── README.md               # Package documentation
```

#### Development Status
- **Backend API**: Basic structure implemented
- **Database Models**: Defined and ready for implementation
- **Frontend**: Planned (React-based)
- **Publication**: Will be published when baseline implementation is complete

---

## 🔗 Package Relationships

### Version Locking
- `lib_package` (todowrite) ↔ `cli_package` (todowrite-cli)
- Always published together with the same version number
- API compatibility guaranteed between locked packages

### Dependencies
```
cli_package (todowrite-cli)
    depends on → lib_package (todowrite)

web_package (todowrite-web)
    depends on → lib_package (todowrite)
```

### Configuration Hierarchy
```
.claude/                           # Root configuration (applies to all)
├── agent_registry.json           # Monorepo package definitions
├── semantic_scoping_*.json       # Universal semantic scoping
└── [30+ enforcement files]       # Quality enforcement system

web_package/src/todowrite_web/.claude/  # Independent web environment
└── agent_registry.json               # Web-specific configuration
```

---

## 🏗️ Development Workflow

### Semantic Scoping
All packages use unified semantic scoping with the following scopes:
- `lib`: Core library functionality
- `cli`: Command-line interface
- `web`: Web application
- `tests`: Test suite and infrastructure
- `docs`: Documentation
- `build`: Build system and packaging
- `config`: Configuration files
- `ci`: Continuous integration
- `deps`: Dependencies

### Quality Enforcement
Comprehensive quality enforcement system including:
- Semantic scoping validation
- Conventional commits enforcement
- Code formatting (Ruff)
- Security analysis (Bandit)
- Secret detection (detect-secrets)
- Database migration validation (Alembic)
- Test artifact cleanup
- Token usage optimization

### Claude Code Integration
- Root `.claude/` configuration governs `lib_package` and `cli_package`
- `web_package` has independent Claude configuration for autonomous development
- Semantic scoping awareness enabled across all packages
- Permanent enforcement survives session resets

---

## 📋 File Organization

### Configuration Files
```
.todowrite/
├── VERSION              # Shared version file
├── development_todowrite.db  # Development database
└── [config files]

.pyproject.toml         # Meta-package configuration
.uv.lock               # Dependency lock file
.pre-commit-config.yaml  # Pre-commit hooks
.alembic.ini           # Database migration configuration
.sqlfluff-config       # SQL linting configuration
.secrets.baseline      # Secret detection baseline
```

### Development Infrastructure
```
.claude/                           # Claude Code development environment
├── agent_registry.json           # Agent configuration + monorepo packages
├── semantic_scoping_*.json       # Semantic scoping configuration
├── comprehensive_quality_*.json  # Quality enforcement
├── conventional_commits_*.json   # Commit message enforcement
├── tdd_workflow.json             # Test-driven development
├── skills_testing_*.json         # Skills testing workflow
├── workflow_enforcement.json     # Development workflow enforcement
├── autorun.py                    # Automatic setup script
├── hooks/                        # Claude hooks
└── [30+ enforcement files]       # Various quality enforcement configs

.hooks/                           # Quality enforcement hooks
├── red-green-refactor-enforcer.py    # TDD methodology enforcement
├── alembic-enforcer.py               # Database migration enforcement
├── test-cleanup-enforcer.py          # Test artifact cleanup
├── tmp-file-enforcer.py              # Hardcoded tmp file prevention
├── token-optimizer.py                # Token usage optimization
└── [additional hooks]                # Various enforcement hooks

alembic/                         # Database migrations
├── versions/                     # Migration files
├── env.py                       # Alembic environment
└── script.py.mako              # Migration template
```

### Testing
```
tests/                           # Shared test suite
├── lib/                         # Library tests
├── cli/                         # CLI tests
├── web/                         # Web tests
├── integration/                 # Integration tests
├── conftest.py                  # pytest configuration
└── [test utilities]             # Test helpers
```

---

## 🚀 Getting Started

### Development Setup
1. Clone the repository
2. Install dependencies: `uv sync`
3. Install pre-commit hooks: `pre-commit install`
4. Initialize development environment: `python .claude/autorun.py`

### Package Development
- **Library**: Work in `lib_package/`
- **CLI**: Work in `cli_package/`
- **Web**: Work in `web_package/` (independent environment)

### Building and Publishing
- **Individual packages**: `uv build` in package directory
- **All packages**: `uv build` in root (builds all packages)
- **Publishing**: Use `uv publish` for individual packages

---

## 📝 Version Management

### Shared Version File
All packages read from the shared `VERSION` file in the project root.

### Version Locking
- `lib_package` and `cli_package` always have the same version
- `web_package` has independent versioning
- Version updates are synchronized across locked packages

### Release Process
1. Update `VERSION` file
2. Update changelogs
3. Build all packages
4. Test thoroughly
5. Publish `lib_package` and `cli_package` together
6. `web_package` published independently when ready

---

## 🔧 Maintenance

### Adding New Packages
1. Create package directory
2. Add package definition to `.claude/agent_registry.json`
3. Configure semantic scoping patterns
4. Add to build system configuration
5. Update this documentation

### Updating Configuration
- Root configuration affects all packages
- Package-specific configuration only for `web_package`
- Semantic scoping patterns defined in root configuration
- Quality enforcement rules applied universally

### Quality Assurance
- All changes go through comprehensive quality gates
- Semantic scoping required for all commits
- Tests must pass for all packages
- Security scans and secret detection enforced
- Code formatting and linting applied automatically