# ToDoWrite: Hierarchical Task Management System

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Version 0.5.0](https://img.shields.io/badge/version-0.5.0-green.svg)](https://github.com/dderyldowney/todowrite)
[![PyPI](https://img.shields.io/badge/todowrite-0.5.0-blue.svg)](https://pypi.org/project/todowrite/)
[![PyPI CLI](https://img.shields.io/badge/todowrite--cli-0.5.0-blue.svg)](https://pypi.org/project/todowrite-cli/)
[![Tests Passing](https://img.shields.io/badge/tests-157%20passing-brightgreen.svg)](https://github.com/dderyldowney/todowrite)
[![Real Implementations](https://img.shields.io/badge/tests-real%20implementations-blue.svg)](https://github.com/dderyldowney/todowrite)
[![Web App Ready](https://img.shields.io/badge/web%20app-react%20%2B%20fastapi-blue.svg)](https://github.com/dderyldowney/todowrite)

**ToDoWrite** is a hierarchical task management system designed for project planning and execution. It provides both CLI capabilities, Python module integration, and a modern web application for developers and project managers who need structured task management with SQLAlchemy-based models, database persistence, and schema validation.

## 🌐 Web Application (NEW!)

ToDoWrite now includes a modern web application that provides an online calendar-like interface for task management. Perfect for users who prefer web-based tools over command-line interfaces!

### Web App Features
- **📅 Calendar View**: Monthly calendar interface for visual task management
- **📊 Dashboard**: Overview with statistics and recent activity
- **✅ Task Management**: Comprehensive task listing with filtering and search
- **🎯 Goal Tracking**: High-level goal visualization with progress tracking
- **🔄 Real-time Sync**: Web app and CLI share the same PostgreSQL database
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

### Quick Start Web App

```bash
# Set up PostgreSQL (required for web app)
source .claude/postgresql_env.sh

# Start the FastAPI backend
cd web_package
uv run uvicorn src.todowrite_web.main:app --reload --port 8000

# In another terminal, start the React frontend
cd web_package/frontend
npm install
npm run dev

# Access your web application at:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
```

### Web App Requirements
- **PostgreSQL**: Required (web app uses production-grade database)
- **Node.js 18+**: For the React frontend
- **Python 3.12+**: For the FastAPI backend
- **Modern Browser**: Chrome, Firefox, Safari, or Edge

The web application provides the same powerful hierarchical task management as the CLI, but with a user-friendly interface that feels like an online calendar for your tasks and goals!

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

- **🌐 Modern Web Application**: React + FastAPI web app with calendar-like task interface
- **📅 Calendar View**: Visual task management like an online calendar
- **📊 Dashboard**: Real-time statistics and activity overview
- **12-Layer Hierarchical Framework**: Goals → Concepts → Contexts → Constraints → Requirements → AcceptanceCriteria → InterfaceContracts → Phases → Steps → Tasks → SubTasks → Commands
- **SQLAlchemy-based Models**: Modern ORM with database relationships and associations
- **CLI and Python API**: Command-line interface and programmatic access
- **Database Storage**: SQLite and PostgreSQL support with auto-generated integer primary keys
- **🔄 Real-time Sync**: Web app and CLI share the same database instantly
- **PostgreSQL-Ready**: Production-grade database with connection pooling
- **Schema Validation**: JSON Schema validation ensures data integrity
- **Progress Tracking**: Track task completion with progress percentages
- **Model Relationships**: Many-to-many associations through proper join tables
- **Import/Export**: JSON and YAML import/export functionality
- **Type Safety**: Comprehensive type hints with Python 3.12+ syntax
- **Status Management**: Track models through planned, in_progress, completed states
- **Real Testing**: 157 tests using actual implementations (no mocks)
- **📱 Responsive Design**: Works on desktop, tablet, and mobile devices

## 🚀 Quick Start

### CLI Usage

```bash
# Initialize a project (creates todowrite.db in current directory)
todowrite init

# Create items using the new CLI
todowrite create --layer goal --title "Implement User Authentication" --description "Create secure user authentication system" --owner "dev-team"
todowrite create --layer concept --title "OAuth2 Authentication Strategy" --description "Use OAuth2 for user login flow" --owner "dev-team"
todowrite create --layer requirement --title "User Registration Form" --description "Form for new user registration" --owner "ui-team"
todowrite create --layer acceptancecriteria --title "Valid Email Required" --description "Users must register with valid email" --owner "qa-team"
todowrite create --layer task --title "Design Database Schema" --description "Design user database schema" --owner "dev-team" --progress 25
todowrite create --layer command --title "Run Database Migration" --description "Execute user table migration script" --run-command "python manage.py migrate" --owner "dev-team"

# View all items
todowrite list

# List items by layer type
todowrite list --layer goal
todowrite list --layer task
todowrite list --layer command

# Filter by owner or status
todowrite list --owner "dev-team"
todowrite list --status "in_progress"

# Get details of a specific item (by integer ID)
todowrite get 1

# Search for items
todowrite search "authentication"
todowrite search "database" --layer task

# View database statistics
todowrite stats

# Use custom database file
todowrite --database myproject.db init
todowrite --database myproject.db list
```

### Available CLI Commands

**Core Commands:**
- `todowrite init` - Initialize the database
- `todowrite create --layer <type> --title <text>` - Create new item
- `todowrite list [--layer <type>] [--owner <name>] [--status <status>]` - List items
- `todowrite get <id>` - Get details of specific item
- `todowrite search <query> [--layer <type>]` - Search items
- `todowrite stats` - Show database statistics

**Layer Types:**
- `goal`, `concept`, `context`, `constraints`
- `requirement`, `acceptancecriteria` (or `ac`), `interfacecontract`
- `phase`, `step`, `task`, `subtask`, `command`, `label`

**Examples:**
```bash
# Create different layer types
todowrite create --layer goal --title "Launch Product" --owner "product-team"
todowrite create --layer task --title "Fix login bug" --owner "dev-team" --status "in_progress"
todowrite create --layer command --title "Run tests" --run-command "pytest" --owner "qa-team"

# Query and filter
todowrite list --layer task --owner "dev-team"
todowrite list --status "completed"
todowrite search "security" --layer requirement

# Get details
todowrite get 1  # Show item with ID 1
todowrite get --database myproject.db 5  # Item 5 from custom database
```

### Python API Usage

```python
from todowrite.core.models import Goal, Task, Requirement, AcceptanceCriteria, Command
from todowrite.core.schema_validator import initialize_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Initialize database
database_url = "sqlite:///myproject.db"
initialize_database(database_url)

# Create database session
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

# Create models using ToDoWrite Models API
goal = Goal(
    title="Implement User Authentication",
    description="Create secure user authentication system",
    owner="dev-team",
    severity="high",
    status="planned"
)
session.add(goal)
session.commit()  # Get the ID

# Create additional models
requirement = Requirement(
    title="User Registration Form",
    description="Form for new user registration",
    owner="ui-team",
    severity="medium",
    status="planned"
)
session.add(requirement)

task = Task(
    title="Design Database Schema",
    description="Design user database schema",
    owner="dev-team",
    severity="medium",
    status="planned",
    progress=0
)
session.add(task)

command = Command(
    title="Run Database Migration",
    description="Execute user table migration script",
    owner="dev-team",
    run_command="python manage.py migrate",
    status="planned"
)
session.add(command)

# Link models through many-to-many associations (if needed)
goal.requirements.append(requirement)
requirement.tasks.append(task)
task.commands.append(command)

session.commit()

# Query examples
goals = session.query(Goal).all()
tasks = session.query(Task).filter_by(owner="dev-team").all()
in_progress_tasks = session.query(Task).filter_by(status="in_progress").all()

print(f"Project has {len(goals)} goals")
print(f"Dev team has {len(tasks)} tasks")
print(f"{len(in_progress_tasks)} tasks in progress")

# Get specific item by ID
goal_id = goal.id  # Auto-generated integer ID
retrieved_goal = session.query(Goal).filter_by(id=goal_id).first()
print(f"Retrieved goal: {retrieved_goal.title}")

# Update item
task.status = "in_progress"
task.progress = 75
session.commit()
```

## 🏗️ **12-Layer Hierarchy**

ToDoWrite uses a comprehensive 12-layer framework that systematically breaks down complex goals into actionable commands. This hierarchical approach ensures nothing falls through the cracks while maintaining complete traceability from high-level objectives to executable actions.

### **Strategic Planning Layers (High-Level Vision)**

#### **1. 🎯 Goals** - Strategic Objectives
**Purpose**: High-level project objectives and deliverables that define project success.
- **What they are**: The ultimate outcomes you want to achieve
- **Characteristics**: Broad, measurable, time-bound, and inspiring
- **Example**: "Launch Q1 Product with complete user authentication system"
- **Typical Count**: 2-5 goals per major project

#### **2. 💡 Concepts** - Design Principles
**Purpose**: Abstract ideas and design philosophies that guide the project direction.
- **What they are**: Core design principles and architectural concepts
- **Characteristics**: High-level, abstract, influence multiple decisions
- **Example**: "Mobile-first responsive design approach" or "Microservices-based architecture"
- **Typical Count**: 3-7 concepts per goal

#### **3. 🌍 Contexts** - Environmental Factors
**Purpose**: Environmental factors, market conditions, and external influences that affect the project.
- **What they are**: External factors that impact project decisions
- **Characteristics**: External constraints, market trends, user expectations
- **Example**: "Target users primarily use mobile devices" or "Compliance with GDPR regulations"
- **Typical Count**: 2-6 contexts per goal

#### **4. ⚠️ Constraints** - Limitations and Boundaries
**Purpose**: Technical, business, or regulatory limitations that the project must operate within.
- **What they are**: Specific limitations that cannot be violated
- **Characteristics**: Concrete, measurable, non-negotiable boundaries
- **Example**: "Must use existing PostgreSQL infrastructure" or "Budget limited to $50,000"
- **Typical Count**: 2-5 constraints per goal

### **Implementation Planning Layers (Detailed Planning)**

#### **5. 📋 Requirements** - Functional Specifications
**Purpose**: Functional and non-functional specifications that must be satisfied.
- **What they are**: Specific functional and technical requirements
- **Characteristics**: Measurable, testable, specific conditions
- **Example**: "User registration form must validate email format" or "System must support 100 concurrent users"
- **Typical Count**: 5-15 requirements per goal

#### **6. ✅ AcceptanceCriteria** - Success Conditions
**Purpose**: Success conditions and validation criteria that prove requirements are met.
- **What they are**: Testable criteria that validate requirement completion
- **Characteristics**: Binary (pass/fail), testable, measurable
- **Example**: "Registration form rejects invalid email formats" or "Login page responds within 2 seconds"
- **Typical Count**: 3-10 acceptance criteria per requirement

#### **7. 🤝 InterfaceContracts** - Integration Points
**Purpose**: API contracts, service interfaces, and integration points between system components.
- **What they are**: Defined interfaces and contracts between systems or components
- **Characteristics**: Technically specific, versioned, documented
- **Example**: "REST API endpoints for user management" or "Database schema version 1.2"
- **Typical Count**: 2-8 interface contracts per requirement

#### **8. 📅 Phases** - Project Phases
**Purpose**: Project phases, milestone planning, and high-level scheduling.
- **What they are**: Time-based phases or sprints that organize work execution
- **Characteristics**: Time-bound, milestone-focused, sequential or parallel
- **Example**: "Phase 1: Backend Development (Weeks 1-4)" or "Sprint 2: Frontend Implementation"
- **Typical Count**: 3-8 phases per goal

### **Execution Layers (Detailed Implementation)**

#### **9. 🔢 Steps** - Sequential Work Items
**Purpose**: Sequential work items within phases that represent logical progress units.
- **What they are**: Logical steps or milestones within a phase
- **Characteristics**: Sequential, logically ordered, measurable progress
- **Example**: "Design database schema" → "Implement authentication API" → "Create frontend login form"
- **Typical Count**: 3-15 steps per phase

#### **10. 📝 Tasks** - Individual Work Assignments
**Purpose**: Individual work assignments that can be assigned to team members.
- **What they are**: Specific work items that can be completed by individuals
- **Characteristics**: Assignable, completable, time-estimable
- **Example**: "Create user registration endpoint" or "Design responsive login form"
- **Typical Count**: 5-25 tasks per step

#### **11. 🔧 SubTasks** - Task Breakdown
**Purpose**: Detailed breakdown of complex tasks into smaller, manageable components.
- **What they are**: Subcomponents of complex tasks that need to be completed individually
- **Characteristics**: Detailed, sequential dependencies, completable
- **Example**: "Setup database connection" → "Create user model" → "Implement validation logic" → "Add error handling"
- **Typical Count**: 1-8 subtasks per task

#### **12. ⚡ Commands** - Executable Actions
**Purpose**: Executable instructions, automated actions, and specific technical operations.
**What they are**: Concrete commands or scripts that can be executed
- **Characteristics**: Executable, specific, automated or manual
- **Example**: "Run database migration" or "Execute pytest test suite" or "Deploy to staging server"
- **Typical Count**: 1-5 commands per subtask

### **Layer Relationships and Data Flow**

#### **Top-Down Strategic Flow**
```
Goals → Concepts → Contexts → Constraints → Requirements → AcceptanceCriteria → InterfaceContracts → Phases → Steps → Tasks → SubTasks → Commands
```
**How it works**: Start with high-level goals and progressively break them down into increasingly detailed components.

#### **Bottom-Up Execution Flow**
```
Commands implement SubTasks
↓
SubTasks complete Tasks
↓
Tasks fulfill Steps
↓
Steps complete Phases
↓
Phases meet AcceptanceCriteria
↓
AcceptanceCriteria satisfy Requirements
↓
Requirements support Goals
```
**How it works**: Execute commands to build up components, progressively completing higher-level objectives.

#### **Cross-Linking and Relationships**
- **Horizontal Links**: Items at the same level can be related (e.g., multiple tasks for one step)
- **Vertical Links**: Each layer can have parent-child relationships
- **Cross-Hierarchy**: Any layer can reference any other layer for complex relationships
- **Many-to-Many**: Multiple items can be associated through labels for flexible organization

### **Practical Example: User Authentication System**

```
🎯 Goal: "Implement Secure User Authentication"
├─ 💡 Concept: "OAuth2-based authentication"
├─ 🌍 Context: "Users expect social login options"
├─ ⚠️ Constraint: "Must use existing auth provider"
│
└─ 📋 Requirement: "User Registration System"
   ├─ ✅ AcceptanceCriteria: "Valid email required"
   ├─ ✅ AcceptanceCriteria: "Password strength enforced"
   │
   └─ 📅 Phase: "Sprint 1 - Backend Development"
      ├─ 🔢 Step: "Database Setup"
      │  ├─ 📝 Task: "Create user table schema"
      │  │  ├─ 🔧 SubTask: "Add email field"
      │  │  ├─ 🔧 SubTask: "Add password hash field"
      │  │  └─ ⚡ Command: "Run migration script"
      │
      └─ 🔢 Step: "Authentication API"
         ├─ 📝 Task: "Implement registration endpoint"
         └─ ⚡ Command: "Run integration tests"
```

### **ID Pattern System for Easy Identification**

Each layer uses a specific ID prefix for easy identification:

- `GOAL-*` - Goals (strategic objectives)
- `CON-*` - Concepts (design principles)
- `CTX-*` - Contexts (environmental factors)
- `CST-*` - Constraints (limitations)
- `R-*` - Requirements (functional specs)
- `AC-*` - AcceptanceCriteria (success conditions)
- `IF-*` - InterfaceContracts (integration points)
- `PH-*` - Phases (milestone planning)
- `STP-*` - Steps (sequential work)
- `TSK-*` - Tasks (individual assignments)
- `SUB-*` - SubTasks (task breakdown)
- `CMD-*` - Commands (executable actions)

### **Benefits of the 12-Layer System**

✅ **Complete Traceability**: Every action can be traced back to its strategic purpose
✅ **Risk Mitigation**: Early identification of constraints and contexts
✅ **Clear Progression**: Natural flow from abstract to concrete
✅ **Flexible Organization**: Cross-linking accommodates complex projects
✅ **Team Scalability**: Different layers can be worked on by different team members
✅ **Quality Assurance**: Acceptance criteria ensure requirements are actually met
✅ **Automated Execution**: Commands can be automated for continuous deployment

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

### Web Application Development

For users who want to extend or modify the web application:

```bash
# Set up PostgreSQL (required for web app)
source .claude/postgresql_env.sh

# Navigate to web package
cd web_package

# Backend development (FastAPI)
source $PWD/.venv/bin/activate
export PYTHONPATH="lib_package/src:cli_package/src"
uv sync --dev
uv run uvicorn src.todowrite_web.main:app --reload --host 127.0.0.1 --port 8000

# Frontend development (React) - in another terminal
cd web_package/frontend
npm install
npm run dev  # Starts at http://localhost:3000

# Access your web application:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

The web application provides a modern, calendar-like interface for task management that seamlessly syncs with the CLI through the shared PostgreSQL database.

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
