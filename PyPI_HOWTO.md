# PyPI Publishing Guide

This guide covers how to build and publish both `todowrite` and `todowrite-cli` packages to PyPI.

## Prerequisites

### Install Required Tools
```bash
# Install build tools
pip install hatchling twine pyright

# Or install via the root pyproject.toml
pip install -e .  # This installs all dev dependencies including hatch, twine, and pyright
```

### Verify PyPI Credentials
Ensure your `~/.pypirc` file is properly configured with TestPyPI as the active API key:

```ini
[pypi]
# username = __token__
# password = your-production-pypi-api-token

[testpypi]
username = __token__
password = your-testpypi-api-token

[distutils]
index-servers =
    pypi
    testpypi
```

## Package Overview

### Library Package (`todowrite`)
- **Name**: `todowrite`
- **Version**: `0.2.0`
- **Directory**: `lib_package/`
- **Dependencies**: `sqlalchemy>=2.0.0`, `jsonschema>=4.0.0`, `pyyaml>=6.0`
- **Entry Point**: Library import (`from todowrite import ToDoWrite`)
- **Type Checking**: Uses pyright for static type analysis

### CLI Package (`todowrite-cli`)
- **Name**: `todowrite-cli`
- **Version**: `0.2.0`
- **Directory**: `cli_package/`
- **Dependencies**: `todowrite>=0.2.0`, `click>=8.0.0`, `rich>=13.0.0`
- **Entry Point**: CLI command (`todowrite`)
- **Type Checking**: Uses pyright for static type analysis

## Building Packages

### Build with Hatchling (Recommended)
```bash
# Build library package
cd lib_package
python -m hatchling build

# Build CLI package
cd ../cli_package
python -m hatchling build
```

### Alternative: Using Hatch CLI
```bash
# Build library package
cd lib_package
hatch build

# Build CLI package
cd ../cli_package
hatch build
```

### Check Build Artifacts
```bash
cd lib_package
ls dist/          # Should see todowrite-0.2.0-py3-none-any.whl and todowrite-0.2.0.tar.gz

cd ../cli_package
ls dist/          # Should see todowrite-cli-0.2.0-py3-none-any.whl and todowrite-cli-0.2.0.tar.gz
```

## Testing Builds (Optional but Recommended)

### Local Testing
```bash
# Test library package
cd lib_package
pip install dist/*.whl
python -c "import todowrite; print(f'Version: {todowrite.__version__}')"

# Test CLI package
cd ../cli_package
pip install dist/*.whl
todowrite --version
```

## Publishing Process

### Step 1: Publish to TestPyPI (Recommended First)
```bash
# Build both packages
cd lib_package
python -m hatchling build

# Upload to TestPyPI
twine upload --repository testpypi dist/*

cd ../cli_package
python -m hatchling build
twine upload --repository testpypi dist/*
```

### Step 2: Verify TestPyPI Installation
```bash
# Install and test from TestPyPI
pip install --index-url https://test.pypi.org/simple/ todowrite
pip install --index-url https://test.pypi.org/simple/ todowrite-cli

# Test functionality
todowrite --help
python -c "from todowrite import ToDoWrite; print('Library imported successfully')"
```

### Step 3: Publish to Production PyPI
```bash
# Switch ~/.pypirc to use production API key
# Uncomment the pypi section and comment out testpypi

# Build both packages
cd lib_package
python -m hatchling build

# Upload to Production PyPI
twine upload dist/*

cd ../cli_package
python -m hatchling build
twine upload dist/*
```

## Automated Publishing with Hatch

### Using Hatch Publish Command
```bash
# For the library package
cd lib_package
hatch publish --repository testpypi   # TestPyPI
hatch publish                         # Production PyPI

# For the CLI package
cd ../cli_package
hatch publish --repository testpypi   # TestPyPI
hatch publish                         # Production PyPI
```

## Troubleshooting

### Common Issues

1. **Build Errors**
   ```bash
   # Clean previous builds
   cd lib_package
   rm -rf build/ dist/

   cd ../cli_package
   rm -rf build/ dist/
   ```

2. **Authentication Issues**
   ```bash
   # Test PyPI connection
   twine check --strict dist/*
   twine upload --repository testpypi --dry-run dist/*
   ```

3. **Type Checking Issues**
   ```bash
   # Run pyright type checking
   cd lib_package
   pyright todowrite/

   cd ../cli_package
   pyright todowrite_cli/
   ```

4. **Version Conflicts**
   - Ensure both packages have the same version number
   - Library must be published before CLI (due to dependency)

5. **Dependency Issues**
   ```bash
   # Check dependencies
   cd lib_package
   pip check

   cd ../cli_package
   pip check
   ```

### Build Verification
```bash
# Verify wheel contents
cd lib_package
pip install wheel
wheel unpack dist/todowrite-0.2.0-py3-none-any.whl

cd ../cli_package
wheel unpack dist/todowrite-cli-0.2.0-py3-none-any.whl
```

## Security Best Practices

1. **Use API Tokens**: Never use username/password
2. **Test First**: Always publish to TestPyPI first
3. **Clean Builds**: Remove old build artifacts
4. **Verify Signatures**: Consider signing your packages
5. **Two-Factor Auth**: Enable 2FA on PyPI account

## Automation Tips

### Version Management
- Keep both packages in sync
- Consider using tools like `bump2version` or `hatch version bump`
- Update versions in both `lib_package/todowrite/version.py` and `cli_package/todowrite_cli/version.py`

### Build Scripts
Create a build script in the root directory:
```bash
#!/bin/bash
# build-and-publish.sh

echo "Building todowrite library..."
cd lib_package
python -m hatchling build
twine upload --repository testpypi dist/*

echo "Building todowrite-cli..."
cd ../cli_package
python -m hatchling build
twine upload --repository testpypi dist/*

echo "Build and publish complete!"
```

Make it executable:
```bash
chmod +x build-and-publish.sh
```

### Clean Up Script
```bash
#!/bin/bash
# clean-builds.sh

echo "Cleaning build artifacts..."
cd lib_package
rm -rf build/ dist/

cd ../cli_package
rm -rf build/ dist/

echo "Clean complete!"
```

## Monitoring

### Check Package Status
```bash
# Check PyPI status
curl -s https://pypi.org/pypi/todowrite/json | jq .info.version
curl -s https://pypi.org/pypi/todowrite-cli/json | jq .info.version

# Check TestPyPI status
curl -s https://test.pypi.org/pypi/todowrite/json | jq .info.version
curl -s https://test.pypi.org/pypi/todowrite-cli/json | jq .info.version
```

## CI/CD Integration

When setting up automated pipelines (see next section), remember:

1. **Build Order**: Library first, then CLI
2. **Version Syncing**: Both packages must have identical versions
3. **Test Environment**: TestPyPI for testing, PyPI for production
4. **Security**: Use GitHub secrets for PyPI tokens
5. **Notifications**: Add success/failure notifications

---

*This guide should be updated whenever package configurations or build processes change.*
