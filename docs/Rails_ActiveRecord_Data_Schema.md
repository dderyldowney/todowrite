# ToDoWrite Rails ActiveRecord Data Schema

**Authoritative Data Schema Documentation - Rails ActiveRecord API Only**

> **IMPORTANT**: This document describes the ONLY supported data schema for ToDoWrite. The old Node-based API has been completely removed and is no longer supported.

## Overview

ToDoWrite uses a **Rails ActiveRecord pattern** with individual tables for each of the 12 hierarchical layers, plus association tables for many-to-many relationships and session tracking infrastructure.

## Core Principles

- **Integer Primary Keys**: All tables use auto-incrementing integer primary keys (1, 2, 3, 4, 5...)
- **Rails Timestamps**: All tables include `created_at` and `updated_at` timestamp fields
- **Individual Tables**: Each layer has its own table (no single "nodes" table)
- **Proper Foreign Keys**: All relationships use proper foreign key constraints
- **Rails Associations**: Many-to-many relationships use join tables following Rails conventions

## Table Schema

### Core Layer Tables (12 Tables)

#### 1. Goals Table
```sql
CREATE TABLE goals (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    description TEXT,
    status VARCHAR NOT NULL DEFAULT 'planned',
    progress INTEGER,
    started_date VARCHAR,
    completion_date VARCHAR,
    owner VARCHAR,
    severity VARCHAR,
    work_type VARCHAR,
    assignee VARCHAR,
    extra_data TEXT,  -- JSON string for additional metadata
    created_at VARCHAR NOT NULL,
    updated_at VARCHAR NOT NULL
);
```

#### 2. Concepts Table
```sql
CREATE TABLE concepts (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    description TEXT,
    status VARCHAR NOT NULL DEFAULT 'planned',
    progress INTEGER,
    started_date VARCHAR,
    completion_date VARCHAR,
    owner VARCHAR,
    severity VARCHAR,
    work_type VARCHAR,
    assignee VARCHAR,
    extra_data TEXT,
    created_at VARCHAR NOT NULL,
    updated_at VARCHAR NOT NULL
);
```

#### 3. Contexts Table
```sql
CREATE TABLE contexts (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    description TEXT,
    status VARCHAR NOT NULL DEFAULT 'planned',
    progress INTEGER,
    started_date VARCHAR,
    completion_date VARCHAR,
    owner VARCHAR,
    severity VARCHAR,
    work_type VARCHAR,
    assignee VARCHAR,
    extra_data TEXT,
    created_at VARCHAR NOT NULL,
    updated_at VARCHAR NOT NULL
);
```

#### 4. Constraints Table
```sql
CREATE TABLE constraints (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    description TEXT,
    status VARCHAR NOT NULL DEFAULT 'planned',
    progress INTEGER,
    started_date VARCHAR,
    completion_date VARCHAR,
    owner VARCHAR,
    severity VARCHAR,
    work_type VARCHAR,
    assignee VARCHAR,
    extra_data TEXT,
    created_at VARCHAR NOT NULL,
    updated_at VARCHAR NOT NULL
);
```

#### 5. Requirements Table
```sql
CREATE TABLE requirements (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    description TEXT,
    status VARCHAR NOT NULL DEFAULT 'planned',
    progress INTEGER,
    started_date VARCHAR,
    completion_date VARCHAR,
    owner VARCHAR,
    severity VARCHAR,
    work_type VARCHAR,
    assignee VARCHAR,
    extra_data TEXT,
    created_at VARCHAR NOT NULL,
    updated_at VARCHAR NOT NULL
);
```

#### 6. Acceptance Criteria Table
```sql
CREATE TABLE acceptance_criteria (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    description TEXT,
    status VARCHAR NOT NULL DEFAULT 'planned',
    progress INTEGER,
    started_date VARCHAR,
    completion_date VARCHAR,
    owner VARCHAR,
    severity VARCHAR,
    work_type VARCHAR,
    assignee VARCHAR,
    extra_data TEXT,
    created_at VARCHAR NOT NULL,
    updated_at VARCHAR NOT NULL
);
```

