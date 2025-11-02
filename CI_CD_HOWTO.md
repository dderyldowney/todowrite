# CI/CD Automation Guide

This guide covers the automated build and publishing workflows for both `todowrite` and `todowrite-cli` packages.

## Overview

The project includes three GitHub Actions workflows for automated publishing:

1. **`publish-lib.yml`** - Library package publishing
2. **`publish-cli.yml`** - CLI package publishing
3. **`publish-both.yml`** - Combined package publishing with version management

## Available Workflows

### 1. Library Package Workflow (`publish-lib.yml`)

**Trigger Conditions:**
- On GitHub release publication
- Manual workflow dispatch

**Features:**
- Runs tests on Python 3.12
- Uploads coverage to Codecov
- Builds and validates package
- Publishes to PyPI (on release) or TestPyPI (manual)

**Manual Dispatch Options:**
- `test_pypi`: Publish to TestPyPI instead of PyPI

### 2. CLI Package Workflow (`publish-cli.yml`)

**Trigger Conditions:**
- On GitHub release publication
- Manual workflow dispatch

**Features:**
- Runs tests on Python 3.12
- Uploads coverage to Codecov
- Builds and validates package
- Publishes to PyPI (on release) or TestPyPI (manual)
- Optional wait for library publishing

**Manual Dispatch Options:**
- `test_pypi`: Publish to TestPyPI instead of PyPI
- `wait_for_lib`: Wait for library package to be published first

### 3. Combined Package Workflow (`publish-both.yml`)

**Trigger Conditions:**
- Manual workflow dispatch only

**Features:**
- Version bumping capability
- Parallel testing for both packages
- Sequential publishing (library first, then CLI)
- TestPyPI option for testing

**Manual Dispatch Options:**
- `test_pypi`: Publish to TestPyPI instead of PyPI
- `version_bump`: Automatic version bump (major/minor/patch)

## Setup Requirements

### GitHub Secrets Configuration

You need to configure these GitHub repository secrets:

1. **`PYPI_API_TOKEN`** - Production PyPI API token
2. **`TEST_PYPI_API_TOKEN`** - TestPyPI API token
3. **`GITHUB_TOKEN`** - Automatically provided by GitHub Actions

### PyPI Token Setup

1. **Production PyPI Token:**
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token with "Upload/Download" permissions
   - Add it as `PYPI_API_TOKEN` secret in GitHub repository

2. **TestPyPI Token:**
   - Go to https://test.pypi.org/manage/account/token/
   - Create a new API token with "Upload/Download" permissions
   - Add it as `TEST_PYPI_API_TOKEN` secret in GitHub repository

### Trusted Publishing (Recommended)

Modern PyPI supports trusted publishing. Configure this in your PyPI account settings:

1. **Production PyPI:**
   - Go to https://pypi.org/manage/project/todowrite/release/
   - Set up trusted publishing for the GitHub repository

2. **TestPyPI:**
   - Go to https://test.pypi.org/manage/project/todowrite/release/
   - Set up trusted publishing for the GitHub repository

## Workflow Usage

### Publishing on Release

When you create a GitHub release, both `publish-lib.yml` and `publish-cli.yml` will automatically:

1. Run tests for both packages
2. Build both packages
3. Publish to production PyPI

### Manual Publishing

#### Single Package Publishing

**Library Package:**
1. Go to Actions tab
2. Select "Publish todowrite Library to PyPI"
3. Click "Run workflow"
4. Check "Publish to TestPyPI" for testing
5. Click "Run workflow"

**CLI Package:**
1. Go to Actions tab
2. Select "Publish todowrite-cli to PyPI"
3. Click "Run workflow"
4. Check "Publish to TestPyPI" for testing
5. Optionally check "Wait for library to be published first"
6. Click "Run workflow"

#### Combined Package Publishing

1. Go to Actions tab
2. Select "Publish Both Packages to PyPI"
3. Click "Run workflow"
4. Choose options:
   - `test_pypi`: Check to publish to TestPyPI
   - `version_bump`: Select version bump type if needed
5. Click "Run workflow"

## Workflow Dependencies

### Publishing Order

The workflows ensure proper dependency management:

1. **Library Package** → **CLI Package**
   - CLI depends on library (`todowrite>=0.2.0`)
   - Library must be published first
   - CLI will wait for library if configured

### Version Management

Both packages must have synchronized versions:

- **Library**: `lib_package/todowrite/version.py`
- **CLI**: `cli_package/todowrite_cli/version.py`

## Security Features

### Environment Protection

- **Production PyPI**: Requires approval via environment protection
- **TestPyPI**: Separate environment for testing
- **Code Review**: Mandatory reviewers for production releases

### Permission Scopes

- **id-token**: Write permission for trusted publishing
- **Contents**: Read access for repository
- **Actions**: Write access for workflow execution

## Monitoring and Notifications

### Success Indicators

- ✅ All tests pass
- ✅ Build artifacts uploaded
- ✅ Package published successfully
- ✅ Coverage reports uploaded to Codecov

### Failure Scenarios

- ❌ Tests fail: Workflow stops, no publishing
- ❌ Build fails: Workflow stops, no publishing
- ❌ Publishing fails: Retries with different repository URL

### Notifications

Add Slack/email notifications by extending the workflows:

```yaml
- name: Send Slack notification
  if: always()
  uses: rtCamp/action-slack-notify@v2
  env:
    SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
    SLACK_COLOR: ${{ job.status }}
    SLACK_MESSAGE: 'Package ${{ matrix.package }} ${{ job.status }}'
```

## Troubleshooting

### Common Issues

1. **Authentication Failures**
   - Verify PyPI tokens are correctly configured
   - Check token permissions (Upload/Download)
   - Ensure trusted publishing is enabled

2. **Build Failures**
   - Clean local builds: `rm -rf build/ dist/`
   - Check Python version compatibility
   - Verify dependencies are satisfied

3. **Test Failures**
   - Check test coverage requirements
   - Verify pytest configuration
   - Check for code quality issues

4. **Dependency Issues**
   - Ensure library is published before CLI
   - Check version compatibility
   - Verify dependency versions

### Debug Mode

Run workflows with debug output:

```bash
# Set debug flag in workflow
- name: Debug
  if: github.event_name == 'workflow_dispatch'
  run: |
    echo "Debug information..."
    echo "Python version: $(python --version)"
    echo "Working directory: $(pwd)"
```

### Local Testing

Test packages locally before publishing:

```bash
# Build and install locally
cd lib_package
python -m build
pip install dist/*.whl

cd ../cli_package
python -m build
pip install dist/*.whl
```

## Best Practices

1. **Test First**: Always publish to TestPyPI first
2. **Version Sync**: Keep both packages in sync
3. **Testing**: Ensure all tests pass before publishing
4. **Security**: Use trusted publishing when possible
5. **Monitoring**: Monitor package downloads and issues
6. **Documentation**: Keep this guide updated with workflow changes

## Workflow Customization

### Adding New Steps

Extend workflows by adding new steps in appropriate sections:

```yaml
- name: Custom step
  run: |
    # Your custom command
    echo "Running custom step"
```

### Adding New Python Versions

Update the `matrix.python-version` section:

```yaml
strategy:
  matrix:
    python-version: ['3.11', '3.12', '3.13']
```

### Adding New Tests

Extend test matrix or add additional test suites:

```yaml
- name: Run type checking
  run: |
    cd cli_package
    pyright todowrite_cli/
```

---

*This guide should be updated whenever workflow configurations change.*