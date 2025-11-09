# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-11-09

### 🚀 MAJOR RELEASE - Claude Code Integration & Release Automation

#### **Enhanced Version Management System**
- **Automated README Badge Updates**: Version badges in README.md now update automatically
- **Enhanced Bump Script**: `scripts/bump_version.py` with `--verify-only`, `--dry-run`, and incremental bumps
- **Zero Maintenance Overhead**: No more manual version updates across documentation
- **Single Source of Truth**: Centralized version management eliminates mismatches

#### **Comprehensive Release Documentation**
- **Complete Release Workflow**: 8-step process from development to production
- **RELEASE_WORKFLOW.md**: Detailed step-by-step guide with verification checkpoints
- **RELEASE_QUICK_REFERENCE.md**: Ultra-fast reference for experienced maintainers
- **Troubleshooting & Rollback**: Complete procedures for error scenarios

#### **Claude Code Integration**
- **Session Initialization**: Automatic Claude Code session setup
- **Development Environment**: Token optimization and agent control systems
- **Project Context**: Automatic loading of project information
- **Enhanced Tooling**: Development tools organized in `dev_tools/` directory

#### **Documentation Cleanup & Standardization**
- **Version Reference Elimination**: Removed hardcoded versions from 14+ documentation files
- **Dynamic Version References**: All docs now point to VERSION file for current version
- **Essential Versions Only**: Preserved Python 3.12+, SQLAlchemy 2.0+, and tool versions
- **Professional Documentation**: No more outdated version references

#### **Enhanced Publishing Process**
- **Automated Publishing**: `./scripts/publish.sh` handles TestPyPI and PyPI publishing
- **Verification Steps**: Always test on TestPyPI before production
- **Quality Assurance**: Package integrity checks and detailed logging
- **GitHub Integration**: Automated release notes creation

#### **Development Workflow Improvements**
- **Pre-commit Enhancements**: Added protection for main branch commits
- **Branch Protection**: Enforced develop → main workflow
- **Quality Gates**: Enhanced verification at every release step
- **Documentation Accuracy**: All docs reflect current project state and usage patterns

#### **Improved Usability**
- **Better Error Messages**: Enhanced error handling throughout the codebase
- **Streamlined Installation**: Clear installation instructions and requirements
- **Enhanced CLI Experience**: Better help text and command organization
- **Performance Optimizations**: Improved response times and resource usage

---

## [0.3.1] - 2025-01-08

### 🏗️ ENHANCEMENTS

#### **Complete Type Annotations Implementation**
- **100% Type Coverage**: All classes, methods, functions, and variables now have complete type hints
- **Python 3.12+ Syntax**: Modern type annotation syntax using `str | None` instead of `Optional[str]`
- **SQLAlchemy 2 Types**: Proper integration with SQLAlchemy 2's type system throughout the codebase
- **Zero Any Types**: Eliminated all `Any` type usage - replaced with precise, specific types
- **Type Safety**: No `pass` statements or type ignores used to gain compliance

#### **Advanced Type System Features**
- **Type Variables**: Implemented `TypeVar`, `ParamSpec`, and proper generic typing patterns
- **Function Overloads**: Added proper overload signatures with `Concatenate` for complex functions
- **TypeAlias**: Used `TypeAlias` for complex data structures improving readability
- **Proper Cast Usage**: Replaced type ignores with proper `cast()` calls where needed

#### **Import System Improvements**
- **Explicit Imports**: Replaced star imports with explicit imports throughout the codebase
- **Complete __all__ Lists**: All modules have complete `__all__` exports for better IDE support
- **Fixed Import Chains**: Resolved circular import issues and cleaned up import dependencies

#### **Code Quality Enhancements**
- **Ruff Integration**: Complete integration with ruff for formatting and linting
- **Modern Python Practices**: Updated to follow current Python 3.12+ best practices
- **Error Handling**: Enhanced type safety in exception handling and error paths
- **Documentation**: Updated docstrings to reflect type improvements

### 🧪 TESTING
- **All Tests Pass**: All 119 tests continue to pass with new type annotations
- **Type Validation**: Tests now validate type correctness as well as functionality
- **No Mocking**: Maintained commitment to real implementations over test doubles

### 📚 DEVELOPER EXPERIENCE
- **IDE Support**: Enhanced IDE autocompletion and type checking support
- **Documentation**: Type hints serve as in-code documentation for better developer experience
- **Error Messages**: More helpful error messages from static type analysis
- **Refactoring Safety**: Type system provides safety nets for future refactoring

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
