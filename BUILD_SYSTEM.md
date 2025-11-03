# Build System Guide

## Overview

This project uses **Hatchling** as the build backend and **Twine** for package publishing. This guide explains why we chose this approach and how to use it.

## Why Hatchling + Twine instead of `python -m build`?

### Hatchling vs `python -m build`

| Aspect | Hatchling (Preferred) | `python -m build` (Deprecated) |
|--------|----------------------|--------------------------------|
| **Modern Standards** | ✅ PEP 517/518 compliant, latest Python packaging standards | ✅ PEP 517/518 compliant but older approach |
| **Performance** | ⚡ Faster build times, optimized for modern projects | 🐢 Slower, generic implementation |
| **Configuration** | 🎯 Single `pyproject.toml` for all build settings | 📝 Multiple configuration files needed |
| **Extensibility** | 🔧 Plugin architecture, highly customizable | 🔒 Limited customization options |
| **Version Sources** 🔄 Dynamic versioning from files, git, VCS | 📋 Static versioning only |
| **Maintenance** | 🚀 Actively maintained by Python Packaging Authority | 📦 Frozen in time, fewer updates |

### Twine for Publishing

**Twine** is the secure, industry-standard tool for uploading packages to PyPI:

- **Security**: HTTPS-only uploads, certificate verification
- **Compatibility**: Works with any PEP 517 build backend
- **Features**: Check for common issues before upload, metadata validation
- **Reliability**: Proven tool used by 99% of Python packages

## Build Commands

### Build Packages

```bash
# Library package (todowrite)
cd lib_package
python -m hatchling build

# CLI package (todowrite-cli)
cd cli_package
python -m hatchling build
```

### Clean Previous Builds

```bash
# Clean library package
cd lib_package
rm -rf dist/ build/ *.egg-info/

# Clean CLI package
cd cli_package
rm -rf dist/ build/ *.egg-info/
```

### Build for Distribution

```bash
# Build both packages
cd lib_package && python -m hatchling build
cd ../cli_package && python -m hatchling build

# Check built packages
ls -la lib_package/dist/
ls -la cli_package/dist/
```

## Publishing with Twine

### Upload to TestPyPI

```bash
# Upload library package
cd lib_package
twine upload --repository testpypi dist/*

# Upload CLI package
cd cli_package
twine upload --repository testpypi dist/*
```

### Upload to PyPI (Production)

```bash
# Upload library package
cd lib_package
twine upload dist/*

# Upload CLI package
cd cli_package
twine upload dist/*
```

### Check Before Upload

```bash
# Verify package integrity
cd lib_package
twine check dist/*

cd cli_package
twine check dist/*
```

## Configuration Files

### `pyproject.toml` (Library Package)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "todowrite"
version = "0.3.0"  # Centrally managed via shared_version.py
# ... other metadata

[tool.hatch.build.targets.wheel]
packages = ["src/todowrite"]
```

### `pyproject.toml` (CLI Package)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "todowrite_cli"
version = "0.3.0"  # Centrally managed via shared_version.py
# ... other metadata

[tool.hatch.build.targets.wheel]
packages = ["src/todowrite_cli"]
```

## Development Workflow

### 1. Make Changes
```bash
# Make code changes
# Update version if needed
python scripts/bump_version.py bump 0.3.1
```

### 2. Test Build
```bash
cd lib_package && python -m hatchling build
cd ../cli_package && python -m hatchling build
```

### 3. Check Packages
```bash
twine check lib_package/dist/*
twine check cli_package/dist/*
```

### 4. Upload to TestPyPI
```bash
cd lib_package && twine upload --repository testpypi dist/*
cd ../cli_package && twine upload --repository testpypi dist/*
```

### 5. Upload to PyPI
```bash
cd lib_package && twine upload dist/*
cd ../cli_package && twine upload dist/*
```

## Migration from `python -m build`

If you were previously using `python -m build`, here's the migration:

### Old Commands (Deprecated)
```bash
# ❌ Don't use these anymore
cd lib_package && python -m build
cd cli_package && python -m build
```

### New Commands (Current)
```bash
# ✅ Use these instead
cd lib_package && python -m hatchling build
cd cli_package && python -m hatchling build
```

## Benefits Summary

1. **Performance**: Faster builds with hatchling
2. **Standards Compliance**: Full PEP 517/518 support
3. **Security**: Secure uploads with twine
4. **Maintainability**: Modern, actively maintained tools
5. **Configuration**: Single source of truth in `pyproject.toml`
6. **Version Management**: Dynamic versioning support
7. **Extensibility**: Plugin system for custom build needs

## Troubleshooting

### Common Issues

**Issue**: `hatchling: command not found`
```bash
# Solution: Install hatchling
pip install hatchling
```

**Issue**: `twine: command not found`
```bash
# Solution: Install twine
pip install twine
```

**Issue**: Build fails due to missing dependencies
```bash
# Solution: Install build requirements
pip install -e .[dev]
```

**Issue**: Upload fails with authentication error
```bash
# Solution: Configure PyPI tokens
python -m twine configure
```

### Clean Build Process

Always clean before building a new release:

```bash
# Clean both packages
cd lib_package && rm -rf dist/ build/ *.egg-info/
cd ../cli_package && rm -rf dist/ build/ *.egg-info/

# Fresh build
cd lib_package && python -m hatchling build
cd ../cli_package && python -m hatchling build
```

This ensures you're only uploading the latest artifacts.
