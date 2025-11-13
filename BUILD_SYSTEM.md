# ToDoWrite Unified Build System

This document describes the unified monorepo build system implemented for the ToDoWrite project.

## 🎯 Overview

The ToDoWrite monorepo uses a modern, unified build system that provides:
- **UV-based environment management** replacing virtualenv+pip
- **Hatchling for package building** within UV environment
- **Consistent tooling** across all implemented packages
- **Simplified development workflows** with comprehensive build scripts
- **Automated code quality enforcement** using Ruff and Bandit
- **Graceful handling** of packages in different development stages

## 🏗️ Architecture

### Workspace Configuration
```
todowrite/
├── pyproject.toml              # Root workspace configuration
├── lib_package/               # Core library (todowrite) - PRODUCTION READY
├── cli_package/               # CLI interface (todowrite_cli) - PRODUCTION READY
├── web_package/               # Web application (todowrite_web) - PLANNING STAGE
└── dev_tools/                 # Development scripts and tools
```

### Package Status

- **lib_package**: ✅ Production ready with full test coverage
- **cli_package**: ✅ Production ready with full CLI functionality
- **web_package**: 🚧 Planning stage - basic structure exists, tests excluded

### Key Components

- **UV**: Environment and dependency management (replaces virtualenv+pip)
  - Manages workspace dependencies across all packages
  - Provides isolated build environments
  - Replaces virtualenv+pip completely

- **Hatchling**: Package building backend
  - Runs within UV environment via `uv run python -m build`
  - Creates build isolation environments (shows "virtualenv+pip" messages internally)
  - Builds distribution artifacts (wheels and tarballs)

- **Twine**: PyPI/TestPyPI deployment
  - Uploads packages to PyPI and TestPyPI
  - Handles deployment workflows

- **Ruff**: Code formatting, linting, and basic security checking
  - Unified formatting with 100-character line length
  - Comprehensive linting rules
  - Fast Python-native implementation

- **Bandit**: Security auditing
  - Additional security checks beyond Ruff
  - Finds common security issues

- **pytest**: Testing framework
  - Runs tests with coverage reporting
  - Excludes web_package tests (planning stage)

- **Database**: Multi-backend support
  - **Production**: PostgreSQL
  - **Development/Testing**: SQLite3 with project-specific databases
  - **Fallback**: YAML file storage

- **Shared Configuration**: Consistent settings across packages
  - Centralized version management
  - Unified tooling configuration
  - Shared dependency groups

## 🚀 Quick Start

### Initial Setup
```bash
# Clone the repository
git clone https://github.com/dderyldowney/todowrite
cd todowrite

# Install dependencies
./dev_tools/build.sh install

# Run development workflow
./dev_tools/build.sh dev
```

### Daily Development
```bash
# Install/update dependencies (recommended)
./dev_tools/build.sh install
# OR directly: uv sync --group dev

# Run tests (excludes web_package)
./dev_tools/build.sh test
# OR directly: uv run pytest tests/ --ignore=tests/web/

# Code quality checks (excludes web_package)
./dev_tools/build.sh lint
./dev_tools/build.sh format
# OR directly: uv run ruff check lib_package/ cli_package/
# OR directly: uv run ruff format lib_package/ cli_package/

# Build all packages
./dev_tools/build.sh build
```

## 📋 Build Scripts

### build.sh - Main Build Script
Primary script for all build operations:

```bash
# Help and information
./dev_tools/build.sh help

# Dependency management
./dev_tools/build.sh install    # Install all dependencies

# Development workflow
./dev_tools/build.sh dev        # Complete development workflow
./dev_tools/build.sh test       # Run tests only
./dev_tools/build.sh lint       # Code quality checks
./dev_tools/build.sh format     # Format code

# Package management
./dev_tools/build.sh build      # Build all packages
./dev_tools/build.sh clean      # Clean build artifacts
./dev_tools/build.sh release    # Prepare for release
./dev_tools/build.sh validate   # Validate build system
```

## 🚧 Package Development Stages

### Handling Mixed Package States

The build system gracefully handles packages at different development stages:

#### Production Ready Packages (lib_package, cli_package)
- ✅ Full test coverage included
- ✅ Code quality enforcement
- ✅ Complete build and deployment support
- ✅ All build scripts operations apply

#### Planning Stage Packages (web_package)
- 🚧 Tests excluded from test runs (`--ignore=tests/web/`)
- 🚧 Linting excluded from quality checks
- 🚧 Formatting excluded from code formatting
- ✅ Basic package building works (for workspace consistency)
- 📝 Clear messaging about exclusion status

