# Installation Guide for ToDoWrite

This guide covers various ways to install and work with the ToDoWrite package, from simple user installations to developer setups.

## 🚀 Quick Installation for Users

### From PyPI (Recommended)
```bash
pip install todowrite
```

### From GitHub (Latest Main Branch)
For the latest development version:
```bash
pip install git+https://github.com/dderyldowney/todowrite.git@main
```

For a specific commit:
```bash
pip install git+https://github.com/dderyldowney/todowrite.git@<commit-hash>
```

## 👨‍💻 Developer Installation

### Prerequisites
- Python 3.12 or higher
- Git
- pip (with --user flag if needed)

### Setup for Development

#### Option 1: Clone and Install
```bash
# Clone the repository
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite

# Install in development mode
pip install -e ".[dev]"
```

#### Option 2: Using setup.py
```bash
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite

# Install with development dependencies
pip install -e ".[dev]"

# Or basic development install
pip install -e .
```

### Development Dependencies

The `[dev]` extras include:
- **mypy>=1.13.0** - Static type checking
- **ruff>=0.7.0** - Fast linter and formatter
- **black>=24.0.0** - Code formatter
- **isort>=5.13.0** - Import sorter
- **pytest>=8.0.0** - Testing framework
- **pre-commit>=4.0.0** - Git hooks
- **bandit[toml]>=1.7.0** - Security linter

### Setting Up Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run all checks manually
pre-commit run --all-files
```

## 🛠️ Building and Packaging

### Building with Hatch
```bash
# Install Hatch if not already installed
pip install hatch

# Build the package
hatch build

# Clean build artifacts
hatch clean
```

### Building with setuptools
```bash
# Build source distribution
python setup.py sdist

# Build wheel
python setup.py bdist_wheel

# Build both
python -m build
```

## 📋 Available Commands

### CLI Commands
After installation, you can use:
```bash
# Initialize the database
todowrite init

# List all items
todowrite list

# Create a new item
todowrite create --layer goal --title "My Goal" --owner "team"

# Get items by status
todowrite list --status in_progress

# Search items
todowrite search "database"

# Export to YAML
todowrite export-yaml

# Import from YAML
todowrite import-yaml

# Check database status
todowrite db-status

## 🛠️ Project Development Utilities

The new ProjectManager class provides centralized utilities that replace individual scripts:

### New CLI Commands
```bash
# Check project setup
todowrite utils validate-setup /path/to/project

# Set up project integration
todowrite utils setup-integration /path/to/project --db-type postgres

# Create project structure
todowrite utils create-structure /path/to/new-project

# Check schema integrity
todowrite utils check-schema
todowrite utils check-deprecated
```

### For AI-Enhanced Development
```bash
# Token optimization features are available when AI dependencies are installed
# All core utilities work without AI requirements
todowrite utils setup-integration /path/to/project --db-type postgres
```

### API Usage

#### Basic Integration
```python
from todowrite import setup_integration, validate_project_setup

# Set up project
setup_integration("/path/to/project", "sqlite")

# Validate project setup
results = validate_project_setup("/path/to/project")
print(f"Project valid: {results['valid']}")
```

See [Project Utilities](docs/PROJECT_UTILITIES.md) for comprehensive documentation.

### Getting Started with SQLAlchemy ORM API

#### Basic Setup
```python
from todowrite import (
    Goal, Concept, Context, Constraints,
    Requirements, AcceptanceCriteria, InterfaceContract,
    Phase, Step, Task, SubTask, Command, Label,
    create_engine, sessionmaker
)

# Initialize database session
engine = create_engine("sqlite:///project.db")
Session = sessionmaker(bind=engine)
session = Session()

print("✅ ToDoWrite SQLAlchemy ORM API ready!")
```

