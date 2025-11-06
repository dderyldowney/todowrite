# TodoWrite Library Verification and Repair Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Comprehensively verify that the TodoWrite library is clean, working properly, and all tests are testing actual implementation rather than mock behavior.

**Architecture:** Systematic verification of core library functionality, starting with failing tests and expanding to cover all components. Focus on real behavior verification.

**Tech Stack:** Python library with SQLite/PostgreSQL backends, pytest testing framework, real file operations.

---

## Task 1: Fix Progress Field Implementation Issue

**Files:**
- Modify: `lib_package/src/todowrite/core/app.py:67-90` (Node creation logic)
- Test: `tests/library/test_api.py:460-482, 338-370` (Progress field tests)

**Step 1: Investigate current progress field behavior**

```python
# Run failing tests to understand exact issue
PYTHONPATH="lib_package/src:cli_package/src" python -m pytest tests/library/test_api.py::TestNodeAPI::test_node_to_dict -v
PYTHONPATH="lib_package/src:cli_package/src" python -m pytest tests/library/test_api.py::TestNodeAPI::test_node_status_progress_properties -v
```

**Step 2: Run test to verify current behavior**

Run: `PYTHONPATH="lib_package/src:cli_package/src" python -c "from todowrite import ToDoWrite; app = ToDoWrite('sqlite:///tmp/debug.db'); app.init_database(); node = app.create_node({'id': 'TEST', 'layer': 'Task', 'title': 'Test', 'progress': 75, 'links': {'parents': [], 'children': []}, 'metadata': {'owner': 'dev', 'labels': []}}); print('Progress:', node.progress); print('To dict progress:', node.to_dict().get('progress'))"`

Expected: Progress is 0 instead of 75, indicating database/implementation issue

**Step 3: Examine database models and app.py**

Read: `lib_package/src/todowrite/database/models.py`
Read: `lib_package/src/todowrite/core/app.py` (specifically create_node and node retrieval logic)

**Step 4: Identify root cause**

Find where progress field gets lost between Node creation and database storage/retrieval

**Step 5: Fix the implementation**

Update the database storage/retrieval logic to properly preserve the progress field

**Step 6: Run tests to verify fix**

Run: `PYTHONPATH="lib_package/src:cli_package/src" python -m pytest tests/library/test_api.py::TestNodeAPI::test_node_to_dict -v`
Run: `PYTHONPATH="lib_package/src:cli_package/src" python -m pytest tests/library/test_api.py::TestNodeAPI::test_node_status_progress_properties -v`
Expected: Both tests PASS

**Step 7: Commit**

```bash
git add lib_package/src/todowrite/core/app.py lib_package/src/todowrite/database/models.py tests/library/test_api.py
git commit -m "fix: resolve progress field storage/retrieval issue"
```

## Task 2: Comprehensive Library API Verification

**Files:**
- Test: `tests/library/test_api.py` (All API tests)
- Modify: `lib_package/src/todowrite/core/__init__.py` (Verify exports)

**Step 1: Run full library API test suite**

Run: `PYTHONPATH="lib_package/src:cli_package/src" python -m pytest tests/library/test_api.py -v`

Expected: All tests pass (after Task 1 fix)

**Step 2: Verify all public API functions work**

```python
# Test all convenience functions
PYTHONPATH="lib_package/src:cli_package/src" python -c "
from todowrite import create_node, get_node, update_node, delete_node, list_nodes, link_nodes, unlink_nodes
import tempfile, os

# Test all functions with real database
db_url = 'sqlite:///tmp/api_test.db'
os.system('rm -f /tmp/api_test.db')

# Test create_node
node = create_node(db_url, {'id': 'TEST-001', 'layer': 'Task', 'title': 'API Test', 'links': {'parents': [], 'children': []}, 'metadata': {'owner': 'dev', 'labels': []}})
print('✓ create_node works')

# Test get_node
retrieved = get_node(db_url, 'TEST-001')
print('✓ get_node works:', retrieved.id if retrieved else 'None')

# Test update_node
updated = update_node(db_url, 'TEST-001', {'title': 'Updated Title'})
print('✓ update_node works:', updated.title if updated else 'None')

# Test list_nodes
all_nodes = list_nodes(db_url)
print('✓ list_nodes works, count:', len(all_nodes))

# Clean up
os.remove('/tmp/api_test.db')
print('✓ All API functions verified')
"
```

