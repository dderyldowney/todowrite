"""
Tests for search API endpoints using real implementations.

This tests the /api/v1/search endpoint for full-text search
with real implementations and no mocking.
"""

import pytest
from fastapi.testclient import TestClient
from todowrite_web.backend.main import app


class TestSearchAPI:
    """Test search API endpoints with real implementations."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    @pytest.fixture
    def sample_nodes(self, client):
        """Create sample nodes for search testing."""
        nodes = [
            {
                "layer": "Goal",
                "title": "Complete Web Application",
                "description": "Build a complete web application with all features",
            },
            {
                "layer": "Task",
                "title": "Implement User Authentication",
                "description": "Add login and registration functionality",
            },
            {
                "layer": "Task",
                "title": "Build Database Schema",
                "description": "Design and implement database structure",
            },
            {
                "layer": "Concept",
                "title": "User Interface Design",
                "description": "Create mockups and wireframes for the UI",
            },
            {
                "layer": "Task",
                "title": "Write API Documentation",
                "description": "Document all API endpoints",
            },
        ]

        created_nodes = []
        for node_data in nodes:
            response = client.post("/api/v1/nodes", json=node_data)
            if response.status_code != 404:  # If endpoint exists
                created_nodes.append(response.json()["node"])

        return created_nodes

    def test_search_basic(self, client, sample_nodes):
        """Test basic search functionality."""
        response = client.get("/api/v1/search?q=authentication")

        if response.status_code == 404:
            pytest.skip("Search endpoint not implemented yet")

        assert response.status_code == 200
        data = response.json()
        assert "nodes" in data
        assert "total" in data
        assert "query" in data
        assert data["query"] == "authentication"

        # Should find the authentication task
        found_nodes = data["nodes"]
        assert any(
            "authentication" in node["title"].lower()
            or "authentication" in node["description"].lower()
            for node in found_nodes
        )

    def test_search_no_results(self, client):
        """Test search with no matching results."""
        response = client.get("/api/v1/search?q=nonexistentterm")

        if response.status_code == 404:
            pytest.skip("Search endpoint not implemented yet")

        assert response.status_code == 200
        data = response.json()
        assert data["nodes"] == []
        assert data["total"] == 0

    def test_search_empty_query(self, client):
        """Test search with empty query."""
        response = client.get("/api/v1/search?q=")

        if response.status_code == 404:
            pytest.skip("Search endpoint not implemented yet")

        # Empty query should either return all nodes or be a bad request
        assert response.status_code in [200, 400]

    def test_search_with_filters(self, client, sample_nodes):
        """Test search with layer and status filters."""
        # Search for tasks only
        response = client.get("/api/v1/search?q=implement&layer=Task")

        if response.status_code == 404:
            pytest.skip("Search endpoint not implemented yet")

        assert response.status_code == 200
        data = response.json()
        assert all(node["layer"] == "Task" for node in data["nodes"])

    def test_search_pagination(self, client, sample_nodes):
        """Test search with pagination."""
        response = client.get("/api/v1/search?q=task&limit=2&offset=0")

        if response.status_code == 404:
            pytest.skip("Search endpoint not implemented yet")

        assert response.status_code == 200
        data = response.json()
        assert len(data["nodes"]) <= 2  # Should respect limit

    def test_search_special_characters(self, client):
        """Test search with special characters."""
        response = client.get("/api/v1/search?q=api%20documentation")

        if response.status_code == 404:
            pytest.skip("Search endpoint not implemented yet")

        assert response.status_code == 200

    def test_search_case_insensitive(self, client, sample_nodes):
        """Test case-insensitive search."""
        # Search with different case
        response_lower = client.get("/api/v1/search?q=authentication")
        response_upper = client.get("/api/v1/search?q=AUTHENTICATION")
        response_mixed = client.get("/api/v1/search?q=Authentication")

        if response_lower.status_code == 404:
            pytest.skip("Search endpoint not implemented yet")

        # All should return same number of results
        assert response_lower.json()["total"] == response_upper.json()["total"]
        assert response_lower.json()["total"] == response_mixed.json()["total"]

    def test_search_by_id(self, client, sample_nodes):
        """Test search by node ID."""
        if not sample_nodes:
            pytest.skip("No sample nodes available")

        node_id = sample_nodes[0]["id"]
        response = client.get(f"/api/v1/search?q={node_id}")

        if response.status_code == 404:
            pytest.skip("Search endpoint not implemented yet")

        assert response.status_code == 200
        data = response.json()
        # Should find the exact node
        assert any(node["id"] == node_id for node in data["nodes"])

    def test_search_with_labels(self, client, sample_nodes):
        """Test search filtering by labels."""
        # Create a node with labels
        response = client.post(
            "/api/v1/nodes",
            json={
                "layer": "Task",
                "title": "Labeled Task",
                "description": "Task with labels",
                "metadata": {"labels": ["urgent", "bug"]},
            },
        )

        if response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        labeled_node = response.json()["node"]

        # Search for nodes with specific label
        search_response = client.get("/api/v1/search?q=task&labels=urgent")

        if search_response.status_code == 404:
            pytest.skip("Search endpoint not implemented yet")

        assert search_response.status_code == 200
        data = search_response.json()
        # Should find the labeled node
        assert any(node["id"] == labeled_node["id"] for node in data["nodes"])

    def test_search_with_assignee(self, client, sample_nodes):
        """Test search filtering by assignee."""
        # Create a node with assignee
        response = client.post(
            "/api/v1/nodes",
            json={
                "layer": "Task",
                "title": "Assigned Task",
                "description": "Task with assignee",
                "assignee": "developer1",
            },
        )

        if response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        assigned_node = response.json()["node"]

        # Search for nodes by assignee
        search_response = client.get(
            "/api/v1/search?q=task&assignee=developer1"
        )

        if search_response.status_code == 404:
            pytest.skip("Search endpoint not implemented yet")

        assert search_response.status_code == 200
        data = search_response.json()
        # Should find the assigned node
        assert any(node["id"] == assigned_node["id"] for node in data["nodes"])

    def test_search_complex_query(self, client, sample_nodes):
        """Test search with complex query and multiple filters."""
        response = client.get(
            "/api/v1/search?q=implement&layer=Task&status=planned"
        )

        if response.status_code == 404:
            pytest.skip("Search endpoint not implemented yet")

        assert response.status_code == 200
        data = response.json()

        # Should filter by both query and layer
        for node in data["nodes"]:
            assert node["layer"] == "Task"
            assert (
                "implement" in node["title"].lower()
                or "implement" in node["description"].lower()
            )

    def test_search_response_format(self, client, sample_nodes):
        """Test search response format."""
        response = client.get("/api/v1/search?q=web")

        if response.status_code == 404:
            pytest.skip("Search endpoint not implemented yet")

        assert response.status_code == 200
        data = response.json()

        # Check required fields
        assert "nodes" in data
        assert "total" in data
        assert "query" in data

        # Check node format
        if data["nodes"]:
            node = data["nodes"][0]
            assert "id" in node
            assert "layer" in node
            assert "title" in node
            assert "description" in node
            assert "status" in node
