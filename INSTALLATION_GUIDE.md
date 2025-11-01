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
- **pyright>=1.1.0** - Static type checking (strict mode enabled)
- **ruff>=0.7.0** - Fast linter and formatter (SIM118, UP007, I001 rules)
- **black>=24.0.0** - Code formatter (88 char line length)
- **isort>=5.13.0** - Import sorter (black profile)
- **pytest>=8.0.0** - Testing framework (9/9 tests passing)
- **pre-commit>=4.0.0** - Git hooks (all quality tools)
- **bandit[toml]>=1.7.0** - Security linter (HIGH severity issues fixed)

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

# List all nodes
todowrite list

# Create a new node
todowrite create

# Get a node by ID
todowrite get <node-id>

# Check database status
todowrite db-status

# Export to YAML
todowrite export-yaml

# Import from YAML
todowrite import-yaml

# Check sync status
todowrite sync-status

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
```python
from todowrite import setup_integration, validate_project_setup

# Set up project
setup_integration("/path/to/project", "sqlite")

# Validate project setup
results = validate_project_setup("/path/to/project")
print(f"Project valid: {results['valid']}")
```

See [Project Utilities](docs/PROJECT_UTILITIES.md) for comprehensive documentation.

### Python Module
```python
import todowrite

# Access version
print(todowrite.__version__)
print(todowrite.get_version())

# Import components
from todowrite.app import ToDoWrite
from todowrite.cli import cli
```

## 🏆 Quality Assurance & Development Standards

### Zero Tech Debt Status ✅
ToDoWrite has achieved **zero tech debt** with all quality tools reporting clean status:

#### Current Quality Metrics:
- **Test Coverage**: 9/9 pytest tests passing ✅
- **Type Safety**: 0 pyright errors (strict mode) ✅
- **Code Style**: 0 ruff linting errors ✅
- **Security**: HIGH severity issues fixed, only LOW warnings remaining ✅

#### Recent Security Hardening (Completed):
- ✅ **HIGH severity** subprocess shell=True → `shlex.split()` + `shell=False`
- ✅ **Try/except/pass** → proper exception handling with logging
- ✅ **Import security** - All subprocess usage hardened
- ✅ **Type annotations** - Full Python 3.12+ pipe syntax (`str | None`)

#### Development Commands:
```bash
# Run all quality checks
make tw-test                    # Comprehensive test suite
ruff check .                   # Linting (0 errors)
pyright .                      # Type checking (0 errors)
bandit -r todowrite/            # Security scan (LOW warnings only)
pre-commit run --all-files     # Pre-commit hooks
```

### 🔍 Troubleshooting

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
4. Type checking passes (`pyright .`)

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