**Step 3: Verify Node object methods**

```python
# Test Node object methods comprehensively
PYTHONPATH="lib_package/src:cli_package/src" python -c "
from todowrite import ToDoWrite, Node
import os

db_url = 'sqlite:///tmp/node_test.db'
os.system('rm -f /tmp/node_test.db')

app = ToDoWrite(db_url)
app.init_database()

# Create comprehensive node
node_data = {
    'id': 'NODE-TEST-001',
    'layer': 'Task',
    'title': 'Comprehensive Test',
    'description': 'Full test',
    'status': 'in_progress',
    'progress': 65,
    'links': {'parents': [], 'children': []},
    'metadata': {
        'owner': 'developer',
        'labels': ['test', 'important'],
        'severity': 'high',
        'work_type': 'testing',
        'assignee': 'tester'
    }
}

node = app.create_node(node_data)

# Test all Node methods
print('✓ Node creation:', node.id)
print('✓ Node str:', str(node))
print('✓ Node repr:', repr(node))
print('✓ Node to_dict keys:', list(node.to_dict().keys()))
print('✓ Node metadata access:', node.metadata.owner)
print('✓ Node links access:', len(node.links.children))

# Test Node.from_dict
node_dict = node.to_dict()
recreated = Node.from_dict(node_dict)
print('✓ Node.from_dict works:', recreated.id)

# Test equality
print('✓ Node equality:', node == recreated)

os.remove('/tmp/node_test.db')
print('✓ Node object methods verified')
"
```

**Step 4: Run all library tests and verify coverage**

Run: `PYTHONPATH="lib_package/src:cli_package/src" python -m pytest tests/library/ -v --cov=lib_package/src/todowrite --cov-report=term-missing`

Expected: All library tests pass, good coverage on core components

**Step 5: Commit any fixes discovered**

```bash
git add -A
git commit -m "fix: resolve library API verification issues"
```

## Task 3: Database Storage Verification

**Files:**
- Modify: `lib_package/src/todowrite/database/models.py` (Verify database schema)
- Test: `tests/database/test_models.py` (Database model tests)

**Step 1: Test database models directly**

Run: `PYTHONPATH="lib_package/src:cli_package/src" python -m pytest tests/database/test_models.py -v`

Expected: All database model tests pass

**Step 2: Verify SQLite backend**

```python
# Test SQLite operations comprehensively
PYTHONPATH="lib_package/src:cli_package/src" python -c "
from todowrite import ToDoWrite
import tempfile
import os

# Test with real SQLite database
db_path = '/tmp/sqlite_verification.db'
db_url = f'sqlite:///{db_path}'
os.system('rm -f ' + db_path)

print('Testing SQLite backend...')
app = ToDoWrite(db_url)
app.init_database()
print('✓ SQLite initialization')

# Test CRUD operations
node = app.create_node({
    'id': 'SQLITE-TEST-001',
    'layer': 'Task',
    'title': 'SQLite Test',
    'description': 'Test SQLite backend',
    'links': {'parents': [], 'children': []},
    'metadata': {'owner': 'dev', 'labels': ['sqlite-test']}
})
print('✓ SQLite create')

retrieved = app.get_node('SQLITE-TEST-001')
print('✓ SQLite retrieve:', retrieved.id if retrieved else 'Failed')

# Test update
updated = app.update_node('SQLITE-TEST-001', {'title': 'Updated SQLite Test'})
print('✓ SQLite update:', updated.title if updated else 'Failed')

# Test listing
all_nodes = app.get_all_nodes()
print('✓ SQLite list:', len(all_nodes))

# Clean up
os.remove(db_path)
print('✓ SQLite backend verified')
"
```

**Step 3: Verify schema validation**

