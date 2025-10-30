# ToDoWrite API Documentation

## Table of Contents
1. [API Overview](#api-overview)
2. [Python Module API (Implemented)](#python-module-api-implemented)
3. [REST API Specification (Planned)](#rest-api-specification-planned)
4. [Data Models and Schema](#data-models-and-schema)
5. [Authentication and Security](#authentication-and-security)
6. [Error Handling](#error-handling)
7. [API Usage Examples](#api-usage-examples)
8. [Implementation Roadmap](#implementation-roadmap)

---

## API Overview

ToDoWrite provides multiple API interfaces for interacting with the 12-layer declarative planning framework:

### Current Implementation Status

| Interface Type | Status | Description |
|---|---|---|
| **Python Module API** | ✅ **Implemented** | Programmatic interface via `ToDoWrite` class |
| **CLI API** | ✅ **Implemented** | Command-line interface via `todowrite` commands |
| **REST API** | 📋 **Planned** | HTTP/JSON API specified in interface contracts |

### Interface Contracts

**Primary API Contract:** `IF-TODOWRITE-API-SCHEMA.yaml`
```yaml
id: IF-TODOWRITE-API-SCHEMA
layer: InterfaceContract
title: ToDoWrite API and CLI Interface Specification
description: >
  CLI Commands: todowrite create {layer} {id} --title "..." --description "..."
  API Endpoints: POST /api/v1/{layer}/, GET /api/v1/{layer}/{id},
  PUT /api/v1/{layer}/{id}, DELETE /api/v1/{layer}/{id}
  Schema Validation: All YAML must validate against todowrite.schema.json
  File Naming: {LAYER_PREFIX}-{IDENTIFIER}.yaml in configs/plans/{layer}/
  ID Pattern: ^(GOAL|CON|CTX|CST|R|AC|IF|PH|STP|TSK|SUB|CMD)-[A-Z0-9_-]+$
```

**Status Tracking API Contract:** `IF-STATUS-TRACKING-API.yaml`
```yaml
id: IF-STATUS-TRACKING-API
layer: InterfaceContract
title: Status Tracking API and CLI Interface Specification
description: >
  CLI Commands: todowrite status update {node-id} --status {value} --progress {0-100}
  todowrite status show --format {tree|flat|json} --filter {status}
  todowrite status report --since {date} --include-completed
  Schema Fields: status (planned|in_progress|completed|blocked|cancelled),
  progress (0-100), started_date (ISO 8601), completion_date (ISO 8601)
```

---

## Python Module API (Implemented)

### Installation and Initialization

```python
from todowrite import ToDoWrite

# Initialize with automatic storage detection
app = ToDoWrite()

# Initialize with specific storage preference
app = ToDoWrite(storage_preference="postgresql_only")

# Initialize with custom database URL
import os
os.environ['TODOWRITE_DATABASE_URL'] = 'postgresql://user:pass@localhost:5432/todowrite'
app = ToDoWrite()
```

### Core CRUD Operations

#### Create Node
```python
def create_node(self, node_data: dict[str, Any]) -> Node
```

**Parameters:**
- `node_data`: Dictionary containing node specification

**Example:**
```python
node_data = {
    "id": "GOAL-SMART-FARMING",
    "layer": "Goal",
    "title": "Smart Farming Initiative",
    "description": "Implement precision agriculture using IoT sensors and AI",
    "links": {"parents": [], "children": []},
    "metadata": {
        "owner": "agricultural-team",
        "labels": ["work:architecture", "iot", "farming"],
        "severity": "high",
        "work_type": "architecture"
    }
}

node = app.create_node(node_data)
print(f"Created node: {node.id}")
```

#### Retrieve Node
```python
def get_node(self, node_id: str) -> Node | None
```

**Parameters:**
- `node_id`: Unique node identifier (e.g., "GOAL-SMART-FARMING")

**Example:**
```python
node = app.get_node("GOAL-SMART-FARMING")
if node:
    print(f"Title: {node.title}")
    print(f"Owner: {node.metadata.owner}")
    print(f"Status: {node.status}")
else:
    print("Node not found")
```

#### List All Nodes
```python
def get_all_nodes(self) -> dict[str, list[Node]]
```

**Returns:** Dictionary with layer names as keys, list of nodes as values

**Example:**
```python
all_nodes = app.get_all_nodes()
for layer, nodes in all_nodes.items():
    print(f"\n{layer} ({len(nodes)} nodes):")
    for node in nodes:
        print(f"  - {node.id}: {node.title}")
```

#### Update Node
```python
def update_node(self, node_id: str, node_data: dict[str, Any]) -> Node | None
```

**Parameters:**
- `node_id`: Node to update
- `node_data`: Dictionary of fields to update

**Example:**
```python
updates = {
    "status": "in_progress",
    "metadata": {
        "owner": "new-owner",
        "severity": "med"
    }
}
updated_node = app.update_node("GOAL-SMART-FARMING", updates)
```

#### Delete Node
```python
def delete_node(self, node_id: str) -> None
```

**Example:**
```python
app.delete_node("GOAL-SMART-FARMING")
```

### Layer-Specific Factory Methods

#### Create Goal (Layer 1)
```python
def add_goal(
    self,
    title: str,
    description: str,
    owner: str = "system",
    labels: list[str] | None = None,
    severity: str = "",
    work_type: str = "architecture"
) -> Node
```

**Example:**
```python
goal = app.add_goal(
    title="Autonomous Greenhouse Control",
    description="Develop AI-driven climate control for optimal plant growth",
    owner="greenhouse-team",
    labels=["work:architecture", "ai", "greenhouse"],
    severity="high"
)
```

#### Create Phase (Layer 8)
```python
def add_phase(
    self,
    parent_ids: list[str],
    title: str,
    description: str,
    owner: str = "system",
    **kwargs
) -> Node
```

**Example:**
```python
phase = app.add_phase(
    parent_ids=["GOAL-GREENHOUSE-CONTROL"],
    title="Sensor Integration Phase",
    description="Install and configure IoT sensors throughout greenhouse",
    owner="iot-team"
)
```

#### Create Task (Layer 10)
```python
def add_task(
    self,
    parent_ids: list[str],
    title: str,
    description: str,
    owner: str = "system",
    severity: str = "",
    **kwargs
) -> Node
```

**Example:**
```python
task = app.add_task(
    parent_ids=["PH-SENSOR-INTEGRATION"],
    title="Install Temperature Sensors",
    description="Deploy wireless temperature sensors at 5-meter intervals",
    owner="technician-alice",
    severity="med"
)
```

#### Create Command (Layer 12)
```python
def add_command(
    self,
    title: str,
    description: str,
    ac_ref: str,
    shell_command: str,
    workdir: str = ".",
    env: dict[str, str] | None = None,
    artifacts: list[str] | None = None,
    **kwargs
) -> Node
```

**Example:**
```python
command = app.add_command(
    title="Validate Sensor Readings",
    description="Execute automated validation of sensor accuracy",
    ac_ref="AC-SENSOR-ACCURACY-95PERCENT",
    shell_command="python tests/sensor_validation.py --threshold 0.95",
    env={"TEST_MODE": "validation"},
    artifacts=[
        "results/CMD-SENSOR-VALIDATION/accuracy_report.json",
        "results/CMD-SENSOR-VALIDATION/sensor_data.csv"
    ]
)
```

### Utility and Management Methods

#### Database Initialization
```python
def init_database(self) -> None
```

Creates database tables if they don't exist.

#### Session Management
```python
def get_session(self) -> Session
```

Returns SQLAlchemy session for advanced database operations.

#### Data Loading
```python
def load_todos(self) -> list[Node]
```

Loads all nodes from storage.

#### Active Items
```python
def get_active_items(self) -> list[Node]
```

Returns nodes with status "in_progress".

#### Storage Information
```python
@property
def storage_type(self) -> StorageType
```

Returns current storage backend type.

```python
def is_database_storage(self) -> bool
```

Returns True if using PostgreSQL or SQLite.

### Complete Layer Hierarchy Methods

```python
# Layer 1: Goal
app.add_goal(title, description, owner, **kwargs)

# Layer 2: Concept
app.add_concept(parent_ids, title, description, owner, **kwargs)

# Layer 3: Context
app.add_context(parent_ids, title, description, owner, **kwargs)

# Layer 4: Constraints
app.add_constraint(parent_ids, title, description, owner, **kwargs)

# Layer 5: Requirements
app.add_requirement(parent_ids, title, description, owner, **kwargs)

# Layer 6: Acceptance Criteria
app.add_acceptance_criteria(parent_ids, title, description, owner, **kwargs)

# Layer 7: Interface Contract
app.add_interface_contract(parent_ids, title, description, owner, **kwargs)

# Layer 8: Phase
app.add_phase(parent_ids, title, description, owner, **kwargs)

# Layer 9: Step
app.add_step(parent_ids, title, description, owner, **kwargs)

# Layer 10: Task
app.add_task(parent_ids, title, description, owner, **kwargs)

# Layer 11: SubTask
app.add_subtask(parent_ids, title, description, owner, **kwargs)

# Layer 12: Command
app.add_command(title, description, ac_ref, shell_command, **kwargs)
```

---

## REST API Specification (Planned)

**Status:** 📋 Specified in interface contracts but not yet implemented

### Base Configuration

```
Base URL: http://localhost:8000/api/v1/
Framework: FastAPI (planned)
Authentication: JWT Bearer tokens (planned)
Content-Type: application/json
```

### API Versioning

```
v1: /api/v1/  - Current planned version
```

### Core Node Management Endpoints

#### List Nodes by Layer
```http
GET /api/v1/{layer}/
```

**Parameters:**
- `layer`: One of 12 layer types (goal, concept, context, constraints, requirements, acceptance_criteria, interface_contracts, phase, step, task, subtask, command)

**Query Parameters:**
- `limit`: Number of results (default: 100)
- `offset`: Pagination offset (default: 0)
- `status`: Filter by status (planned, in_progress, blocked, done, rejected)
- `owner`: Filter by owner
- `severity`: Filter by severity (low, med, high)

**Response:**
```json
{
  "layer": "goal",
  "total": 15,
  "limit": 100,
  "offset": 0,
  "nodes": [
    {
      "id": "GOAL-SMART-FARMING",
      "layer": "Goal",
      "title": "Smart Farming Initiative",
      "description": "Implement precision agriculture using IoT sensors and AI",
      "status": "in_progress",
      "metadata": {
        "owner": "agricultural-team",
        "labels": ["work:architecture", "iot", "farming"],
        "severity": "high",
        "work_type": "architecture"
      },
      "links": {
        "parents": [],
        "children": ["CON-IOT-SENSOR-NETWORK", "CON-AI-DECISION-ENGINE"]
      },
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-20T14:22:00Z"
    }
  ]
}
```

#### Create Node
```http
POST /api/v1/{layer}/
```

**Request Body:**
```json
{
  "id": "GOAL-GREENHOUSE-AUTOMATION",
  "title": "Greenhouse Automation System",
  "description": "Develop autonomous greenhouse climate control",
  "metadata": {
    "owner": "greenhouse-team",
    "labels": ["work:architecture", "automation"],
    "severity": "high",
    "work_type": "architecture"
  },
  "links": {
    "parents": [],
    "children": []
  }
}
```

**Response:** `201 Created`
```json
{
  "id": "GOAL-GREENHOUSE-AUTOMATION",
  "layer": "Goal",
  "title": "Greenhouse Automation System",
  "description": "Develop autonomous greenhouse climate control",
  "status": "planned",
  "metadata": {
    "owner": "greenhouse-team",
    "labels": ["work:architecture", "automation"],
    "severity": "high",
    "work_type": "architecture"
  },
  "links": {
    "parents": [],
    "children": []
  },
  "created_at": "2024-01-21T09:15:00Z",
  "updated_at": "2024-01-21T09:15:00Z"
}
```

#### Get Specific Node
```http
GET /api/v1/{layer}/{id}
```

**Example:**
```http
GET /api/v1/goal/GOAL-SMART-FARMING
```

**Response:** `200 OK`
```json
{
  "id": "GOAL-SMART-FARMING",
  "layer": "Goal",
  "title": "Smart Farming Initiative",
  "description": "Implement precision agriculture using IoT sensors and AI",
  "status": "in_progress",
  "metadata": {
    "owner": "agricultural-team",
    "labels": ["work:architecture", "iot", "farming"],
    "severity": "high",
    "work_type": "architecture"
  },
  "links": {
    "parents": [],
    "children": ["CON-IOT-SENSOR-NETWORK", "CON-AI-DECISION-ENGINE"]
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T14:22:00Z"
}
```

#### Update Node
```http
PUT /api/v1/{layer}/{id}
```

**Request Body:**
```json
{
  "status": "done",
  "metadata": {
    "owner": "new-owner",
    "severity": "med"
  }
}
```

**Response:** `200 OK` (returns updated node)

#### Delete Node
```http
DELETE /api/v1/{layer}/{id}
```

**Response:** `204 No Content`

### Cross-Layer Operations

#### List All Nodes
```http
GET /api/v1/nodes/
```

**Query Parameters:**
- `layer`: Filter by specific layer
- `status`: Filter by status
- `owner`: Filter by owner
- `search`: Text search in title/description
- `limit`, `offset`: Pagination

**Response:**
```json
{
  "total": 127,
  "nodes_by_layer": {
    "Goal": 5,
    "Concept": 12,
    "Requirements": 23,
    "Task": 45,
    "Command": 18
  },
  "nodes": [
    // Array of nodes from all layers
  ]
}
```

#### Get Hierarchy View
```http
GET /api/v1/hierarchy/
```

**Query Parameters:**
- `root_id`: Start from specific node
- `depth`: Maximum depth to traverse
- `format`: `tree` | `flat` | `graph`

**Response:**
```json
{
  "format": "tree",
  "root_nodes": [
    {
      "id": "GOAL-SMART-FARMING",
      "title": "Smart Farming Initiative",
      "layer": "Goal",
      "children": [
        {
          "id": "CON-IOT-SENSOR-NETWORK",
          "title": "IoT Sensor Network",
          "layer": "Concept",
          "children": [...]
        }
      ]
    }
  ]
}
```

#### Get Node Traceability
```http
GET /api/v1/trace/{id}
```

**Response:**
```json
{
  "node_id": "R-SENSOR-ACCURACY",
  "layer": "Requirements",
  "ancestors": [
    {"id": "GOAL-SMART-FARMING", "layer": "Goal", "distance": 2},
    {"id": "CON-IOT-SENSORS", "layer": "Concept", "distance": 1}
  ],
  "descendants": [
    {"id": "AC-95PERCENT-ACCURACY", "layer": "AcceptanceCriteria", "distance": 1},
    {"id": "CMD-SENSOR-VALIDATION", "layer": "Command", "distance": 2}
  ],
  "siblings": [
    {"id": "R-SENSOR-RELIABILITY", "layer": "Requirements"}
  ]
}
```

#### Validate Node Data
```http
POST /api/v1/validate/
```

**Request Body:**
```json
{
  "id": "GOAL-TEST-VALIDATION",
  "layer": "Goal",
  "title": "Test Goal",
  "description": "Testing validation",
  "links": {"parents": [], "children": []}
}
```

**Response:** `200 OK`
```json
{
  "valid": true,
  "errors": [],
  "warnings": []
}
```

### Command Execution Endpoints (Layer 12)

#### Execute Command
```http
POST /api/v1/commands/{id}/execute
```

**Request Body:**
```json
{
  "async": true,
  "timeout": 300,
  "env_overrides": {
    "DEBUG": "true"
  }
}
```

**Response:** `202 Accepted`
```json
{
  "execution_id": "exec-cmd-sensor-validation-20240121-091500",
  "command_id": "CMD-SENSOR-VALIDATION",
  "status": "running",
  "started_at": "2024-01-21T09:15:00Z",
  "estimated_duration": 180
}
```

#### Get Command Execution Status
```http
GET /api/v1/commands/{id}/status
```

**Response:**
```json
{
  "command_id": "CMD-SENSOR-VALIDATION",
  "status": "completed",
  "started_at": "2024-01-21T09:15:00Z",
  "completed_at": "2024-01-21T09:18:23Z",
  "duration": 203,
  "exit_code": 0,
  "artifacts_generated": 3
}
```

#### Get Command Artifacts
```http
GET /api/v1/commands/{id}/artifacts
```

**Response:**
```json
{
  "command_id": "CMD-SENSOR-VALIDATION",
  "artifacts": [
    {
      "path": "results/CMD-SENSOR-VALIDATION/accuracy_report.json",
      "size": 1547,
      "created_at": "2024-01-21T09:18:20Z",
      "download_url": "/api/v1/artifacts/cmd-sensor-validation/accuracy_report.json"
    },
    {
      "path": "results/CMD-SENSOR-VALIDATION/sensor_data.csv",
      "size": 8924,
      "created_at": "2024-01-21T09:18:23Z",
      "download_url": "/api/v1/artifacts/cmd-sensor-validation/sensor_data.csv"
    }
  ]
}
```

### Bulk Operations

#### Bulk Import
```http
POST /api/v1/import/
```

**Request:** `multipart/form-data` with YAML files

#### Bulk Export
```http
GET /api/v1/export/
```

**Query Parameters:**
- `format`: `yaml` | `json`
- `layers`: Comma-separated layer list
- `include_artifacts`: Include command artifacts

---

## Data Models and Schema

### Core Data Types

```typescript
// TypeScript-style definitions for API

type LayerType =
  | "Goal" | "Concept" | "Context" | "Constraints"
  | "Requirements" | "AcceptanceCriteria" | "InterfaceContract"
  | "Phase" | "Step" | "Task" | "SubTask" | "Command"

type StatusType = "planned" | "in_progress" | "blocked" | "done" | "rejected"

type SeverityType = "low" | "med" | "high"

type WorkType =
  | "architecture" | "spec" | "interface" | "validation"
  | "implementation" | "docs" | "ops" | "refactor" | "chore" | "test"
```

### Node Model

```typescript
interface Node {
  id: string                    // Pattern: ^(GOAL|CON|CTX|CST|R|AC|IF|PH|STP|TSK|SUB|CMD)-[A-Z0-9_-]+$
  layer: LayerType
  title: string                 // Required, min length 1
  description: string
  status: StatusType            // Default: "planned"
  metadata: Metadata
  links: Links
  command?: Command             // Only for layer "Command"
  created_at: string           // ISO 8601 timestamp
  updated_at: string           // ISO 8601 timestamp
}

interface Metadata {
  owner?: string
  labels: string[]
  severity?: SeverityType
  work_type?: WorkType
}

interface Links {
  parents: string[]             // Array of node IDs
  children: string[]            // Array of node IDs
}

interface Command {
  ac_ref: string               // Pattern: ^AC-[A-Z0-9_-]+$
  run: CommandRun
  artifacts: string[]          // File paths
}

interface CommandRun {
  shell: string                // Required: shell command to execute
  workdir?: string             // Working directory, default "."
  env?: Record<string, string> // Environment variables
}
```

### Request/Response Models

#### Create Node Request
```typescript
interface CreateNodeRequest {
  id: string
  title: string
  description: string
  metadata?: Partial<Metadata>
  links?: Partial<Links>
  command?: Command             // Only for Command layer
}
```

#### Update Node Request
```typescript
interface UpdateNodeRequest {
  title?: string
  description?: string
  status?: StatusType
  metadata?: Partial<Metadata>
  links?: Partial<Links>
  command?: Command
}
```

#### List Response
```typescript
interface ListResponse<T> {
  total: number
  limit: number
  offset: number
  items: T[]
}
```

#### Error Response
```typescript
interface ErrorResponse {
  error: string                // Error type
  message: string              // Human-readable message
  details?: Record<string, any> // Additional error context
  timestamp: string            // ISO 8601 timestamp
}
```

### JSON Schema Validation

All API requests validate against the JSON Schema defined in `configs/schemas/todowrite.schema.json`:

**Key Validation Rules:**
- **ID Pattern:** Must match layer prefix pattern
- **Required Fields:** id, layer, title, description, links
- **Layer Constraints:** Command layer must have command field, others must not
- **Enum Validation:** layer, status, severity, work_type must be valid values
- **Links Structure:** parents and children must be arrays of strings

**Example Validation Error:**
```json
{
  "error": "ValidationError",
  "message": "Node validation failed",
  "details": {
    "field": "id",
    "constraint": "pattern",
    "expected": "^GOAL-[A-Z0-9_-]+$",
    "received": "goal-invalid-format"
  },
  "timestamp": "2024-01-21T09:15:00Z"
}
```

---

## Authentication and Security

### Planned Authentication

**Method:** JWT Bearer tokens
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### User Roles (Planned)

```typescript
interface User {
  id: string
  username: string
  email: string
  roles: Role[]
}

interface Role {
  name: string              // "admin", "manager", "developer", "viewer"
  permissions: Permission[]
}

type Permission =
  | "node:create" | "node:read" | "node:update" | "node:delete"
  | "command:execute" | "command:view_artifacts"
  | "system:admin" | "export:all"
```

### Security Features (Planned)

- **Rate Limiting:** 1000 requests/hour per user
- **CORS Configuration:** Configurable allowed origins
- **Input Sanitization:** All string inputs sanitized
- **SQL Injection Protection:** Parameterized queries only
- **File Upload Security:** Whitelist YAML/JSON only
- **Audit Logging:** All API calls logged with user context

---

## Error Handling

### HTTP Status Codes

| Code | Description | Usage |
|------|-------------|-------|
| 200 | OK | Successful GET, PUT |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Missing/invalid auth token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Node does not exist |
| 409 | Conflict | Node ID already exists |
| 422 | Unprocessable Entity | Validation errors |
| 500 | Internal Server Error | Server-side errors |

### Error Response Format

```json
{
  "error": "ValidationError",
  "message": "Node validation failed",
  "details": {
    "field": "links.parents",
    "error": "Parent node 'GOAL-NONEXISTENT' does not exist"
  },
  "timestamp": "2024-01-21T09:15:00Z",
  "request_id": "req-7f3a8b9c-1234-5678-9abc-def012345678"
}
```

### Common Error Scenarios

#### Validation Errors
```json
{
  "error": "ValidationError",
  "message": "Multiple validation errors",
  "details": {
    "errors": [
      {
        "field": "id",
        "message": "ID must match pattern ^GOAL-[A-Z0-9_-]+$"
      },
      {
        "field": "title",
        "message": "Title cannot be empty"
      }
    ]
  }
}
```

#### Dependency Errors
```json
{
  "error": "DependencyError",
  "message": "Cannot delete node with dependencies",
  "details": {
    "node_id": "GOAL-SMART-FARMING",
    "dependent_children": ["CON-IOT-SENSORS", "CON-AI-ENGINE"],
    "suggestion": "Delete children first or use force_cascade=true"
  }
}
```

#### Command Execution Errors
```json
{
  "error": "ExecutionError",
  "message": "Command execution failed",
  "details": {
    "command_id": "CMD-SENSOR-VALIDATION",
    "exit_code": 1,
    "stderr": "FileNotFoundError: test_data.csv not found",
    "execution_time": 12.5
  }
}
```

---

## API Usage Examples

### Complete Agricultural Project Setup

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"
headers = {"Authorization": "Bearer YOUR_JWT_TOKEN"}

# 1. Create main goal
goal_data = {
    "id": "GOAL-PRECISION-AGRICULTURE",
    "title": "Precision Agriculture System",
    "description": "Develop IoT-enabled precision agriculture for optimal crop yields",
    "metadata": {
        "owner": "agricultural-team",
        "labels": ["work:architecture", "iot", "agriculture", "precision"],
        "severity": "high",
        "work_type": "architecture"
    },
    "links": {"parents": [], "children": []}
}

response = requests.post(f"{BASE_URL}/goal/", json=goal_data, headers=headers)
goal = response.json()
print(f"Created goal: {goal['id']}")

# 2. Create concept
concept_data = {
    "id": "CON-SENSOR-MESH-NETWORK",
    "title": "Wireless Sensor Mesh Network",
    "description": "Distributed sensor network for real-time field monitoring",
    "metadata": {
        "owner": "network-architect",
        "labels": ["work:architecture", "wireless", "sensors", "mesh"],
        "severity": "high",
        "work_type": "architecture"
    },
    "links": {
        "parents": ["GOAL-PRECISION-AGRICULTURE"],
        "children": []
    }
}

response = requests.post(f"{BASE_URL}/concept/", json=concept_data, headers=headers)
concept = response.json()

# 3. Create requirement
requirement_data = {
    "id": "R-REAL-TIME-MONITORING",
    "title": "Real-time Environmental Monitoring",
    "description": "System must provide soil moisture, temperature, and pH readings every 5 minutes",
    "metadata": {
        "owner": "requirements-engineer",
        "labels": ["work:spec", "real-time", "monitoring"],
        "severity": "high",
        "work_type": "spec"
    },
    "links": {
        "parents": ["CON-SENSOR-MESH-NETWORK"],
        "children": []
    }
}

response = requests.post(f"{BASE_URL}/requirements/", json=requirement_data, headers=headers)

# 4. Create acceptance criteria
ac_data = {
    "id": "AC-MONITORING-ACCURACY",
    "title": "Monitoring Data Accuracy Validation",
    "description": "PASS: All sensor readings accurate within ±2% compared to laboratory standards",
    "metadata": {
        "owner": "qa-engineer",
        "labels": ["work:validation", "accuracy", "testing"],
        "severity": "high",
        "work_type": "validation"
    },
    "links": {
        "parents": ["R-REAL-TIME-MONITORING"],
        "children": []
    }
}

response = requests.post(f"{BASE_URL}/acceptance_criteria/", json=ac_data, headers=headers)

# 5. Create executable command
command_data = {
    "id": "CMD-ACCURACY-VALIDATION",
    "title": "Execute Sensor Accuracy Validation",
    "description": "Automated test comparing sensor readings to laboratory standards",
    "metadata": {
        "owner": "test-engineer",
        "labels": ["generated", "automated", "validation"],
        "severity": "med",
        "work_type": "validation"
    },
    "links": {
        "parents": ["AC-MONITORING-ACCURACY"],
        "children": []
    },
    "command": {
        "ac_ref": "AC-MONITORING-ACCURACY",
        "run": {
            "shell": "python tests/sensor_accuracy.py --field-sensors all --lab-reference standards/lab_data.json",
            "workdir": ".",
            "env": {
                "TEST_MODE": "accuracy_validation",
                "TOLERANCE": "2"
            }
        },
        "artifacts": [
            "results/CMD-ACCURACY-VALIDATION/accuracy_report.json",
            "results/CMD-ACCURACY-VALIDATION/sensor_comparison.csv"
        ]
    }
}

response = requests.post(f"{BASE_URL}/command/", json=command_data, headers=headers)
command = response.json()

# 6. Execute the command
execution_response = requests.post(
    f"{BASE_URL}/commands/{command['id']}/execute",
    json={"async": True, "timeout": 600},
    headers=headers
)
execution = execution_response.json()
print(f"Started execution: {execution['execution_id']}")

# 7. Check execution status
status_response = requests.get(
    f"{BASE_URL}/commands/{command['id']}/status",
    headers=headers
)
status = status_response.json()
print(f"Execution status: {status['status']}")

# 8. Get project hierarchy
hierarchy_response = requests.get(
    f"{BASE_URL}/hierarchy/?root_id=GOAL-PRECISION-AGRICULTURE",
    headers=headers
)
hierarchy = hierarchy_response.json()
print("Project hierarchy:", json.dumps(hierarchy, indent=2))
```

### Status Tracking and Progress Management

```python
# Update node status
status_update = {
    "status": "in_progress",
    "metadata": {
        "owner": "field-engineer",
        "labels": ["work:implementation", "sensors", "deployment"]
    }
}

response = requests.put(
    f"{BASE_URL}/task/TSK-DEPLOY-SENSORS",
    json=status_update,
    headers=headers
)

# Get all in-progress items
in_progress = requests.get(
    f"{BASE_URL}/nodes/?status=in_progress",
    headers=headers
)

print("Items in progress:")
for node in in_progress.json()['nodes']:
    print(f"- {node['id']}: {node['title']} (Owner: {node['metadata']['owner']})")

# Get project completion status
completion_stats = requests.get(
    f"{BASE_URL}/nodes/?limit=1000",
    headers=headers
)

nodes = completion_stats.json()['nodes']
status_counts = {}
for node in nodes:
    status = node['status']
    status_counts[status] = status_counts.get(status, 0) + 1

print("Project completion status:")
for status, count in status_counts.items():
    print(f"  {status}: {count} nodes")
```

---

## Implementation Roadmap

### Phase 1: Core REST API (Planned)

**Dependencies to Add:**
```toml
dependencies = [
    # ... existing dependencies
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "pydantic>=2.5.0",
    "python-jose>=3.3.0",  # JWT handling
    "python-multipart>=0.0.6",  # File uploads
]
```

**Implementation Tasks:**
1. **FastAPI Application Setup**
   - Create `todowrite/api/main.py`
   - Configure CORS, middleware
   - Add OpenAPI documentation

2. **Route Implementation**
   - Node CRUD endpoints
   - Layer-specific routes
   - Cross-layer operations

3. **Request/Response Models**
   - Pydantic models for validation
   - Error response models
   - Pagination models

4. **Authentication System**
   - JWT token handling
   - User management
   - Role-based permissions

### Phase 2: Advanced Features (Future)

1. **Real-time Updates**
   - WebSocket connections
   - Event streaming
   - Live hierarchy updates

2. **File Management**
   - Artifact upload/download
   - YAML import/export API
   - Bulk operations

3. **Monitoring & Analytics**
   - API metrics
   - Performance monitoring
   - Usage analytics

### Phase 3: Enterprise Features (Future)

1. **Scalability**
   - Database connection pooling
   - Caching layer (Redis)
   - Load balancing support

2. **Integration**
   - Webhook support
   - External system APIs
   - CI/CD pipeline integration

3. **Advanced Security**
   - OAuth2 integration
   - API key management
   - Audit logging

### Development Guide

**To implement the REST API:**

1. **Add FastAPI dependencies**
2. **Create API module structure:**
   ```
   todowrite/api/
   ├── __init__.py
   ├── main.py              # FastAPI app
   ├── routes/
   │   ├── __init__.py
   │   ├── nodes.py         # Node CRUD routes
   │   ├── layers.py        # Layer-specific routes
   │   ├── commands.py      # Command execution routes
   │   └── admin.py         # Admin operations
   ├── models/
   │   ├── __init__.py
   │   ├── requests.py      # Pydantic request models
   │   ├── responses.py     # Pydantic response models
   │   └── auth.py          # Authentication models
   ├── middleware/
   │   ├── __init__.py
   │   ├── auth.py          # JWT authentication
   │   ├── cors.py          # CORS configuration
   │   └── logging.py       # Request logging
   └── utils/
       ├── __init__.py
       ├── security.py      # Security utilities
       └── validation.py    # Additional validation
   ```

3. **Update Docker configuration** to include API service
4. **Add API tests** in `tests/test_api.py`
5. **Update documentation** with live API examples

The REST API implementation would reuse all existing business logic from the `ToDoWrite` class, providing a web interface to the same functionality currently available via CLI and Python module.

---

*This API documentation covers both implemented (Python module) and planned (REST API) interfaces for ToDoWrite v0.1.7.0. The REST API specifications are based on the interface contracts defined in the planning framework.*
