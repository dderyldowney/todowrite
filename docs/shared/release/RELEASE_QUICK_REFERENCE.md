# 🚀 ToDoWrite Release Quick Reference

**Complete release process from development to production in minutes!**

## ⚡ Ultra-Fast Release (When You're Experienced)

```bash
# 1. Bump version (choose one)
python scripts/bump_version.py patch    # 0.4.0 → 0.4.1
python scripts/bump_version.py minor    # 0.4.0 → 0.5.0
python scripts/bump_version.py 0.4.1   # Explicit version

# 2. Commit version bump
git add README.md VERSION
git commit -m "feat: bump version to 0.4.1"

# 3. Push and merge to main
git push origin develop
git checkout main && git pull origin main
git merge develop

# 4. Tag and push
git tag v0.4.1
git push origin main develop v0.4.1

# 5. Create GitHub release
gh release create v0.4.1 --generate-notes

# 6. Publish (TestPyPI first, then PyPI)
./scripts/publish.sh test clean
./scripts/publish.sh prod clean

# 7. Return to development
git checkout develop && git pull origin develop
```

---

## 📋 Pre-Release Checklist

**Before you start:**
- [ ] On `develop` branch: `git branch`
- [ ] Clean working directory: `git status`
- [ ] Tests pass: `python -m pytest tests/ -v`
- [ ] Code quality passes: `ruff check lib_package/src cli_package/src`

**Quick verification:**
```bash
python scripts/bump_version.py --verify-only
```

---

## 🎯 Version Bump Options

### Incremental Bumps (Recommended)
```bash
python scripts/bump_version.py patch    # Bug fixes (0.4.0 → 0.4.1)
python scripts/bump_version.py minor    # New features (0.4.0 → 0.5.0)
python scripts/bump_version.py major    # Breaking changes (0.4.0 → 1.0.0)
```

### Explicit Version
```bash
python scripts/bump_version.py 0.4.1
```

### Verification Tools
```bash
# Check current status
python scripts/bump_version.py --verify-only

# Preview changes
python scripts/bump_version.py 0.4.1 --dry-run
```

---

## 🔄 Git Workflow Summary

```bash
# From develop to production
# 1. Bump and commit on develop
# 2. Push develop
# 3. Switch to main, merge develop
# 4. Tag and push everything
# 5. Create GitHub release
# 6. Publish packages
# 7. Return to develop
```

**Branch flow:** `develop` → `main` → `tag` → `GitHub` → `PyPI`

---

## 🧪 Publishing Verification

### TestPyPI Verification
```bash
# Check if packages exist
curl -s https://test.pypi.org/pypi/todowrite/0.4.1/json | jq -r '.info.version'
curl -s https://test.pypi.org/pypi/todowrite-cli/0.4.1/json | jq -r '.info.version'

# Test install (optional)
pip install --index-url https://test.pypi.org/simple/ todowrite==0.4.1
```

### PyPI Verification
```bash
# Check if packages exist
curl -s https://pypi.org/pypi/todowrite/0.4.1/json | jq -r '.info.version'
curl -s https://pypi.org/pypi/todowrite-cli/0.4.1/json | jq -r '.info.version'

# Test install (optional)
pip install todowrite==0.4.1
```

---

## ✅ Post-Release Verification

**URLs to check:**
- GitHub Release: https://github.com/dderyldowney/todowrite/releases/tag/v0.4.1
- PyPI Library: https://pypi.org/project/todowrite/
- PyPI CLI: https://pypi.org/project/todowrite-cli/

**Commands to run:**
```bash
# Verify install works
pip install todowrite==0.4.1 todowrite-cli==0.4.1
todowrite --help

# Verify git status
git status
git branch -v
```

---

## 🚨 Common Issues & Quick Fixes

### Git Push Fails
```bash
git push --force-with-lease origin main
git push --force-with-lease origin develop
```

### Tag Issues
```bash
git tag -d v0.4.1 && git tag v0.4.1
git push --delete origin v0.4.1 && git push origin v0.4.1
```

### TestPyPI Fails
```bash
# Check build artifacts
ls lib_package/dist/ cli_package/dist/
# Retry publish
./scripts/publish.sh test clean
```

### PyPI Fails
```bash
# Check if version already exists
curl -s https://pypi.org/pypi/todowrite/ | grep 0.4.1 || echo "Version available"
```

---

## 📚 Essential Documentation Links

- **Complete Process**: [RELEASE_WORKFLOW.md](RELEASE_WORKFLOW.md) - Full step-by-step guide
- **Development**: [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute
- **Version Management**: [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md) - Version strategy
- **PyPI Details**: [PyPI_HOWTO.md](PyPI_HOWTO.md) - Publishing details

---

## 🛠️ Tools Reference

### Version Management
- `scripts/bump_version.py` - Enhanced version bump script
- `VERSION` file - Single source of truth for version

### Publishing
- `scripts/publish.sh` - Automated publishing script
- `scripts/build.sh` - Build script

### Git
- `gh` - GitHub CLI for release creation
- Standard git commands for branching and tagging

---

## 💡 Pro Tips

1. **Always TestPyPI First**: Never skip the TestPyPI verification step
2. **Use Incremental Bumps**: Prefer `patch/minor/major` over explicit versions
3. **Verify Before Committing**: Use `--dry-run` to preview changes
4. **Check Git Status**: Ensure clean working directory before starting
5. **Use GitHub CLI**: `gh release create --generate-notes` saves time
6. **Keep VERSION Single Source**: Never manually edit version numbers elsewhere

---

## 🔧 Environment Setup

Ensure you have these tools installed and configured:

```bash
# Required tools
gh --version          # GitHub CLI
python --version      # Python 3.12+
pip list | grep twine  # Twine for PyPI publishing
git --version         # Git

# Check permissions
gh auth status        # GitHub authentication
```

---

**🎉 That's it! You now have everything needed for reliable ToDoWrite releases!**

For detailed troubleshooting and rollback procedures, see the complete [RELEASE_WORKFLOW.md](RELEASE_WORKFLOW.md).