```python
# Test that database schema validation works
PYTHONPATH="lib_package/src:cli_package/src" python -c "
from todowrite.storage import validate_database_schema
from todowrite import ToDoWrite
import os

db_path = '/tmp/schema_validation.db'
db_url = f'sqlite:///{db_path}'
os.system('rm -f ' + db_path)

app = ToDoWrite(db_url)
app.init_database()

# Test schema validation
try:
    validate_database_schema(db_url)
    print('✓ Database schema validation passed')
except Exception as e:
    print('✗ Schema validation failed:', e)

os.remove(db_path)
"
```

**Step 4: Test data integrity**

```python
# Test that data is preserved correctly
PYTHONPATH="lib_package/src:cli_package/src" python -c "
from todowrite import ToDoWrite
import os

db_path = '/tmp/data_integrity.db'
db_url = f'sqlite:///{db_path}'
os.system('rm -f ' + db_path)

app = ToDoWrite(db_url)
app.init_database()

# Create comprehensive test data
test_data = {
    'id': 'INTEGRITY-TEST-001',
    'layer': 'Goal',
    'title': 'Data Integrity Test',
    'description': 'Test preserving all fields',
    'status': 'in_progress',
    'progress': 42,
    'links': {'parents': [], 'children': []},
    'metadata': {
        'owner': 'test-user',
        'labels': ['integrity', 'test', 'data'],
        'severity': 'medium',
        'work_type': 'verification',
        'assignee': 'tester'
    }
}

original = app.create_node(test_data)
print('✓ Original created')

# Retrieve and compare
retrieved = app.get_node('INTEGRITY-TEST-001')
print('✓ Retrieved')

# Check critical fields
assert retrieved.id == original.id, 'ID mismatch'
assert retrieved.title == original.title, 'Title mismatch'
assert retrieved.status == original.status, 'Status mismatch'
assert retrieved.progress == original.progress, 'Progress mismatch'
assert retrieved.metadata.owner == original.metadata.owner, 'Owner mismatch'
assert retrieved.metadata.labels == original.metadata.labels, 'Labels mismatch'

print('✓ Data integrity verified')
os.remove(db_path)
"
```

**Step 5: Commit any database fixes**

```bash
git add lib_package/src/todowrite/database/ tests/database/
git commit -m "fix: resolve database storage and integrity issues"
```

## Task 4: Storage Layer Verification

**Files:**
- Test: `tests/storage/test_yaml.py` (YAML storage tests)
- Modify: `lib_package/src/todowrite/storage/yaml_manager.py` (YAML operations)

**Step 1: Run storage tests**

Run: `PYTHONPATH="lib_package/src:cli_package/src" python -m pytest tests/storage/ -v`

Expected: All storage tests pass

**Step 2: Test YAML operations directly**

```python
# Test YAML storage operations
PYTHONPATH="lib_package/src:cli_package/src" python -c "
from todowrite.storage import YAMLManager
import tempfile
import os
import yaml

# Test with real YAML files
with tempfile.TemporaryDirectory() as tmp_dir:
    yaml_path = os.path.join(tmp_dir, 'test.yaml')

    # Test YAML manager
    manager = YAMLManager(yaml_path)
    print('✓ YAML Manager initialization')

    # Test writing data
    test_data = {
        'nodes': {
            'TEST-001': {
                'id': 'TEST-001',
                'layer': 'Task',
                'title': 'YAML Test',
                'description': 'Test YAML operations',
                'status': 'planned',
                'links': {'parents': [], 'children': []},
                'metadata': {'owner': 'test', 'labels': []}
            }
        }
    }

    manager.write_yaml(test_data)
    print('✓ YAML write operation')

    # Test reading data
    read_data = manager.read_yaml()
    assert read_data['nodes']['TEST-001']['title'] == 'YAML Test'
    print('✓ YAML read operation')

    # Test file exists
    assert os.path.exists(yaml_path)
    print('✓ YAML file creation')

print('✓ YAML storage operations verified')
"
```

**Step 3: Test schema validation with YAML**

