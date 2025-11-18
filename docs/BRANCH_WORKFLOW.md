# ToDoWrite Branch Workflow Guide

## Branch Strategy Overview

We use a **GitFlow-inspired** branching model with simplified conventions tailored for our monorepo structure.

## 🌳 Main Branches

### `main`
- **Status**: Production-ready, stable code
- **Purpose**: Released versions only
- **Protection**: Direct commits prohibited, PRs required
- **When to merge**: Only from `develop` after release preparation

### `develop`
- **Status**: Next version integration branch
- **Purpose**: Stabilization of completed features for next release
- **Protection**: Direct commits prohibited, PRs required
- **When to merge**: Only from feature branches after completion

## 🚀 Feature Branches

**ALL development work happens on feature branches off `develop`**

### Branch Naming Convention

```bash
# Format: <type>/<short-description>
feature/user-authentication
fix/cli-version-sync
refactor/cleanup-legacy-code
docs/api-documentation
test/database-tests
build/uv-sync-integration
```

### Branch Types

- **`feature/`**: New functionality
- **`fix/`**: Bug fixes
- **`refactor/`**: Code restructuring without functional changes
- **`docs/`**: Documentation updates
- **`test/`**: Test additions or improvements
- **`build/`**: Build system or CI/CD changes
- **`chore/`**: Maintenance tasks (dependencies, config, etc.)

## 🔄 Workflow Process

### 1. Start New Work
```bash
# Always start from the latest develop
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### 2. Development Work
- **Work only on your feature branch**
- **Commit frequently with conventional commits**
- **Keep develop updated**: `git checkout develop && git pull`
- **Rebase your branch**: `git checkout feature/your-feature && git rebase develop`

### 3. Complete Work
```bash
# Ensure your branch is up to date
git checkout develop
git pull origin develop
git checkout feature/your-feature
git rebase develop

# Run tests and quality checks
./dev_tools/build.sh dev

# Push and create PR
git push origin feature/your-feature
```

### 4. Pull Request Process
- **Target**: Always PR to `develop` (never to `main`)
- **Title**: Use conventional commit format
- **Description**: Clear description of changes
- **Requirements**:
  - All tests pass
  - Code quality checks pass
  - Documentation updated if needed
  - Breaking changes documented

### 5. Merge to Develop
- **Merge method**: Squash and merge (clean history)
- **Delete branch**: After successful merge
- **Update local**: `git checkout develop && git pull origin develop`

## 🚦 Branch Protection Rules

### `develop` Branch
- ❌ **No direct commits**
- ❌ **No force pushes**
- ✅ **PR reviews required**
- ✅ **CI/CD must pass**
- ✅ **Up-to-date with base branch**

### `main` Branch
- ❌ **No direct commits**
- ❌ **No force pushes**
- ✅ **PR reviews required** (from develop only)
- ✅ **CI/CD must pass**
- ✅ **Release tag required**

## 📝 Conventional Commit Standards

```bash
# Format: <type>(<scope>): <description>

feat(cli): add version synchronization feature
fix(database): resolve connection timeout issue
refactor(models): simplify active record patterns
docs(readme): update installation instructions
test(api): add comprehensive endpoint coverage
build(deps): update uv to latest version
chore(version): bump to 0.6.0
```

### Types
- **`feat`**: New feature
- **`fix`**: Bug fix
- **`refactor`**: Code refactoring
- **`docs`**: Documentation
- **`test`**: Testing
- **`build`**: Build system/dependencies
- **`chore`**: Maintenance

### Scopes
- **Package-based**: `lib`, `cli`, `web`
- **Layer-based**: `database`, `api`, `models`, `storage`
- **Component-based**: `auth`, `validation`, `testing`

## 🔄 Integration Process

### Feature → Develop
1. Feature completed and tested
2. PR created targeting `develop`
3. Code review and CI/CD validation
4. Merge to `develop` (squash merge)
5. Feature branch deleted

### Develop → Main (Release)
1. `develop` deemed release-ready
2. Create release branch: `git checkout -b release/v0.6.0`
3. Final testing and bug fixes
4. Update version numbers and changelog
5. Merge to `main` with tag: `git tag v0.6.0`
6. Merge `main` back to `develop`: `git checkout develop && git merge main`
7. Push all: `git push origin main develop --tags`

## 🛠️ Practical Commands

### Daily Development
```bash
# Start new feature
git checkout develop && git pull
git checkout -b feature/new-cool-thing

# Keep updated
git checkout develop && git pull
git checkout feature/new-cool-thing && git rebase develop

# Finish feature
./dev_tools/build.sh dev
git push origin feature/new-cool-thing
```

### Emergency Hotfix (from main)
```bash
# Create hotfix from main
git checkout main && git pull
git checkout -b hotfix/critical-bug-fix

# Fix and test
# ... make changes ...
./dev_tools/build.sh test

# Merge back to main and develop
git checkout main && git merge --no-ff hotfix/critical-bug-fix
git tag v0.5.1
git checkout develop && git merge --no-ff hotfix/critical-bug-fix
git push origin main develop --tags
git branch -d hotfix/critical-bug-fix
```

## 📋 Branch Status Commands

```bash
# See all branches
git branch -a

# See branch tracking
git branch -vv

# See branch status
git status --porcelain --branch

# See recent commits on branch
git log --oneline -10

# See differences with develop
git diff develop...HEAD
```

## ⚠️ Important Rules

1. **NEVER commit directly to `develop` or `main`**
2. **ALWAYS work on feature branches**
3. **KEEP branches short-lived** (days, not weeks)
4. **USE conventional commits** consistently
5. **REBASE before merging** to keep history clean
6. **DELETE merged branches** to keep repo clean
7. **PULL frequently** to avoid conflicts
8. **TEST thoroughly** before PR

## 🔍 Branch Hygiene

### Good Branch Names
```bash
✅ feature/user-authentication
✅ fix/cli-version-sync
✅ refactor/cleanup-legacy-code
✅ docs/api-documentation
```

### Bad Branch Names
```bash
❌ feature-branch
❌ stuff
❌ temp
❌ user-auth-feature-working
❌ fix-cli-version
```

This workflow ensures clean history, proper isolation of work, and smooth integration process while maintaining the stability of both `main` and `develop` branches.