#### Your First Project
```python
# Create a goal
goal = Goal(
    title="Learn ToDoWrite",
    description="Master the SQLAlchemy ORM API",
    owner="your-name",
    severity="medium"
)
session.add(goal)
session.commit()

# Add tasks to your goal
setup_task = Task(
    title="Install todowrite",
    description="Use UV to install todowrite",
    owner="your-name"
)
session.add(setup_task)
session.commit()

api_task = Task(
    title="Try SQLAlchemy ORM API",
    description="Use SQLAlchemy sessions and queries",
    owner="your-name"
)
session.add(api_task)
session.commit()

# Associate tasks with goal
goal.tasks.extend([setup_task, api_task])
session.commit()

# Start working on tasks
setup_task.status = "in_progress"
setup_task.progress = 25
session.commit()
print(f"Started: {setup_task.title}")

# Mark a task complete
api_task.status = "completed"
api_task.progress = 100
session.commit()
print(f"Completed: {api_task.title}")

# Check your progress
all_tasks = goal.tasks
completed_tasks = [t for t in all_tasks if t.status == "completed"]
print(f"Goal: {goal.title}")
print(f"Total tasks: {len(all_tasks)}")
print(f"Completed: {len(completed_tasks)}")
```

#### Common Patterns
```python
# Find existing items
goal = session.query(Goal).filter(Goal.title == "Learn ToDoWrite").first()
all_goals = session.query(Goal).all()

# Create new items
task = Task(
    title="New task",
    owner="your-name"
)
session.add(task)
session.commit()

# Update items
task.title = "Updated task title"
session.commit()

# Business workflows
task.status = "in_progress"
task.progress = 50
session.commit()

# Collection operations
goal_tasks = goal.tasks
task_count = len(goal_tasks) if goal_tasks else 0
print(f"Goal has {task_count} tasks")
```

### Python Module
```python
import todowrite

# Access version
print(todowrite.__version__)
print(todowrite.get_version())

# Import components - ALL 12 LAYERS
from todowrite import (
    Goal, Concept, Context, Constraints,
    Requirements, AcceptanceCriteria, InterfaceContract,
    Phase, Step, Task, SubTask, Command, Label,
    create_engine, sessionmaker
)
```

## 🔍 Troubleshooting

### Installation Issues

#### Python Version Mismatch
```bash
# Check Python version
python --version  # Should be 3.12+

# Use specific Python version
python3.12 -m pip install todowrite
```

#### Permission Issues
```bash
# Install for current user only
pip install --user todowrite

# Or use virtual environment
python -m venv myenv
source myenv/bin/activate  # On Unix
myenv\Scripts\activate     # On Windows
pip install todowrite
```

#### Git Installation Issues
```bash
# If git+https fails, use SSH
pip install git+ssh://git@github.com/dderyldowney/todowrite.git@main

# Or download ZIP and install locally
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite
pip install -e .
```

### Development Issues

#### Import Errors
```bash
# Ensure PYTHONPATH includes current directory
export PYTHONPATH=$PYTHONPATH:.

# Or run from project root
python -c "import todowrite; print(todowrite.__version__)"
```

#### Pre-commit Hook Failures
```bash
# Skip pre-commit hooks temporarily (not recommended)
git commit -m "message" --no-verify

# Fix the issues and run manually
pre-commit run --all-files
```

## 🔄 Updates and Upgrades

### Update from PyPI
```bash
pip install --upgrade todowrite
```

### Update from GitHub
```bash
# Reinstall from latest main
pip install --force-reinstall git+https://github.com/dderyldowney/todowrite.git@main
```

### Update Development Version
```bash
cd todowrite
git pull origin main
pip install --upgrade -e ".[dev]"
```

## 📦 Distribution

### For Contributors
When submitting changes, ensure:
1. All tests pass (`make tw-test`)
2. Code is formatted (`black .` and `isort .`)
3. Linting passes (`ruff check .`)
4. Type checking passes (`mypy .`)

### Package Structure
```
todowrite/
├── setup.py              # Installation script
├── pyproject.toml        # Modern package configuration
├── requirements.txt      # Core dependencies
├── README.md             # Project documentation
├── todowrite/            # Main package directory
│   ├── __init__.py      # Package initialization
│   ├── version.py        # Version information
│   ├── app.py           # Main application
│   ├── cli.py           # CLI interface
│   ├── schema.py        # Schema definitions
│   └── ...
├── tests/               # Test files
└── docs/                # Additional documentation
```

## 📚 More Information

- **Project Repository**: https://github.com/dderyldowney/todowrite
- **Issues**: https://github.com/dderyldowney/todowrite/issues
- **Documentation**: See docs/ directory in repository
- **Contributing**: See CONTRIBUTING.md in repository
