# ToDoWrite Library Documentation

**Comprehensive Python library documentation for ToDoWrite.**

---

## 🚀 Quick Start

### Installation
```bash
pip install todowrite
```

### Basic Usage
```python
from todowrite import ToDoWrite, link_nodes

# Initialize
app = ToDoWrite("sqlite:///project.db")
app.init_database()

# Create nodes
goal = app.[REMOVED_LEGACY_PATTERN]({
    "id": "GOAL-001",
    "layer": "Goal",
    "title": "Build TodoWrite App",
    "description": "Create the application",
    "metadata": {"owner": "dev-team"}
})

task = app.[REMOVED_LEGACY_PATTERN]({
    "id": "TSK-001",
    "layer": "Task",
    "title": "Set up database",
    "description": "Initialize database schema",
    "metadata": {"owner": "dev-team"}
})

# Link nodes
link_nodes("sqlite:///project.db", goal.id, task.id)

# Get all nodes
all_nodes = app.get_all_nodes()
```

## 📚 Documentation Sections

### User Guides
- **[Integration Guide](guides/INTEGRATION_GUIDE.md)** - How to integrate ToDoWrite into applications
- **[How-To Guide](guides/ToDoWrite-HOWTO.md)** - Comprehensive usage examples

### Examples
- **[Code Examples](examples/README.md)** - Practical examples and patterns *(coming soon)*

## 🔧 Development

For library development documentation, see the shared development resources:

- **[Development Guide](../shared/development/README.md)** - Development workflow and setup
- **[Build System](../shared/development/BUILD_SYSTEM.md)** - Build system and tools
- **[Database Architecture](../shared/development/UNIVERSAL_DATABASE_ARCHITECTURE.md)** - Database design and patterns

## 🌐 Generated Documentation

For automatically generated API documentation:

**📖 [Live Library Documentation](https://todowrite.davidderyldowney.com/library/)**

### API Coverage
- **Core Classes** - `ToDoWrite`, `NodeManager`, etc.
- **Database Layer** - Models, connections, migrations
- **Storage Backends** - SQLite, PostgreSQL, YAML
- **Tools & Utilities** - Validation, tracing, linting

## 🏗️ Architecture

The todowrite library follows a layered architecture:

1. **Core Layer** (`core/`) - Main application logic and node management
2. **Database Layer** (`database/`) - Database models and operations
3. **Storage Layer** (`storage/`) - Storage backends and abstraction
4. **Tools Layer** (`tools/`) - Validation, tracing, and utility functions

---

**Last Updated**: 2025-11-17
**Package**: `todowrite`
**Status**: Production Ready
