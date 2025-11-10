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
- **12 Layer Types**: Goal, Concept, Context, Constraints, Requirements, AcceptanceCriteria, InterfaceContract, Phase, Step, Task, SubTask, Command
- **6 Status Types**: planned, in_progress, completed, blocked, cancelled, rejected
- **10 Work Types**: architecture, spec, interface, validation, implementation, docs, ops, refactor, chore, test
- **Rich Metadata**: owner, labels, severity, work_type, assignee

#### **Multi-Backend Storage**
1. **PostgreSQL** (primary)
2. **SQLite** (fallback)
3. **YAML files** (last resort)
4. **Automatic fallback** with smart detection

#### **Core Library Classes**
The core library is organized into several key modules:

**Core Classes (`lib_package/src/todowrite/core/`)**
```
todowrite/core/
├── app.py
│   └── ToDoWrite
│       ├── __init__()                    # Initialize storage, schema, caching
│       ├── _clear_expired_cache()        # Clear expired cache entries
│       ├── _clear_node_cache()           # Clear cache for specific node
│       ├── get_session()                 # Get database session with caching
│       ├── get_db_session()              # Get database session
│       ├── init_database()               # Initialize database tables
│       ├── create_node()                 # Create new node
│       ├── get_node()                    # Get node by ID
│       ├── get_all_nodes()               # Get all nodes grouped by layer
│       ├── update_node()                 # Update existing node
│       ├── delete_node()                 # Delete node
│       ├── update_node_status()          # Update node status
│       ├── search_nodes()                # Search nodes by query
│       ├── export_nodes()                # Export nodes in various formats
│       ├── import_nodes()                # Import nodes from file
│       ├── add_goal()                    # Add goal node
│       ├── add_phase()                   # Add phase node
│       ├── add_step()                    # Add step node
│       ├── add_task()                    # Add task node
│       ├── add_subtask()                 # Add subtask node
│       ├── add_command()                 # Add command node
│       ├── add_concept()                 # Add concept node
│       ├── add_context()                 # Add context node
│       ├── add_constraint()              # Add constraint node
│       ├── add_requirement()             # Add requirement node
│       ├── add_acceptance_criteria()     # Add acceptance criteria node
│       ├── add_interface_contract()      # Add interface contract node
│       ├── get_active_items()            # Get active (non-completed/rejected) items
│       └── load_todos()                  # Load all todos from storage
├── app_node_updater.py
│   └── NodeUpdater
│       ├── __init__()                    # Initialize with session
│       ├── update_node_fields()          # Update basic node fields
│       ├── update_links()                # Update parent-child relationships
│       ├── update_labels()               # Update node labels
│       └── update_command()              # Update command and artifacts
├── types.py
│   ├── Node                              # Main entity dataclass
│   │   ├── to_dict()                     # Convert to dictionary
│   │   └── from_dict()                   # Create from dictionary
│   ├── Metadata                          # Metadata dataclass
│   ├── Link                              # Relationship dataclass
│   ├── Command                           # Command dataclass
│   └── Label                             # Label dataclass
├── utils.py                              # Utility functions
├── exceptions.py                         # Custom exceptions
├── constants.py                          # Constants and enums
├── project_manager.py                    # Project management utilities
└── schema.py                             # Schema definitions
```

