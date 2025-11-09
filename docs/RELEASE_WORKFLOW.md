# 🚀 Complete ToDoWrite Release Process

This document provides the **complete, step-by-step process** for releasing ToDoWrite from development to production (GitHub, TestPyPI, and PyPI).

## 📋 Prerequisites Checklist

Before starting any release, verify:

- [ ] All tests pass: `python -m pytest tests/ -v`
- [ ] Code quality checks pass: `ruff check lib_package/src cli_package/src`
- [ ] You're on develop branch: `git branch` should show `* develop`
- [ ] Develop is up to date: `git pull origin develop`
- [ ] No uncommitted changes: `git status` should be clean

---

## 🎯 Step 1: Version Bump (Enhanced System)

### 1.1 Current Status Verification
```bash
# Check current version status
python scripts/bump_version.py --verify-only
```
**Expected Output:**
```
Current version: 0.4.0
🔍 Verifying README.md versions...
✅ README.md badges correctly show version 0.4.0
```

### 1.2 Bump Version
```bash
# For patch release (0.4.0 → 0.4.1)
python scripts/bump_version.py patch

# For minor release (0.4.0 → 0.5.0)
python scripts/bump_version.py minor

# For major release (0.4.0 → 1.0.0)
python scripts/bump_version.py major

# OR explicit version
python scripts/bump_version.py 0.4.1
```

**What the script does automatically:**
1. ✅ Verifies current README badges match VERSION file
2. ✅ Updates README.md badges to new version
3. ✅ Updates VERSION file to new version
4. ✅ Verifies both files are correctly updated
5. ✅ Reports what changed

### 1.3 Verify Bump Success
```bash
# Confirm the bump worked
python scripts/bump_version.py --verify-only
```
**Expected Output:**
```
Current version: 0.4.1
🔍 Verifying README.md versions...
✅ README.md badges correctly show version 0.4.1
```

---

## 📝 Step 2: Commit Version Changes

### 2.1 Stage and Commit
```bash
# Stage both files (they must be committed together)
git add README.md VERSION

# Commit with proper message format
git commit -m "feat: bump version to 0.4.1

- Update VERSION file to 0.4.1
- Update README.md badges to reflect new version
- Prepare for 0.4.1 release

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 2.2 Push to Develop
```bash
# Push version bump to develop branch
git push origin develop
```

---

## 🌟 Step 3: Merge to Main Branch

### 3.1 Switch to Main
```bash
git checkout main
```

### 3.2 Update Main
```bash
# Ensure main is up to date
git pull origin main
```

### 3.3 Merge Develop
```bash
# Merge develop into main (fast-forward preferred)
git merge develop
```

### 3.4 Verify Merge
```bash
# Check merge was successful
git log --oneline -3
git status
```
**Expected:** You should see the version bump commit as the latest commit.

---

## 🏷️ Step 4: Tag and Push to GitHub

### 4.1 Create Version Tag
```bash
# Create annotated tag for the new version
git tag v0.4.1
```

### 4.2 Push Everything to GitHub
```bash
# Push main branch
git push origin main

# Push develop branch
git push origin develop

# Push the tag
git push origin v0.4.1
```

### 4.3 Verify GitHub Status
```bash
# Check remote status
git remote -v
git branch -vv
git tag -l | grep v0.4.1
```

---

## 🎉 Step 5: Create GitHub Release

### 5.1 Automated Release Notes
```bash
# Create GitHub release with auto-generated notes
gh release create v0.4.1 --title "ToDoWrite v0.4.1" --generate-notes
```

### 5.2 Custom Release Notes (Optional)
```bash
# Create release with custom notes
gh release create v0.4.1 \
  --title "ToDoWrite v0.4.1 - Bug Fixes and Improvements" \
  --notes "## Changes
- Fixed progress field storage issue
- Updated documentation
- Enhanced error handling

## Installation
\`\`\`bash
pip install todowrite==0.4.1
pip install todowrite-cli==0.4.1
\`\`\`"
```

### 5.3 Verify GitHub Release
- Visit: https://github.com/dderyldowney/todowrite/releases
- Confirm release exists with correct tag and notes
- Check that source code archive is available

---

## 🧪 Step 6: Publish to TestPyPI (Verification)

### 6.1 Build and Publish to TestPyPI
```bash
# Clean build and publish to TestPyPI
./scripts/publish.sh test clean
```

**Expected Output:**
```
[INFO] Publishing to TestPyPI
Repository URL: https://test.pypi.org/
Packages will be available at:
  - https://test.pypi.org/project/todowrite/
  - https://test.pypi.org/project/todowrite-cli/
...
[SUCCESS] All done! 🚀
```

### 6.2 Verify TestPyPI Publication
```bash
# Verify packages exist on TestPyPI
curl -s https://test.pypi.org/pypi/todowrite/0.4.1/json | jq -r '.info.version'
curl -s https://test.pypi.org/pypi/todowrite-cli/0.4.1/json | jq -r '.info.version'
```

**Expected Output:** Both commands should return `0.4.1`

### 6.3 Test Install from TestPyPI (Optional but Recommended)
```bash
# Create temporary test environment
python -m venv test_env
source test_env/bin/activate

# Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ todowrite==0.4.1
pip install --index-url https://test.pypi.org/simple/ todowrite-cli==0.4.1

# Test functionality
todowrite --help

# Cleanup
deactivate
rm -rf test_env
```

---

## 🚀 Step 7: Publish to Production PyPI

### 7.1 Confirm TestPyPI Success
**Only proceed if TestPyPI publication was successful!**

### 7.2 Publish to Production PyPI
```bash
# Publish to production PyPI
./scripts/publish.sh prod clean
```