#### Example Output
```bash
$ ./dev_tools/build.sh test
[BUILD] Running tests with unified configuration...
[Note: web_package excluded from testing (planning stage)]
✅ All tests completed

$ ./dev_tools/build.sh lint
[BUILD] Running code quality checks...
[Note: web_package excluded from linting (planning stage)]
✅ Code quality checks completed
```

### deploy.sh - Deployment Script
For PyPI/TestPyPI deployments:

```bash
# Build packages (uses UV environment + hatchling)
./dev_tools/deploy.sh build

# Deploy all packages
./dev_tools/deploy.sh testpypi    # To TestPyPI
./dev_tools/deploy.sh pypi        # To PyPI (production - main branch only)

# Deploy single packages
./dev_tools/deploy.sh pypi-single lib    # Deploy lib_package only
./dev_tools/deploy.sh pypi-single cli    # Deploy cli_package only
./dev_tools/deploy.sh testpypi-single web  # Deploy web_package to TestPyPI

# Pre-deployment checks
./dev_tools/deploy.sh check
```

### setup_dev.sh - Environment Setup
Legacy environment setup (updated for unified system):

```bash
# Sets up development environment
./dev_tools/setup_dev.sh
```

## 🛠️ Development Workflows

### 1. New Development
```bash
# 1. Install dependencies
./dev_tools/build.sh install

# 2. Create feature branch
git checkout -b feature/new-feature

# 3. Make changes...

# 4. Run development workflow
./dev_tools/build.sh dev

# 5. Commit changes
git add .
git commit -m "feat: add new feature"

# 6. Push and create PR
git push origin feature/new-feature
```

### 2. Testing
```bash
# Run all tests
./dev_tools/build.sh test

# Run specific test file
uv run pytest tests/test_specific.py

# Run with coverage
uv run pytest tests/ --cov=lib_package/src --cov-report=html

# Run integration tests
uv run pytest tests/integration/
```

### 3. Code Quality
```bash
# Check code quality
./dev_tools/build.sh lint

# Format code
./dev_tools/build.sh format

# Both linting and formatting
uv run ruff check --fix .
uv run ruff format .
```

### 4. Release Process
```bash
# 1. Update version
echo "0.5.0" > VERSION

# 2. Prepare release
./dev_tools/build.sh release

# 3. Test packages
./dev_tools/deploy.sh check

# 4. Deploy to TestPyPI
./dev_tools/deploy.sh testpypi

# 5. Deploy to PyPI (production)
./dev_tools/deploy.sh pypi
```

## 📦 Package Structure

### lib_package (todowrite)
```bash
# Build package
python -m build lib_package/

# Install locally
pip install -e lib_package/

# Test package
uv run pytest tests/lib_package/
```

### cli_package (todowrite_cli)
```bash
# Build package
python -m build cli_package/

# Install locally
pip install -e cli_package/

# Test CLI
python -m todowrite_cli.main --help
```

### web_package (todowrite_web)
```bash
# Build package
python -m build web_package/

# Install locally
pip install -e web_package/

# Test web package
uv run pytest tests/web_package/
```

## 🔧 Configuration

### Dependencies
Dependencies are managed through UV dependency groups in `pyproject.toml`:

```bash
# Core dependencies (shared by all packages)
uv sync --group core

# Development dependencies
uv sync --group dev

# Type checking dependencies
uv sync --group types

# All dependencies
uv sync --group all
```

### Code Quality
Unified Ruff configuration across all packages:
- **Line length**: 100 characters
- **Python version**: 3.12+
- **Comprehensive rules**: pycodestyle, pyflakes, isort, security, etc.

### Version Management
- **Single source of truth**: `VERSION` file in project root (currently 0.4.1)
- **Dynamic version reading**: All packages use `dynamic = ["version"]` with path to central VERSION
- **Build integration**: Hatchling automatically reads VERSION during package builds
- **Release management**: Commitizen configured for conventional commits
- **Workspace consistency**: UV workspace ensures all packages use same version

## 📚 Best Practices

### Development
1. **Always run the dev workflow** before committing:
   ```bash
   ./dev_tools/build.sh dev  # install + format + lint + test
   ```

2. **Use UV for dependency management**:
   ```bash
   ./dev_tools/build.sh install  # Recommended approach
   # OR directly: uv sync --group dev
   ```

3. **Follow the conventional commit format**:
   ```bash
   git commit -m "feat: add new feature"
   git commit -m "fix: resolve bug in CLI"
   ```

### Code Quality
1. **Use unified build scripts for quality checks**:
   ```bash
   ./dev_tools/build.sh format  # Formats implemented packages only
   ./dev_tools/build.sh lint    # Lints implemented packages only
   ```

