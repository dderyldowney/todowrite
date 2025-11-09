# Version Management Guide

This document explains the proper version management workflow for the ToDoWrite project.

## Architecture Overview

The ToDoWrite project uses a **single source of truth** architecture for version management:

1. **VERSION file** - The authoritative source for the version number
2. **shared_version.py** - Provides version access functions and maintains Hatch compatibility
3. **scripts/bump_version.py** - Automated tool for version bumping

## Key Components

### 1. VERSION File
- **Location**: Project root (`./VERSION`)
- **Format**: Semantic version (e.g., `0.3.1`)
- **Purpose**: Single source of truth for all version information

### 2. shared_version.py
- **Location**: Project root (`./shared_version.py`)
- **Key Functions**:
  - `get_version()` - Returns current version from VERSION file
  - `_get_version()` - Internal function with fallback
  - `sync_version()` - Syncs literal `__version__` with VERSION file
- **Hatch Compatibility**: Maintains literal `__version__` string for Hatch build system

### 3. scripts/bump_version.py
- **Location**: `./scripts/bump_version.py`
- **Purpose**: Automated version bumping with proper synchronization
- **Features**:
  - Semantic version bumping (patch, minor, major)
  - Explicit version setting
  - Dry-run mode for testing
  - Automatic synchronization between VERSION file and shared_version.py

## Usage

### Method 1: Automated Version Bumping (Recommended)

```bash
# Bump patch version (0.3.1 → 0.3.2)
python scripts/bump_version.py patch

# Bump minor version (0.3.1 → 0.4.0)
python scripts/bump_version.py minor

# Bump major version (0.3.1 → 1.0.0)
python scripts/bump_version.py major

# Set specific version
python scripts/bump_version.py 1.2.3

# Dry run to preview changes
python scripts/bump_version.py --dry-run patch
```

### Method 2: Manual Version Management

```bash
# 1. Edit VERSION file
echo "0.3.2" > VERSION

# 2. Sync with shared_version.py
python -c "from shared_version import sync_version; sync_version()"
```

### Method 3: Direct Function Access

```python
from shared_version import get_version, sync_version

# Get current version
current = get_version()
print(f"Current version: {current}")

# Sync after manual VERSION file edit
sync_version()
```

## Workflow Examples

### Typical Release Workflow (Develop → Main)

```bash
# 1. Complete feature development on develop branch
# ... development work on develop branch ...

# 2. Ensure all tests pass
PYTHONPATH="lib_package/src:cli_package/src" python -m pytest

# 3. Bump version for release on develop branch
python scripts/bump_version.py patch

# 4. Verify version bump
python -c "from shared_version import get_version; print(f'Releasing version: {get_version()}')"

# 5. Commit version changes on develop
git add VERSION
git commit -m "bump: version 0.3.2"

# 6. Merge develop to main
git checkout main
git merge develop

# 7. Create release tag
git tag v0.3.2

# 8. Push to remote
git push origin main
git push origin v0.3.2
git push origin develop  # Update develop branch on remote
```

### Feature Branch Workflow

```bash
# 1. Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/new-feature

# 2. Develop feature
# ... coding ...

# 3. If needed for testing, bump to prerelease
python scripts/bump_version.py 0.3.2-rc1

# 4. Complete feature development

# 5. Merge feature branch to develop
git checkout develop
git merge feature/new-feature

# 6. Push to develop for integration
git push origin develop

# 7. Delete feature branch (optional)
git branch -d feature/new-feature
```

### Emergency Fix Workflow

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-fix

# 2. Fix the issue
# ... coding ...

# 3. Bump patch version
python scripts/bump_version.py patch

# 4. Merge hotfix directly to main (bypass develop)
git checkout main
git merge hotfix/critical-fix

# 5. Tag and release
git tag v0.3.3
git push origin main
git push origin v0.3.3