**Expected Output:**
```
[INFO] Publishing to Production PyPI
Repository URL: https://pypi.org/
Packages will be available at:
  - https://pypi.org/project/todowrite/
  - https://pypi.org/project/todowrite-cli/
...
[SUCCESS] All done! 🚀
```

### 7.3 Verify PyPI Publication
```bash
# Verify packages exist on PyPI
curl -s https://pypi.org/pypi/todowrite/0.4.1/json | jq -r '.info.version'
curl -s https://pypi.org/pypi/todowrite-cli/0.4.1/json | jq -r '.info.version'
```

**Expected Output:** Both commands should return `0.4.1`

### 7.4 Test Production Install (Optional but Recommended)
```bash
# Create fresh test environment
python -m venv prod_test
source prod_test/bin/activate

# Test install from production PyPI
pip install todowrite==0.4.1
pip install todowrite-cli==0.4.1

# Test functionality
todowrite --help

# Cleanup
deactivate
rm -rf prod_test
```

---

## 🔄 Step 8: Return to Development

### 8.1 Switch Back to Develop
```bash
git checkout develop
```

### 8.2 Update Develop
```bash
# Ensure develop is up to date
git pull origin develop
```

### 8.3 Verify Status
```bash
git status
git branch -v
```
**Expected:** You should be on develop branch and it should be up to date.

---

## 🛠️ Version Management Tools

### Enhanced Bump Script Features

The `scripts/bump_version.py` script includes several enhancements:

#### New Flags:
- `--verify-only`: Check if README badges match current VERSION
- `--dry-run`: Preview what changes would be made
- `patch/minor/major`: Incremental version bumps

#### Examples:
```bash
# Check current status
python scripts/bump_version.py --verify-only

# Preview a version bump
python scripts/bump_version.py 0.4.1 --dry-run

# Incremental bump
python scripts/bump_version.py patch

# Explicit version
python scripts/bump_version.py 1.0.0
```

### Automated README Updates

The script automatically updates these README badges:
- Version badge: `[![Version X.Y.Z](https://img.shields.io/badge/version-X.Y.Z-green.svg)]`
- PyPI library badge: `[![PyPI](https://img.shields.io/badge/todowrite-X.Y.Z-blue.svg)]`
- PyPI CLI badge: `[![PyPI CLI](https://img.shields.io/badge/todowrite--cli-X.Y.Z-blue.svg)]`

---

## ⚠️ Troubleshooting & Rollback Procedures

### If Git Push Fails
```bash
# Force push local changes (use carefully)
git push --force-with-lease origin main
git push --force-with-lease origin develop
```

### If Tag Push Fails
```bash
# Delete local tag and recreate
git tag -d v0.4.1
git tag v0.4.1
git push origin v0.4.1

# Delete remote tag if needed
git push --delete origin v0.4.1
git push origin v0.4.1
```

### If TestPyPI Fails
```bash
# Check build artifacts
ls lib_package/dist/
ls cli_package/dist/

# Manually check package integrity
twine check lib_package/dist/*
twine check cli_package/dist/*

# Retry publish
./scripts/publish.sh test clean
```

### If PyPI Fails
```bash
# Check if version already exists on PyPI
curl -s https://pypi.org/pypi/todowrite/ | grep -o '0\.4\.1' || echo "Version not on PyPI"

# Check for PyPI authentication issues
twine upload --repository testpypi --verbose lib_package/dist/todowrite-*.whl
```

### Complete Rollback (Emergency Only)
```bash
# WARNING: This removes the release from public view
# Only use if something is seriously wrong

# Delete tag (local and remote)
git tag -d v0.4.1
git push --delete origin v0.4.1

# Reset main to previous commit
git checkout main
git reset --hard v0.4.0
git push --force-with-lease origin main

# Delete GitHub release (via CLI or web interface)
gh release delete v0.4.1 --yes
```

---

## ✅ Post-Release Verification Checklist

After completing the release:

- [ ] **GitHub Release**: https://github.com/dderyldowney/todowrite/releases/tag/v0.4.1 exists
- [ ] **PyPI Packages**: https://pypi.org/project/todowrite/ and /todowrite-cli/ show 0.4.1
- [ ] **TestPyPI**: Packages available for testing (optional verification)
- [ ] **Install Test**: `pip install todowrite==0.4.1` works
- [ ] **CLI Test**: `todowrite --help` shows correct version
- [ ] **Git Status**: Clean working directory on develop branch
- [ ] **Branch Status**: Both main and develop are up to date

---

## 📚 Quick Reference Commands

```bash
# Complete release process (patch release example)
python scripts/bump_version.py patch
git add README.md VERSION
git commit -m "feat: bump version to X.Y.Z..."
git push origin develop
git checkout main
git pull origin main
git merge develop
git tag vX.Y.Z
git push origin main develop vX.Y.Z
gh release create vX.Y.Z --title "ToDoWrite vX.Y.Z" --generate-notes
./scripts/publish.sh test clean
# Verify TestPyPI success, then:
./scripts/publish.sh prod clean
git checkout develop
git pull origin develop
```

---

## 🔗 Related Documentation

- [CONTRIBUTING.md](../CONTRIBUTING.md) - Development contribution guidelines
- [PyPI HOWTO](PyPI_HOWTO.md) - Detailed PyPI publishing information
- [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md) - Version management strategy
- [BUILD_SYSTEM.md](BUILD_SYSTEM.md) - Build system documentation

This process ensures **reliable, repeatable releases** with verification at every step and clear rollback procedures if anything goes wrong. The enhanced version bump system eliminates manual version updates across documentation while maintaining complete traceability.