2. **Direct UV commands (for specific needs)**:
   ```bash
   uv run ruff format lib_package/ cli_package/  # Specific packages
   uv run ruff check lib_package/ cli_package/
   ```

3. **Maintain test coverage** above 80% for implemented packages
   - web_package tests excluded (planning stage)
   - Focus on lib_package and cli_package coverage

### Release
1. **Test thoroughly before release**:
   ```bash
   ./dev_tools/build.sh test      # Tests implemented packages
   ./dev_tools/build.sh validate  # Validates build system
   ./dev_tools/deploy.sh check    # Checks package integrity
   ```

2. **Deploy to TestPyPI first**:
   ```bash
   ./dev_tools/deploy.sh testpypi  # Builds and deploys all packages
   ```

3. **Deploy production packages** (main branch only):
   ```bash
   git checkout main
   ./dev_tools/deploy.sh pypi      # Production deployment
   ```

4. **Single package deployment**:
   ```bash
   ./dev_tools/deploy.sh pypi-single lib   # Deploy just lib_package
   ./dev_tools/deploy.sh pypi-single cli   # Deploy just cli_package
   ```

5. **Version management**:
   - Update VERSION file (single source of truth)
   - Use conventional commits with commitizen
   - Let hatchling read VERSION during builds

## 🔍 Troubleshooting

### Common Issues

**Dependency conflicts**:
```bash
# Clean and reinstall using UV
./dev_tools/build.sh clean
./dev_tools/build.sh install

# OR directly with UV
uv cache clean
uv sync --group dev --refresh
```

**Build failures**:
```bash
# Check package-specific issues with UV environment
./dev_tools/build.sh build lib    # Build specific package
./dev_tools/build.sh validate     # Validate build system

# OR directly with UV + hatchling
uv run python -m build lib_package/
```

**Test failures**:
```bash
# Run tests with verbose output (excludes web_package)
./dev_tools/build.sh test

# OR directly with UV
uv run pytest tests/ --ignore=tests/web/ -v

# Run specific test file
uv run pytest tests/lib/test_specific.py -v
```

**web_package build issues (expected)**:
```bash
# web_package is in planning stage - some failures are expected
# Tests are excluded, but basic building may work
./dev_tools/build.sh build web  # May work for basic structure
```

**Linting errors**:
```bash
# Auto-fix linting issues (implemented packages only)
./dev_tools/build.sh lint      # Shows issues
uv run ruff check --fix lib_package/ cli_package/  # Auto-fixes

# Format code (implemented packages only)
./dev_tools/build.sh format
# OR directly: uv run ruff format lib_package/ cli_package/
```

### Getting Help

1. **Check build script help**:
   ```bash
   ./dev_tools/build.sh help
   ./dev_tools/deploy.sh help
   ```

2. **Consult logs** for detailed error messages

3. **Check UV workspace status**:
   ```bash
   uv tree
   ```

4. **Verify package builds**:
   ```bash
   ./dev_tools/build.sh build      # Uses UV + hatchling
   # OR directly: uv run python -m build lib_package/
   ```

## 📈 Implementation Status

### ✅ **PRODUCTION READY**
- **UV Workspace**: Complete with all packages configured
- **Build Scripts**: Full development and deployment automation
- **Version Management**: Centralized VERSION file system
- **Code Quality**: Ruff + Bandit security checks
- **Testing**: pytest with coverage (excluding web_package)
- **Package Building**: Hatchling + UV integration

### 🚧 **PLANNING STAGE**
- **web_package**: Basic structure exists, tests excluded
  - FastAPI backend models implemented
  - Missing runtime dependencies (httpx, etc.)
  - Not ready for production deployment

### 🎯 **KEY ACCOMPLISHMENTS**
- Replaced virtualenv+pip with UV completely
- Unified build system with comprehensive scripts
- Graceful handling of mixed package development stages
- Clean git history (removed inappropriate artifacts)
- Comprehensive documentation and troubleshooting

## 📈 Benefits

The unified build system provides:

1. **Consistency**: Same tools and configuration across all packages
2. **Efficiency**: Single command for common operations
3. **Reliability**: Automated testing and quality checks
4. **Simplicity**: Easy onboarding and reduced cognitive load
5. **Scalability**: Easy to add new packages to the workspace

## 🔄 Migration

The unified build system replaces the previous fragmented approach:

- ✅ **UV workspace** instead of separate dependency management
- ✅ **Unified Ruff config** instead of per-package configurations
- ✅ **Central build scripts** instead of scattered makefiles
- ✅ **Shared version management** instead of multiple VERSION files
- ✅ **Automated workflows** instead of manual processes

All existing functionality is preserved while providing a more streamlined development experience.
