"""Tests for shared models using real implementations."""

from datetime import datetime

import pytest
from todowrite_web.backend.models import (
    Command,
    CommandRun,
    CreateNodeRequest,
    ErrorResponse,
    Node,
    NodeLayer,
    NodeLinks,
    NodeMetadata,
    NodeStatus,
    Project,
    SearchRequest,
    Severity,
    UpdateNodeRequest,
    WorkType,
)


class TestNodeLayer:
    """Test NodeLayer enum."""

    def test_layer_values(self):
        """Test that all expected layer values exist."""
        expected_layers = [
            "Goal",
            "Concept",
            "Context",
            "Constraints",
            "Requirements",
            "AcceptanceCriteria",
            "InterfaceContract",
            "Phase",
            "Step",
            "Task",
            "SubTask",
            "Command",
        ]
        actual_layers = [layer.value for layer in NodeLayer]
        assert sorted(actual_layers) == sorted(expected_layers)


class TestNodeStatus:
    """Test NodeStatus enum."""

    def test_status_values(self):
        """Test that all expected status values exist."""
        expected_statuses = [
            "planned",
            "in_progress",
            "completed",
            "blocked",
            "cancelled",
        ]
        actual_statuses = [status.value for status in NodeStatus]
        assert sorted(actual_statuses) == sorted(expected_statuses)


class TestNodeMetadata:
    """Test NodeMetadata model."""

    def test_empty_metadata(self):
        """Test creating empty metadata."""
        metadata = NodeMetadata()
        assert metadata.owner is None
        assert metadata.labels is None
        assert metadata.severity is None
        assert metadata.work_type is None
        assert metadata.assignee is None
        assert metadata.extra == {}

    def test_metadata_with_values(self):
        """Test creating metadata with values."""
        metadata = NodeMetadata(
            owner="test_user",
            labels=["test", "dev"],
            severity=Severity.HIGH,
            work_type=WorkType.DEVELOPMENT,
            assignee="developer",
            extra={"custom_field": "value"},
        )
        assert metadata.owner == "test_user"
        assert metadata.labels == ["test", "dev"]
        assert metadata.severity == Severity.HIGH
        assert metadata.work_type == WorkType.DEVELOPMENT
        assert metadata.assignee == "developer"
        assert metadata.extra == {"custom_field": "value"}


class TestCommand:
    """Test Command model."""

    def test_command_creation(self):
        """Test creating a valid command."""
        command = Command(
            ac_ref="AC-TEST123",
            run=CommandRun(shell="echo hello", workdir="/tmp"),
        )
        assert command.ac_ref == "AC-TEST123"
        assert command.run.shell == "echo hello"
        assert command.run.workdir == "/tmp"
        assert command.artifacts is None

    def test_command_with_artifacts(self):
        """Test creating command with artifacts."""
        command = Command(
            ac_ref="AC-TEST456",
            run=CommandRun(shell="make build"),
            artifacts=["build.log", "output.bin"],
        )
        assert command.artifacts == ["build.log", "output.bin"]

    def test_invalid_ac_ref_format(self):
        """Test that invalid ac_ref format raises error."""
        with pytest.raises(ValueError):
            Command(ac_ref="INVALID-REF", run=CommandRun(shell="echo test"))


class TestNodeLinks:
    """Test NodeLinks model."""

    def test_empty_links(self):
        """Test creating empty links."""
        links = NodeLinks()
        assert links.parents == []
        assert links.children == []

    def test_links_with_values(self):
        """Test creating links with values."""
        links = NodeLinks(
            parents=["GOAL-PARENT1", "GOAL-PARENT2"],
            children=["TSK-CHILD1", "TSK-CHILD2"],
        )
        assert len(links.parents) == 2
        assert len(links.children) == 2
        assert "GOAL-PARENT1" in links.parents


