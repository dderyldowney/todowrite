# ToDoWrite Complete Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Database Schemas](#database-schemas)
3. [YAML File Structure](#yaml-file-structure)
4. [CLI Commands Reference](#cli-commands-reference)
5. [Python Module API](#python-module-api)
6. [REST API Specification](#rest-api-specification)
7. [Storage Backend Configuration](#storage-backend-configuration)
8. [Validation and Tooling](#validation-and-tooling)
9. [Development Workflow](#development-workflow)
10. [Examples and Usage Patterns](#examples-and-usage-patterns)

---

## System Overview

**ToDoWrite** is a 12-layer declarative planning framework with enforced Separation of Concerns, designed for systematic project planning and execution in software engineering and agricultural automation projects.

### Key Characteristics
- **Version:** See VERSION file (Production Ready)
- **Architecture:** 12-layer hierarchy (11 declarative + 1 executable)
- **Language:** Python 3.12+ with strict type checking
- **Storage:** Three-tier fallback chain (PostgreSQL → SQLite → YAML)
- **Validation:** JSON Schema with build-time validation
- **CLI:** Click-based command interface
- **Framework:** Comprehensive Makefile automation

### Core Principles
1. **Separation of Concerns:** Layers 1-11 are non-executable, only Layer 12 executes
2. **Traceability:** Forward/backward links between all layers
3. **Single Responsibility:** One concern per node
4. **Build-time Validation:** Schema and architectural constraint enforcement

---

## Database Schemas

### PostgreSQL/SQLite Schema

ToDoWrite uses SQLAlchemy ORM with the following database structure:

#### `nodes` Table
```sql
CREATE TABLE nodes (
    id VARCHAR PRIMARY KEY,                 -- LAYER_PREFIX-IDENTIFIER format
    layer VARCHAR NOT NULL,                 -- 12 layer types
    title VARCHAR NOT NULL,                 -- Human-readable title
    description TEXT,                       -- Detailed description
    status VARCHAR DEFAULT 'planned',       -- Status tracking (planned, in_progress, blocked, done, rejected)
    owner VARCHAR,                          -- Node owner/assignee
    severity VARCHAR,                       -- Priority level (low, med, high)
    work_type VARCHAR                       -- Work classification (architecture, spec, interface, etc.)
);
```

#### `links` Table (Traceability)
```sql
CREATE TABLE links (
    parent_id VARCHAR REFERENCES nodes(id),
    child_id VARCHAR REFERENCES nodes(id),
    PRIMARY KEY (parent_id, child_id)
);
```

#### `labels` and `node_labels` (Tagging System)
```sql
CREATE TABLE labels (
    label VARCHAR PRIMARY KEY
);

CREATE TABLE node_labels (
    node_id VARCHAR REFERENCES nodes(id),
    label VARCHAR REFERENCES labels(label),
    PRIMARY KEY (node_id, label)
);
```

#### `commands` Table (Layer 12 - Executable Commands)
```sql
CREATE TABLE commands (
    node_id VARCHAR REFERENCES nodes(id) PRIMARY KEY,
    ac_ref VARCHAR,                         -- Reference to Acceptance Criteria
    run TEXT                                -- JSON-encoded execution configuration
);
```

#### `artifacts` Table (Command Outputs)
```sql
CREATE TABLE artifacts (
    artifact VARCHAR,
    command_id VARCHAR REFERENCES commands(node_id),
    PRIMARY KEY (artifact, command_id)
);
```

### Data Models (Python Dataclasses)

```python
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class Metadata:
    owner: Optional[str] = None
    labels: List[str] = None
    severity: Optional[str] = None  # "low", "med", "high"
    work_type: Optional[str] = None  # "architecture", "spec", "interface", etc.

@dataclass
class Link:
    parents: List[str]
    children: List[str]

@dataclass
class Command:
    ac_ref: str                             # AC-IDENTIFIER reference
    run: Dict[str, Any]                     # Execution configuration
    artifacts: List[str] = None             # Output file paths

@dataclass
class Node:
    id: str                                 # LAYER_PREFIX-IDENTIFIER
    layer: str                              # 12 layer types
    title: str
    description: str
    links: Link
    status: str = "planned"
    metadata: Optional[Metadata] = None
    command: Optional[Command] = None       # Only for Layer 12
```

---

## YAML File Structure

### Storage Organization
```
configs/
├── plans/                              # Layers 1-11 (Non-executable)
│   ├── goals/                          # Layer 1: GOAL-*
│   ├── concepts/                       # Layer 2: CON-*
│   ├── contexts/                       # Layer 3: CTX-*
│   ├── constraints/                    # Layer 4: CST-*
│   ├── requirements/                   # Layer 5: R-*
│   ├── acceptance_criteria/            # Layer 6: AC-*
│   ├── interface_contracts/            # Layer 7: IF-*
│   ├── phases/                         # Layer 8: PH-*
│   ├── steps/                          # Layer 9: STP-*
│   ├── tasks/                          # Layer 10: TSK-*
│   └── subtasks/                       # Layer 11: SUB-*
├── commands/                           # Layer 12: CMD-* (Executable)
└── schemas/
    └── todowrite.schema.json           # JSON Schema validation
```

### YAML File Format

#### Standard Node Format (Layers 1-11)
```yaml
id: GOAL-TODOWRITE-SYSTEM-IMPLEMENTATION
layer: Goal
title: Complete ToDoWrite System Implementation
description: >
  Implement the complete ToDoWrite 12-layer declarative planning framework
  with enforced Separation of Concerns, build-time validation, traceability,
  and comprehensive tooling to enable systematic project planning and execution
  for software engineering and agricultural automation projects.
metadata:
  owner: system-architect
  labels: ["work:architecture", todowrite, planning-framework, automation]
  severity: high
  work_type: architecture
links:
  parents: []
  children: [CON-DECLARATIVE-SEPARATION-ARCHITECTURE]
```

#### Command Node Format (Layer 12 Only)
```yaml
id: CMD-DOCUMENTATION-COMPLETE
layer: Command
title: Execute validation for Complete documentation
description: Automated execution to verify documentation completeness
metadata:
  owner: documentation-engineer
  labels: [generated, automated, verification]
  severity: med
  work_type: validation
links:
  parents: [AC-DOCUMENTATION-COMPLETE]
  children: []
command:
  ac_ref: AC-DOCUMENTATION-COMPLETE
  run:
    shell: python -m todowrite --help && echo 'CLI commands verified'
    workdir: .
    env:
      TODOWRITE_MODE: validation
      AC_REF: AC-DOCUMENTATION-COMPLETE
  artifacts:
    - results/CMD-DOCUMENTATION-COMPLETE/execution.log
    - results/CMD-DOCUMENTATION-COMPLETE/doc_verification.json
```

### ID Patterns and Layer Prefixes
```
Layer               Prefix   Pattern
Goal                GOAL     ^GOAL-[A-Z0-9_-]+$
Concept             CON      ^CON-[A-Z0-9_-]+$
Context             CTX      ^CTX-[A-Z0-9_-]+$
Constraints         CST      ^CST-[A-Z0-9_-]+$
Requirements        R        ^R-[A-Z0-9_-]+$
AcceptanceCriteria  AC       ^AC-[A-Z0-9_-]+$
InterfaceContract   IF       ^IF-[A-Z0-9_-]+$
Phase               PH       ^PH-[A-Z0-9_-]+$
Step                STP      ^STP-[A-Z0-9_-]+$
Task                TSK      ^TSK-[A-Z0-9_-]+$
SubTask             SUB      ^SUB-[A-Z0-9_-]+$
Command             CMD      ^CMD-[A-Z0-9_-]+$
```

### Status Enumerations
```yaml
# Node Status Options
status: planned      # Initial state
status: in_progress  # Currently being worked on
status: blocked      # Waiting for dependencies
status: done         # Completed successfully
status: rejected     # Cancelled or rejected

# Severity Options
severity: low        # Low priority
severity: med        # Medium priority
severity: high       # High priority

# Work Type Classifications
work_type: architecture    # System design
work_type: spec           # Specification
work_type: interface      # API/Interface design
work_type: validation     # Testing/Verification
work_type: implementation # Coding/Development
work_type: docs           # Documentation
work_type: ops            # Operations/Deployment
work_type: refactor       # Code refactoring
work_type: chore          # Maintenance tasks
work_type: test           # Testing
```

---

## CLI Commands Reference

### Primary CLI: `todowrite`

#### Basic Commands
```bash
# Initialize database
todowrite init

# Create a new node
todowrite create <layer> <title> <description> [--parent <parent_id>]

# Get node information
todowrite get <node_id>

# List all nodes
todowrite list

# Check storage status
todowrite db-status [--storage-preference <preference>]
```

#### Storage Management
```bash
# Import YAML files to database
todowrite import-yaml [--force] [--dry-run]

# Export database to YAML
todowrite export-yaml [--output-dir <dir>] [--no-backup]

# Check synchronization status
todowrite sync-status
```

#### ToDoWrite Framework Commands: `todowrite todowrite`

```bash
# Schema and validation
todowrite todowrite validate-plan [--strict]

# Traceability analysis
todowrite todowrite trace-links [--summary]

# Command generation
todowrite todowrite generate-commands [--force]

# Command execution
todowrite todowrite execute-commands [<command_id> | --all] [--dry-run]

# Hierarchy display
todowrite todowrite show-hierarchy [--layer <layer>] [--format <tree|flat|json>]

# Separation of Concerns checking
todowrite todowrite check-soc
```

#### Global Options
```bash
--storage-preference auto|postgresql_only|sqlite_only|yaml_only
```

### Makefile Interface

#### Core Workflow Targets
```bash
make tw-all          # Run schema, lint, validate, trace, prove (default)
make tw-init         # Initialize directory structure
make tw-deps         # Install Python dependencies
make tw-schema       # Generate JSON schema
make tw-lint         # Check Separation of Concerns
make tw-validate     # Validate YAML against schema
make tw-trace        # Build traceability matrix
make tw-prove        # Generate command stubs
make tw-hooks        # Install git commit hooks
make tw-clean        # Remove generated files
```

#### Quality & Integration Targets
```bash
make tw-check        # Full validation (strict mode)
make tw-test         # Test complete system
make tw-dev          # Development workflow (lint + validate + prove)
make tw-prod         # Production workflow (full validation + traceability + commands)
```

### Usage Examples

#### Creating a Complete Planning Hierarchy
```bash
# Create a goal
todowrite create Goal "Agricultural Automation" "Enable autonomous equipment coordination"

# Create supporting concept
todowrite create Concept "Multi-Agent Coordination" "Distributed control architecture" --parent GOAL-AGRICULTURAL-AUTOMATION

# Create requirements
todowrite create Requirements "Real-time Communication" "System must support sub-100ms latency" --parent CON-MULTI-AGENT-COORDINATION

# Validate the planning structure
make tw-all
```

#### Development Workflow
```bash
# Initialize new project
make tw-init tw-deps tw-hooks

# Development cycle
make tw-dev                    # Validate and generate commands
git add -A
git commit -m "feat(req): add real-time communication requirement"

# Production deployment
make tw-prod                   # Full validation before release
```

---

## Python Module API

### Main Entry Point

```python
from todowrite import ToDoWrite

# Initialize with auto-storage detection
app = ToDoWrite()

# Initialize with specific storage preference
app = ToDoWrite(storage_preference="postgresql_only")
```

### Core CRUD Operations

```python
# Create a node
node_data = {
    "id": "GOAL-NEW-PROJECT",
    "layer": "Goal",
    "title": "New Project Goal",
    "description": "Detailed description",
    "links": {"parents": [], "children": []},
    "metadata": {
        "owner": "developer",
        "labels": ["work:architecture"],
        "severity": "high",
        "work_type": "architecture"
    }
}
node = app.create_node(node_data)

# Retrieve nodes
node = app.get_node("GOAL-NEW-PROJECT")
all_nodes = app.get_all_nodes()

# Update node
updated_data = {"title": "Updated Project Goal"}
updated_node = app.update_node("GOAL-NEW-PROJECT", updated_data)

# Delete node
app.delete_node("GOAL-NEW-PROJECT")
```

### Layer-Specific Factory Methods

```python
# Create layer-specific nodes with convenience methods
goal = app.add_goal(
    title="Agricultural Automation",
    description="Enable autonomous equipment coordination",
    owner="product-team"
)

phase = app.add_phase(
    title="Development Phase 1",
    description="Core system implementation",
    parent_ids=["GOAL-AGRICULTURAL-AUTOMATION"]
)

task = app.add_task(
    title="Implement Communication Protocol",
    description="Low-latency messaging system",
    parent_ids=["PH-DEVELOPMENT-PHASE-1"],
    owner="developer",
    severity="high"
)

# Create executable command (Layer 12)
command = app.add_command(
    title="Run Integration Tests",
    description="Execute test suite",
    ac_ref="AC-INTEGRATION-TESTS-PASS",
    shell_command="pytest tests/integration/ -v",
    artifacts=["results/CMD-INTEGRATION-TESTS/test_report.json"]
)
```

### Utility Methods

```python
# Database management
app.init_database()
session = app.get_session()

# Data loading and management
app.load_todos()
active_items = app.get_active_items()

# Storage backend information
storage_type = app.storage_type
is_database = app.is_database_storage()
```

### Type Definitions

```python
from todowrite.app import LayerType, StatusType, Node, Link, Metadata, Command

# Layer types (string literals)
LayerType = Literal[
    "Goal", "Concept", "Context", "Constraints", "Requirements",
    "AcceptanceCriteria", "InterfaceContract", "Phase", "Step",
    "Task", "SubTask", "Command"
]

# Status types
StatusType = Literal["planned", "in_progress", "blocked", "done", "rejected"]
```

---

## REST API Specification

**Note:** REST API endpoints are currently specified in interface contracts but not yet implemented. The following represents the planned API structure:

### Base URL
```
http://localhost:8000/api/v1/
```

### Authentication
- Authentication mechanism: TBD
- Authorization: TBD

### Endpoints Overview

#### Node Management
```
GET    /api/v1/{layer}/           # List nodes by layer
POST   /api/v1/{layer}/           # Create new node
GET    /api/v1/{layer}/{id}       # Get specific node
PUT    /api/v1/{layer}/{id}       # Update node
DELETE /api/v1/{layer}/{id}       # Delete node
```

#### Cross-Layer Operations
```
GET    /api/v1/nodes/             # List all nodes
GET    /api/v1/hierarchy/         # Get hierarchy view
GET    /api/v1/trace/{id}         # Get traceability for node
POST   /api/v1/validate/          # Validate node data
```

#### Command Execution (Layer 12)
```
POST   /api/v1/commands/{id}/execute    # Execute command
GET    /api/v1/commands/{id}/status     # Get execution status
GET    /api/v1/commands/{id}/artifacts  # Get execution artifacts
```

### Request/Response Format

#### Standard Node Response
```json
{
  "id": "GOAL-AGRICULTURAL-AUTOMATION",
  "layer": "Goal",
  "title": "Agricultural Automation",
  "description": "Enable autonomous equipment coordination",
  "status": "planned",
  "metadata": {
    "owner": "product-team",
    "labels": ["work:architecture", "automation"],
    "severity": "high",
    "work_type": "architecture"
  },
  "links": {
    "parents": [],
    "children": ["CON-MULTI-AGENT-COORDINATION"]
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Command Node Response (Layer 12)
```json
{
  "id": "CMD-INTEGRATION-TESTS",
  "layer": "Command",
  "title": "Run Integration Tests",
  "description": "Execute comprehensive test suite",
  "command": {
    "ac_ref": "AC-INTEGRATION-TESTS-PASS",
    "run": {
      "shell": "pytest tests/integration/ -v",
      "workdir": ".",
      "env": {
        "TEST_MODE": "integration"
      }
    },
    "artifacts": [
      "results/CMD-INTEGRATION-TESTS/test_report.json",
      "results/CMD-INTEGRATION-TESTS/coverage.xml"
    ]
  },
  "execution_status": "completed",
  "last_executed": "2024-01-15T14:22:00Z"
}
```

#### Error Response Format
```json
{
  "error": "ValidationError",
  "message": "Node ID pattern validation failed",
  "details": {
    "field": "id",
    "expected_pattern": "^GOAL-[A-Z0-9_-]+$",
    "received": "goal-invalid-format"
  }
}
```

### Planned Implementation Notes
- **Framework:** FastAPI with Pydantic validation
- **Database Integration:** Same SQLAlchemy models as CLI
- **Authentication:** JWT-based authentication planned
- **Validation:** Real-time JSON Schema validation
- **WebSocket Support:** Planned for real-time updates
- **File Upload:** Support for bulk YAML import/export

---

## Storage Backend Configuration

### Three-Tier Fallback Chain

ToDoWrite automatically detects and uses the best available storage backend:

1. **PostgreSQL (Priority 1)** - Enterprise-grade, preferred for production
2. **SQLite (Priority 2)** - Reliable fallback, development-friendly
3. **YAML Files (Priority 3)** - Last resort, no database required

### Environment Configuration

```bash
# Full database URL override
export TODOWRITE_DATABASE_URL="postgresql://user:password@localhost:5432/todowrite"

# Standard database URL (fallback)
export DATABASE_URL="postgresql://user:password@localhost:5432/todowrite"

# Storage preference override
export TODOWRITE_STORAGE_PREFERENCE="auto"  # auto|postgresql_only|sqlite_only|yaml_only
```

### PostgreSQL Setup

#### Docker Configuration
```yaml
# docker-compose.yml
version: '3.9'
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: todowrite
      POSTGRES_USER: todowrite
      POSTGRES_PASSWORD: todowrite_dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U todowrite"]
      interval: 30s
      timeout: 10s
      retries: 5

volumes:
  postgres_data:
```

#### Manual Setup
```bash
# Create database
createdb todowrite

# Set environment
export TODOWRITE_DATABASE_URL="postgresql://username:password@localhost:5432/todowrite"

# Initialize
todowrite init
```

### SQLite Configuration

SQLite is automatically configured with sensible defaults:

```python
# Default SQLite locations (tried in order)
DEFAULT_SQLITE_PATHS = [
    "todowrite.db",                    # Current directory
    "data/todowrite.db",               # Data subdirectory
    str(Path.home() / ".todowrite.db") # Home directory
]
```

### YAML-Only Mode

```bash
# Force YAML-only storage
export TODOWRITE_STORAGE_PREFERENCE="yaml_only"

# Or use CLI flag
todowrite --storage-preference yaml_only init
```

### Storage Status Checking

```bash
# Check current storage configuration
todowrite db-status

# Check with different preference
todowrite db-status --storage-preference postgresql_only
```

Example output:
```
🗄️  ToDoWrite Storage Status
==============================
Storage Type: postgresql
Priority Level: 1
Is Fallback: False
Storage Location: postgresql://todowrite:***@localhost:5432/todowrite
Preference: auto
Connection Status: ✅ Connected
Nodes in Database: 42

💡 Setup Guidance:
✅ PostgreSQL: Connected and operational
⚪ SQLite: Available as fallback
⚪ YAML: Available as fallback
```

---

## Validation and Tooling

### Project Development Utilities

The new ProjectManager class provides centralized utilities that replace individual scripts:

#### CLI Commands
```bash
# Check project setup
todowrite utils validate-setup /path/to/project

# Set up project integration
todowrite utils setup-integration /path/to/project --db-type postgres

# Create project structure
todowrite utils create-structure /path/to/new-project

# Check schema integrity
todowrite utils check-schema
todowrite utils check-deprecated

# Get initialization SQL
todowrite utils init-database-sql
```

#### API Usage
```python
from todowrite import setup_integration, validate_project_setup

# Set up project
setup_integration("/path/to/project", "sqlite")

# Validate project setup
results = validate_project_setup("/path/to/project")
print(f"Project valid: {results['valid']}")

# Check schema changes
from todowrite import check_schema_changes
check_schema_changes()
```

See [Project Utilities](docs/PROJECT_UTILITIES.md) for comprehensive documentation.

### JSON Schema Validation

#### Schema Location
```
configs/schemas/todowrite.schema.json
```

#### Key Validation Rules
- **ID Pattern Validation:** Enforces `^(GOAL|CON|CTX|CST|R|AC|IF|PH|STP|TSK|SUB|CMD)-[A-Z0-9_-]+$`
- **Layer Enumeration:** Validates against 12 defined layer types
- **Required Fields:** `id`, `layer`, `title`, `description`, `links`
- **Conditional Validation:**
  - Layer 12 (Command) MUST have `command` field
  - Layers 1-11 MUST NOT have `command` field
- **Metadata Constraints:** Severity and work_type enumerations

#### Validation Tools

```bash
# Manual validation
python todowrite/tools/tw_validate.py

# Strict mode (fails on warnings)
python todowrite/tools/tw_validate.py --strict

# Via Makefile
make tw-validate
```

### Separation of Concerns (SoC) Linting

Enforces architectural constraints preventing executable code in declarative layers:

```bash
# Run SoC linter
python todowrite/tools/tw_lint_soc.py

# Via Makefile
make tw-lint
```

#### SoC Rules
- **Layers 1-11:** No `command` field, no shell commands, no executable content
- **Layer 12 Only:** Can contain executable commands with proper structure
- **Forbidden Patterns:** Detects `exec()`, `subprocess`, shell command patterns in non-executable layers

### Traceability Analysis

```bash
# Build traceability matrix and dependency graph
python todowrite/tools/tw_trace.py

# Summary mode
python todowrite/tools/tw_trace.py --summary

# Via Makefile
make tw-trace
```

#### Outputs
- **`trace/trace.csv`** - Forward/backward traceability matrix
- **`trace/graph.json`** - Node/edge dependency graph
- **Console Report** - Orphaned nodes, circular dependencies

#### Traceability Features
- Forward/backward link mapping
- Orphaned node detection
- Circular dependency detection
- Dependency graph generation
- Coverage analysis

### Command Stub Generation

Automatically generates executable commands from Acceptance Criteria:

```bash
# Generate command stubs
python todowrite/tools/tw_stub_command.py

# Force regeneration
python todowrite/tools/tw_stub_command.py --force

# Via Makefile
make tw-prove
```

#### Generation Rules
- Scans `acceptance_criteria/` directory for AC-* files
- Creates corresponding CMD-* files in `commands/` directory
- Intelligent shell command generation based on AC content
- Updates AC links to include generated commands

### Git Integration

#### Conventional Commits Enforcement
```bash
# Install git hooks
make tw-hooks

# Manual installation
cp todowrite/tools/git-commit-msg-hook.sh .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

#### Commit Format
```
<type>(<scope>): <short summary>

# Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
# ToDoWrite scopes: goal, concept, context, constraints, req, ac, iface, phase, step, task, subtask, cmd, schema, lint, trace, docs

# Examples:
feat(req): add real-time communication requirement
build(schema): generate todowrite.schema.json
docs(spec): clarify Interface Contract units and endianness
```

---

## Development Workflow

### Session Startup (MANDATORY)
```bash
# Essential initialization
make tw-deps        # Install dependencies
make tw-init        # Initialize directory structure
make tw-hooks       # Install git hooks

# Validate current state
make tw-all         # Schema + lint + validate + trace + prove
```

### Development Cycle

#### Standard Development
```bash
# Development workflow
make tw-dev                           # Lint + validate + generate commands

# Make changes to YAML files
# ...

# Validate changes
make tw-validate

# Commit with conventional format
git add -A
git commit -m "feat(req): add new requirement for authentication"
```

#### Production Deployment
```bash
# Full production validation
make tw-prod                          # Complete validation + traceability

# Quality assurance
make tw-check                         # Strict validation
make tw-test                          # System tests

# Deploy
git push origin main
```

### Quality Gates

#### Pre-Commit Checks
1. **Schema Validation** - All YAML files validate against schema
2. **SoC Compliance** - No executable code in layers 1-11
3. **Traceability** - Complete forward/backward links
4. **Conventional Commits** - Proper commit message format

#### Pre-Release Checks
1. **Strict Validation** - Zero warnings/errors
2. **System Tests** - All automated tests pass
3. **Command Generation** - All AC have corresponding commands
4. **Documentation** - All APIs and interfaces documented

### Directory Management

#### Initial Project Setup
```bash
# Clone and setup
git clone <repository>
cd ToDoWrite
make tw-deps tw-init tw-hooks

# Verify setup
make tw-all
todowrite db-status
```

#### File Organization Best Practices
- **One concern per YAML file**
- **Meaningful IDs with proper prefixes**
- **Complete parent/child linking**
- **Comprehensive metadata**
- **Regular validation cycles**

---

## Examples and Usage Patterns

### Complete Project Planning Example

#### 1. Define Project Goal
```yaml
# configs/plans/goals/GOAL-IRRIGATION-SYSTEM.yaml
id: GOAL-IRRIGATION-SYSTEM
layer: Goal
title: Autonomous Irrigation System
description: >
  Develop an intelligent irrigation system that automatically adjusts
  water distribution based on soil moisture, weather forecasts, and
  crop requirements while minimizing water usage and maximizing yield.
metadata:
  owner: agricultural-team
  labels: ["work:architecture", irrigation, automation, agriculture]
  severity: high
  work_type: architecture
links:
  parents: []
  children: [CON-SENSOR-NETWORK-ARCHITECTURE]
```

#### 2. Define Architectural Concept
```yaml
# configs/plans/concepts/CON-SENSOR-NETWORK-ARCHITECTURE.yaml
id: CON-SENSOR-NETWORK-ARCHITECTURE
layer: Concept
title: Distributed Sensor Network Architecture
description: >
  Implement a mesh network of soil moisture sensors, weather stations,
  and actuators that communicate wirelessly to provide real-time field
  monitoring and control capabilities.
metadata:
  owner: systems-architect
  labels: ["work:architecture", sensors, mesh-network, wireless]
  severity: high
  work_type: architecture
links:
  parents: [GOAL-IRRIGATION-SYSTEM]
  children: [CTX-FIELD-DEPLOYMENT-ENVIRONMENT]
```

#### 3. Define Requirements
```yaml
# configs/plans/requirements/R-MOISTURE-SENSING.yaml
id: R-MOISTURE-SENSING
layer: Requirements
title: Real-time Soil Moisture Monitoring
description: >
  System must continuously monitor soil moisture levels across the field
  with sensors placed at 10-meter intervals, providing readings every
  5 minutes with ±2% accuracy.
metadata:
  owner: requirements-engineer
  labels: ["work:spec", sensors, real-time, accuracy]
  severity: high
  work_type: spec
links:
  parents: [CON-SENSOR-NETWORK-ARCHITECTURE]
  children: [AC-MOISTURE-READING-ACCURACY]
```

#### 4. Define Acceptance Criteria
```yaml
# configs/plans/acceptance_criteria/AC-MOISTURE-READING-ACCURACY.yaml
id: AC-MOISTURE-READING-ACCURACY
layer: AcceptanceCriteria
title: Moisture Reading Accuracy Validation
description: >
  PASS: Soil moisture readings are within ±2% of laboratory reference
  measurements across all sensor locations over 24-hour test period.
  FAIL: Any sensor reading deviates more than ±2% from reference.
metadata:
  owner: qa-engineer
  labels: ["work:validation", testing, accuracy, sensors]
  severity: high
  work_type: validation
links:
  parents: [R-MOISTURE-SENSING]
  children: [CMD-MOISTURE-ACCURACY-TEST]
```

#### 5. Generate and Execute Commands
```bash
# Generate command stub from AC
make tw-prove

# Results in: configs/commands/CMD-MOISTURE-ACCURACY-TEST.yaml
```

```yaml
# configs/commands/CMD-MOISTURE-ACCURACY-TEST.yaml (auto-generated)
id: CMD-MOISTURE-ACCURACY-TEST
layer: Command
title: Execute moisture reading accuracy validation
description: Automated test to verify sensor accuracy against laboratory reference
metadata:
  owner: qa-engineer
  labels: [generated, automated, testing]
  severity: high
  work_type: validation
links:
  parents: [AC-MOISTURE-READING-ACCURACY]
  children: []
command:
  ac_ref: AC-MOISTURE-READING-ACCURACY
  run:
    shell: python tests/sensor_accuracy.py --duration 24h --tolerance 2%
    workdir: .
    env:
      TEST_MODE: accuracy_validation
      AC_REF: AC-MOISTURE-READING-ACCURACY
  artifacts:
    - results/CMD-MOISTURE-ACCURACY-TEST/accuracy_report.json
    - results/CMD-MOISTURE-ACCURACY-TEST/sensor_data.csv
```

### API Integration Example

#### Using Python Module
```python
from todowrite import ToDoWrite

# Initialize application
app = ToDoWrite()

# Create complete planning hierarchy
goal = app.add_goal(
    title="Smart Greenhouse Control",
    description="Automated climate control for optimal plant growth",
    owner="greenhouse-team"
)

concept = app.add_concept(
    title="Multi-Zone Climate Control",
    description="Independent temperature and humidity control per zone",
    parent_ids=[goal.id],
    owner="systems-architect"
)

requirement = app.add_requirement(
    title="Temperature Control Precision",
    description="Maintain temperature within ±1°C of target across all zones",
    parent_ids=[concept.id],
    severity="high"
)

ac = app.add_acceptance_criteria(
    title="Temperature Control Validation",
    description="PASS: All zones maintain target ±1°C for 48 hours continuous",
    parent_ids=[requirement.id]
)

# Generate and execute validation command
command = app.add_command(
    title="Execute Temperature Control Test",
    description="Automated temperature control validation",
    ac_ref=ac.id,
    shell_command="python tests/temperature_control.py --zones all --duration 48h",
    artifacts=["results/temperature_validation.json"]
)

# Get complete hierarchy
hierarchy = app.get_all_nodes()
for layer, nodes in hierarchy.items():
    print(f"{layer}: {len(nodes)} nodes")
```

### Makefile Integration Example

```bash
# Custom project Makefile extending ToDoWrite
# Project-specific Makefile

include ToDoWrite/Makefile

# Project-specific targets
.PHONY: deploy test-integration build-docs

# Custom development workflow
dev-full: tw-dev test-integration
	@echo "Complete development cycle finished"

# Integration with ToDoWrite validation
test-integration: tw-validate
	@echo "Running integration tests..."
	@python -m pytest tests/integration/ -v
	@todowrite todowrite execute-commands --all

# Documentation build with validation
build-docs: tw-check
	@echo "Building documentation with ToDoWrite validation..."
	@sphinx-build -b html docs/ docs/_build/
	@todowrite todowrite show-hierarchy --format json > docs/hierarchy.json

# Deployment pipeline
deploy: tw-prod test-integration build-docs
	@echo "Deploying with full ToDoWrite validation..."
	@docker build -t irrigation-system .
	@docker push irrigation-system:latest
```

### Advanced Traceability Example

```bash
# Generate comprehensive traceability report
todowrite todowrite trace-links

# View specific node traceability
todowrite todowrite show-hierarchy --layer requirements --format tree

# Check for orphaned nodes
python todowrite/tools/tw_trace.py --summary
```

Example traceability output:
```
📊 Traceability Analysis Summary
================================
Total Nodes: 47
Properly Linked: 45
Orphaned Nodes: 2
Circular Dependencies: 0

🔗 Dependency Chain Coverage:
Goals → Concepts: 100%
Concepts → Requirements: 95%
Requirements → Acceptance Criteria: 90%
Acceptance Criteria → Commands: 100%

⚠️  Orphaned Nodes:
- R-LEGACY-REQUIREMENT (no parents)
- AC-OBSOLETE-TEST (no children)

✅ No circular dependencies detected
```

---

## Appendix

### File Extensions and Naming Conventions
- **YAML Files:** `.yaml` extension (not `.yml`)
- **ID Format:** `{PREFIX}-{IDENTIFIER}` where identifier uses uppercase, numbers, hyphens, underscores
- **File Names:** Match the ID exactly (e.g., `GOAL-AGRICULTURAL-AUTOMATION.yaml`)
- **Directory Names:** Lowercase with underscores (e.g., `acceptance_criteria/`)

### Version Compatibility
- **Python:** 3.12+ (required for type union syntax)
- **Dependencies:** See `pyproject.toml` for exact versions
- **Database:** PostgreSQL 12+, SQLite 3.31+
- **Git:** Any recent version (hooks use standard format)

### Performance Considerations
- **YAML Files:** Suitable for projects up to ~1000 nodes
- **SQLite:** Handles 10,000+ nodes efficiently
- **PostgreSQL:** Recommended for enterprise scale (100,000+ nodes)
- **Traceability:** O(n²) complexity - optimize for large projects

### Troubleshooting Common Issues

#### Schema Validation Failures
```bash
# Check specific file
python todowrite/tools/tw_validate.py configs/plans/goals/GOAL-*.yaml

# Verbose error output
python todowrite/tools/tw_validate.py --strict
```

#### Storage Backend Issues
```bash
# Check storage status
todowrite db-status

# Force storage preference
export TODOWRITE_STORAGE_PREFERENCE="sqlite_only"
todowrite init
```

#### Git Hook Problems
```bash
# Reinstall hooks
make tw-hooks

# Test commit message format
echo "feat(req): test message" | .git/hooks/commit-msg
```

### Contributing Guidelines
1. **Follow 12-Layer Architecture** - Respect SoC principles
2. **Validate Before Commit** - Run `make tw-check`
3. **Use Conventional Commits** - Required for all changes
4. **Maintain Traceability** - Link all nodes properly
5. **Update Documentation** - Keep this file current
6. **Test Thoroughly** - Run `make tw-test` before PR

---

*This documentation covers ToDoWrite. For the latest version, see the VERSION file.*
