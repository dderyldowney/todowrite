ToDoWrite Models Data Schema
============================

This document describes the complete database schema for the ToDoWrite Models system, which provides individual tables for each of the 12 hierarchical layers.

Schema Overview
---------------

The ToDoWrite Models system uses a **clean, normalized database design** with:

- **Individual tables** for each layer (goals, concepts, contexts, etc.)
- **Integer primary keys** with auto-increment (1, 2, 3, 4, 5...)
- **Referential integrity** enforced through proper foreign keys
- **Timestamp fields** for creation and update tracking
- **Many-to-many relationships** through join tables
- **JSON storage** for complex data structures

Core Tables
-----------

### Goals Table

High-level project objectives and strategic outcomes.

.. code-block:: sql

    CREATE TABLE goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR NOT NULL,
        description TEXT,
        status VARCHAR DEFAULT 'planned',
        progress INTEGER DEFAULT 0,
        owner VARCHAR,
        severity VARCHAR,
        work_type VARCHAR,
        assignee VARCHAR,
        started_date VARCHAR,
        completion_date VARCHAR,
        extra_data TEXT,  -- JSON for complex data
        created_at VARCHAR NOT NULL,
        updated_at VARCHAR NOT NULL
    );

**Fields:**
- ``id``: Unique integer identifier (auto-increment, never reused)
- ``title``: Goal title (required)
- ``description``: Detailed description (optional)
- ``status``: Current status (planned, in_progress, completed, blocked, cancelled)
- ``progress``: Progress percentage (0-100)
- ``owner``: Team or person responsible
- ``severity``: Priority level (low, medium, high, critical)
- ``work_type``: Type of work (implementation, design, testing, etc.)
- ``assignee``: Specific person assigned
- ``started_date``: ISO timestamp when work began
- ``completion_date``: ISO timestamp when completed
- ``extra_data``: JSON field for additional metadata
- ``created_at``: ISO timestamp of creation (readonly)
- ``updated_at``: ISO timestamp of last update

### Concepts Table

Design concepts, architectural patterns, and theoretical approaches.

.. code-block:: sql

    CREATE TABLE concepts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR NOT NULL,
        description TEXT,
        status VARCHAR DEFAULT 'planned',
        progress INTEGER DEFAULT 0,
        owner VARCHAR,
        severity VARCHAR,
        work_type VARCHAR,
        assignee VARCHAR,
        started_date VARCHAR,
        completion_date VARCHAR,
        extra_data TEXT,  -- JSON for complex data
        created_at VARCHAR NOT NULL,
        updated_at VARCHAR NOT NULL
    );

### Contexts Table

Environmental context, project background, and situational factors.

.. code-block:: sql

    CREATE TABLE contexts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR NOT NULL,
        description TEXT,
        status VARCHAR DEFAULT 'planned',
        progress INTEGER DEFAULT 0,
        owner VARCHAR,
        severity VARCHAR,
        work_type VARCHAR,
        assignee VARCHAR,
        started_date VARCHAR,
        completion_date VARCHAR,
        extra_data TEXT,  -- JSON for complex data
        created_at VARCHAR NOT NULL,
        updated_at VARCHAR NOT NULL
    );

### Constraints Table

Project constraints, limitations, and boundary conditions.

.. code-block:: sql

    CREATE TABLE constraints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR NOT NULL,
        description TEXT,
        status VARCHAR DEFAULT 'planned',
        progress INTEGER DEFAULT 0,
        owner VARCHAR,
        severity VARCHAR,
        work_type VARCHAR,
        assignee VARCHAR,
        started_date VARCHAR,
        completion_date VARCHAR,
        extra_data TEXT,  -- JSON for complex data
        created_at VARCHAR NOT NULL,
        updated_at VARCHAR NOT NULL
    );

### Requirements Table

Functional and non-functional requirements.

.. code-block:: sql

    CREATE TABLE requirements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR NOT NULL,
        description TEXT,
        status VARCHAR DEFAULT 'planned',
        progress INTEGER DEFAULT 0,
        owner VARCHAR,
        severity VARCHAR,
        work_type VARCHAR,
        assignee VARCHAR,
        started_date VARCHAR,
        completion_date VARCHAR,
        extra_data TEXT,  -- JSON for complex data
        created_at VARCHAR NOT NULL,
        updated_at VARCHAR NOT NULL
    );