**Database Models (`lib_package/src/todowrite/database/models.py`)**
```
todowrite/database/
└── models.py
    ├── Base                              # SQLAlchemy declarative base
    ├── Node                              # Main database entity
    │   ├── id (String, PK, NOT NULL)     # Unique identifier
    │   ├── layer (String, NOT NULL)      # Layer type (Goal, Task, etc.)
    │   ├── title (String, NOT NULL)      # Node title
    │   ├── description (Text, NULLABLE)  # Optional description
    │   ├── status (String, DEFAULT 'planned') # Status (planned, in_progress, completed, blocked, cancelled, rejected)
    │   ├── progress (Integer, NULLABLE)  # Progress percentage (0-100)
    │   ├── started_date (String, NULLABLE) # Start date (ISO format)
    │   ├── completion_date (String, NULLABLE) # Completion date (ISO format)
    │   ├── owner (String, NULLABLE)      # Node owner
    │   ├── severity (String, NULLABLE)   # Severity level (low, med, high, critical)
    │   ├── work_type (String, NULLABLE)  # Work type (architecture, implementation, test, etc.)
    │   ├── assignee (String, NULLABLE)   # Assigned person
    │   └── Relationships:
    │       ├── labels (Many-to-Many)     # → node_labels → Label
    │       ├── command (One-to-One)      # → Command (1:1)
    │       ├── parents (Many-to-Many)    # → links → Node (self-referential)
    │       └── children (Many-to-Many)   # → links → Node (self-referential)
    ├── Link                              # Parent-child relationships (Association Table)
    │   ├── parent_id (String, FK→nodes.id, PK) # Parent node ID
    │   └── child_id (String, FK→nodes.id, PK)  # Child node ID
    ├── Label                             # Tag system
    │   ├── label (String, PK, NOT NULL)  # Label name (unique)
    │   └── nodes (Many-to-Many)          # → node_labels → Node
    ├── node_labels                       # Node-Label Association Table
    │   ├── node_id (String, FK→nodes.id, PK) # Node reference
    │   └── label (String, FK→labels.label, PK) # Label reference
    ├── Command                           # Executable commands
    │   ├── node_id (String, FK→nodes.id, PK, NOT NULL) # Associated node ID
    │   ├── ac_ref (String, NULLABLE)     # Acceptance criteria reference
    │   ├── run (Text, NULLABLE)          # Command definition (JSON/YAML)
    │   └── Relationships:
    │       ├── node (One-to-One)         # ← Node (1:1)
    │       └── artifacts (One-to-Many)   # → Artifact (1:N)
    └── Artifact                          # Command outputs/artifacts
        ├── artifact (String, PK, NOT NULL) # Artifact identifier/file path
        └── command_id (String, FK→commands.node_id, PK) # Associated command
└── config.py                            # Storage configuration
```

**Database Schema Layout**
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                 ToDoWrite Database Schema                     │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│       nodes         │    │       links         │    │       labels        │
├─────────────────────┤    ├─────────────────────┤    ├─────────────────────┤
│ id (PK)             │◄──►│ parent_id (PK,FK)   │    │ label (PK)          │
│ layer (NOT NULL)    │    │ child_id (PK,FK)    │◄──►│                     │
│ title (NOT NULL)    │    └─────────────────────┘    └─────────────────────┘
│ description         │              ▲                            ▲
│ status (DEFAULT)    │              │                            │
│ progress            │              │                            │
│ started_date        │              │                            │
│ completion_date     │              │                            │
│ owner               │              │                            │
│ severity            │              │                            │
│ work_type           │              │                            │
│ assignee            │              │                            │
└─────────────────────┘              │                            │
          ▲                         │                            │
          │                         │                            │
          │                         │                            │
          │              ┌─────────────────────┐               │
          │              │    node_labels      │               │
          │              ├─────────────────────┤               │
          │              │ node_id (PK,FK)    │               │
          │              │ label (PK,FK)      │               │
          │              └─────────────────────┘               │
          │                         ▲                            │
          │                         │                            │
┌─────────────────────┐              │                            │
│      commands       │              │                            │
├─────────────────────┤              │                            │
│ node_id (PK,FK)     │◄─────────────┘                            │
│ ac_ref              │                                           │
│ run                 │                                           │
└─────────────────────┘                                           │
          ▲                                                      │
          │                                                      │
          │              ┌─────────────────────┐                 │
          │              │     artifacts       │                 │
          │              ├─────────────────────┤                 │
          │              │ artifact (PK)      │                 │
          │              │ command_id (PK,FK) │                 │
          │              └─────────────────────┘                 │
          │                                                      │
          └──────────────────────────────────────────────────────┘

**Relationship Summary:**
• nodes ↔ nodes (Many-to-Many via links) - Hierarchical parent/child relationships
• nodes ↔ labels (Many-to-Many via node_labels) - Tagging system
• nodes → commands (One-to-One) - Each node can have one command
• commands → artifacts (One-to-Many) - Commands can generate multiple artifacts