```python
# Test YAML schema validation
PYTHONPATH="lib_package/src:cli_package/src" python -c "
from todowrite.storage import validate_node_data, YAMLManager
import tempfile
import os

with tempfile.TemporaryDirectory() as tmp_dir:
    # Test valid node data
    valid_node = {
        'id': 'VALID-001',
        'layer': 'Task',
        'title': 'Valid Node',
        'description': 'This should pass validation',
        'links': {'parents': [], 'children': []},
        'metadata': {'owner': 'dev', 'labels': []}
    }

    try:
        validate_node_data(valid_node)
        print('✓ Valid node validation passed')
    except Exception as e:
        print('✗ Valid node validation failed:', e)

    # Test invalid node data
    invalid_node = {
        'id': 'INVALID-001',
        # Missing required fields
    }

    try:
        validate_node_data(invalid_node)
        print('✗ Invalid node validation should have failed')
    except Exception as e:
        print('✓ Invalid node validation correctly failed:', type(e).__name__)

print('✓ YAML schema validation verified')
"
```

**Step 4: Verify import/export functionality**

```python
# Test data import/export
PYTHONPATH="lib_package/src:cli_package/src" python -c "
from todowrite import ToDoWrite, import_nodes, export_nodes
import os
import json

db_path = '/tmp/import_export.db'
db_url = f'sqlite:///{db_path}'
os.system('rm -f ' + db_path)

# Initialize with data
app = ToDoWrite(db_url)
app.init_database()

# Create test nodes
nodes_to_create = [
    {
        'id': 'IMPORT-TEST-001',
        'layer': 'Goal',
        'title': 'Import Test Goal',
        'description': 'Test import functionality',
        'links': {'parents': [], 'children': []},
        'metadata': {'owner': 'dev', 'labels': ['import-test']}
    },
    {
        'id': 'IMPORT-TEST-002',
        'layer': 'Task',
        'title': 'Import Test Task',
        'description': 'Test import functionality',
        'links': {'parents': [], 'children': []},
        'metadata': {'owner': 'dev', 'labels': ['import-test']}
    }
]

for node_data in nodes_to_create:
    app.create_node(node_data)

print('✓ Test data created')

# Export data
export_path = '/tmp/test_export.json'
exported_nodes = export_nodes(db_url, export_path)
print('✓ Data exported:', len(exported_nodes))

# Verify export file exists and contains data
with open(export_path, 'r') as f:
    exported_data = json.load(f)
    assert len(exported_data) > 0
    print('✓ Export file verified')

# Clean up
os.remove(db_path)
os.remove(export_path)
print('✓ Import/export functionality verified')
"
```

**Step 5: Commit storage layer fixes**

```bash
git add lib_package/src/todowrite/storage/ tests/storage/
git commit -m "fix: resolve storage layer verification issues"
```

## Task 5: Schema Validation Verification

**Files:**
- Test: `tests/schema/test_validation.py` (Schema validation tests)
- Modify: `lib_package/src/todowrite/storage/schema_validator.py` (Schema validation logic)

**Step 1: Run schema validation tests**

Run: `PYTHONPATH="lib_package/src:cli_package/src" python -m pytest tests/schema/test_validation.py -v`

Expected: All schema validation tests pass

**Step 2: Test comprehensive schema validation**