### Acceptance Criteria Table

Success conditions and acceptance criteria for requirements.

.. code-block:: sql

    CREATE TABLE acceptance_criteria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR NOT NULL,
        description TEXT,
        status VARCHAR DEFAULT 'planned',
        progress INTEGER DEFAULT 0,
        owner VARCHAR,
        severity VARCHAR,
        work_type VARCHAR,
        assignee VARCHAR,
        started_date VARCHAR,
        completion_date VARCHAR,
        extra_data TEXT,  -- JSON for complex data
        created_at VARCHAR NOT NULL,
        updated_at VARCHAR NOT NULL
    );

### Interface Contracts Table

Interface specifications and contracts between components.

.. code-block:: sql

    CREATE TABLE interface_contracts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR NOT NULL,
        description TEXT,
        status VARCHAR DEFAULT 'planned',
        progress INTEGER DEFAULT 0,
        owner VARCHAR,
        severity VARCHAR,
        work_type VARCHAR,
        assignee VARCHAR,
        started_date VARCHAR,
        completion_date VARCHAR,
        extra_data TEXT,  -- JSON for complex data
        created_at VARCHAR NOT NULL,
        updated_at VARCHAR NOT NULL
    );

### Phases Table

Project phases, milestones, and major stages.

.. code-block:: sql

    CREATE TABLE phases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR NOT NULL,
        description TEXT,
        status VARCHAR DEFAULT 'planned',
        progress INTEGER DEFAULT 0,
        owner VARCHAR,
        severity VARCHAR,
        work_type VARCHAR,
        assignee VARCHAR,
        started_date VARCHAR,
        completion_date VARCHAR,
        extra_data TEXT,  -- JSON for complex data
        created_at VARCHAR NOT NULL,
        updated_at VARCHAR NOT NULL
    );

### Steps Table

Implementation steps and major activities.

.. code-block:: sql

    CREATE TABLE steps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR NOT NULL,
        description TEXT,
        status VARCHAR DEFAULT 'planned',
        progress INTEGER DEFAULT 0,
        owner VARCHAR,
        severity VARCHAR,
        work_type VARCHAR,
        assignee VARCHAR,
        started_date VARCHAR,
        completion_date VARCHAR,
        extra_data TEXT,  -- JSON for complex data
        created_at VARCHAR NOT NULL,
        updated_at VARCHAR NOT NULL
    );

### Tasks Table

Specific tasks with progress tracking and execution details.

.. code-block:: sql

    CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR NOT NULL,
        description TEXT,
        status VARCHAR DEFAULT 'planned',
        progress INTEGER DEFAULT 0,
        owner VARCHAR,
        severity VARCHAR,
        work_type VARCHAR,
        assignee VARCHAR,
        started_date VARCHAR,
        completion_date VARCHAR,
        extra_data TEXT,  -- JSON for complex data
        created_at VARCHAR NOT NULL,
        updated_at VARCHAR NOT NULL
    );

### Sub Tasks Table

Sub-tasks that break down larger tasks into smaller units.

.. code-block:: sql

    CREATE TABLE sub_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR NOT NULL,
        description TEXT,
        status VARCHAR DEFAULT 'planned',
        progress INTEGER DEFAULT 0,
        owner VARCHAR,
        severity VARCHAR,
        work_type VARCHAR,
        assignee VARCHAR,
        started_date VARCHAR,
        completion_date VARCHAR,
        extra_data TEXT,  -- JSON for complex data
        created_at VARCHAR NOT NULL,
        updated_at VARCHAR NOT NULL
    );

### Commands Table

Executable commands and automation scripts.

