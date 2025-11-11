# ToDoWrite Project Knowledge Base

## Core Architecture

### 12-Layer Hierarchical Framework
The ToDoWrite system implements a **12-layer declarative planning framework**:

1. **Goal** - Strategic objectives and high-level goals
2. **Concept** - Core ideas and fundamental principles
3. **Context** - Environmental conditions and background information
4. **Constraint** - Limitations and boundary conditions
5. **Requirement** - Specific functional and non-functional requirements
6. **AcceptanceCriteria** - Success criteria and validation conditions
7. **InterfaceContract** - API contracts and interface specifications
8. **Phase** - Major project phases and milestones
9. **Step** - Individual implementation steps and actions
10. **Task** - Work units and actionable items
11. **SubTask** - Detailed breakdown of tasks
12. **Command** - Executable commands and shell operations

### Technology Stack

#### Core Technologies
- **Language**: Python 3.12+ with strict static typing
- **Database**: SQLAlchemy 2.0 with SQLite (default) and PostgreSQL support
- **Validation**: JSON Schema 4.17+ for data validation
- **Configuration**: YAML 6.0+ for human-readable configuration
- **CLI Framework**: Click 8.1+ for command-line interface

#### Build and Quality Tools
- **Build System**: Hatchling with custom version extraction
- **Type Checking**: Pyright in strict mode (100% type coverage)
- **Code Formatting**: Ruff for formatting, linting, import sorting
- **Testing**: pytest with pytest-cov, pytest-asyncio
- **Security**: Bandit for security scanning
- **Pre-commit**: Automated quality gates

## Package Implementation Status

### lib_package/ (todowrite)
**Status**: ✅ Production Ready
**Version**: 0.4.1
**Features**:
- Full 12-layer hierarchy implementation
- Complete Python API with type safety
- Database abstraction (SQLite + PostgreSQL)
- YAML import/export functionality
- Comprehensive validation system
- 100% test coverage with real implementations

**Key Components**:
```python
# Core API
from todowrite import ToDoWrite

app = ToDoWrite(database_path="project.db")
goal = app.create_node("goal", "Implement User Authentication", "Create secure auth system")
task = app.create_node("task", "Design Database Schema", "Design user database schema")
app.link_nodes(goal["id"], task["id"])
```

### cli_package/ (todowrite-cli)
**Status**: ✅ Production Ready (Limited)
**Version**: 0.4.1
**Features**:
- Complete CLI interface for 4 layers (Goal, Task, Concept, Command)
- Multiple output formats (table, JSON, YAML)
- Configuration management
- Interactive mode support
- Import/export operations

**Limitation**: Only supports 4/12 layers currently

**Available Commands**:
```bash
# Core operations
todowrite create --goal "My Goal" --description "Goal description"
todowrite get NODE-ID
todowrite update NODE-ID --title "New Title"
todowrite delete NODE-ID
todowrite list --layer goal
todowrite search "query terms"

# Data operations
todowrite export-yaml --output project.yaml
todowrite import-yaml --input project.yaml
todowrite db-status
```

### web_package/ (todowrite-web)
**Status**: 🚧 **Currently in Development**
**Version**: In development
**Current Focus**: Active development work in progress
- REST API for all 12 layers
- React/Vue.js frontend
- Real-time collaboration
- Multi-user support
- Visual hierarchy navigation

## Database Schema

### Core Tables
```sql
-- Main nodes table (supports all 12 layers)
CREATE TABLE nodes (
    id TEXT PRIMARY KEY,
    layer TEXT NOT NULL,  -- One of the 12 layer types
    title TEXT NOT NULL,
    description TEXT,
    metadata TEXT,        -- JSON string for additional data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Parent-child relationships
CREATE TABLE node_relationships (
    parent_id TEXT NOT NULL,
    child_id TEXT NOT NULL,
    relationship_type TEXT DEFAULT 'parent-child',
    FOREIGN KEY (parent_id) REFERENCES nodes(id),
    FOREIGN KEY (child_id) REFERENCES nodes(id),
    PRIMARY KEY (parent_id, child_id)
);

-- Cross-references and links
CREATE TABLE node_links (
    source_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    link_type TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (source_id) REFERENCES nodes(id),
    FOREIGN KEY (target_id) REFERENCES nodes(id),
    PRIMARY KEY (source_id, target_id, link_type)
);
```

### Supported Storage Backends
1. **SQLite**: Default, file-based, suitable for development
2. **PostgreSQL**: Production-ready, supports multiple connections
3. **YAML Files**: Human-readable, suitable for version control

## Development Standards

### Code Quality Requirements
- **100% Type Coverage**: No `Any` types allowed
- **80%+ Test Coverage**: Measured with pytest-cov
- **Zero Mocking Policy**: Use real implementations only
- **Security Hardened**: All subprocess calls use shell=False
- **Documentation**: Complete docstrings with examples

### Testing Philosophy
```python
# Real implementation testing only
def test_create_node():
    with tempfile.NamedTemporaryFile() as tmp:
        app = ToDoWrite(database_path=tmp.name)
        node = app.create_node("goal", "Test Goal", "Description")

        assert node["id"].startswith("GOAL-")
        assert node["type"] == "goal"
        assert node["title"] == "Test Goal"

        # Verify database persistence
        retrieved = app.get_node(node["id"])
        assert retrieved == node
```