**Key Constraints:**
• All ID fields use String type for UUID/semantic IDs
• Links table uses composite primary key (parent_id, child_id)
• node_labels table uses composite primary key (node_id, label)
• Foreign key constraints ensure referential integrity
• Self-referential relationships allow unlimited hierarchy depth
```

**Storage Layer (`lib_package/src/todowrite/storage/`)**
```
todowrite/storage/
├── yaml_storage.py
│   └── YAMLStorage                       # YAML file-based storage
│       ├── __init__()                    # Initialize storage paths
│       ├── ensure_directories()          # Create required directories
│       ├── load_node()                   # Load single node from YAML
│       ├── save_node()                   # Save node to YAML file
│       ├── update_node()                 # Update existing node
│       ├── delete_node()                 # Delete node file
│       ├── load_all_nodes()              # Load all nodes from YAML
│       ├── node_exists()                 # Check if node exists
│       ├── update_node_links()           # Update node relationships
│       ├── get_nodes_by_layer()          # Get nodes by layer type
│       └── count_nodes()                 # Count total nodes
├── schema_validator.py                  # Cross-backend schema validation
└── yaml_manager.py                       # Database-YAML synchronization
```

**Tools (`lib_package/src/todowrite/tools/`)**
```
todowrite/tools/
├── tw_validate.py                        # Node validation utilities
├── tw_trace.py                           # Relationship tracing and analysis
├── tw_lint_soc.py                        # Social coding linting
├── tw_stub_command.py                    # Command stubbing utilities
└── extract_schema.py                     # Schema extraction utilities
```

### 3. **CLI Interface (cli_package)**
Rich terminal interface built with Click and Rich:

**CLI Package Structure (`cli_package/src/todowrite_cli/`)**
```
todowrite_cli/
├── main.py                               # Main CLI implementation
│   ├── get_current_username()            # Get current system username
│   ├── capitalize_status()               # Format status for display
│   ├── get_app()                         # Get ToDoWrite application instance
│   ├── cli()                             # Main CLI entry point
│   ├── init()                            # Initialize database/YAML storage
│   ├── create()                          # Create new nodes
│   ├── get()                             # Get and display node details
│   ├── list_command()                    # List nodes with filtering
│   ├── status()                          # Show database status
│   ├── show()                            # Show node details
│   ├── complete()                        # Mark node as completed
│   ├── global_status()                   # Update global status
│   ├── import_yaml()                     # Import from YAML files
│   ├── export_yaml()                     # Export to YAML format
│   ├── sync_status()                     # Sync YAML to database
│   ├── db_status()                       # Show database status
│   ├── delete()                          # Delete nodes
│   ├── update()                          # Update existing nodes
│   ├── search()                          # Search nodes
│   └── main()                            # Main CLI function
├── __main__.py                           # Module execution entry point
├── __init__.py                           # Package initialization
└── version.py                            # Version information
```

**CLI Features**
- **CRUD Operations**: create, get, list, update, delete
- **Status Management**: progress tracking, status updates
- **Import/Export**: YAML synchronization, bulk operations
- **Search**: Text-based search across all nodes

### 4. **Database Model Structure**
The database schema is designed around a hierarchical node system:

**Node Table (`nodes`)**
- `id` (String, Primary Key): Unique identifier
- `layer` (String): One of 12 layer types
- `title` (String): Node title
- `description` (Text): Optional description
- `status` (String): One of 6 status types (default: "planned")
- `progress` (Integer): Progress percentage (optional)
- `started_date` (String): Start date (optional)
- `completion_date` (String): Completion date (optional)
- `owner` (String): Node owner (optional)
- `severity` (String): Severity level (optional)
- `work_type` (String): Work type (optional)
- `assignee` (String): Assigned person (optional)

**Relationship Tables**
- `links`: Many-to-many parent-child relationships between nodes
- `node_labels`: Many-to-many relationship between nodes and labels
- `commands`: One-to-one relationship with nodes for executable commands
- `artifacts`: One-to-many relationship with commands for output artifacts

**Key Relationships**
- Nodes have self-referential many-to-many parent/child relationships
- Nodes can have multiple labels (tags)
- Nodes can have one command with multiple artifacts

### 5. **Key Features**

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

### 6. **Build System & Development**

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

### 7. **Data Flow**

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