#### 7. Interface Contracts Table
```sql
CREATE TABLE interface_contracts (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    description TEXT,
    status VARCHAR NOT NULL DEFAULT 'planned',
    progress INTEGER,
    started_date VARCHAR,
    completion_date VARCHAR,
    owner VARCHAR,
    severity VARCHAR,
    work_type VARCHAR,
    assignee VARCHAR,
    extra_data TEXT,
    created_at VARCHAR NOT NULL,
    updated_at VARCHAR NOT NULL
);
```

#### 8. Phases Table
```sql
CREATE TABLE phases (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    description TEXT,
    status VARCHAR NOT NULL DEFAULT 'planned',
    progress INTEGER,
    started_date VARCHAR,
    completion_date VARCHAR,
    owner VARCHAR,
    severity VARCHAR,
    work_type VARCHAR,
    assignee VARCHAR,
    extra_data TEXT,
    created_at VARCHAR NOT NULL,
    updated_at VARCHAR NOT NULL
);
```

#### 9. Steps Table
```sql
CREATE TABLE steps (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    description TEXT,
    status VARCHAR NOT NULL DEFAULT 'planned',
    progress INTEGER,
    started_date VARCHAR,
    completion_date VARCHAR,
    owner VARCHAR,
    severity VARCHAR,
    work_type VARCHAR,
    assignee VARCHAR,
    extra_data TEXT,
    created_at VARCHAR NOT NULL,
    updated_at VARCHAR NOT NULL
);
```

#### 10. Tasks Table
```sql
CREATE TABLE tasks (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    description TEXT,
    status VARCHAR NOT NULL DEFAULT 'planned',
    progress INTEGER,
    started_date VARCHAR,
    completion_date VARCHAR,
    owner VARCHAR,
    severity VARCHAR,
    work_type VARCHAR,
    assignee VARCHAR,
    extra_data TEXT,
    created_at VARCHAR NOT NULL,
    updated_at VARCHAR NOT NULL
);
```

#### 11. SubTasks Table
```sql
CREATE TABLE sub_tasks (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    description TEXT,
    status VARCHAR NOT NULL DEFAULT 'planned',
    progress INTEGER,
    started_date VARCHAR,
    completion_date VARCHAR,
    owner VARCHAR,
    severity VARCHAR,
    work_type VARCHAR,
    assignee VARCHAR,
    extra_data TEXT,
    created_at VARCHAR NOT NULL,
    updated_at VARCHAR NOT NULL
);
```

#### 12. Commands Table
```sql
CREATE TABLE commands (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    description TEXT,
    status VARCHAR NOT NULL DEFAULT 'planned',
    progress INTEGER,
    started_date VARCHAR,
    completion_date VARCHAR,
    owner VARCHAR,
    severity VARCHAR,
    work_type VARCHAR,
    assignee VARCHAR,
    extra_data TEXT,
    created_at VARCHAR NOT NULL,
    updated_at VARCHAR NOT NULL
);
```

### Shared Tables

#### Labels Table
```sql
CREATE TABLE labels (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL UNIQUE,
    created_at VARCHAR NOT NULL,
    updated_at VARCHAR NOT NULL
);
```

### Association Tables (Many-to-Many Relationships)

#### Label Associations (12 Tables)
Each layer can be associated with multiple labels:

```sql
-- Goals to Labels
CREATE TABLE goals_labels (
    goal_id INTEGER NOT NULL,
    label_id INTEGER NOT NULL,
    PRIMARY KEY (goal_id, label_id),
    FOREIGN KEY (goal_id) REFERENCES goals(id),
    FOREIGN KEY (label_id) REFERENCES labels(id)
);

-- Concepts to Labels
CREATE TABLE concepts_labels (
    concept_id INTEGER NOT NULL,
    label_id INTEGER NOT NULL,
    PRIMARY KEY (concept_id, label_id),
    FOREIGN KEY (concept_id) REFERENCES concepts(id),
    FOREIGN KEY (label_id) REFERENCES labels(id)
);

-- ... (similar patterns for contexts, constraints, requirements,
--     acceptance_criteria, interface_contracts, phases, steps,
--     tasks, sub_tasks, commands)
```

#### Hierarchical Associations

