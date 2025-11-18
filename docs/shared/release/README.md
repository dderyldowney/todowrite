# Release Process

**Release management and deployment procedures for ToDoWrite with ActiveRecord-inspired architecture.**

---

## 🚀 Release Workflow

### 1. Development Phase (develop branch)
- ✅ ActiveRecord model implementation
- ✅ Association management (has_many, belongs_to)
- ✅ Migration system
- ✅ Query builder
- ✅ Model validations

### 2. Testing Phase
```bash
# Full test suite
./dev_tools/build.sh test

# Documentation build
./dev_tools/build.sh docs

# Quality gates
./dev_tools/build.sh quality-gate
```

### 3. Release Phase
```bash
# Update version
echo "0.5.0" > VERSION

# Tag release
git tag v0.5.0

# Deploy to PyPI
./dev_tools/deploy.sh pypi
```

## 📋 Current Release Status

### **Version 0.4.1** - Current
- ✅ Basic Sphinx documentation system
- ✅ Documentation reorganization
- ✅ TDD implementation
- ✅ Build system integration

### **Version 0.5.0** - Next Release
- 🔄 ActiveRecord-inspired architecture
- 🔄 Model relationships and associations
- 🔄 Migration system
- 🔄 Updated API documentation

## 🔧 Release Tools

### Build System Integration
```bash
# Build all packages
./dev_tools/build.sh build

# Prepare for release
./dev_tools/build.sh release

# Validate build system
./dev_tools/build.sh validate
```

### Documentation Deployment
```bash
# Build documentation
./dev_tools/build.sh docs

# Deploy to GitHub Pages (automatic on push to develop)
git push origin develop
```

---

**Last Updated**: 2025-11-17
**Architecture**: ActiveRecord-inspired
**Next Release**: 0.5.0