```python
# Test all schema validation rules
PYTHONPATH="lib_package/src:cli_package/src" python -c "
from todowrite.storage import validate_node_data, validate_database_schema
from todowrite import LayerType, StatusType

# Test all valid layer types
valid_layers = list(LayerType.__args__) if hasattr(LayerType, '__args__') else ['Goal', 'Concept', 'Context', 'Constraints', 'Requirements', 'AcceptanceCriteria', 'InterfaceContract', 'Phase', 'Step', 'Task', 'SubTask', 'Command']

for layer in valid_layers:
    valid_node = {
        'id': f'VALID-{layer.upper()}-001',
        'layer': layer,
        'title': f'Valid {layer}',
        'description': f'Test valid {layer} node',
        'links': {'parents': [], 'children': []},
        'metadata': {'owner': 'dev', 'labels': []}
    }

    try:
        validate_node_data(valid_node)
        print(f'✓ {layer} validation passed')
    except Exception as e:
        print(f'✗ {layer} validation failed:', e)

# Test all valid status types
valid_statuses = list(StatusType.__args__) if hasattr(StatusType, '__args__') else ['planned', 'in_progress', 'completed', 'blocked', 'cancelled']

for status in valid_statuses:
    valid_node = {
        'id': f'STATUS-{status.upper()}-001',
        'layer': 'Task',
        'title': f'Test {status} status',
        'status': status,
        'links': {'parents': [], 'children': []},
        'metadata': {'owner': 'dev', 'labels': []}
    }

    try:
        validate_node_data(valid_node)
        print(f'✓ {status} validation passed')
    except Exception as e:
        print(f'✗ {status} validation failed:', e)

print('✓ Comprehensive schema validation completed')
"
```

**Step 3: Test edge cases and error handling**

```python
# Test schema validation edge cases
PYTHONPATH="lib_package/src:cli_package/src" python -c "
from todowrite.storage import validate_node_data

# Test missing required fields
test_cases = [
    ({'title': 'No ID'}, 'Missing ID'),
    ({'id': 'NO-LAYER-001', 'title': 'No Layer'}, 'Missing layer'),
    ({'id': 'NO-TITLE-001', 'layer': 'Task'}, 'Missing title'),
    ({'id': 'INVALID-LAYER-001', 'layer': 'InvalidLayer', 'title': 'Test'}, 'Invalid layer'),
    ({'id': 'INVALID-STATUS-001', 'layer': 'Task', 'title': 'Test', 'status': 'InvalidStatus'}, 'Invalid status'),
]

for test_data, description in test_cases:
    try:
        # Add default required fields if not present
        if 'links' not in test_data:
            test_data['links'] = {'parents': [], 'children': []}
        if 'metadata' not in test_data:
            test_data['metadata'] = {'owner': 'dev', 'labels': []}
        if 'layer' not in test_data:
            test_data['layer'] = 'Task'
        if 'title' not in test_data:
            test_data['title'] = 'Test'

        validate_node_data(test_data)
        print(f'✗ {description} should have failed')
    except Exception as e:
        print(f'✓ {description} correctly rejected:', type(e).__name__)

print('✓ Schema validation edge cases verified')
"
```

**Step 4: Commit schema validation fixes**

```bash
git add lib_package/src/todowrite/storage/ tests/schema/
git commit -m "fix: resolve schema validation verification issues"
```

## Task 6: Real Workflow Verification

**Files:**
- Test: `tests/workflows/test_user_library_workflows.py` (User workflow tests)

**Step 1: Run workflow tests**

Run: `PYTHONPATH="lib_package/src:cli_package/src" python -m pytest tests/workflows/test_user_library_workflows.py -v`

Expected: All workflow tests pass

**Step 2: Test complete user workflows**