```sql
-- Goals to Tasks
CREATE TABLE goals_tasks (
    goal_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL,
    PRIMARY KEY (goal_id, task_id),
    FOREIGN KEY (goal_id) REFERENCES goals(id),
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);

-- Goals to Concepts
CREATE TABLE goals_concepts (
    goal_id INTEGER NOT NULL,
    concept_id INTEGER NOT NULL,
    PRIMARY KEY (goal_id, concept_id),
    FOREIGN KEY (goal_id) REFERENCES goals(id),
    FOREIGN KEY (concept_id) REFERENCES concepts(id)
);

-- Goals to Contexts
CREATE TABLE goals_contexts (
    goal_id INTEGER NOT NULL,
    context_id INTEGER NOT NULL,
    PRIMARY KEY (goal_id, context_id),
    FOREIGN KEY (goal_id) REFERENCES goals(id),
    FOREIGN KEY (context_id) REFERENCES contexts(id)
);

-- Goals to Phases
CREATE TABLE goals_phases (
    goal_id INTEGER NOT NULL,
    phase_id INTEGER NOT NULL,
    PRIMARY KEY (goal_id, phase_id),
    FOREIGN KEY (goal_id) REFERENCES goals(id),
    FOREIGN KEY (phase_id) REFERENCES phases(id)
);
```

#### Layer-to-Layer Associations

```sql
-- Constraints to Requirements
CREATE TABLE constraints_requirements (
    constraint_id INTEGER NOT NULL,
    requirement_id INTEGER NOT NULL,
    PRIMARY KEY (constraint_id, requirement_id),
    FOREIGN KEY (constraint_id) REFERENCES constraints(id),
    FOREIGN KEY (requirement_id) REFERENCES requirements(id)
);

-- Requirements to Acceptance Criteria
CREATE TABLE requirements_acceptance_criteria (
    requirement_id INTEGER NOT NULL,
    acceptance_criterion_id INTEGER NOT NULL,
    PRIMARY KEY (requirement_id, acceptance_criterion_id),
    FOREIGN KEY (requirement_id) REFERENCES requirements(id),
    FOREIGN KEY (acceptance_criterion_id) REFERENCES acceptance_criteria(id)
);

-- Acceptance Criteria to Interface Contracts
CREATE TABLE acceptance_criteria_interface_contracts (
    acceptance_criterion_id INTEGER NOT NULL,
    interface_contract_id INTEGER NOT NULL,
    PRIMARY KEY (acceptance_criterion_id, interface_contract_id),
    FOREIGN KEY (acceptance_criterion_id) REFERENCES acceptance_criteria(id),
    FOREIGN KEY (interface_contract_id) REFERENCES interface_contracts(id)
);

-- Interface Contracts to Phases
CREATE TABLE interface_contracts_phases (
    interface_contract_id INTEGER NOT NULL,
    phase_id INTEGER NOT NULL,
    PRIMARY KEY (interface_contract_id, phase_id),
    FOREIGN KEY (interface_contract_id) REFERENCES interface_contracts(id),
    FOREIGN KEY (phase_id) REFERENCES phases(id)
);

-- Phases to Steps
CREATE TABLE phases_steps (
    phase_id INTEGER NOT NULL,
    step_id INTEGER NOT NULL,
    PRIMARY KEY (phase_id, step_id),
    FOREIGN KEY (phase_id) REFERENCES phases(id),
    FOREIGN KEY (step_id) REFERENCES steps(id)
);

-- Steps to Tasks
CREATE TABLE steps_tasks (
    step_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL,
    PRIMARY KEY (step_id, task_id),
    FOREIGN KEY (step_id) REFERENCES steps(id),
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);

-- Tasks to SubTasks
CREATE TABLE tasks_sub_tasks (
    task_id INTEGER NOT NULL,
    sub_task_id INTEGER NOT NULL,
    PRIMARY KEY (task_id, sub_task_id),
    FOREIGN KEY (task_id) REFERENCES tasks(id),
    FOREIGN KEY (sub_task_id) REFERENCES sub_tasks(id)
);

-- SubTasks to Commands
CREATE TABLE sub_tasks_commands (
    sub_task_id INTEGER NOT NULL,
    command_id INTEGER NOT NULL,
    PRIMARY KEY (sub_task_id, command_id),
    FOREIGN KEY (sub_task_id) REFERENCES sub_tasks(id),
    FOREIGN KEY (command_id) REFERENCES commands(id)
);
```

### Session Tracking Tables

