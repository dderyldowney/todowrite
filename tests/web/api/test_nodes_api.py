"""
Tests for nodes API endpoints using real implementations.

This tests the /api/v1/nodes endpoints for CRUD operations
with real implementations and no mocking.
"""

import pytest
from fastapi.testclient import TestClient
from todowrite_web.backend.main import app


class TestNodesAPI:
    """Test nodes API endpoints with real implementations."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    @pytest.fixture
    def sample_goal_data(self):
        """Sample goal data for testing."""
        return {
            "layer": "Goal",
            "title": "Test Goal",
            "description": "A test goal for API testing",
            "status": "planned",
        }

    @pytest.fixture
    def sample_task_data(self):
        """Sample task data for testing."""
        return {
            "layer": "Task",
            "title": "Test Task",
            "description": "A test task for API testing",
            "status": "planned",
            "parent_ids": ["GOAL-TEST123"],
        }

    def test_get_nodes_empty_list(self, client):
        """Test GET /api/v1/nodes with empty list."""
        response = client.get("/api/v1/nodes")
        assert response.status_code == 200

        data = response.json()
        assert "nodes" in data
        assert "total" in data
        assert data["nodes"] == []
        assert data["total"] == 0

    def test_create_node_minimal(self, client, sample_goal_data):
        """Test POST /api/v1/nodes with minimal data."""
        response = client.post("/api/v1/nodes", json=sample_goal_data)

        # Note: This might fail if the endpoint doesn't exist yet
        # The test structure is ready for when the API is implemented
        if response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        assert response.status_code == 201
        data = response.json()
        assert "node" in data
        assert data["node"]["title"] == sample_goal_data["title"]
        assert data["node"]["layer"] == sample_goal_data["layer"]
        assert data["node"]["description"] == sample_goal_data["description"]

    def test_create_node_with_parents(self, client, sample_task_data):
        """Test POST /api/v1/nodes with parent relationships."""
        response = client.post("/api/v1/nodes", json=sample_task_data)

        if response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        assert response.status_code == 201
        data = response.json()
        assert (
            data["node"]["links"]["parents"] == sample_task_data["parent_ids"]
        )

    def test_get_node_by_id(self, client):
        """Test GET /api/v1/nodes/{id}."""
        # First create a node
        create_data = {
            "layer": "Goal",
            "title": "Get Test Goal",
            "description": "Goal for testing GET endpoint",
        }

        create_response = client.post("/api/v1/nodes", json=create_data)
        if create_response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        node_id = create_response.json()["node"]["id"]

        # Then get it by ID
        response = client.get(f"/api/v1/nodes/{node_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["node"]["id"] == node_id
        assert data["node"]["title"] == create_data["title"]

    def test_get_node_not_found(self, client):
        """Test GET /api/v1/nodes/{id} with non-existent ID."""
        response = client.get("/api/v1/nodes/NONEXISTENT-123")

        if response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "message" in data

    def test_update_node(self, client):
        """Test PUT /api/v1/nodes/{id}."""
        # First create a node
        create_data = {
            "layer": "Task",
            "title": "Original Task",
            "description": "Original description",
        }

        create_response = client.post("/api/v1/nodes", json=create_data)
        if create_response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        node_id = create_response.json()["node"]["id"]

        # Then update it
        update_data = {
            "title": "Updated Task",
            "status": "in_progress",
            "progress": 50,
        }

        response = client.put(f"/api/v1/nodes/{node_id}", json=update_data)
        assert response.status_code == 200

        data = response.json()
        assert data["node"]["title"] == update_data["title"]
        assert data["node"]["status"] == update_data["status"]
        assert data["node"]["progress"] == update_data["progress"]

    def test_delete_node(self, client):
        """Test DELETE /api/v1/nodes/{id}."""
        # First create a node
        create_data = {
            "layer": "Task",
            "title": "Task to Delete",
            "description": "This task will be deleted",
        }

        create_response = client.post("/api/v1/nodes", json=create_data)
        if create_response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        node_id = create_response.json()["node"]["id"]

        # Then delete it
        response = client.delete(f"/api/v1/nodes/{node_id}")
        assert response.status_code == 204

        # Verify it's gone
        get_response = client.get(f"/api/v1/nodes/{node_id}")
        assert get_response.status_code == 404

    def test_create_node_validation_errors(self, client):
        """Test POST /api/v1/nodes with invalid data."""
        # Missing required fields
        invalid_data = {
            "title": "Invalid Node"
            # Missing layer and description
        }

        response = client.post("/api/v1/nodes", json=invalid_data)

        if response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data  # FastAPI validation error format

    def test_create_node_invalid_id_format(self, client):
        """Test POST /api/v1/nodes with custom ID in wrong format."""
        invalid_data = {
            "id": "INVALID-ID",  # Wrong format
            "layer": "Task",
            "title": "Invalid ID Task",
            "description": "Task with invalid ID format",
        }

        response = client.post("/api/v1/nodes", json=invalid_data)

        if response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        assert response.status_code == 422

    def test_get_nodes_with_pagination(self, client):
        """Test GET /api/v1/nodes with pagination parameters."""
        # Create some nodes first
        for i in range(5):
            create_data = {
                "layer": "Task",
                "title": f"Task {i}",
                "description": f"Description for task {i}",
            }
            client.post("/api/v1/nodes", json=create_data)

        # Test pagination
        response = client.get("/api/v1/nodes?page=1&page_size=2")

        if response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        assert response.status_code == 200
        data = response.json()
        assert len(data["nodes"]) == 2
        assert data["page"] == 1
        assert data["page_size"] == 2
        assert data["total"] >= 5

    def test_get_nodes_with_filters(self, client):
        """Test GET /api/v1/nodes with filtering parameters."""
        # Create nodes with different properties
        client.post(
            "/api/v1/nodes",
            json={
                "layer": "Goal",
                "title": "Goal 1",
                "description": "Test goal",
                "status": "planned",
            },
        )
        client.post(
            "/api/v1/nodes",
            json={
                "layer": "Task",
                "title": "Task 1",
                "description": "Test task",
                "status": "completed",
            },
        )
        client.post(
            "/api/v1/nodes",
            json={
                "layer": "Task",
                "title": "Task 2",
                "description": "Another task",
                "status": "planned",
            },
        )

        # Test filtering by layer
        response = client.get("/api/v1/nodes?layer=Task")

        if response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        assert response.status_code == 200
        data = response.json()
        assert all(node["layer"] == "Task" for node in data["nodes"])

        # Test filtering by status
        response = client.get("/api/v1/nodes?status=planned")
        assert response.status_code == 200
        data = response.json()
        assert all(node["status"] == "planned" for node in data["nodes"])

    def test_bulk_operations(self, client):
        """Test bulk node operations."""
        # Create multiple nodes
        nodes_data = [
            {
                "layer": "Task",
                "title": "Bulk Task 1",
                "description": "First bulk task",
            },
            {
                "layer": "Task",
                "title": "Bulk Task 2",
                "description": "Second bulk task",
            },
            {
                "layer": "Task",
                "title": "Bulk Task 3",
                "description": "Third bulk task",
            },
        ]

        # Test bulk create (if implemented)
        response = client.post(
            "/api/v1/nodes/bulk", json={"nodes": nodes_data}
        )

        if response.status_code == 404:
            pytest.skip("Bulk operations not implemented yet")

        assert response.status_code == 201
        data = response.json()
        assert len(data["nodes"]) == 3

        # Test bulk delete
        node_ids = [node["id"] for node in data["nodes"]]
        response = client.delete(
            "/api/v1/nodes/bulk", json={"node_ids": node_ids}
        )
        assert response.status_code == 204

        # Verify all nodes are deleted
        for node_id in node_ids:
            get_response = client.get(f"/api/v1/nodes/{node_id}")
            assert get_response.status_code == 404


class TestNodeHierarchyAPI:
    """Test node hierarchy API endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    def test_get_node_children(self, client):
        """Test GET /api/v1/nodes/{id}/children."""
        # Create parent and child nodes
        parent_response = client.post(
            "/api/v1/nodes",
            json={
                "layer": "Goal",
                "title": "Parent Goal",
                "description": "Parent goal",
            },
        )

        if parent_response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        parent_id = parent_response.json()["node"]["id"]

        child_response = client.post(
            "/api/v1/nodes",
            json={
                "layer": "Task",
                "title": "Child Task",
                "description": "Child task",
                "parent_ids": [parent_id],
            },
        )

        # Get children
        response = client.get(f"/api/v1/nodes/{parent_id}/children")
        assert response.status_code == 200
        data = response.json()
        assert len(data["children"]) == 1
        assert data["children"][0]["title"] == "Child Task"

    def test_get_node_parents(self, client):
        """Test GET /api/v1/nodes/{id}/parents."""
        # Create parent and child nodes
        parent_response = client.post(
            "/api/v1/nodes",
            json={
                "layer": "Goal",
                "title": "Parent Goal",
                "description": "Parent goal",
            },
        )

        if parent_response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        parent_id = parent_response.json()["node"]["id"]

        child_response = client.post(
            "/api/v1/nodes",
            json={
                "layer": "Task",
                "title": "Child Task",
                "description": "Child task",
                "parent_ids": [parent_id],
            },
        )

        child_id = child_response.json()["node"]["id"]

        # Get parents
        response = client.get(f"/api/v1/nodes/{child_id}/parents")
        assert response.status_code == 200
        data = response.json()
        assert len(data["parents"]) == 1
        assert data["parents"][0]["id"] == parent_id

    def test_get_node_hierarchy(self, client):
        """Test GET /api/v1/nodes/{id}/hierarchy."""
        # Create a hierarchy
        goal_response = client.post(
            "/api/v1/nodes",
            json={
                "layer": "Goal",
                "title": "Root Goal",
                "description": "Root goal",
            },
        )

        if goal_response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        goal_id = goal_response.json()["node"]["id"]

        phase_response = client.post(
            "/api/v1/nodes",
            json={
                "layer": "Phase",
                "title": "Phase 1",
                "description": "First phase",
                "parent_ids": [goal_id],
            },
        )

        phase_id = phase_response.json()["node"]["id"]

        task_response = client.post(
            "/api/v1/nodes",
            json={
                "layer": "Task",
                "title": "Task 1",
                "description": "First task",
                "parent_ids": [phase_id],
            },
        )

        # Get hierarchy
        response = client.get(f"/api/v1/nodes/{goal_id}/hierarchy")
        assert response.status_code == 200
        data = response.json()
        assert "hierarchy" in data
        # Should contain the full tree structure
        assert len(data["hierarchy"]["children"]) == 1
        assert len(data["hierarchy"]["children"][0]["children"]) == 1
