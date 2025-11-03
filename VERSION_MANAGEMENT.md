# Centralized Version Management

This document explains the centralized version management system for the ToDoWrite project, which ensures that both the library (`todowrite`) and CLI (`todowrite_cli`) packages maintain synchronized versions from a single source of truth.

## 🎯 Problem Solved

Previously, version numbers were defined in **4 separate locations**:

1. `lib_package/src/todowrite/version.py`
2. `cli_package/src/todowrite_cli/version.py`
3. `lib_package/pyproject.toml`
4. `cli_package/pyproject.toml`

This manual process was error-prone and led to version mismatches between packages.

## 🏗️ Solution Architecture

### Single Source of Truth

```
todowrite/
├── VERSION                    # ← Single source of truth
├── shared_version.py          # Centralized version module
├── _build_version_hook.py     # Build-time version access
├── scripts/bump_version.py    # Version management CLI
└── [package directories]
    └── src/[package]/version.py  # Import from shared_version.py
```

### Key Components

#### 1. `VERSION` File
- **Purpose**: Contains the current version string only
- **Format**: `X.Y.Z` (e.g., `0.2.2`)
- **Location**: Project root

#### 2. `shared_version.py`
- **Purpose**: Centralized version module that all packages import from
- **Functionality**: Reads VERSION file and provides version/metadata
- **Fallback**: Provides default version if VERSION file is missing

#### 3. `scripts/bump_version.py`
- **Purpose**: CLI tool for version management
- **Commands**:
  ```bash
  python scripts/bump_version.py get          # Show current version
  python scripts/bump_version.py bump 1.0.0  # Set new version
  ```

#### 4. Build Integration
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
# Bump to a new version
python scripts/bump_version.py bump 1.0.0

# Verify the change
python scripts/bump_version.py get  # Should output "1.0.0"

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
# 1. Update version
python scripts/bump_version.py bump 1.0.0

# 2. Verify version propagation
python scripts/bump_version.py get  # Should show "1.0.0"

# 3. Reinstall development packages
pip install -e lib_package/
pip install -e cli_package/

# 4. Verify CLI shows new version
todowrite --version  # Should show "1.0.0"

# 5. Build packages
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
