# ToDoWrite Release Workflow

This document outlines the enhanced release process for ToDoWrite that includes automated README badge updates.

## 🚀 Enhanced Release Process

The release process has been improved to ensure README.md badges automatically stay synchronized with version numbers.

### Prerequisites

- Ensure all tests pass: `python -m pytest tests/ -v`
- Verify code quality: `ruff check lib_package/src cli_package/src`
- Checkout develop branch: `git checkout develop`
- Ensure develop is up to date: `git pull origin develop`

### Step-by-Step Release Process

#### 1. Version Bump (Enhanced)

The `bump_version.py` script now automatically updates both the VERSION file and README.md badges:

```bash
# For explicit version
python scripts/bump_version.py 0.4.1

# For incremental bumps
python scripts/bump_version.py patch    # 0.4.0 → 0.4.1
python scripts/bump_version.py minor    # 0.4.0 → 0.5.0
python scripts/bump_version.py major    # 0.4.0 → 1.0.0

# Verify current status
python scripts/bump_version.py --verify-only

# Preview changes before applying
python scripts/bump_version.py 0.4.1 --dry-run
```

**What the script does:**
1. ✅ **Verifies** current README badges match VERSION file
2. ✅ **Updates** README.md badges to new version
3. ✅ **Updates** VERSION file to new version
4. ✅ **Verifies** both files are correctly updated
5. ✅ **Reports** what was changed

#### 2. Commit Changes

Both README.md and VERSION file changes are committed together:

```bash
git add README.md VERSION
git commit -m "feat: bump version to 0.4.1

- Update VERSION file to 0.4.1
- Update README.md badges to reflect new version
- Prepare for 0.4.1 release

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

#### 3. Switch and Merge to Main

```bash
git checkout main
git pull origin main
git merge develop
```

#### 4. Tag and Push

```bash
# Tag the new version
git tag v0.4.1

# Push everything
git push origin main
git push origin develop
git push origin v0.4.1
```

#### 5. Create GitHub Release

```bash
# Create automated release notes
gh release create v0.4.1 --title "ToDoWrite v0.4.1" --generate-notes
```

#### 6. Publish to PyPI

```bash
# Test on TestPyPI first
./scripts/publish.sh test clean

# If successful, publish to production PyPI
./scripts/publish.sh prod clean
```

#### 7. Return to Develop

```bash
git checkout develop
git pull origin develop
```

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

## 🔍 Verification Process

The enhanced system includes automatic verification:

1. **Pre-bump verification**: Ensures README matches current VERSION
2. **Post-bump verification**: Confirms README shows new version
3. **Pattern matching**: Validates badge format consistency

## 📋 Release Checklist

Before each release, verify:

- [ ] All tests pass: `python -m pytest tests/ -v`
- [ ] Code quality checks pass: `ruff check`
- [ ] README badges are current: `python scripts/bump_version.py --verify-only`
- [ ] Version bump succeeds: `python scripts/bump_version.py X.Y.Z`
- [ ] Changes committed: `git add README.md VERSION && git commit`
- [ ] Branches merged: `git merge develop` (on main)
- [ ] Tags created: `git tag vX.Y.Z`
- [ ] Pushed to remote: `git push` all branches and tags
- [ ] GitHub release created: `gh release create`
- [ ] Published to TestPyPI: `./scripts/publish.sh test`
- [ ] Published to PyPI: `./scripts/publish.sh prod`
- [ ] Returned to develop: `git checkout develop`

## 🚨 Troubleshooting

### README Badge Issues

If badges don't update correctly:

```bash
# Force update to current VERSION
python scripts/bump_version.py $(cat VERSION)

# Manually verify badge patterns
grep -E "version-|todowrite-" README.md
```

### Version Mismatch

If VERSION and README disagree:

```bash
# Check current status
python scripts/bump_version.py --verify-only

# Force synchronization
python scripts/bump_version.py $(cat VERSION)
```

### Release Rollback

If a release needs to be rolled back:

```bash
# Delete tag (if not yet pushed widely)
git tag -d v0.4.1
git push origin :refs/tags/v0.4.1

# Reset main to previous commit
git checkout main
git reset --hard v0.4.0
git push --force-with-lease origin main
```

## 📚 Additional Resources

- [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md) - Detailed version management strategy
- [PyPI HOWTO](docs/PyPI_HOWTO.md) - PyPI publishing guide
- [BUILD_SYSTEM](docs/BUILD_SYSTEM.md) - Build system documentation

---

This enhanced workflow ensures that README.md badges automatically stay synchronized with version numbers, eliminating manual badge updates and preventing version mismatches in releases.
