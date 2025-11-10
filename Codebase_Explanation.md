# ToDoWrite Codebase Explanation

## Overview
**ToDoWrite** is a sophisticated **hierarchical task management system** designed for managing complex software projects. It's built as a Python monorepo with a clean separation between core business logic and user interfaces.

## Architecture

### 1. **Monorepo Structure**
```
todowrite/
├── lib_package/          # Core library (business logic)
├── cli_package/          # Command-line interface
├── web_package/          # Web interface (Docker-based)
├── tests/               # Comprehensive test suite
├── scripts/             # Build/deployment automation
├── docs/                # Documentation
└── dev_tools/           # Development utilities
```

### 2. **Core Library (lib_package)**
The heart of the system with these key components:

#### **Hierarchical Data Model**
- **13 Layer Types**: Goal → Concept → Context → Requirements → AcceptanceCriteria → InterfaceContract → Phase → Step → Task → SubTask → Command
- **5 Status Types**: planned, in_progress, completed, blocked, cancelled
- **Rich Metadata**: owner, labels, severity, work_type, assignee

#### **Multi-Backend Storage**
1. **PostgreSQL** (primary)
2. **SQLite** (fallback)
3. **YAML files** (last resort)
4. **Automatic fallback** with smart detection

#### **Core Classes**
- `Node` (`lib_package/src/todowrite/core/types.py:72`): Main entity with hierarchical relationships
- `ToDoWrite` (`lib_package/src/todowrite/core/app.py`): Primary orchestration class
- Database models (`lib_package/src/todowrite/database/models.py`): SQLAlchemy ORM models

### 3. **CLI Interface (cli_package)**
Rich terminal interface built with Click and Rich:
- **CRUD Operations**: create, get, list, update, delete
- **Status Management**: progress tracking, status updates
- **Import/Export**: YAML synchronization, bulk operations
- **Search**: Text-based search across all nodes

### 4. **Key Features**

#### **Schema Validation**
- JSONSchema validation across all storage backends
- Cross-platform data integrity guarantees
- Automatic migration and synchronization

#### **Command System**
- Executable commands with artifacts
- Output capture and storage
- Integration with development workflows

#### **Development Tools**
- `tw_validate`: Node validation
- `tw_trace`: Relationship tracing
- `tw_lint_soc`: Social coding linting
- `extract_schema`: Schema extraction

### 5. **Build System & Development**

#### **Modern Python Tooling**
- **uv**: Modern package management (recently integrated)
- **Hatchling**: Build backend with shared version management
- **Ruff**: All-in-one linting and formatting
- **Pytest**: Testing with coverage requirements

#### **Quality Assurance**
- Pre-commit hooks for code quality
- Comprehensive type annotations (Python 3.12+)
- Security auditing with Bandit
- 46+ test files covering all components

### 6. **Data Flow**

```
User Input → CLI → Core Library → Storage Backend
                ↓
          Schema Validation
                ↓
          Database/YAML Storage
```

## Key Strengths

1. **Modular Design**: Clear separation of concerns
2. **Type Safety**: Comprehensive type annotations
3. **Multi-Backend Support**: Flexible storage with fallbacks
4. **Rich CLI**: Modern terminal interface
5. **Extensible**: Plugin architecture for new features
6. **Production Ready**: Comprehensive testing and error handling

## Current State
- **Active Development**: Recent commits show uv integration and cleanup
- **Mature Architecture**: Well-established patterns and comprehensive feature set
- **Build Issue**: There's a known issue with the hatchling build process mentioned in recent conversations

The codebase represents a well-engineered approach to hierarchical task management, balancing flexibility, reliability, and developer experience.