.. code-block:: sql

    CREATE TABLE commands (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR NOT NULL,
        description TEXT,
        status VARCHAR DEFAULT 'planned',
        progress INTEGER DEFAULT 0,
        owner VARCHAR,
        severity VARCHAR,
        work_type VARCHAR,
        assignee VARCHAR,
        started_date VARCHAR,
        completion_date VARCHAR,
        cmd TEXT,  -- Executable command
        cmd_params TEXT,  -- Command parameters
        runtime_env TEXT,  -- Environment variables
        output TEXT,  -- Command output
        artifacts TEXT,  -- Expected output files
        extra_data TEXT,  -- JSON for complex data
        created_at VARCHAR NOT NULL,
        updated_at VARCHAR NOT NULL
    );

**Command-Specific Fields:**
- ``cmd``: The executable script or command name
- ``cmd_params``: Command parameters and arguments
- ``runtime_env``: Environment variables and runtime configuration (JSON)
- ``output``: Command execution output (stdout/stderr)
- ``artifacts``: Expected output files and generated artifacts (JSON)

Labels Table
-----------

Shared labels table for many-to-many relationships across all layers.

.. code-block:: sql

    CREATE TABLE labels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR NOT NULL UNIQUE,
        created_at VARCHAR NOT NULL,
        updated_at VARCHAR NOT NULL
    );

**Fields:**
- ``id``: Unique integer identifier
- ``name``: Label name (must be unique)
- ``created_at``: ISO timestamp of creation
- ``updated_at``: ISO timestamp of last update

Join Tables
-----------

Many-to-many relationships are handled through join tables following the pattern ``{layer}_labels``:

.. code-block:: sql

    -- Goals to Labels
    CREATE TABLE goals_labels (
        goal_id INTEGER NOT NULL REFERENCES goals(id),
        label_id INTEGER NOT NULL REFERENCES labels(id)
    );

    -- Concepts to Labels
    CREATE TABLE concepts_labels (
        concept_id INTEGER NOT NULL REFERENCES concepts(id),
        label_id INTEGER NOT NULL REFERENCES labels(id)
    );

    -- Tasks to Labels
    CREATE TABLE tasks_labels (
        task_id INTEGER NOT NULL REFERENCES tasks(id),
        label_id INTEGER NOT NULL REFERENCES labels(id)
    );

    -- ... similar join tables for all 12 layers

**Join Table Characteristics:**
- **Composite primary key**: Combination of the two foreign keys
- **No additional fields**: Simple many-to-many relationships
- **Lexical naming**: ``{layer}_labels`` pattern (e.g., ``goals_labels``)
- **Bidirectional access**: Both ``goal.labels`` and ``label.goals`` work

Hierarchical Relationships
------------------------

The 12-layer hierarchy is implemented through foreign key relationships:

.. list-table:: Hierarchy Levels
   :header-rows: 1
   :widths: 20 30 20 30

   * - Layer
     - Table
     - Parent Field
     - Children Collections
   * - **Level 1**
     - ``goals``
     - N/A (top level)
     - ``goal.concepts``, ``goal.phases``
   * - **Level 2**
     - ``concepts``
     - ``goal_id``
     - ``concept.contexts``, ``concept.requirements``
   * - **Level 3**
     - ``contexts``
     - ``concept_id``
     - ``context.constraints``
   * - **Level 4**
     - ``constraints``
     - ``context_id``
     - ``constraints.requirements``
   * - **Level 5**
     - ``requirements``
     - ``constraint_id``
     - ``requirements.acceptance_criteria``
   * - **Level 6**
     - ``acceptance_criteria``
     - ``requirement_id``
     - ``acceptance_criteria.interface_contracts``
   * - **Level 7**
     - ``interface_contracts``
     - ``acceptance_criteria_id``
     - ``interface_contracts.phases``
   * - **Level 8**
     - ``phases``
     - ``interface_contract_id``
     - ``phases.steps``
   * - **Level 9**
     - ``steps``
     - ``phase_id``
     - ``steps.tasks``
   * - **Level 10**
     - ``tasks``
     - ``step_id``
     - ``tasks.sub_tasks``
   * - **Level 11**
     - ``sub_tasks``
     - ``task_id``
     - ``sub_tasks.commands``
   * - **Level 12**
     - ``commands``
     - ``sub_task_id``
     - N/A (executable layer)

**Note**: The hierarchical relationships above represent the conceptual flow. In the current implementation, relationships are more flexible and can be defined as needed for your specific use case.

