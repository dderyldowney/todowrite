# ToDoWrite Deployment Tools Configuration

## Build System & Package Publishing

This document specifies the deployment tools and processes used for the ToDoWrite project. All deployment operations must use the tools specified below.

### **MANDATORY: Use Hatchling (NEVER Setuptools)**

#### Build System
```bash
# Build package using hatchling (NEVER setuptools)
# PREFERRED: uv run hatchling build (RECOMMENDED)
# LEGACY: python -m hatchling build (current scripts use this)
uv run hatchling build

# Build in specific package directory
cd lib_package && uv run hatchling build
cd cli_package && uv run hatchling build
cd web_package && uv run hatchling build

# Or use the provided build script (uses python -m hatchling build)
./scripts/build.sh [clean]
```

#### pyproject.toml Configuration (ALL PACKAGES)
```toml
[build-system]
requires = ["hatchling"]  # NEVER setuptools
build-backend = "hatchling.build"

[project]
name = "package-name"
version = "0.4.1"  # From VERSION file
description = "Package description"
requires-python = ">=3.12"

[build]
# Hatchling-specific build configuration
```

### **MANDATORY: Use Twine for PyPI/TestPyPI Publishing**

#### **CRITICAL: TestPyPI First, Then Production PyPI**
**MANDATORY SEQUENCE:**
1. **ALWAYS** push to TestPyPI first
2. **ONLY** if TestPyPI succeeds, then push to production PyPI
3. **NEVER** skip TestPyPI validation

#### TestPyPI Publishing (MANDATORY FIRST STEP)
```bash
# Build and publish to TestPyPI (ALWAYS FIRST)
uv run hatchling build
uv run twine upload --repository testpypi dist/*

# Check TestPyPI upload
uv run twine check dist/*
```

#### PyPI Production Publishing (ONLY AFTER TestPyPI SUCCESS)
```bash
# Build and publish to production PyPI (ONLY AFTER TestPyPI SUCCESS)
uv run hatchling build
uv run twine upload dist/*

# Verify package on PyPI
uv run twine check dist/*
```

#### Twine Configuration
```bash
# Configure TestPyPI credentials (in ~/.pypirc)
[twine]
repositories.testpypi.url = https://test.pypi.org/legacy/
```

### **MANDATORY: Use GitHub CLI for GitHub Releases**

#### Create GitHub Releases
```bash
# Create release for the entire codebase with GitHub CLI (NEVER GitHub web interface)
gh release create v0.4.1 \
  --title "Release v0.4.1" \
  --notes "Release notes for version 0.4.1"

# Create draft release
gh release create v0.4.1 \
  --title "Draft Release v0.4.1" \
  --draft \
  --notes "Draft release notes"

# List releases
gh release list

# View release details
gh release view v0.4.1
```

#### Automated Release Workflow
```bash
# Combined release process (PREFERRED uv run commands)
#!/bin/bash
set -e

echo "🏗️  Building packages..."
uv run hatchling build

echo "✅ Checking packages..."
uv run twine check dist/*

echo "🎉 Creating GitHub release for the entire codebase (BEFORE PyPI pushes)..."
gh release create v0.4.1 \
  --title "Release v0.4.1" \
  --notes "Automated release v0.4.1"

echo "📦 Publishing to TestPyPI (MANDATORY FIRST)..."
uv run twine upload --repository testpypi dist/*

echo "⏳ Waiting for TestPyPI validation..."
# Add verification step here if needed

echo "🚀 Publishing to production PyPI (ONLY AFTER TestPyPI SUCCESS)..."
uv run twine upload dist/*

echo "✅ Release complete!"
```

### Package-Specific Deployment

#### lib_package (todowrite)
```bash
cd lib_package
uv run hatchling build
gh release create v0.4.1 --title "todowrite v0.4.1"  # GitHub release for codebase FIRST
uv run twine upload --repository testpypi dist*       # TestPyPI SECOND
uv run twine upload dist/*                            # Production PyPI THIRD
```

#### cli_package (todowrite_cli)
```bash
cd cli_package
uv run hatchling build
gh release create v0.4.1 --title "todowrite_cli v0.4.1"  # GitHub release for codebase FIRST
uv run twine upload --repository testpypi dist*           # TestPyPI SECOND
uv run twine upload dist/*                                # Production PyPI THIRD
```

#### web_package (todowrite_web) - When Ready
```bash
cd web_package
uv run hatchling build
gh release create v0.4.1 --title "todowrite_web v0.4.1"  # GitHub release for codebase FIRST
uv run twine upload --repository testpypi dist*           # TestPyPI SECOND
uv run twine upload dist/*                                # Production PyPI THIRD
```

### Version Management

#### Central Version Control
```bash
# Update VERSION file (centralized version source)
echo "0.4.2" > VERSION

# Update all packages
scripts/update_all_versions.py

# Build and release
./scripts/release_all.sh
```

#### Version Bumping
```bash
# Bump patch version
scripts/bump_version.py patch

# Bump minor version
scripts/bump_version.py minor

# Bump major version
scripts/bump_version.py major
```

### FORBIDDEN Tools (NEVER USE)

❌ **NEVER use setuptools for building**
❌ **NEVER use setup.py install**
❌ **NEVER use GitHub web interface for releases**
❌ **NEVER use pip install -e for production builds**

### REQUIRED Tools (ALWAYS USE)

✅ **hatchling** - Build system
✅ **twine** - PyPI/TestPyPI publishing
✅ **gh** (GitHub CLI) - GitHub releases
✅ **uv** - Package management and build execution

### Deployment Checklist

Before any deployment:

- [ ] Version updated in central VERSION file
- [ ] All packages built with `uv run hatchling build` (PREFERRED & RECOMMENDED)
- [ ] Packages validated with `uv run twine check`
- [ ] GitHub release created with `gh release create` (FIRST)
- [ ] TestPyPI deployment completed and validated (SECOND)
- [ ] Production PyPI deployment completed (THIRD - ONLY AFTER TestPyPI SUCCESS)
- [ ] Documentation updated with new version
- [ ] CHANGELOG.md updated with release notes

This configuration ensures consistent, reliable deployments across all ToDoWrite packages using modern Python packaging standards.

---

**IMPORTANT:** This deployment configuration is stored in MCP episodic memory and must be followed for ALL ToDoWrite package deployments.
