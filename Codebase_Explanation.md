# ToDoWrite Codebase Explanation

## Overview
**ToDoWrite** is a sophisticated **hierarchical task management system** designed for managing complex software projects. It's built as a [Python 3.12+](https://docs.python.org/release/3.12.12/) monorepo with a clean separation between core business logic and user interfaces.

**Project Homepage**: [ToDoWrite GitHub Repository](https://github.com/dderyldowney/todowrite)

## Architecture

### 1. **Monorepo Structure**

**Published Packages:**
- [lib_package](https://pypi.org/project/todowrite/) - Core library (business logic)
- [cli_package](https://pypi.org/project/todowrite-cli/) - Command-line interface

**Repository Structure:**
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

**Quick Links:**
- [Documentation](https://github.com/dderyldowney/todowrite/tree/develop/docs) - Project documentation
- [Repository](https://github.com/dderyldowney/todowrite) - GitHub repository

### 2. **Core Library (lib_package)**
The heart of the system with these key components:

#### **Hierarchical Data Model**
- **12 Layer Types**: Goal, Concept, Context, Constraints, Requirements, AcceptanceCriteria, InterfaceContract, Phase, Step, Task, SubTask, Command
- **6 Status Types**: planned, in_progress, completed, blocked, cancelled, rejected
- **10 Work Types**: architecture, spec, interface, validation, implementation, docs, ops, refactor, chore, test
- **Rich Metadata**: owner, labels, severity, work_type, assignee

#### **Multi-Backend Storage**
1. **[PostgreSQL](https://www.postgresql.org/)** (primary)
2. **[SQLite](https://www.sqlite.org/)** (fallback)
3. **[YAML](https://yaml.org/) files** (last resort)
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
todowrite/database/                                    # Database package
└── models.py                                          # Database models definition
    ├── Base                                           # SQLAlchemy declarative base class
    ├── Node                                           # Main database entity with all node fields
    │   ├── id (String, PK)                           # Unique identifier
    │   ├── layer (String)                            # Layer type (Goal, Task, etc.)
    │   ├── title (String)                            # Node title
    │   ├── description (Text)                        # Optional description
    │   ├── status (String)                           # Status (6 types)
    │   ├── progress (Integer)                        # Progress (0-100)
    │   ├── started_date (String)                     # Start date (ISO format)
    │   ├── completion_date (String)                  # Completion date (ISO format)
    │   ├── owner (String)                            # Node owner
    │   ├── severity (String)                         # Severity level
    │   ├── work_type (String)                        # Work type (10 types)
    │   ├── assignee (String)                         # Assigned person
    │   └── Relationships                             # Node relationships
    │       ├── labels (M:M)                          # Many-to-many via node_labels
    │       ├── command (1:1)                         # One-to-one → Command
    │       ├── parents (M:M)                         # Many-to-many via links
    │       └── children (M:M)                        # Many-to-many via links
    ├── Link                                           # Parent-child relationships
    │   ├── parent_id (String, PK, FK)                # Parent node ID (FK to nodes.id)
    │   └── child_id (String, PK, FK)                 # Child node ID (FK to nodes.id)
    ├── Label                                          # Tag system
    │   ├── label (String, PK)                        # Label name (unique, PK)
    │   └── nodes (M:M)                               # Many-to-many via node_labels
    ├── node_labels                                    # Node-Label Association Table
    │   ├── node_id (String, PK, FK)                  # Node reference (FK to nodes.id)
    │   └── label (String, PK, FK)                    # Label reference (FK to labels.label)
    ├── Command                                        # Executable commands
    │   ├── node_id (String, PK, FK)                  # Associated node ID (FK to nodes.id)
    │   ├── ac_ref (String)                           # Acceptance criteria reference
    │   ├── run (Text)                                # Command definition (JSON/YAML)
    │   └── Relationships                             # Command relationships
    │       ├── node (1:1)                            # One-to-one ← Node
    │       └── artifacts (1:N)                       # One-to-many → Artifact
    └── Artifact                                      # Command outputs/artifacts
        ├── artifact (String, PK)                     # Artifact identifier/file path (PK)
        └── command_id (String, PK, FK)               # Associated command (FK to commands.node_id)
```

**Database Schema Layout (`lib_package/src/todowrite/core/schemas/todowrite.schema.json`)**

```
                    ToDoWrite Database Schema

          ┌─────────────────┐
          │     labels      │
          ├─────────────────┤
          │ label (PK)      │
          └─────────────────┘
                   ▲
                   │
┌─────────────────┐    │    ┌─────────────────┐
│     nodes       │◄───┼────│  node_labels    │
├─────────────────┤    │    ├─────────────────┤
│ id (PK)         │    │    │ node_id (PK)    │
│ layer           │    │    │ label (PK)      │
│ title           │    │    └─────────────────┘
│ description     │    │           ▲
│ status          │    │           │
│ progress        │    │           │
│ started_date    │    │           │
│ completion_date │    │           │
│ owner           │    │    ┌─────────────────┐
│ severity        │    │    │     links       │
│ work_type       │    │    ├─────────────────┤
│ assignee        │    │    │ parent_id (PK)  │
└─────────────────┘    │    │ child_id (PK)   │
         ▲             │    └─────────────────┘
         │             │             ▲
         │             │             │
         │             │             │
┌─────────────────┐    │             │
│    commands     │◄───┼─────────────┘
├─────────────────┤    │
│ node_id (PK)    │    │
│ ac_ref          │    │
│ run             │    │
└─────────────────┘    │
         ▲             │
         │             │
         │    ┌─────────────────┐
         │    │   artifacts     │
         └────┤─────────────────┤
              │ artifact (PK)   │
              │ command_id (PK) │
              └─────────────────┘

Relationship Summary:
• nodes ↔ nodes (M:M via links) - Hierarchical parent/child
• nodes ↔ labels (M:M via node_labels) - Tagging system
• nodes → commands (1:1) - Each node can have one command
• commands → artifacts (1:N) - Commands generate artifacts

Key Constraints:
• String-based IDs for UUID/semantic identifiers
• Composite primary keys for association tables
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
├── tw_validate.py                        # Schema validation tool
│   └── ToDoWriteValidator
│       ├── __init__()                    # Initialize validator with schema
│       ├── _load_schema()                # Load JSON schema from file
│       ├── validate_file()               # Validate single YAML file
│       ├── validate_directory()          # Validate all YAML files in directory
│       ├── validate_schema()             # Validate database against schema
│       └── print_validation_report()     # Generate validation report
├── tw_trace.py                           # Traceability analysis tool
│   └── TraceabilityBuilder
│       ├── __init__()                    # Initialize traceability builder
│       ├── _find_yaml_files()            # Discover all YAML files
│       ├── _load_yaml_file()             # Load and parse YAML file
│       ├── build_traceability_matrix()   # Build forward/backward links
│       ├── find_orphaned_nodes()         # Find disconnected nodes
│       ├── detect_circular_dependencies() # Find circular dependencies
│       ├── export_csv()                  # Export traceability to CSV
│       └── generate_report()             # Generate analysis report
├── tw_lint_soc.py                        # Separation of Concerns linter
│   └── SoCLinter
│       ├── __init__()                    # Initialize SoC linter
│       ├── _check_executable_patterns()   # Check for executable content
│       ├── _validate_layer_separation()  # Ensure proper layer separation
│       ├── lint_file()                   # Lint single YAML file
│       ├── lint_directory()              # Lint all YAML files
│       ├── _check_command_layer()        # Validate Command layer content
│       └── print_violations()            # Print SoC violations
├── tw_stub_command.py                    # Command stub generator
│   └── CommandStubGenerator
│       ├── __init__()                    # Initialize stub generator
│       ├── _find_acceptance_criteria_files() # Find AC files
│       ├── _find_existing_commands()     # Find existing command files
│       ├── _generate_command_stub()      # Generate command from AC
│       ├── _create_command_yaml()        # Create command YAML structure
│       ├── _generate_executable_content() # Generate executable stub
│       └── generate_all_stubs()          # Generate all missing commands
└── extract_schema.py                     # Schema extraction utility
    ├── extract_and_write_schema()        # Extract JSON schema from Markdown
    ├── _find_schema_block()              # Find schema in Markdown file
    └── _validate_schema_structure()      # Validate extracted schema
```

**Built-in Libraries and Dependencies**
```
Core Libraries Used:
├── [SQLAlchemy](https://www.sqlalchemy.org/)           # ORM and database interaction
├── [jsonschema](https://python-jsonschema.readthedocs.io/)  # JSON schema validation
├── [PyYAML](https://pyyaml.org/)                       # YAML file parsing and generation
├── [Click](https://click.palletsprojects.com/)         # CLI framework (cli_package)
├── [Rich](https://rich.readthedocs.io/)                # Terminal formatting (cli_package)
├── [pathlib](https://docs.python.org/3/library/pathlib.html)  # File system operations
├── [typing](https://docs.python.org/3/library/typing.html)     # Type hints and annotations
└── [argparse](https://docs.python.org/3/library/argparse.html) # Command-line argument parsing

Validation & Processing:
├── [Draft202012Validator](https://python-jsonschema.readthedocs.io/en/stable/validate/#jsonschema.Draft202012Validator)  # JSON Schema validator
├── [ValidationError](https://python-jsonschema.readthedocs.io/en/stable/exceptions/#jsonschema.exceptions.ValidationError)  # Schema validation errors
├── [yaml.safe_load()](https://pyyaml.org/wiki/PyYAMLDocumentation#loading-yaml)  # Secure YAML loading
└── [re (regex)](https://docs.python.org/3/library/re.html)  # Pattern matching and validation
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
- **[uv](https://github.com/astral-sh/uv)**: Modern package management (recently integrated)
- **[Hatchling](https://hatch.pypa.io/)**: Build backend with shared version management
- **[Ruff](https://github.com/astral-sh/ruff)**: All-in-one linting and formatting
- **[Pytest](https://pytest.org/)**: Testing with coverage requirements

#### **Quality Assurance**
- [Pre-commit hooks](https://pre-commit.com/) for code quality
- Comprehensive [type annotations](https://typing.python.org/en/latest/) (Python 3.12+)
- Security auditing with [Ruff](https://github.com/astral-sh/ruff) in S mode
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