class TestNode:
    """Test Node model with real implementations."""

    def test_minimal_node(self):
        """Test creating a minimal valid node."""
        node = Node(
            id="GOAL-TEST123",
            layer=NodeLayer.GOAL,
            title="Test Goal",
            description="A test goal",
            links=NodeLinks(),
        )
        assert node.id == "GOAL-TEST123"
        assert node.layer == NodeLayer.GOAL
        assert node.title == "Test Goal"
        assert node.description == "A test goal"
        assert node.status == NodeStatus.PLANNED  # Default value
        assert node.links.parents == []
        assert node.links.children == []
        assert node.command is None

    def test_complete_node(self):
        """Test creating a complete node with all fields."""
        started_date = datetime.utcnow()
        command = Command(ac_ref="AC-TEST789", run=CommandRun(shell="run tests"))

        node = Node(
            id="TSK-COMPLETE456",
            layer=NodeLayer.TASK,
            title="Complete Task",
            description="A complete task with all fields",
            status=NodeStatus.IN_PROGRESS,
            metadata=NodeMetadata(
                owner="test_owner",
                labels=["important"],
                severity=Severity.CRITICAL,
            ),
            progress=75,
            started_date=started_date,
            assignee="developer",
            links=NodeLinks(parents=["GOAL-PARENT"], children=["SUBTASK-CHILD"]),
        )

        assert node.id == "TSK-COMPLETE456"
        assert node.layer == NodeLayer.TASK
        assert node.status == NodeStatus.IN_PROGRESS
        assert node.progress == 75
        assert node.started_date == started_date
        assert node.metadata.owner == "test_owner"
        assert node.metadata.labels == ["important"]
        assert node.metadata.severity == Severity.CRITICAL
        assert node.assignee == "developer"
        assert len(node.links.parents) == 1
        assert len(node.links.children) == 1

    def test_command_node_validation(self):
        """Test that command nodes require command field."""
        # Command node without command should fail
        with pytest.raises(ValueError, match="Command layer nodes must have a command"):
            Node(
                id="CMD-INVALID123",
                layer=NodeLayer.COMMAND,
                title="Invalid Command",
                description="Missing command",
                links=NodeLinks(),
            )

    def test_non_command_node_with_command_fails(self):
        """Test that non-command nodes cannot have command field."""
        command = Command(ac_ref="AC-TEST123", run=CommandRun(shell="echo test"))

        with pytest.raises(ValueError, match="Only Command layer nodes can have a command"):
            Node(
                id="GOAL-INVALID456",
                layer=NodeLayer.GOAL,
                title="Invalid Goal",
                description="Should not have command",
                command=command,
                links=NodeLinks(),
            )

    def test_command_node_with_command(self):
        """Test that command nodes with command field succeed."""
        command = Command(ac_ref="AC-VALID123", run=CommandRun(shell="run something"))

        node = Node(
            id="CMD-VALID123",
            layer=NodeLayer.COMMAND,
            title="Valid Command",
            description="A valid command node",
            command=command,
            links=NodeLinks(),
        )

        assert node.command == command
        assert node.layer == NodeLayer.COMMAND

    def test_invalid_node_id_format(self):
        """Test that invalid node ID format raises error."""
        with pytest.raises(ValueError):
            Node(
                id="INVALID-ID",
                layer=NodeLayer.GOAL,
                title="Invalid Node",
                description="Has invalid ID",
                links=NodeLinks(),
            )

    def test_progress_validation(self):
        """Test progress field validation."""
        # Valid progress
        node = Node(
            id="TSK-PROGRESS123",
            layer=NodeLayer.TASK,
            title="Progress Test",
            description="Test progress validation",
            progress=50,
            links=NodeLinks(),
        )
        assert node.progress == 50

        # Progress out of range should fail
        with pytest.raises(ValueError):
            Node(
                id="TSK-INVALID124",
                layer=NodeLayer.TASK,
                title="Invalid Progress",
                description="Progress out of range",
                progress=150,
                links=NodeLinks(),
            )

    def test_title_min_length(self):
        """Test title minimum length validation."""
        with pytest.raises(ValueError):
            Node(
                id="GOAL-EMPTY125",
                layer=NodeLayer.GOAL,
                title="",
                description="Empty title",
                links=NodeLinks(),
            )


class TestCreateNodeRequest:
    """Test CreateNodeRequest model."""

    def test_minimal_request(self):
        """Test minimal create request."""
        request = CreateNodeRequest(
            layer=NodeLayer.CONCEPT,
            title="New Concept",
            description="A new concept",
        )
        assert request.layer == NodeLayer.CONCEPT
        assert request.title == "New Concept"
        assert request.description == "A new concept"
        assert request.status == NodeStatus.PLANNED
        assert request.parent_ids is None

    def test_full_request(self):
        """Test create request with all fields."""
        command = Command(ac_ref="AC-REQUEST123", run=CommandRun(shell="run command"))

        request = CreateNodeRequest(
            layer=NodeLayer.COMMAND,
            title="New Command",
            description="A command with all fields",
            status=NodeStatus.PLANNED,
            metadata=NodeMetadata(owner="creator"),
            assignee="executor",
            parent_ids=["GOAL-PARENT"],
            command=command,
        )

        assert request.command == command
        assert request.parent_ids == ["GOAL-PARENT"]
        assert request.metadata.owner == "creator"


class TestUpdateNodeRequest:
    """Test UpdateNodeRequest model."""

    def test_empty_update(self):
        """Test empty update request."""
        request = UpdateNodeRequest()
        assert request.title is None
        assert request.description is None
        assert request.status is None

    def test_partial_update(self):
        """Test partial update request."""
        request = UpdateNodeRequest(title="Updated Title", status=NodeStatus.COMPLETED)
        assert request.title == "Updated Title"
        assert request.status == NodeStatus.COMPLETED
        assert request.description is None


