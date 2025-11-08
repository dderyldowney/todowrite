# ToDoWrite Documentation

**Version**: 0.3.1
**Status**: Production Ready
**Last Updated**: November 8, 2025

## Documentation Overview

Welcome to the ToDoWrite documentation suite. This comprehensive guide covers everything from getting started to advanced usage and development.

## Quick Start

1. **[Installation Guide](installation.md)** - Get ToDoWrite installed and running
2. **[Integration Guide](INTEGRATION_GUIDE.md)** - Learn how to use ToDoWrite in real projects
3. **[Main Project README](../README.md)** - Project overview and quick start examples

## Core Documentation

### Getting Started
- **[Installation Guide](installation.md)** - Complete installation instructions for all platforms
- **[Integration Guide](INTEGRATION_GUIDE.md)** - Step-by-step integration examples and tutorials
- **[Main Project Documentation](../README.md)** - Project overview, features, and quick start

### User Guides
- **[Project Utilities](PROJECT_UTILITIES.md)** - Available utilities and helper functions
- **[Status Tracking](STATUS_TRACKING.md)** - Progress and status management features
- **[CLI Reference](../cli_package/README.md)** - Complete command-line interface reference

### Developer Documentation
- **[Contributing Guidelines](../CONTRIBUTING.md)** - How to contribute to the project
- **[Project Architecture](../MONOREPO_STRUCTURE.md)** - Monorepo structure and organization
- **[Build System](../BUILD_SYSTEM.md)** - Build system documentation and workflows
- **[Version Management](../VERSION_MANAGEMENT.md)** - Centralized version management system

### Quality Assurance
- **[Verification Report](VERIFICATION_REPORT.md)** - Comprehensive testing and verification results
- **[PyPI Publishing Guide](../PyPI_HOWTO.md)** - Package publishing and release procedures

## Documentation Structure

```
docs/
├── README.md                    # This file - documentation index
├── installation.md              # Installation guide
├── INTEGRATION_GUIDE.md         # Integration examples and tutorials
├── PROJECT_UTILITIES.md         # Available utilities and helpers
├── STATUS_TRACKING.md           # Status and progress tracking
└── VERIFICATION_REPORT.md       # Testing and verification results

../
├── README.md                    # Main project documentation
├── CONTRIBUTING.md              # Contribution guidelines
├── MONOREPO_STRUCTURE.md        # Project architecture
├── BUILD_SYSTEM.md              # Build system documentation
├── VERSION_MANAGEMENT.md        # Version management system
├── PyPI_HOWTO.md                # Publishing guide
└── cli_package/README.md        # CLI reference
```

## Recommended Reading Order

### For New Users
1. [Installation Guide](installation.md) - Install ToDoWrite
2. [Main Project README](../README.md) - Understand the project
3. [Integration Guide](INTEGRATION_GUIDE.md) - See real examples
4. [CLI Reference](../cli_package/README.md) - Learn command-line usage

### For Developers
1. [Installation Guide](installation.md) - Development setup
2. [Contributing Guidelines](../CONTRIBUTING.md) - Contribution workflow
3. [Project Architecture](../MONOREPO_STRUCTURE.md) - Understand the codebase
4. [Build System](../BUILD_SYSTEM.md) - Build and release processes
5. [Version Management](../VERSION_MANAGEMENT.md) - Version control workflow

### For Advanced Users
1. [Project Utilities](PROJECT_UTILITIES.md) - Advanced utilities
2. [Status Tracking](STATUS_TRACKING.md) - Progress management
3. [Verification Report](VERIFICATION_REPORT.md) - Quality assurance details

## Key Features Covered

### Hierarchical Task Management
- **12 Layers**: Goal → Concept → Context → Constraints → Requirements → AcceptanceCriteria → InterfaceContract → Phase → Step → Task → SubTask → Command
- **Database Storage**: SQLite and PostgreSQL support
- **Schema Validation**: JSON Schema validation ensures data integrity

### Status and Progress Tracking
- **5 Status Types**: planned, in_progress, completed, blocked, cancelled
- **Progress Tracking**: 0-100% progress monitoring
- **Date Tracking**: Started and completion dates
- **Assignee Management**: User assignment and tracking

### Import/Export Capabilities
- **YAML Support**: Layer-based YAML file organization
- **Database Sync**: Bidirectional synchronization
- **Backup/Restore**: Complete project backup utilities

### Development Features
- **Type Safety**: Comprehensive type hints with Python 3.12+ syntax
- **Real Testing**: 157 tests with actual implementations (no mocking)
- **Static Analysis**: MyPy, Ruff, and Black compliance
- **Pre-commit Hooks**: Automated quality gates

## Current Project Status

- **Version**: 0.3.1
- **Python**: 3.12+ required
- **Tests**: 157/157 passing ✅
- **Coverage**: 54.25%
- **Documentation**: Complete and current ✅
- **Build Status**: Production ready ✅

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/dderyldowney/todowrite/issues)
- **Discussions**: [GitHub Discussions](https://github.com/dderyldowney/todowrite/discussions)
- **Documentation**: This comprehensive guide
- **Examples**: [Integration Guide](INTEGRATION_GUIDE.md)

## Contributing to Documentation

We welcome improvements to the documentation! Please see the [Contributing Guidelines](../CONTRIBUTING.md) for information on how to contribute.

When updating documentation:
1. Keep information current with the codebase
2. Include working examples
3. Update cross-references when adding new files
4. Follow the existing documentation style
5. Test all code examples

## Quick Links

- **[Install Now](installation.md)** →
- **[See Examples](INTEGRATION_GUIDE.md)** →
- **[CLI Reference](../cli_package/README.md)** →
- **[Contribute](../CONTRIBUTING.md)** →

---

**Project**: [ToDoWrite](https://github.com/dderyldowney/todowrite)
**License**: [MIT](https://opensource.org/licenses/MIT)
**Python**: 3.12+
**Status**: Production Ready ✅
