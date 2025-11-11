# TDD Red-Green-Refactor Compliance Demonstration

## MANDATORY TDD Methodology

This document demonstrates the exact TDD workflow that **ALL** development sessions **MUST** follow. No code may be generated without tests.

### Step 1: RED - Write Failing Test

```python
# tests/test_web_package_api.py
import pytest
from todowrite_web.api.backend.main import app
from fastapi.testclient import TestClient

def test_create_node_endpoint_returns_201():
    """
    RED: Test does not exist yet, will fail
    Testing that POST /api/v1/nodes returns 201 status
    """
    client = TestClient(app)
    response = client.post(
        "/api/v1/nodes",
        json={
            "type": "goal",
            "title": "Test Goal",
            "description": "Test Description"
        }
    )

    assert response.status_code == 201
    assert response.json()["type"] == "goal"
    assert response.json()["id"].startswith("GOAL-")
```

**Run Test (Expected to FAIL):**
```bash
# Using pytest with coverage
uv run pytest tests/test_web_package_api.py::test_create_node_endpoint_returns_201 -v

# Expected output: FAILED - AttributeError: module 'todowrite_web.api.backend.main' has no attribute 'app'
```

### Step 2: GREEN - Minimal Implementation

```python
# web_package/src/todowrite_web/api/backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ToDoWrite Web API")

class NodeCreateRequest(BaseModel):
    type: str
    title: str
    description: str

class NodeResponse(BaseModel):
    id: str
    type: str
    title: str
    description: str

@app.post("/api/v1/nodes", response_model=NodeResponse, status_code=201)
def create_node(request: NodeCreateRequest) -> NodeResponse:
    """
    GREEN: Minimal implementation to pass the test
    """
    import uuid

    node_id = f"{request.type.upper()}-{uuid.uuid4().hex[:8]}"

    return NodeResponse(
        id=node_id,
        type=request.type,
        title=request.title,
        description=request.description
    )
```

**Run Test (Expected to PASS):**
```bash
uv run pytest tests/test_web_package_api.py::test_create_node_endpoint_returns_201 -v

# Expected output: PASSED
```

### Step 3: REFACTOR - Enhanced Implementation

```python
# web_package/src/todowrite_web/api/backend/main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, validator
from typing import Optional
import uuid
from datetime import datetime

app = FastAPI(title="ToDoWrite Web API")

# Constants
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000
VALID_NODE_TYPES = {
    "goal", "concept", "context", "constraint",
    "requirement", "acceptance_criteria", "interface_contract",
    "phase", "step", "task", "subtask", "command"
}

class NodeCreateRequest(BaseModel):
    type: str
    title: str
    description: str
    metadata: Optional[dict] = None

    @validator('type')
    def validate_node_type(cls, v):
        if v not in VALID_NODE_TYPES:
            raise ValueError(f"Invalid node type: {v}. Must be one of {VALID_NODE_TYPES}")
        return v

    @validator('title')
    def validate_title_length(cls, v):
        if len(v) > MAX_TITLE_LENGTH:
            raise ValueError(f"Title too long: {len(v)} > {MAX_TITLE_LENGTH}")
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @validator('description')
    def validate_description_length(cls, v):
        if len(v) > MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"Description too long: {len(v)} > {MAX_DESCRIPTION_LENGTH}")
        return v.strip()

class NodeResponse(BaseModel):
    id: str
    type: str
    title: str
    description: str
    created_at: str
    metadata: Optional[dict] = None

def get_database():
    """Dependency injection for database connection"""
    # TODO: Implement actual database connection
    pass

@app.post("/api/v1/nodes", response_model=NodeResponse, status_code=201)
def create_node(request: NodeCreateRequest, db=Depends(get_database)) -> NodeResponse:
    """
    REFACTOR: Enhanced implementation with validation, typing, and error handling
    """
    node_id = f"{request.type.upper()}-{uuid.uuid4().hex[:8]}"

    # TODO: Save to database
    # save_node_to_database(db, request.dict(), node_id)

    return NodeResponse(
        id=node_id,
        type=request.type,
        title=request.title,
        description=request.description,
        created_at=datetime.utcnow().isoformat(),
        metadata=request.metadata
    )
```

**Run All Tests (Expected to PASS):**
```bash
uv run pytest tests/test_web_package_api.py -v --cov=todowrite_web.api.backend

# Expected output: PASSED with coverage report
```

## Local CLI Tools Integration (MANDATORY)

### Using grep for Test Discovery
```bash
# Find all test files in web_package
find web_package -name "test_*.py" -type f

# Find all API endpoint tests
grep -r "def test_.*endpoint" web_package/tests/

# Find all FastAPI route definitions
grep -r "@app\." web_package/src/
```