class TestSearchRequest:
    """Test SearchRequest model."""

    def test_minimal_search(self):
        """Test minimal search request."""
        request = SearchRequest(query="test query")
        assert request.query == "test query"
        assert request.layer is None
        assert request.limit == 50  # Default value
        assert request.offset == 0  # Default value

    def test_full_search(self):
        """Test search request with all filters."""
        request = SearchRequest(
            query="specific query",
            layer=NodeLayer.TASK,
            status=NodeStatus.IN_PROGRESS,
            assignee="developer",
            labels=["urgent", "bug"],
            limit=100,
            offset=10,
        )
        assert request.query == "specific query"
        assert request.layer == NodeLayer.TASK
        assert request.assignee == "developer"
        assert request.labels == ["urgent", "bug"]
        assert request.limit == 100
        assert request.offset == 10


class TestErrorResponse:
    """Test ErrorResponse model."""

    def test_minimal_error(self):
        """Test minimal error response."""
        error = ErrorResponse(error="ValidationError", message="Invalid input data")
        assert error.error == "ValidationError"
        assert error.message == "Invalid input data"
        assert error.details is None

    def test_error_with_details(self):
        """Test error response with details."""
        details = {"field": "title", "issue": "too short"}
        error = ErrorResponse(
            error="ValidationError",
            message="Validation failed",
            details=details,
        )
        assert error.details == details


class TestProject:
    """Test Project model."""

    def test_project_creation(self):
        """Test creating a project."""
        last_updated = datetime.utcnow()
        project = Project(
            id="PROJ-TEST123",
            title="Test Project",
            description="A test project",
            status=NodeStatus.IN_PROGRESS,
            progress=65,
            node_count=10,
            completed_count=6,
            last_updated=last_updated,
        )

        assert project.id == "PROJ-TEST123"
        assert project.title == "Test Project"
        assert project.status == NodeStatus.IN_PROGRESS
        assert project.progress == 65
        assert project.node_count == 10
        assert project.completed_count == 6
        assert project.last_updated == last_updated

    def test_progress_bounds(self):
        """Test progress bounds validation."""
        # Valid progress
        project = Project(
            id="PROJ-VALID123",
            title="Valid Project",
            description="Valid progress",
            status=NodeStatus.PLANNED,
            progress=0,
            node_count=1,
            completed_count=0,
            last_updated=datetime.utcnow(),
        )
        assert project.progress == 0

        # Invalid progress (negative)
        with pytest.raises(ValueError):
            Project(
                id="PROJ-INVALID124",
                title="Invalid Project",
                description="Invalid progress",
                status=NodeStatus.PLANNED,
                progress=-10,
                node_count=1,
                completed_count=0,
                last_updated=datetime.utcnow(),
            )

        # Invalid progress (over 100)
        with pytest.raises(ValueError):
            Project(
                id="PROJ-INVALID125",
                title="Invalid Project",
                description="Invalid progress",
                status=NodeStatus.PLANNED,
                progress=150,
                node_count=1,
                completed_count=0,
                last_updated=datetime.utcnow(),
            )


class TestModelSerialization:
    """Test model serialization/deserialization."""

    def test_node_serialization(self):
        """Test node model serialization."""
        node = Node(
            id="GOAL-SERIAL123",
            layer=NodeLayer.GOAL,
            title="Serialization Test",
            description="Testing serialization",
            metadata=NodeMetadata(owner="test_user", labels=["test", "serialization"]),
            links=NodeLinks(parents=["PHASE-PARENT"], children=["TASK-CHILD"]),
        )

        # Test dict serialization
        node_dict = node.model_dump()
        assert node_dict["id"] == "GOAL-SERIAL123"
        assert node_dict["layer"] == "Goal"
        assert node_dict["metadata"]["owner"] == "test_user"
        assert node_dict["metadata"]["labels"] == ["test", "serialization"]

        # Test JSON serialization
        json_str = node.model_dump_json()
        assert "GOAL-SERIAL123" in json_str
        assert "Serialization Test" in json_str

    def test_datetime_serialization(self):
        """Test datetime field serialization."""
        test_time = datetime.now()
        node = Node(
            id="TSK-DATETIME123",
            layer=NodeLayer.TASK,
            title="DateTime Test",
            description="Testing datetime serialization",
            started_date=test_time,
            links=NodeLinks(),
        )

        node_dict = node.model_dump()
        assert "started_date" in node_dict
        # Should be datetime object (Pydantic v2 keeps datetimes as objects by default)
        assert isinstance(node_dict["started_date"], datetime)

        # Test JSON serialization doesn't fail
        json_str = node.model_dump_json()
        assert test_time.isoformat()[:10] in json_str  # At least date part