### Error Handling Patterns
```python
# Structured error handling
class ToDoWriteError(Exception):
    """Base exception for ToDoWrite operations."""
    pass

class NodeNotFoundError(ToDoWriteError):
    def __init__(self, node_id: str):
        self.node_id = node_id
        super().__init__(f"Node not found: {node_id}")

class ValidationError(ToDoWriteError):
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"Validation error in {field}: {message}")
```

## Build and Release Process

### Version Management
- **Central Version**: Single `VERSION` file in project root
- **Automatic Sync**: `shared_version.py` updated by pre-commit hook
- **Semantic Versioning**: MAJOR.MINOR.PATCH pattern
- **Release Automation**: GitHub Actions for publishing

### Build Commands
```bash
# Development setup
./setup_dev.sh

# Build all packages
./scripts/build.sh

# Run full test suite
./scripts/test.sh

# Publish to TestPyPI
./scripts/publish.sh

# Publish to PyPI (production)
./scripts/publish.sh prod
```

### Quality Gates
- **Pre-commit hooks**: Automatic formatting and linting
- **CI Pipeline**: Full test suite on every commit
- **Security Scans**: Bandit integration in CI
- **Type Checking**: Pyright validation in CI

## Performance Characteristics

### Database Performance
- **Indexed Queries**: Optimized for common lookup patterns
- **Connection Pooling**: SQLAlchemy 2.0 async support
- **Batch Operations**: Support for bulk node operations
- **Query Caching**: Memory caching for frequently accessed data

### Memory Efficiency
- **Lazy Loading**: Large datasets loaded on demand
- **Dataclasses with slots**: Memory-efficient node storage
- **Generator Patterns**: Streaming operations for large result sets
- **Resource Cleanup**: Proper context management

### CLI Performance
- **Fast Startup**: Minimal import overhead
- **Concurrent Operations**: Async support for I/O operations
- **Progress Indicators**: Rich integration for user feedback
- **Caching**: Smart caching for repeated operations

## Security Considerations

### Input Validation
- **JSON Schema**: Comprehensive data validation
- **SQL Injection Prevention**: SQLAlchemy parameterized queries
- **Path Traversal Protection**: pathlib for file operations
- **Command Injection Prevention**: subprocess with shell=False

### Data Protection
- **Secure Defaults**: No insecure configurations
- **Input Sanitization**: All user inputs validated
- **Error Handling**: No sensitive data in error messages
- **Audit Trail**: Operation logging for security monitoring

### File Operations
```python
# Secure file operations
def safe_file_operation(file_path: Path, operation: Callable[[Path], T]) -> T:
    """Perform file operation with security checks."""
    # Validate path is within allowed directory
    if not file_path.resolve().is_relative_to(allowed_base_path):
        raise SecurityError("Path traversal attempt detected")

    # Check file permissions
    if file_path.exists() and not os.access(file_path, os.R_OK):
        raise PermissionError(f"No read access to {file_path}")

    return operation(file_path)
```

## Known Issues and Limitations

### Current Limitations
1. **CLI Layer Support**: Only 4/12 layers accessible via CLI
2. **Web Package**: Not yet implemented
3. **Performance**: Large datasets (>10K nodes) may need optimization
4. **Documentation**: API reference incomplete for some layers

### Technical Debt
- **Zero Technical Debt**: All code quality checks pass
- **Test Coverage**: 157/157 tests passing
- **Security**: Zero high-priority security issues
- **Dependencies**: All dependencies up-to-date

## Future Development Plans

### Short-term (Q1 2025)
- **CLI Enhancement**: Support for all 12 layers
- **Performance Optimization**: Improved query performance
- **Documentation**: Complete API reference
- **Testing**: Integration test suite expansion

### Medium-term (Q2 2025)
- **Web Package**: Basic web interface implementation
- **REST API**: Complete API for all operations
- **Real-time Features**: WebSocket support
- **Collaboration**: Multi-user capabilities

### Long-term (Q3-Q4 2025)
- **Enterprise Features**: User management, permissions
- **Advanced Analytics**: Project progress tracking
- **Integration**: Third-party tool integrations
- **Mobile**: Progressive web app support

## Debugging and Troubleshooting

### Common Issues
1. **Database Locks**: Use connection pooling, handle timeouts
2. **Memory Usage**: Implement streaming for large datasets
3. **Type Errors**: Use Pyright strict mode for early detection
4. **Import Issues**: Verify PYTHONPATH and package installation

### Debugging Tools
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Database query debugging
import sqlalchemy as sa
engine = sa.create_engine(database_url, echo=True)

# Performance profiling
import cProfile
cProfile.run('app.list_nodes()')
```

### Development Utilities
```bash
# Database inspection
todowrite db-status

# Export/import for debugging
todowrite export-yaml --output debug.yaml
todowrite import-yaml --input debug.yaml

# Validation
python -c "from todowrite import ToDoWrite; ToDoWrite().validate_schema()"
```

## External Dependencies

### Core Dependencies
- **sqlalchemy>=2.0.23**: Database ORM and abstraction
- **jsonschema>=4.17.3**: Data validation
- **pyyaml>=6.0.1**: YAML configuration support
- **click>=8.1.0**: CLI framework (cli_package)

### Development Dependencies
- **pytest>=7.0.0**: Testing framework
- **pytest-cov>=4.0.0**: Coverage measurement
- **black>=24.0.0**: Code formatting (replaced by Ruff)
- **ruff>=0.6.0**: Formatting, linting, import sorting
- **pyright>=1.1.0**: Static type checking
- **bandit>=1.7.0**: Security scanning

This knowledge base provides comprehensive information about the ToDoWrite project architecture, implementation details, and development practices for efficient future development work.
