# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2024-11-03

### 🚀 MAJOR RELEASE BREAKING CHANGES

This major release represents a significant architectural overhaul of the ToDoWrite project. While the core API remains backward compatible, the project structure and build system have been completely restructured.

### 🏗️ ADDED

#### **Monorepo Restructuring**
- **Python Packaging Standards Compliance**: Complete restructure to follow official Python packaging guidelines
- **Self-Contained Packages**: Both `todowrite` library and `todowrite_cli` are now completely self-contained packages
- **Standard src/ Layout**: Both packages now use the standard `src/` directory structure
- **Independent Development**: Each package can be developed, tested, and released independently
- **Proper Build Configuration**: All build configurations updated for the new structure

#### **Centralized Version Management**
- **Single Source of Truth**: Version numbers now managed from a single `VERSION` file
- **Automatic Synchronization**: Both library and CLI packages always have identical versions
- **Version Management CLI**: `scripts/bump_version.py` for easy version updates
- **Dynamic Versioning**: Build system reads version from VERSION file automatically
- **Version Validation**: Built-in validation prevents invalid version strings

#### **Development Infrastructure**
- **Comprehensive Documentation**: `MONOREPO_STRUCTURE.md` and `VERSION_MANAGEMENT.md` added
- **Asyncio Warning Fix**: Resolved pytest-asyncio deprecation warnings
- **Code Quality Improvements**: Fixed linting issues and improved code quality standards
- **Enhanced Testing**: All 114 tests pass with new structure

### 🔧 CHANGED

#### **Project Structure**
```
# BEFORE (Non-standard)
todowrite/
├── lib_package/todowrite/          # Library at package root
├── cli_package/todowrite_cli/      # CLI at package root

# AFTER (Standards-compliant)
todowrite/
├── lib_package/
│   ├── src/todowrite/             # Library in src/ layout
│   └── pyproject.toml
├── cli_package/
│   ├── src/todowrite_cli/         # CLI in src/ layout
│   └── pyproject.toml
└── VERSION                        # Single version source
```

#### **Build Configuration**
- Both packages now use `dynamic = ["version"]` in pyproject.toml
- Build targets updated for new src/ structure
- Coverage paths and test configurations updated
- Tool configurations (pyright, ruff, pytest) updated

#### **Version Management**
- **Before**: Manual updates across 4 separate files
- **After**: Single command updates entire project

### 🚨 BREAKING CHANGES

#### **Development Setup Changes**
- **Python Path**: Now requires `PYTHONPATH="lib_package/src:cli_package/src"` for development
- **Editable Installation**: Must install both packages separately:
  ```bash
  pip install -e lib_package/
  pip install -e cli_package/
  ```
- **Build Commands**: Package-specific build commands:
  ```bash
  cd lib_package && python -m build
  cd ../cli_package && python -m build
  ```

#### **Import Changes**
- No breaking changes to public APIs
- All existing imports work unchanged
- Internal package structure reorganized but external API preserved

### ✅ IMPROVEMENTS

#### **Developer Experience**
- **Professional Python Workflows**: Now follows packaging best practices
- **Easier Onboarding**: Familiar structure for Python developers
- **Better Dependency Management**: Clear separation between packages
- **Independent Release Cycles**: Library and CLI can be released independently

#### **Build System**
- **Automated Versioning**: No more manual version coordination
- **Standard Python Packaging**: Compatible with standard Python tools
- **Better Testing**: Isolated test environments for each package
- **Code Quality**: Enhanced linting and type checking

#### **Documentation**
- **Comprehensive Guides**: Added detailed structure and version management docs
- **Migration Guide**: Clear instructions for moving to new structure
- **Development Documentation**: Improved workflow documentation

### 📈 Impact Assessment

#### **For Users**
- ✅ **No Breaking API Changes**: All existing code continues to work
- ✅ **Improved Stability**: Better packaging and dependency management
- ✅ **Enhanced Documentation**: More comprehensive guides and documentation

#### **For Developers**
- ✅ **Professional Setup**: Now follows Python packaging standards
- ✅ **Easier Contribution**: Familiar structure and workflows
- ✅ **Better Testing**: Isolated and improved test environments
- ⚠️ **Setup Changes**: Requires learning new project structure

#### **For Maintainers**
- ✅ **Simplified Releases**: Centralized version management
- ✅ **Independent Packages**: Can release library and CLI separately
- ✅ **Better CI/CD**: Standard Python packaging workflows
- ✅ **Reduced Maintenance**: Single source of truth for versions

### 🔄 Migration Guide

#### **For Users**
No action required - all existing code continues to work unchanged.

#### **For Developers**
```bash
# New development setup
pip install -e lib_package/
pip install -e cli_package/

# Updated testing
PYTHONPATH="lib_package/src:cli_package/src" python -m pytest tests/

# Updated building
cd lib_package && python -m build
cd ../cli_package && python -m build
```

### 📝 Technical Notes

- **Backward Compatibility**: Maintained for all public APIs
- **Performance**: No performance impact from structural changes
- **Dependencies**: No new external dependencies added
- **Testing**: All 114 tests continue to pass
- **Documentation**: Fully updated for new structure

### 🎉 Summary

This release represents a major architectural improvement while maintaining full backward compatibility. The changes establish a solid foundation for future development and make the project more maintainable and contributor-friendly.

**Key Outcomes:**
- 🏗️ **Professional Python Packaging**: Follows official standards
- 🔧 **Centralized Management**: Single source of truth for versions
- 📚 **Enhanced Documentation**: Comprehensive guides and documentation
- 🧪 **Improved Testing**: Better isolated test environments
- 🚀 **Developer Experience**: Familiar workflows and structure

## [0.2.2] - 2024-10-29

### ✅ IMPROVEMENTS

- **Performance**: Enhanced database query optimization
- **Documentation**: Updated installation and usage guides
- **CLI**: Improved error messages and user feedback
- **Stability**: Better error handling and edge case management

## [0.2.1] - 2024-10-15

### ✅ IMPROVEMENTS

- **Documentation**: Comprehensive API documentation
- **Testing**: Added integration tests for CLI workflows
- **Stability**: Improved YAML import/export reliability
- **CLI**: Enhanced status tracking functionality

## [0.2.0] - 2024-10-01

### 🚀 MAJOR FEATURES

- **Command Layer**: Added support for shell commands and artifact tracking
- **Enhanced CLI**: Improved command-line interface with better help system
- **YAML Integration**: Improved synchronization between YAML files and database
- **Status Tracking**: Enhanced status management across all node types

### ✅ IMPROVEMENTS

- **Performance**: Significant performance improvements for large projects
- **Documentation**: Complete rewrite of documentation and guides
- **Testing**: Expanded test coverage with integration tests
- **Error Handling**: Better error messages and recovery mechanisms

## [0.1.0] - 2024-09-15

### 🚀 INITIAL RELEASE

- **Core Library**: Complete ToDoWrite library with 12-layer framework
- **CLI Interface**: Full command-line interface for all operations
- **Database Support**: SQLAlchemy-based storage with PostgreSQL and SQLite support
- **YAML Integration**: Import/export functionality for project files
- **Comprehensive Testing**: Full test suite with high coverage