```python
# Test realistic user workflows
PYTHONPATH="lib_package/src:cli_package/src" python -c "
from todowrite import ToDoWrite
import os

db_path = '/tmp/workflow_test.db'
db_url = f'sqlite:///{db_path}'
os.system('rm -f ' + db_path)

print('Testing real user workflows...')

# Initialize project
app = ToDoWrite(db_url)
app.init_database()
print('✓ Project initialization')

# Create goal hierarchy
goal = app.create_node({
    'id': 'PROJECT-GOAL-001',
    'layer': 'Goal',
    'title': 'Build TodoWrite Library',
    'description': 'Create comprehensive task management library',
    'status': 'in_progress',
    'progress': 25,
    'links': {'parents': [], 'children': []},
    'metadata': {
        'owner': 'project-lead',
        'labels': ['library', 'python'],
        'severity': 'high',
        'work_type': 'development'
    }
})
print('✓ Goal creation:', goal.title)

# Create concepts
concept1 = app.create_node({
    'id': 'CONCEPT-001',
    'layer': 'Concept',
    'title': 'Hierarchical Task Structure',
    'description': '12-layer declarative framework',
    'links': {'parents': [], 'children': []},
    'metadata': {'owner': 'architect', 'labels': ['concept', 'hierarchy']}
})

concept2 = app.create_node({
    'id': 'CONCEPT-002',
    'layer': 'Concept',
    'title': 'Database Abstraction',
    'description': 'Multi-backend database support',
    'links': {'parents': [], 'children': []},
    'metadata': {'owner': 'architect', 'labels': ['concept', 'database']}
})
print('✓ Concepts created')

# Create tasks
task1 = app.create_node({
    'id': 'TASK-001',
    'layer': 'Task',
    'title': 'Implement Core Types',
    'description': 'Create Node, Metadata, Link dataclasses',
    'status': 'completed',
    'progress': 100,
    'links': {'parents': [], 'children': []},
    'metadata': {
        'owner': 'developer',
        'labels': ['implementation'],
        'severity': 'medium'
    }
})

task2 = app.create_node({
    'id': 'TASK-002',
    'layer': 'Task',
    'title': 'Implement Database Layer',
    'description': 'SQLite and PostgreSQL support',
    'status': 'in_progress',
    'progress': 60,
    'links': {'parents': [], 'children': []},
    'metadata': {
        'owner': 'developer',
        'labels': ['implementation', 'database'],
        'severity': 'medium'
    }
})
print('✓ Tasks created')

# Link hierarchy
from todowrite.core.app import link_nodes

link_nodes(db_url, goal.id, concept1.id)
link_nodes(db_url, goal.id, concept2.id)
link_nodes(db_url, concept2.id, task2.id)
print('✓ Hierarchy linked')

# Verify hierarchy
all_nodes = app.get_all_nodes()
total_nodes = sum(len(nodes) for nodes in all_nodes.values())
print(f'✓ Total nodes in system: {total_nodes}')

# Test search functionality
from todowrite import search_nodes
results = search_nodes(db_url, {'status': 'in_progress'})
print(f'✓ Search results: {len(results)} nodes with in_progress status')

# Test progress tracking
goals = all_nodes.get('Goal', [])
if goals:
    goal_progress = goals[0].progress
    print(f'✓ Goal progress tracking: {goal_progress}%')

os.remove(db_path)
print('✓ Real user workflow verification completed')
"
```

**Step 3: Test error handling workflows**

```python
# Test error handling in workflows
PYTHONPATH="lib_package/src:cli_package/src" python -c "
from todowrite import ToDoWrite, get_node, update_node, delete_node
from todowrite.core.exceptions import NodeNotFoundError
import os

db_path = '/tmp/error_handling.db'
db_url = f'sqlite:///{db_path}'
os.system('rm -f ' + db_path)

app = ToDoWrite(db_url)
app.init_database()

# Test getting non-existent node
try:
    result = get_node(db_url, 'NONEXISTENT')
    assert result is None
    print('✓ Non-existent node returns None')
except Exception as e:
    print(f'✗ Non-existent node handling failed: {e}')

# Test updating non-existent node
try:
    result = update_node(db_url, 'NONEXISTENT', {'title': 'Should not work'})
    assert result is None
    print('✓ Non-existent update returns None')
except Exception as e:
    print(f'✗ Non-existent update handling failed: {e}')

# Test deleting non-existent node (should not raise)
try:
    delete_node(db_url, 'NONEXISTENT')
    print('✓ Non-existent delete does not raise')
except Exception as e:
    print(f'✗ Non-existent delete handling failed: {e}')

# Test invalid data handling
try:
    invalid_node = {
        'id': 'INVALID-001',
        'layer': 'InvalidLayer',
        'title': 'Should fail validation',
        'links': {'parents': [], 'children': []},
        'metadata': {'owner': 'dev', 'labels': []}
    }
    node = app.create_node(invalid_node)
    print('✗ Invalid node creation should have failed')
except Exception as e:
    print(f'✓ Invalid node correctly rejected: {type(e).__name__}')

os.remove(db_path)
print('✓ Error handling workflows verified')
"
```