#### Development Sessions Table
```sql
CREATE TABLE development_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT,
    tasks_worked_on TEXT,  -- JSON array of task IDs
    commits_made INTEGER DEFAULT 0,
    description TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

#### Session Tasks Association Table
```sql
CREATE TABLE session_tasks (
    session_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL,
    time_spent_minutes INTEGER DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (session_id) REFERENCES development_sessions(id),
    PRIMARY KEY (session_id, task_id)
);
```

## Rails ActiveRecord API Usage

### Installation
```bash
# Install the library and CLI in development mode
pip install -e ./lib_package
pip install -e ./cli_package
```

### Basic Usage
```python
from todowrite import Goal, Task, Label, create_engine, sessionmaker

# Initialize database session
engine = create_engine("sqlite:///development_todowrite.db")
Session = sessionmaker(bind=engine)
session = Session()

# Create a goal
goal = Goal(
    title="Build TodoWrite Application",
    description="Create the complete TodoWrite system",
    owner="development-team",
    severity="high"
)
session.add(goal)
session.commit()

print(f"Created goal with ID: {goal.id}")  # Integer ID: 1, 2, 3...

# Create a task
task = Task(
    title="Set up database schema",
    description="Create Rails ActiveRecord tables",
    owner="database-team",
    severity="medium"
)
session.add(task)
session.commit()

print(f"Created task with ID: {task.id}")  # Integer ID: 1, 2, 3...

# Add labels
label = Label(name="database")
session.add(label)
session.commit()

# Associate label with goal and task
goal.labels.append(label)
task.labels.append(label)
session.commit()

# Query records
all_goals = session.query(Goal).all()
high_priority_tasks = session.query(Task).filter(Task.severity == "high").all()

# Update records
goal.progress = 50
session.commit()

# Delete records
session.delete(task)
session.commit()
```

### Association Management
```python
# Many-to-many relationships (Rails-style)
goal.labels.append(label)
session.commit()

# Access associated records
print(f"Goal labels: {[l.name for l in goal.labels]}")
print(f"Label goals: {[g.title for g in label.goals]}")

# Hierarchical relationships
phase = Phase(title="Database Setup")
goal.phases.append(phase)
session.commit()
```

## Data Types and Constraints

### Field Types
- **id**: `INTEGER PRIMARY KEY AUTOINCREMENT` - Unique identifier
- **title**: `VARCHAR NOT NULL` - Required title field
- **description**: `TEXT` - Optional description
- **status**: `VARCHAR NOT NULL DEFAULT 'planned'` - Status field
- **progress**: `INTEGER` - Progress percentage (0-100)
- **started_date**: `VARCHAR` - ISO format date string
- **completion_date**: `VARCHAR` - ISO format date string
- **owner**: `VARCHAR` - Owner identifier
- **severity**: `VARCHAR` - Priority level (low, medium, high, critical)
- **work_type**: `VARCHAR` - Type of work
- **assignee**: `VARCHAR` - Assigned person
- **extra_data**: `TEXT` - JSON string for additional metadata
- **created_at**: `VARCHAR NOT NULL` - Creation timestamp
- **updated_at**: `VARCHAR NOT NULL` - Last update timestamp

### Constraints
- **Primary Keys**: Auto-incrementing integers
- **Foreign Keys**: Proper referential integrity
- **Unique Constraints**: Label names must be unique
- **Not Null**: Required fields enforced
- **Default Values**: Sensible defaults provided

## Migration Notes

### From Old Node-Based API
- **Removed**: All old Node-based functionality
- **Replaced**: With Rails ActiveRecord models
- **Changed**: String IDs to integer primary keys
- **Updated**: All foreign key relationships
- **Enhanced**: Proper association management

### Session Tracking
- **Automatic**: Sessions are tracked automatically
- **Comprehensive**: Tracks tasks, commits, and time spent
- **Queryable**: Session data available for analysis

## Performance Considerations

- **Indexed**: Primary keys are automatically indexed
- **Foreign Keys**: Indexed for relationship performance
- **Labels**: Unique constraint on label names
- **Sessions**: Optimized for session-based queries

## Compliance

This schema is **authoritative** and **exclusive**:
- **No Old API**: Old Node-based patterns are completely removed
- **Rails Only**: Only Rails ActiveRecord patterns are supported
- **Type Safety**: All relationships are properly typed
- **Data Integrity**: Enforced through foreign key constraints
- **Documentation**: This is the single source of truth for data schema

For any questions about the data schema, refer to this document as the authoritative source.