# 6. Also merge hotfix back to develop for future releases
git checkout develop
git merge hotfix/critical-fix
git push origin develop
```

## Git Branching Strategy

This project uses **GitFlow** methodology with two primary branches:

- **`main`**: Production-ready releases (stable)
- **`develop`**: Integration branch for features (unstable)

### Branch Rules

- **All feature branches** start from `develop`
- **Version bumping** happens on `develop` branch
- **Release tags** are created on `main` branch after merging
- **Hotfixes** can bypass `develop` and go directly to `main`

**Important**: Never commit directly to `main` - always use a merge from `develop` or hotfix branches.

### Branch Lifecycle

1. **Feature Development**: `develop` → `feature/branch-name` → `develop`
2. **Release**: `develop` → `main` (with version bump and tag)
3. **Hotfix**: `main` → `hotfix/branch-name` → `main` + `develop`

## Troubleshooting

### Version Sync Issues

If you notice inconsistencies between VERSION file and shared_version.py:

```bash
# Check current versions
python -c "from shared_version import get_version; print(f'get_version(): {get_version()}')"
python -c "import shared_version; print(f'__version__: {shared_version.__version__}')"
cat VERSION

# Resync if needed
python -c "from shared_version import sync_version; sync_version()"
```

### Build System Issues

If Hatch build system fails with version-related errors:

1. **Check VERSION file format**:
   ```bash
   cat VERSION  # Should be just: 0.3.1
   ```

2. **Verify shared_version.py literal**:
   ```bash
   grep -n "__version__ = " shared_version.py  # Should be: __version__ = "0.3.1"
   ```

3. **Run sync**:
   ```bash
   python -c "from shared_version import sync_version; sync_version()"
   ```

## Best Practices

1. **Always use the automated script** for version bumping
2. **Test with --dry-run** before actual version changes
3. **Commit VERSION and shared_version.py together**
4. **Tag releases immediately after version bumps**
5. **Keep semantic versioning** (major.minor.patch)
6. **Use prerelease versions** for testing (e.g., 0.3.2-rc1)

## Integration with Build Systems

### Hatch Build System
The `shared_version.py` module is designed to work seamlessly with Hatch:

```toml
# pyproject.toml
[tool.hatch.version]
path = "shared_version.py"
```

Hatch reads the literal `__version__` string, which is kept in sync with the VERSION file.

## File Structure

```
todowrite/
├── VERSION                    # Single source of truth
├── shared_version.py          # Version access functions
├── scripts/
│   └── bump_version.py        # Automated version bumping
└── VERSION_MANAGEMENT.md      # This documentation
```

## Important Notes

### Hatch Build System Compatibility

This version management system was specifically designed to resolve a critical **Hatch build system issue** where Hatch's regex-based version parsing requires a literal string assignment like:

```python
__version__ = "0.3.1"  # Hatch can parse this
```

Instead of:

```python
__version__ = _get_version()  # Hatch cannot parse this
```

The solution maintains both:
- **Single source of truth**: VERSION file
- **Hatch compatibility**: Literal `__version__` string
- **Automatic synchronization**: `sync_version()` function

### Workflow Summary

**When you need to bump the version:**

1. **ALWAYS** edit the VERSION file first
2. **OR** use the automated script: `python scripts/bump_version.py patch`
3. **NEVER** edit `shared_version.py` directly (except for code changes)
4. **VERIFY** the sync worked: `python -c "from shared_version import get_version; print(get_version())"`

The automated script handles all of this for you, making it the recommended approach.
- Both packages use dynamic versioning in their `pyproject.toml`
- Build system reads from `VERSION` file via `_build_version_hook.py`
- No hardcoded versions in build configuration

## 🔄 Development Workflow

### Checking Current Version

```bash
# From anywhere in the project
python scripts/bump_version.py get

# Or programmatically
from todowrite import __version__
from todowrite_cli import __version__
print(__version__)  # Both return the same version
```

### Updating Version

```bash
# Bump to a specific version
python scripts/bump_version.py 1.0.0

# Or bump by type (patch, minor, major)
python scripts/bump_version.py patch
python scripts/bump_version.py minor
python scripts/bump_version.py major

# Verify the change
python scripts/bump_version.py --dry-run patch  # Preview change
python -c "from shared_version import get_version; print(get_version())"  # Should output new version

# Reinstall packages to pick up new version
pip install -e lib_package/
pip install -e cli_package/

# Verify versions are synchronized
python -c "import todowrite, todowrite_cli; print(todowrite.__version__ == todowrite_cli.__version__)"
```

### Building with Updated Version

```bash
# Build packages - they'll automatically use the version from VERSION file
cd lib_package && python -m build
cd ../cli_package && python -m build

# Built packages will have synchronized versions from VERSION file
```

## 🔧 Technical Implementation

### Version Import Structure

Each package's `version.py` imports from the central module:

```python
# lib_package/src/todowrite/version.py
import sys
from pathlib import Path