**Step 4: Commit workflow fixes**

```bash
git add tests/workflows/
git commit -m "fix: resolve user workflow verification issues"
```

## Task 7: Final Comprehensive Verification

**Files:**
- Test: All test files
- Modify: Any remaining implementation issues

**Step 1: Run full test suite with coverage**

Run: `PYTHONPATH="lib_package/src:cli_package/src" python -m pytest tests/ -v --cov=lib_package/src/todowrite --cov-report=term-missing --cov-report=html`

Expected: All tests pass, coverage ≥ 80%

**Step 2: Verify no mocking artifacts**

```bash
# Search for any mock imports or usage in tests
grep -r "from unittest.mock\|import mock\|@patch\|Mock\(" tests/ || echo "No mocking found - good!"
grep -r "MagicMock\|Mock(\|mock_" tests/ || echo "No mock objects found - good!"
```

Expected: No mocking found in library tests

**Step 3: Test library installation and import**

```bash
# Test that library can be installed and imported
cd /tmp
cp -r /Users/dderyldowney/Documents/GitHub/dderyldowney/todowrite/lib_package .
cd lib_package
pip install -e .
python -c "import todowrite; print('✓ Library imports successfully after installation'); from todowrite import ToDoWrite, Node; print('✓ Core classes importable'); print(f'✓ Version: {todowrite.__version__}')"
```

Expected: Clean installation and import

**Step 4: Performance verification**

```python
# Test library performance with realistic data
PYTHONPATH="lib_package/src:cli_package/src" python -c "
import time
from todowrite import ToDoWrite
import os

db_path = '/tmp/performance_test.db'
db_url = f'sqlite:///{db_path}'
os.system('rm -f ' + db_path)

app = ToDoWrite(db_url)
app.init_database()

# Test performance with many nodes
start_time = time.time()
for i in range(100):
    node_data = {
        'id': f'PERF-TASK-{i:03d}',
        'layer': 'Task',
        'title': f'Performance Test Task {i}',
        'description': f'Test task number {i} for performance verification',
        'links': {'parents': [], 'children': []},
        'metadata': {'owner': 'perf-tester', 'labels': ['performance']}
    }
    app.create_node(node_data)

create_time = time.time() - start_time
print(f'✓ Created 100 nodes in {create_time:.2f} seconds')

# Test retrieval performance
start_time = time.time()
all_nodes = app.get_all_nodes()
retrieval_time = time.time() - start_time
total_nodes = sum(len(nodes) for nodes in all_nodes.values())
print(f'✓ Retrieved {total_nodes} nodes in {retrieval_time:.2f} seconds')

# Test individual node retrieval
start_time = time.time()
for i in range(0, 100, 10):
    node = app.get_node(f'PERF-TASK-{i:03d}')
    assert node is not None
individual_time = time.time() - start_time
print(f'✓ Retrieved 10 individual nodes in {individual_time:.2f} seconds')

os.remove(db_path)
print('✓ Performance verification completed')
"
```

**Step 5: Static analysis verification**

```bash
# Run static analysis tools
PYTHONPATH="lib_package/src:cli_package/src" mypy lib_package/src/todowrite --ignore-missing-imports
PYTHONPATH="lib_package/src:cli_package/src" ruff check lib_package/src/todowrite
PYTHONPATH="lib_package/src:cli_package/src" ruff format lib_package/src/todowrite --check
```

Expected: No critical static analysis issues

**Step 6: Final integration test**

