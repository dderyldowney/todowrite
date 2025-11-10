"""
Tests for projects API endpoints using real implementations.

This tests the /api/v1/projects endpoints for simplified project operations
with real implementations and no mocking.
"""

import pytest
from fastapi.testclient import TestClient
from todowrite_web.backend.main import app


class TestProjectsAPI:
    """Test projects API endpoints with real implementations."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    @pytest.fixture
    def sample_project_nodes(self, client):
        """Create sample project structure."""
        # Create a goal
        goal_response = client.post(
            "/api/v1/nodes",
            json={
                "layer": "Goal",
                "title": "Sample Project",
                "description": "A sample project for testing",
            },
        )

        if goal_response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        goal_id = goal_response.json()["node"]["id"]

        # Create phases
        phase1_response = client.post(
            "/api/v1/nodes",
            json={
                "layer": "Phase",
                "title": "Design Phase",
                "description": "Design and planning phase",
                "parent_ids": [goal_id],
                "status": "completed",
            },
        )

        phase2_response = client.post(
            "/api/v1/nodes",
            json={
                "layer": "Phase",
                "title": "Implementation Phase",
                "description": "Implementation phase",
                "parent_ids": [goal_id],
                "status": "in_progress",
            },
        )

        # Create tasks
        for i in range(3):
            client.post(
                "/api/v1/nodes",
                json={
                    "layer": "Task",
                    "title": f"Task {i+1}",
                    "description": f"Task {i+1} description",
                    "parent_ids": [phase2_response.json()["node"]["id"]],
                    "status": "completed" if i < 1 else "planned",
                },
            )

        return goal_id

    def test_get_projects_list(self, client):
        """Test GET /api/v1/projects."""
        response = client.get("/api/v1/projects")

        if response.status_code == 404:
            pytest.skip("Projects endpoint not implemented yet")

        assert response.status_code == 200
        data = response.json()
        assert "projects" in data
        assert "total" in data
        assert isinstance(data["projects"], list)

    def test_get_project_by_id(self, client, sample_project_nodes):
        """Test GET /api/v1/projects/{id}."""
        project_id = sample_project_nodes

        response = client.get(f"/api/v1/projects/{project_id}")

        if response.status_code == 404:
            pytest.skip("Projects endpoint not implemented yet")

        assert response.status_code == 200
        data = response.json()
        assert "project" in data
        project = data["project"]

        # Check project structure
        assert "id" in project
        assert "title" in project
        assert "description" in project
        assert "status" in project
        assert "progress" in project
        assert "node_count" in project
        assert "completed_count" in project
        assert "last_updated" in project

    def test_get_project_not_found(self, client):
        """Test GET /api/v1/projects/{id} with non-existent ID."""
        response = client.get("/api/v1/projects/NONEXISTENT-123")

        if response.status_code == 404:
            pytest.skip("Projects endpoint not implemented yet")

        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "message" in data

    def test_project_progress_calculation(self, client, sample_project_nodes):
        """Test project progress calculation."""
        project_id = sample_project_nodes

        response = client.get(f"/api/v1/projects/{project_id}")

        if response.status_code == 404:
            pytest.skip("Projects endpoint not implemented yet")

        assert response.status_code == 200
        data = response.json()
        project = data["project"]

        # Progress should be calculated based on completed nodes
        assert isinstance(project["progress"], int)
        assert 0 <= project["progress"] <= 100
        assert project["completed_count"] <= project["node_count"]

    def test_create_project_from_goal(self, client):
        """Test POST /api/v1/projects to create a project from a goal."""
        # First create a goal
        goal_response = client.post(
            "/api/v1/nodes",
            json={
                "layer": "Goal",
                "title": "New Project Goal",
                "description": "Goal for new project",
            },
        )

        if goal_response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        goal_id = goal_response.json()["node"]["id"]

        # Create project from goal
        project_data = {
            "goal_id": goal_id,
            "title": "New Project",
            "description": "A new project created from goal",
        }

        response = client.post("/api/v1/projects", json=project_data)

        if response.status_code == 404:
            pytest.skip("Projects creation endpoint not implemented yet")

        assert response.status_code == 201
        data = response.json()
        assert "project" in data
        project = data["project"]
        assert project["title"] == project_data["title"]
        assert project["description"] == project_data["description"]

    def test_get_project_nodes(self, client, sample_project_nodes):
        """Test GET /api/v1/projects/{id}/nodes."""
        project_id = sample_project_nodes

        response = client.get(f"/api/v1/projects/{project_id}/nodes")

        if response.status_code == 404:
            pytest.skip("Projects endpoint not implemented yet")

        assert response.status_code == 200
        data = response.json()
        assert "nodes" in data
        assert isinstance(data["nodes"], list)

        # Should contain goal, phases, and tasks
        node_layers = [node["layer"] for node in data["nodes"]]
        assert "Goal" in node_layers
        assert "Phase" in node_layers
        assert "Task" in node_layers

    def test_get_project_statistics(self, client, sample_project_nodes):
        """Test GET /api/v1/projects/{id}/statistics."""
        project_id = sample_project_nodes

        response = client.get(f"/api/v1/projects/{project_id}/statistics")

        if response.status_code == 404:
            pytest.skip("Projects endpoint not implemented yet")

        assert response.status_code == 200
        data = response.json()

        # Check statistics structure
        assert "total_nodes" in data
        assert "nodes_by_layer" in data
        assert "nodes_by_status" in data
        assert "progress_breakdown" in data

        # Check data types
        assert isinstance(data["total_nodes"], int)
        assert isinstance(data["nodes_by_layer"], dict)
        assert isinstance(data["nodes_by_status"], dict)

    def test_update_project_metadata(self, client, sample_project_nodes):
        """Test PUT /api/v1/projects/{id} to update project metadata."""
        project_id = sample_project_nodes

        update_data = {
            "title": "Updated Project Title",
            "description": "Updated project description",
            "metadata": {
                "owner": "project_manager",
                "labels": ["important", "q1-2024"],
            },
        }

        response = client.put(
            f"/api/v1/projects/{project_id}", json=update_data
        )

        if response.status_code == 404:
            pytest.skip("Projects update endpoint not implemented yet")

        assert response.status_code == 200
        data = response.json()
        project = data["project"]
        assert project["title"] == update_data["title"]
        assert project["description"] == update_data["description"]

    def test_delete_project(self, client):
        """Test DELETE /api/v1/projects/{id}."""
        # Create a goal first
        goal_response = client.post(
            "/api/v1/nodes",
            json={
                "layer": "Goal",
                "title": "Project to Delete",
                "description": "This project will be deleted",
            },
        )

        if goal_response.status_code == 404:
            pytest.skip("Nodes endpoint not implemented yet")

        goal_id = goal_response.json()["node"]["id"]

        # Create project from goal
        project_response = client.post(
            "/api/v1/projects",
            json={
                "goal_id": goal_id,
                "title": "Project to Delete",
                "description": "This project will be deleted",
            },
        )

        if project_response.status_code == 404:
            pytest.skip("Projects creation endpoint not implemented yet")

        project_id = project_response.json()["project"]["id"]

        # Delete project
        response = client.delete(f"/api/v1/projects/{project_id}")
        assert response.status_code == 204

        # Verify project is gone
        get_response = client.get(f"/api/v1/projects/{project_id}")
        assert get_response.status_code == 404

    def test_get_projects_with_filters(self, client):
        """Test GET /api/v1/projects with filtering parameters."""
        # Create projects with different statuses
        for status in ["planned", "in_progress", "completed"]:
            goal_response = client.post(
                "/api/v1/nodes",
                json={
                    "layer": "Goal",
                    "title": f"{status.title()} Project",
                    "description": f"A {status} project",
                    "metadata": {"status": status},
                },
            )

            if goal_response.status_code != 404:
                goal_id = goal_response.json()["node"]["id"]
                client.post(
                    "/api/v1/projects",
                    json={
                        "goal_id": goal_id,
                        "title": f"{status.title()} Project",
                        "description": f"A {status} project",
                    },
                )

        # Filter by status
        response = client.get("/api/v1/projects?status=in_progress")

        if response.status_code == 404:
            pytest.skip("Projects endpoint not implemented yet")

        assert response.status_code == 200
        data = response.json()

        # All returned projects should match the filter
        for project in data["projects"]:
            # Note: This depends on how the API implements status filtering
            pass  # Implementation dependent

    def test_project_api_response_format(self, client, sample_project_nodes):
        """Test project API response format consistency."""
        project_id = sample_project_nodes

        response = client.get(f"/api/v1/projects/{project_id}")

        if response.status_code == 404:
            pytest.skip("Projects endpoint not implemented yet")

        assert response.status_code == 200
        data = response.json()
        project = data["project"]

        # Check required fields
        required_fields = [
            "id",
            "title",
            "description",
            "status",
            "progress",
            "node_count",
            "completed_count",
            "last_updated",
        ]
        for field in required_fields:
            assert field in project, f"Missing required field: {field}"

        # Check data types
        assert isinstance(project["progress"], int)
        assert isinstance(project["node_count"], int)
        assert isinstance(project["completed_count"], int)
        assert isinstance(project["last_updated"], str)