current_file = Path(__file__)
project_root = current_file.parent.parent.parent.parent.parent

if (project_root / "shared_version.py").exists():
    sys.path.insert(0, str(project_root))
    from shared_version import __author__, __email__, __version__, get_version
else:
    # Fallback for development/testing
    __version__ = "0.2.2"
    __author__ = "D Deryl Downey"
    __email__ = "dderyldowney@gmail.com"
```

### Build Configuration

```toml
# Both pyproject.toml files use dynamic versioning
[tool.hatch.version]
source = "script"
path = "../_build_version_hook.py"
expression = "get_project_version()"

[project]
name = "todowrite"  # or "todowrite_cli"
dynamic = ["version"]  # Version comes from build hook
```

## ✅ Benefits

### 1. Single Point of Change
- **Before**: Update version in 4 different files manually
- **After**: Update one `VERSION` file, everything else updates automatically

### 2. Eliminates Version Mismatches
- Both packages guaranteed to have identical versions
- Build system and runtime versions stay synchronized

### 3. Simplified Release Process
- No more manual coordination between packages
- Single command to update versions across the entire project

### 4. Version Validation
- `bump_version.py` validates version format
- Prevents invalid version strings from being committed

### 5. Development-Friendly
- Fallback versions allow development even if central files are missing
- Clear separation between version source and version consumers

## 🚀 Usage Examples

### Daily Development

```bash
# Check current version
python scripts/bump_version.py get

# Both packages show the same version
python -c "import todowrite, todowrite_cli; print(todowrite.__version__)"

# CLI shows correct version
todowrite --version
```

### Preparing a Release

```bash
# 1. Update version on develop branch
python scripts/bump_version.py patch  # or minor/major

# 2. Verify version propagation
python -c "from shared_version import get_version; print(get_version())"  # Should show new version

# 3. Reinstall development packages
pip install -e lib_package/
pip install -e cli_package/

# 4. Verify CLI shows new version
todowrite --version  # Should show new version

# 5. Run tests to ensure everything works
PYTHONPATH="lib_package/src:cli_package/src" python -m pytest

# 6. Build packages
cd lib_package && python -m build
cd ../cli_package && python -m build
```

### Version Validation

```bash
# Test that both packages have the same version
python -c "
import todowrite, todowrite_cli
assert todowrite.__version__ == todowrite_cli.__version__, 'Version mismatch!'
print('✅ Versions are synchronized:', todowrite.__version__)
"
```

## 📝 File References

- **`VERSION`**: Single source of truth for version number
- **`shared_version.py`**: Centralized version module
- **`scripts/bump_version.py`**: Version management CLI tool
- **`lib_package/src/todowrite/version.py`**: Library version imports
- **`cli_package/src/todowrite_cli/version.py`**: CLI version imports
- **`_build_version_hook.py`**: Build-time version access
- **`VERSION_MANAGEMENT.md`**: This documentation

## 🔍 Debugging

### Version Mismatch Issues

If packages show different versions:

1. **Check the source**:
   ```bash
   python scripts/bump_version.py get
   cat VERSION
   ```

2. **Check imports**:
   ```bash
   python -c "from lib_package.src.todowrite.version import __version__ as lib_ver"
   python -c "from cli_package.src.todowrite_cli.version import __version__ as cli_ver"
   echo "Library: $lib_ver, CLI: $cli_ver"
   ```

3. **Reinstall packages** (editable installs cache versions):
   ```bash
   pip install -e lib_package/
   pip install -e cli_package/
   ```

### Import Errors

If version imports fail:

1. **Check file paths**:
   ```bash
   ls -la VERSION shared_version.py
   ```

2. **Check package structure**:
   ```bash
   ls -la lib_package/src/todowrite/version.py
   ls -la cli_package/src/todowrite_cli/version.py
   ```

3. **Test version module directly**:
   ```bash
   python -c "from shared_version import get_version; print(get_version())"
   ```

## 🎉 Summary

The centralized version management system transforms version management from a manual, error-prone process into an automated, single-source-of-truth system. This ensures consistency between packages and simplifies the release process significantly.

**Key outcomes:**
- ✅ **4 locations → 1 location** for version changes
- ✅ **Automatic synchronization** between packages
- ✅ **Validated version format** and error prevention
- ✅ **Simplified release workflow**
- ✅ **Development-friendly** fallbacks and validation