```python
# Final comprehensive integration test
PYTHONPATH="lib_package/src:cli_package/src" python -c "
print('Running final comprehensive integration test...')

# Test all major library components
from todowrite import (
    ToDoWrite, Node, Metadata, Link,
    create_node, get_node, update_node, delete_node,
    list_nodes, search_nodes, link_nodes, unlink_nodes,
    export_nodes, import_nodes,
    validate_node, validate_schema,
    LayerType, StatusType
)

import os
import tempfile

# Create temporary database
db_fd, db_path = tempfile.mkstemp(suffix='.db')
os.close(db_fd)
db_url = f'sqlite:///{db_path}'

try:
    # Test initialization
    app = ToDoWrite(db_url)
    app.init_database()
    print('✓ Initialization')

    # Test core CRUD operations
    node = create_node(db_url, {
        'id': 'FINAL-TEST-001',
        'layer': 'Task',
        'title': 'Final Integration Test',
        'description': 'Comprehensive test of all functionality',
        'status': 'in_progress',
        'progress': 50,
        'links': {'parents': [], 'children': []},
        'metadata': {
            'owner': 'integration-tester',
            'labels': ['final', 'integration', 'test'],
            'severity': 'high',
            'work_type': 'verification'
        }
    })
    print('✓ Node creation')

    # Test retrieval and validation
    retrieved = get_node(db_url, 'FINAL-TEST-001')
    assert retrieved is not None
    assert retrieved.id == node.id
    assert retrieved.progress == 50
    print('✓ Node retrieval')

    # Test validation
    validate_node(retrieved.to_dict())
    print('✓ Node validation')

    # Test update
    updated = update_node(db_url, 'FINAL-TEST-001', {
        'progress': 75,
        'status': 'completed'
    })
    assert updated.progress == 75
    assert updated.status == 'completed'
    print('✓ Node update')

    # Test listing
    all_nodes = list_nodes(db_url)
    assert len(all_nodes) > 0
    print('✓ Node listing')

    # Test search
    search_results = search_nodes(db_url, {'owner': 'integration-tester'})
    assert len(search_results) > 0
    print('✓ Node search')

    # Test linking
    parent_node = create_node(db_url, {
        'id': 'FINAL-PARENT-001',
        'layer': 'Goal',
        'title': 'Parent Goal',
        'description': 'Parent for linking test',
        'links': {'parents': [], 'children': []},
        'metadata': {'owner': 'tester', 'labels': []}
    })

    link_result = link_nodes(db_url, parent_node.id, retrieved.id)
    assert link_result == True
    print('✓ Node linking')

    # Test Node object methods
    node_dict = retrieved.to_dict()
    recreated = Node.from_dict(node_dict)
    assert recreated.id == retrieved.id
    assert recreated.progress == 75
    print('✓ Node serialization')

    # Test metadata access
    assert retrieved.metadata.owner == 'integration-tester'
    assert 'final' in retrieved.metadata.labels
    print('✓ Metadata access')

    # Test type definitions
    assert 'Task' in LayerType.__args__ if hasattr(LayerType, '__args__') else True
    assert 'completed' in StatusType.__args__ if hasattr(StatusType, '__args__') else True
    print('✓ Type definitions')

    print('✅ ALL INTEGRATION TESTS PASSED - LIBRARY IS CLEAN AND FUNCTIONAL')

finally:
    # Clean up
    os.unlink(db_path)
"
```

**Step 7: Final commit and documentation**

```bash
git add -A
git commit -m "feat: complete library verification and repair

- Fixed progress field storage/retrieval issue
- Verified all API functions work with real implementations
- Confirmed database storage integrity
- Tested storage layer operations
- Validated schema enforcement
- Verified real user workflows
- Ensured no mocking artifacts in tests
- Confirmed performance characteristics
- Validated static analysis compliance

TodoWrite library is now clean, functional, and thoroughly verified"

echo "🎉 Library verification completed successfully!"
echo "📋 Summary:"
echo "   ✅ All tests passing (2 failing tests fixed)"
echo "   ✅ Real implementations verified (no mocks)"
echo "   ✅ Database integrity confirmed"
echo "   ✅ API functionality verified"
echo "   ✅ Storage layer working"
echo "   ✅ Schema validation enforced"
echo "   ✅ User workflows tested"
echo "   ✅ Static analysis clean"
echo "   ✅ Performance acceptable"
echo ""
echo "🚀 TodoWrite library is ready for production use!"
```

---

**Plan complete and saved to `docs/plans/2025-11-06-library-verification.md`.**

**Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**