Timestamp Fields
---------------

All tables use ISO 8601 timestamp format:

.. code-block:: python

    # Example timestamp values
    "2025-01-18T14:30:00Z"  # UTC with Z suffix
    "2025-01-18T14:30:00+08:00"  # With timezone offset

**Timestamp Behavior:**
- **created_at**: Set once on record creation, never changes
- **updated_at**: Automatically updated on every save operation
- **started_date**: Optional field set when work begins
- **completion_date**: Optional field set when work completes

JSON Data Fields
----------------

The ``extra_data`` field stores complex data structures as JSON strings:

.. code-block:: python

    # Example JSON data for a task
    extra_data = {
        "estimated_hours": 8,
        "actual_hours": 6,
        "dependencies": ["TASK-001", "TASK-002"],
        "tags": ["frontend", "react", "ui"],
        "metadata": {
            "complexity": "medium",
            "risk_level": "low"
        }
    }

Database Variations
-------------------

### SQLite (Development)

.. code-block:: sql

    -- SQLite uses AUTOINCREMENT
    id INTEGER PRIMARY KEY AUTOINCREMENT

    -- Text fields for timestamps
    created_at VARCHAR NOT NULL
    updated_at VARCHAR NOT NULL

### PostgreSQL (Production)

.. code-block:: sql

    -- PostgreSQL uses SERIAL or IDENTITY
    id SERIAL PRIMARY KEY
    -- Or modern IDENTITY syntax:
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY

    -- Native timestamp fields
    created_at TIMESTAMP NOT NULL
    updated_at TIMESTAMP NOT NULL

Schema Validation
-----------------

The schema is validated through:

1. **SQLAlchemy Models**: Python class definitions enforce field types
2. **JSON Schema**: ``todowrite_models.schema.json`` validates data structure
3. **Database Constraints**: Foreign keys and unique constraints
4. **Application Validation**: Custom validators for business rules

Migration Strategy
------------------

From the legacy Node system:

1. **Data Extraction**: Export existing Node data to JSON
2. **Data Transformation**: Map Node hierarchy to ToDoWrite Models tables
3. **Data Import**: Load transformed data into new schema
4. **Validation**: Verify referential integrity and data consistency

The legacy ``nodes`` table remains during migration for backward compatibility.

Indexing Strategy
-----------------

Recommended indexes for performance:

.. code-block:: sql

    -- Primary indexes (auto-created)
    CREATE UNIQUE INDEX goals_id_idx ON goals(id);
    CREATE UNIQUE INDEX tasks_id_idx ON tasks(id);

    -- Query optimization indexes
    CREATE INDEX goals_owner_idx ON goals(owner);
    CREATE INDEX tasks_status_idx ON tasks(status);
    CREATE INDEX tasks_severity_idx ON tasks(severity);

    -- Join table indexes
    CREATE INDEX goals_labels_goal_id_idx ON goals_labels(goal_id);
    CREATE INDEX goals_labels_label_id_idx ON goals_labels(label_id);

    -- Timestamp indexes
    CREATE INDEX goals_created_at_idx ON goals(created_at);
    CREATE INDEX tasks_updated_at_idx ON tasks(updated_at);

Data Integrity
--------------

The schema enforces data integrity through:

1. **Primary Keys**: Unique, auto-incrementing integers never reused
2. **Foreign Keys**: Referential integrity between related tables
3. **Unique Constraints**: Label names must be unique
4. **Not Null Constraints**: Required fields cannot be empty
5. **Default Values**: Sensible defaults for status and progress

Performance Considerations
--------------------------

**Query Optimization:**
- Use specific field queries instead of ``SELECT *``
- Leverage indexes on commonly filtered fields
- Consider ``JOIN`` strategies for hierarchical queries
- Use pagination for large result sets

**Database Choice:**
- **SQLite**: Development, testing, smaller projects
- **PostgreSQL**: Production, large datasets, concurrent access

**Connection Management:**
- Use connection pooling for production
- Proper session management with SQLAlchemy
- Transaction boundaries for complex operations

This schema provides a robust foundation for hierarchical task management while maintaining flexibility for various project structures and workflows.