### Using awk for Test Metrics
```bash
# Count tests by module
awk '
/^def test_/ {
    gsub(/\(.*$/, "", $0)
    tests[FILENAME]++
}
END {
    for (file in tests) {
        print file ": " tests[file] " tests"
    }
    print "Total: " length(tests) " tests"
}
' web_package/tests/*.py
```

### Using sed for Test Updates
```bash
# Add import statement to all test files
find web_package/tests -name "*.py" -exec sed -i '1i import pytest\n' {} \;

# Replace assert statements with more descriptive assertions
sed -i 's/assert response.status_code == 200/assert response.status_code == 200, f"Expected 200, got {response.status_code}"/g' web_package/tests/*.py
```

### Using patch for Code Review
```bash
# Create patch for reviewer
git diff web_package/src/todowrite_web/api/backend/main.py > api_implementation.patch

# Apply reviewer's suggested changes
git apply reviewer_suggestions.patch
```

## Token Optimization Patterns

### Efficient Test Organization
```python
# Use parametrized tests to reduce code duplication
@pytest.mark.parametrize("node_type,expected_prefix", [
    ("goal", "GOAL"),
    ("task", "TASK"),
    ("concept", "CONCEPT"),
])
def test_node_id_generation(node_type, expected_prefix):
    """Single test covers multiple scenarios"""
    request = NodeCreateRequest(
        type=node_type,
        title="Test Title",
        description="Test Description"
    )
    response = create_node(request)
    assert response.id.startswith(expected_prefix)
```

### Use Fixtures for Repeated Setup
```python
@pytest.fixture
def client():
    """Reusable FastAPI test client"""
    return TestClient(app)

@pytest.fixture
def sample_node_request():
    """Reusable test data"""
    return NodeCreateRequest(
        type="goal",
        title="Test Goal",
        description="Test Description"
    )

def test_create_node_with_fixture(client, sample_node_request):
    """Test using reusable fixtures"""
    response = client.post("/api/v1/nodes", json=sample_node_request.dict())
    assert response.status_code == 201
```

## Mandatory Compliance Checklist

For EVERY development session:

### ✅ RED Phase
- [ ] Write test that FAILS before implementation
- [ ] Test follows naming convention: `test_<feature>_<scenario>`
- [ ] Test is specific and isolated
- [ ] Test includes clear assertions

### ✅ GREEN Phase
- [ ] Write MINIMAL code to make test pass
- [ ] No extra functionality beyond test requirements
- [ ] Code follows project style guidelines
- [ ] All existing tests still pass

### ✅ REFACTOR Phase
- [ ] Enhance implementation while keeping tests passing
- [ ] Add proper error handling and validation
- [ ] Improve code organization and readability
- [ ] Update/add tests for new functionality
- [ ] Maintain 100% test coverage

### ✅ CLI Tools Usage
- [ ] Use `grep` for code analysis and discovery
- [ ] Use `sed` for bulk transformations
- [ ] Use `awk` for data processing and metrics
- [ ] Use `patch` for code review and changes

### ✅ Token Optimization
- [ ] Use episodic memory to search past solutions
- [ ] Write reusable test fixtures and utilities
- [ ] Use parametrized tests for multiple scenarios
- [ ] Avoid redundant test code

## Example Session Workflow

```bash
# 1. Check episodic memory for similar features
~/.claude/plugins/cache/episodic-memory/cli/search-conversations "FastAPI endpoint creation"

# 2. Write failing test (RED)
# Edit tests/test_web_package_api.py

# 3. Run test (expect failure)
uv run pytest tests/test_web_package_api.py::test_create_node_endpoint_returns_201 -v

# 4. Implement minimal code (GREEN)
# Edit web_package/src/todowrite_web/api/backend/main.py

# 5. Run test (expect success)
uv run pytest tests/test_web_package_api.py::test_create_node_endpoint_returns_201 -v

# 6. Refactor and enhance
# Improve implementation with validation and error handling

# 7. Run all tests (ensure no regressions)
uv run uv run pytest tests/test_web_package_api.py -v --cov=todowrite_web.api.backend

# 8. Use CLI tools for code quality
uv run ruff check web_package/src/todowrite_web/api/backend/main.py
uv run pyright web_package/src/todowrite_web/api/backend/main.py

# 9. Index knowledge for future sessions
~/.claude/plugins/cache/episodic-memory/cli/episodic-memory index --cleanup
```

This methodology ensures robust, maintainable code with zero regressions and maximum development efficiency.
