# ToDoWrite: Hierarchical Task Management System

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Version 0.4.1](https://img.shields.io/badge/version-0.4.1-green.svg)](https://github.com/dderyldowney/todowrite)
[![PyPI](https://img.shields.io/badge/todowrite-0.4.1-blue.svg)](https://pypi.org/project/todowrite/)
[![PyPI CLI](https://img.shields.io/badge/todowrite--cli-0.4.1-blue.svg)](https://pypi.org/project/todowrite-cli/)
[![Tests Passing](https://img.shields.io/badge/tests-157%20passing-brightgreen.svg)](https://github.com/dderyldowney/todowrite)
[![Real Implementations](https://img.shields.io/badge/tests-real%20implementations-blue.svg)](https://github.com/dderyldowney/todowrite)

**ToDoWrite** is a hierarchical task management system designed for project planning and execution. It provides both CLI capabilities and Python module integration for developers and project managers who need structured task management with SQLAlchemy-based models, database persistence, and schema validation.

## 🚀 Installation

### Using uv (Recommended)

Install both the core library and CLI interface using uv:

```bash
# Install core library
uv add todowrite

# Install CLI interface (requires todowrite library)
uv add todowrite-cli

# For PostgreSQL support
uv add 'todowrite[postgres]'
uv add 'todowrite-cli[postgres]'

# Quick install (all-in-one)
uv add todowrite todowrite-cli
```

### Using pip

```bash
# Install core library
pip install todowrite

# Install CLI interface (requires todowrite library)
pip install todowrite-cli

# For PostgreSQL support
pip install 'todowrite[postgres]'
pip install 'todowrite-cli[postgres]'

# Quick install (all-in-one)
pip install todowrite todowrite-cli
```

### From GitHub (Development Version)

For the latest development version:

```bash
pip install git+https://github.com/dderyldowney/todowrite.git@main
pip install git+https://github.com/dderyldowney/todowrite.git@main#subdirectory=cli_package
```

### For Development

If you want to contribute or modify the code:

```bash
# Clone the repository
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite

# Install development environment using uv (recommended)
uv sync --dev

# Or install development environment using pip
pip install -e "./lib_package[dev]"
pip install -e "./cli_package[dev]"
pip install -e "./web_package[dev]"

# Run setup script (handles both uv and pip)
./setup_dev.sh
```

### Requirements

- **Python**: 3.12 or higher
- **Operating System**: Windows, macOS, or Linux
- **Dependencies**: SQLAlchemy 2.0+, JSONSchema 4.0+, PyYAML 6.0+

## 🎯 Overview

ToDoWrite transforms complex project planning into a structured, hierarchical framework that ensures nothing falls through the cracks. Whether you're managing software development projects, or any complex multi-stage initiative, ToDoWrite provides the structure and tools to break down goals into actionable commands.

### Key Features

- **12-Layer Hierarchical Framework**: Goals → Concepts → Contexts → Constraints → Requirements → AcceptanceCriteria → InterfaceContracts → Phases → Steps → Tasks → SubTasks → Commands
- **SQLAlchemy-based Models**: Modern ORM with database relationships and associations
- **CLI and Python API**: Command-line interface and programmatic access
- **Database Storage**: SQLite and PostgreSQL support with auto-generated integer primary keys
- **Schema Validation**: JSON Schema validation ensures data integrity
- **Progress Tracking**: Track task completion with progress percentages
- **Model Relationships**: Many-to-many associations through proper join tables
- **Import/Export**: JSON and YAML import/export functionality
- **Type Safety**: Comprehensive type hints with Python 3.12+ syntax
- **Status Management**: Track models through planned, in_progress, completed states
- **Real Testing**: 157 tests using actual implementations (no mocks)

## 🚀 Quick Start

### CLI Usage

```bash
# Initialize a project (creates todowrite.db in current directory)
todowrite init

# Create a goal
todowrite create --layer goal --title "Implement User Authentication" --description "Create secure user authentication system" --owner "dev-team"

# Create additional layers
todowrite create --layer concept --title "OAuth2 Authentication Strategy" --description "Use OAuth2 for user login flow"
todowrite create --layer requirement --title "User Registration Form" --description "Form for new user registration" --owner "ui-team"
todowrite create --layer acceptancecriteria --title "Valid Email Required" --description "Users must register with valid email"
todowrite create --layer phase --title "Authentication Backend" --description "Implement core authentication logic"
todowrite create --layer task --title "Design Database Schema" --description "Design user database schema" --owner "dev-team"
todowrite create --layer command --title "Run Database Migration" --description "Execute user table migration script"

# View all items
todowrite list

# Search for items
todowrite search "authentication"

# Export to YAML
todowrite export-yaml

# List items by layer
todowrite list --layer goal
todowrite list --layer task
todowrite list --layer command

# View project statistics
todowrite stats

# Show relationships between items
todowrite relationships --layer goal --id 1
```

### Python API Usage

```python
from todowrite import create_engine, sessionmaker
from todowrite.core.models import Goal, Task, Requirement, AcceptanceCriteria, Command

# Initialize database connection
engine = create_engine("sqlite:///myproject.db")
Session = sessionmaker(bind=engine)
session = Session()

# Create models using ToDoWrite Models API
goal = Goal(
    title="Implement User Authentication",
    description="Create secure user authentication system",
    owner="dev-team",
    severity="high"
)
session.add(goal)
session.commit()

# Create additional models
concept = Concept(
    title="OAuth2 Authentication Strategy",
    description="Use OAuth2 for user login flow",
    owner="dev-team"
)
session.add(concept)

requirement = Requirement(
    title="User Registration Form",
    description="Form for new user registration",
    owner="ui-team",
    severity="medium"
)
session.add(requirement)

acceptance_criteria = AcceptanceCriteria(
    title="Valid Email Required",
    description="Users must register with valid email",
    owner="qa-team"
)
session.add(acceptance_criteria)

task = Task(
    title="Design Database Schema",
    description="Design user database schema",
    owner="dev-team",
    severity="medium"
)
session.add(task)

command = Command(
    title="Email Format Validation Test",
    description="Test email validation logic",
    owner="dev-team",
    run_command="uv run pytest tests/test_email_validation.py",
    artifacts=["test_report.html"]
)
session.add(command)

# Create relationships using many-to-many associations
goal.concepts.append(concept)
goal.requirements.append(requirement)
requirement.acceptance_criteria.append(acceptance_criteria)
acceptance_criteria.tasks.append(task)
task.commands.append(command)

session.commit()

# Query project overview
goals = session.query(Goal).all()
tasks = session.query(Task).all()
requirements = session.query(Requirement).all()

print(f"Project has {len(goals)} goals, {len(requirements)} requirements, {len(tasks)} tasks")

# Example: Get all tasks for a specific goal
for goal in goals:
    print(f"Goal: {goal.title}")
    for requirement in goal.requirements:
        print(f"  Requirement: {requirement.title}")
        for task in requirement.tasks:
            print(f"    Task: {task.title} (Status: {task.status})")
```

## 🏗️ **12-Layer Hierarchy**

ToDoWrite uses a comprehensive 12-layer framework that breaks down complex goals into actionable commands:

### **Strategic Planning Layers**
1. **🎯 Goals** - High-level project objectives and deliverables
2. **💡 Concepts** - Abstract ideas and design principles
3. **🌍 Contexts** - Environmental factors and external constraints
4. **⚠️ Constraints** - Technical, business, or regulatory limitations

### **Implementation Planning Layers**
5. **📋 Requirements** - Functional and non-functional specifications
6. **✅ AcceptanceCriteria** - Success conditions and validation criteria
7. **🤝 InterfaceContracts** - API contracts and integration points
8. **📅 Phases** - Project phases and milestone planning

### **Execution Layers**
9. **🔢 Steps** - Sequential work items within phases
10. **📝 Tasks** - Individual work assignments
11. **🔧 SubTasks** - Detailed breakdown of complex tasks
12. **⚡ Commands** - Executable instructions and automated actions

### **Layer Relationships**
- **Top-Down Flow**: Goals → Concepts → Contexts → Constraints → Requirements → AcceptanceCriteria → InterfaceContracts → Phases → Steps → Tasks → SubTasks → Commands
- **Bottom-Up Execution**: Commands implement SubTasks, which complete Tasks, which fulfill Steps, which complete Phases, which meet AcceptanceCriteria, which satisfy Requirements
- **Cross-Linking**: Any layer can link to any other layer for complex relationships

### **ID Pattern System**
Each layer uses a specific ID prefix for easy identification:
- `GOAL-*` - Goals
- `CON-*` - Concepts
- `CTX-*` - Contexts
- `CST-*` - Constraints
- `R-*` - Requirements
- `AC-*` - AcceptanceCriteria
- `IF-*` - InterfaceContracts
- `PH-*` - Phases
- `STP-*` - Steps
- `TSK-*` - Tasks
- `SUB-*` - SubTasks
- `CMD-*` - Commands

## 📚 Documentation

### 🌐 Documentation Hub
- **[Documentation Hub](docs/README.md)**: Complete documentation index and navigation

### 📖 Generated Documentation (Sphinx)
- **🔗 Live Documentation**: [https://todowrite.davidderyldowney.com](https://todowrite.davidderyldowney.com)
- **📚 Library API Reference**: Complete API documentation for all classes and methods
- **🔧 Build locally**: `./dev_tools/build.sh docs`

### 🔧 Shared Resources
- **[Development Guide](docs/shared/development/README.md)**: Complete development workflow and standards
- **[Build System](docs/shared/development/BUILD_SYSTEM.md)**: Build tools and automation
- **[Contributing](docs/shared/contributing/README.md)**: Contribution guidelines and workflow
- **[Release Process](docs/shared/release/README.md)**: Release management and deployment procedures

### 📚 Package Documentation
- **[Library Documentation](docs/library/README.md)**: Core todowrite library documentation
- **[CLI Reference](docs/cli/README.md)**: Complete CLI command reference and examples
- **[Web Documentation](docs/web/README.md)**: Web application documentation (planning stage)

### 🏗️ Project Architecture
- **[ToDoWrite Models](docs/ToDoWrite.md)**: Complete architectural overview and SQLAlchemy-based models
- **[Monorepo Structure](docs/MONOREPO_STRUCTURE.md)**: Detailed monorepo architecture and package relationships

### Quality Enforcement
- **🔧 Semantic Scoping**: Automatic scope detection for conventional commits
- **🚦 Conventional Commits**: Enforced commit message format
- **🧪 Test-Driven Development**: Red-Green-Refactor methodology enforcement
- **🔍 Security Analysis**: Automated vulnerability scanning
- **📊 Code Quality**: Comprehensive linting, formatting, and type checking
- **🔒 Secret Detection**: Prevents accidental credential commits
- **🗃️ Database Migration**: Automated migration validation
- **⚡ Token Optimization**: AI model efficiency optimization

## 🚀 Quick Release (For Maintainers)

**To cut a new release, simply run:**

```bash
# Cut a specific release (e.g., 0.4.2)
./scripts/release.sh 0.4.2

# Cut a patch release automatically
./scripts/release.sh patch

# Preview what would happen
./scripts/release.sh patch --dry-run
```

The automated script handles the entire process from version bump to PyPI publishing. Just say "cut a 0.4.2 release" and any agent will know what to run!

## 🤝 Contributing

We welcome contributions to ToDoWrite! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## 🔧 Code Quality & Security

### Quality Assurance Status ✅
- **Zero Tech Debt**: All code quality checks pass
- **Code Quality**: ruff handles all formatting, linting, import sorting, security checks, and type checking
- **Test Coverage**: 157/157 tests passing with comprehensive pytest suite (54.25% coverage)
- **Real Implementation Testing**: All tests use actual implementations, no mocks
- **Pre-commit**: Automated ruff quality gates for all commits

### Recent Improvements
- ✅ **Progress Field Fix**: Resolved storage/retrieval issue for model progress tracking
- ✅ **Library Verification Complete**: Comprehensive verification of all library components
- ✅ **Real Implementation Testing**: Verified all tests use actual implementations, no mocks
- ✅ **Database Integrity Confirmed**: SQLite/PostgreSQL backends thoroughly tested
- ✅ **Schema Validation Robust**: All 12 layer types and 5 status types validated
- ✅ **Performance Verified**: Handles 100+ models efficiently
- ✅ **Static Analysis Compliant**: MyPy and Ruff validation passing
- ✅ **Installation Verified**: Package installs and imports correctly
- ✅ **Centralized Version Management**: Single source of truth for both packages
- ✅ **Modern Build System**: Hatchling + Twine with comprehensive tooling
- ✅ **Monorepo Structure**: Proper Python packaging standards
- ✅ **Asyncio Support**: Updated pytest configuration for modern async patterns
- ✅ **Security Hardening**: All subprocess calls use shell=False with proper validation

### Development Standards
- ✅ **Python 3.12+**: Modern syntax with type union operators (`str | None`)
- ✅ **PEP 517/518**: Compliant build system with hatchling backend
- ✅ **Static Analysis**: ruff handles all code quality: formatting, linting, import sorting, security, and type checking
- ✅ **Security**: Subprocess calls secured, proper exception handling throughout

## 🛠️ Development

### Build System

We use **Hatchling** as our build backend with **Twine** for publishing:

```bash
# Build packages
./scripts/build.sh

# Publish to TestPyPI
./scripts/publish.sh

# Publish to PyPI
./scripts/publish.sh prod

# Clean and build
./scripts/build.sh clean
```

See [BUILD_SYSTEM.md](BUILD_SYSTEM.md) for detailed documentation.

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite

# Run development setup script
./setup_dev.sh

# Install development dependencies manually
pip install -e "./lib_package[dev]"
pip install -e "./cli_package[dev]"
```

### Version Management

Version is centrally managed using the `VERSION` file:

```bash
# Get current version
python scripts/bump_version.py --verify-only

# Bump patch version
python scripts/bump_version.py patch

# Set explicit version
python scripts/bump_version.py 0.4.1
```

See [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md) for complete details.

---

**Current Version**: See VERSION file or README badges
**Python**: 3.12+
**Database**: SQLite (development) / PostgreSQL (production)
**Architecture**: Hierarchical task management with 12-layer planning framework
**Build System**: Hatchling + Twine
**Quality Status**: Zero Tech Debt Achieved 🎉
**Test Status**: All tests passing, real implementations verified ✅
**License**: MIT

### Package Information

- **[todowrite](https://pypi.org/project/todowrite/)**: Core Python library
- **[todowrite-cli](https://pypi.org/project/todowrite-cli/)**: Command-line interface
- **[GitHub Repository](https://github.com/dderyldowney/todowrite)**: Source code and development
