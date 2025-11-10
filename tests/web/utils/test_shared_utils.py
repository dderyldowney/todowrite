"""Tests for shared utilities using real implementations."""

import csv
import json
from datetime import UTC, datetime, timedelta
from io import StringIO

import pytest
from todowrite_web.backend.models import (
    Node,
    NodeLayer,
    NodeLinks,
    NodeMetadata,
    NodeStatus,
)
from todowrite_web.backend.utils import (
    build_hierarchy,
    calculate_node_progress,
    # Progress utilities
    calculate_progress,
    can_transition_to,
    create_node_links,
    export_to_csv,
    # Export utilities
    export_to_json,
    filter_nodes_by_assignee,
    filter_nodes_by_labels,
    # Search and filter utilities
    filter_nodes_by_layer,
    filter_nodes_by_status,
    # Date utilities
    format_date,
    format_datetime,
    generate_node_id,
    get_all_ancestors,
    get_all_descendants,
    get_layer_prefix,
    get_leaf_nodes,
    get_next_status,
    get_node_depth,
    get_root_nodes,
    # Status utilities
    get_status_color,
    # Import utilities
    import_nodes_from_json,
    is_overdue,
    # Node utilities
    is_valid_node_id,
    # Metadata utilities
    merge_node_metadata,
    sanitize_node_id,
    search_nodes,
    # Validation utilities
    validate_node_structure,
)


class TestNodeUtilities:
    """Test node-related utility functions."""

    def test_is_valid_node_id(self):
        """Test node ID validation."""
        # Valid IDs
        assert is_valid_node_id("GOAL-TEST123") is True
        assert is_valid_node_id("CON-ABC_DEF") is True
        assert is_valid_node_id("CMD-123456789") is True

        # Invalid IDs
        assert is_valid_node_id("INVALID-ID") is False
        assert is_valid_node_id("goal-test123") is False
        assert is_valid_node_id("GOAL") is False
        assert is_valid_node_id("") is False
        assert (
            is_valid_node_id("GOAL-TEST-INVALID") is True
        )  # This is actually valid

    def test_get_layer_prefix(self):
        """Test layer prefix retrieval."""
        assert get_layer_prefix(NodeLayer.GOAL) == "GOAL"
        assert get_layer_prefix(NodeLayer.CONCEPT) == "CON"
        assert get_layer_prefix(NodeLayer.COMMAND) == "CMD"

    def test_generate_node_id(self):
        """Test node ID generation."""
        # Generate with auto suffix
        node_id = generate_node_id(NodeLayer.TASK)
        assert node_id.startswith("TSK-")
        assert is_valid_node_id(node_id) is True
        assert len(node_id) > 10  # Should have reasonable length

        # Generate with custom suffix
        custom_id = generate_node_id(NodeLayer.GOAL, "CUSTOM123")
        assert custom_id == "GOAL-CUSTOM123"

    def test_sanitize_node_id(self):
        """Test node ID sanitization."""
        # Valid ID should pass through
        assert sanitize_node_id("goal-test123") == "GOAL-TEST123"
        assert sanitize_node_id("  CON-ABC123  ") == "CON-ABC123"

        # Invalid ID should raise error
        with pytest.raises(ValueError):
            sanitize_node_id("INVALID-FORMAT")

        with pytest.raises(ValueError):
            sanitize_node_id("")


class TestStatusUtilities:
    """Test status-related utility functions."""

    def test_get_status_color(self):
        """Test status color retrieval."""
        assert get_status_color(NodeStatus.PLANNED) == "#6B7280"
        assert get_status_color(NodeStatus.IN_PROGRESS) == "#3B82F6"
        assert get_status_color(NodeStatus.COMPLETED) == "#10B981"
        assert get_status_color(NodeStatus.BLOCKED) == "#EF4444"
        assert get_status_color(NodeStatus.CANCELLED) == "#9CA3AF"

    def test_get_next_status(self):
        """Test next status in workflow."""
        assert get_next_status(NodeStatus.PLANNED) == NodeStatus.IN_PROGRESS
        assert get_next_status(NodeStatus.IN_PROGRESS) == NodeStatus.COMPLETED
        assert get_next_status(NodeStatus.COMPLETED) == NodeStatus.COMPLETED
        assert get_next_status(NodeStatus.BLOCKED) == NodeStatus.PLANNED
        assert get_next_status(NodeStatus.CANCELLED) == NodeStatus.PLANNED

    def test_can_transition_to(self):
        """Test valid status transitions."""
        # Valid transitions
        assert (
            can_transition_to(NodeStatus.PLANNED, NodeStatus.IN_PROGRESS)
            is True
        )
        assert (
            can_transition_to(NodeStatus.PLANNED, NodeStatus.CANCELLED) is True
        )
        assert (
            can_transition_to(NodeStatus.IN_PROGRESS, NodeStatus.COMPLETED)
            is True
        )
        assert (
            can_transition_to(NodeStatus.IN_PROGRESS, NodeStatus.BLOCKED)
            is True
        )

        # Invalid transitions
        assert (
            can_transition_to(NodeStatus.COMPLETED, NodeStatus.PLANNED)
            is False
        )
        assert (
            can_transition_to(NodeStatus.PLANNED, NodeStatus.BLOCKED) is False
        )
        assert (
            can_transition_to(NodeStatus.CANCELLED, NodeStatus.IN_PROGRESS)
            is False
        )


class TestProgressUtilities:
    """Test progress-related utility functions."""

    def test_calculate_progress_empty(self):
        """Test progress calculation with empty list."""
        assert calculate_progress([]) == 0

    def test_calculate_progress_all_completed(self):
        """Test progress calculation with all completed nodes."""
        nodes = [
            create_test_node("TSK-1", NodeStatus.COMPLETED),
            create_test_node("TSK-2", NodeStatus.COMPLETED),
            create_test_node("TSK-3", NodeStatus.COMPLETED),
        ]
        assert calculate_progress(nodes) == 100

    def test_calculate_progress_none_completed(self):
        """Test progress calculation with no completed nodes."""
        nodes = [
            create_test_node("TSK-1", NodeStatus.PLANNED),
            create_test_node("TSK-2", NodeStatus.IN_PROGRESS),
            create_test_node("TSK-3", NodeStatus.BLOCKED),
        ]
        assert calculate_progress(nodes) == 0

    def test_calculate_progress_partial(self):
        """Test progress calculation with partial completion."""
        nodes = [
            create_test_node("TSK-1", NodeStatus.COMPLETED),
            create_test_node("TSK-2", NodeStatus.COMPLETED),
            create_test_node("TSK-3", NodeStatus.PLANNED),
            create_test_node("TSK-4", NodeStatus.IN_PROGRESS),
        ]
        assert calculate_progress(nodes) == 50  # 2 out of 4 completed

    def test_calculate_node_progress(self):
        """Test progress calculation for a specific node."""
        # Create test nodes
        parent = create_test_node("GOAL-PARENT", NodeStatus.IN_PROGRESS)
        child1 = create_test_node("TSK-CHILD1", NodeStatus.COMPLETED)
        child2 = create_test_node("TSK-CHILD2", NodeStatus.PLANNED)

        # Set up relationships
        parent.links.children = ["TSK-CHILD1", "TSK-CHILD2"]
        child1.links.parents = ["GOAL-PARENT"]
        child2.links.parents = ["GOAL-PARENT"]

        all_nodes = {
            "GOAL-PARENT": parent,
            "TSK-CHILD1": child1,
            "TSK-CHILD2": child2,
        }

        # Calculate progress
        progress = calculate_node_progress(parent, all_nodes)
        assert progress == 50  # 1 out of 2 children completed


class TestHierarchyUtilities:
    """Test hierarchy-related utility functions."""

    def test_get_root_nodes(self):
        """Test finding root nodes."""
        root1 = create_test_node("GOAL-ROOT1")
        root2 = create_test_node("GOAL-ROOT2")
        child = create_test_node("TSK-CHILD")
        child.links.parents = ["GOAL-ROOT1"]

        nodes = [root1, root2, child]
        roots = get_root_nodes(nodes)

        assert len(roots) == 2
        assert root1 in roots
        assert root2 in roots
        assert child not in roots

    def test_get_leaf_nodes(self):
        """Test finding leaf nodes."""
        root = create_test_node("GOAL-ROOT")
        child1 = create_test_node("TSK-CHILD1")
        child2 = create_test_node("TSK-CHILD2")
        grandchild = create_test_node(
            "SUB-GRANDCHILD", layer=NodeLayer.SUBTASK
        )

        # Set up relationships
        root.links.children = ["TSK-CHILD1", "TSK-CHILD2"]
        child1.links.parents = ["GOAL-ROOT"]
        child2.links.parents = ["GOAL-ROOT"]
        child2.links.children = ["SUB-GRANDCHILD"]
        grandchild.links.parents = ["TSK-CHILD2"]

        nodes = [root, child1, child2, grandchild]
        leaves = get_leaf_nodes(nodes)

        assert len(leaves) == 2
        assert child1 in leaves
        assert grandchild in leaves
        assert root not in leaves
        assert child2 not in leaves

    def test_build_hierarchy(self):
        """Test building hierarchy mapping."""
        parent = create_test_node("GOAL-PARENT")
        child1 = create_test_node("TSK-CHILD1")
        child2 = create_test_node("TSK-CHILD2")

        # Set up relationships
        parent.links.children = ["TSK-CHILD1", "TSK-CHILD2"]
        child1.links.parents = ["GOAL-PARENT"]
        child2.links.parents = ["GOAL-PARENT"]

        nodes = [parent, child1, child2]
        hierarchy = build_hierarchy(nodes)

        assert "GOAL-PARENT" in hierarchy
        assert len(hierarchy["GOAL-PARENT"]) == 2
        assert child1 in hierarchy["GOAL-PARENT"]
        assert child2 in hierarchy["GOAL-PARENT"]

    def test_get_node_depth(self):
        """Test calculating node depth."""
        root = create_test_node("GOAL-ROOT")
        child = create_test_node("TSK-CHILD")
        grandchild = create_test_node(
            "SUB-GRANDCHILD", layer=NodeLayer.SUBTASK
        )

        # Set up relationships
        root.links.children = ["TSK-CHILD"]
        child.links.parents = ["GOAL-ROOT"]
        child.links.children = ["SUB-GRANDCHILD"]
        grandchild.links.parents = ["TSK-CHILD"]

        all_nodes = {
            "GOAL-ROOT": root,
            "TSK-CHILD": child,
            "SUB-GRANDCHILD": grandchild,
        }

        assert get_node_depth(root, all_nodes) == 0
        assert get_node_depth(child, all_nodes) == 1
        assert get_node_depth(grandchild, all_nodes) == 2

    def test_get_all_descendants(self):
        """Test getting all descendants of a node."""
        root = create_test_node("GOAL-ROOT")
        child1 = create_test_node("TSK-CHILD1")
        child2 = create_test_node("TSK-CHILD2")
        grandchild1 = create_test_node(
            "SUB-GRANDCHILD1", layer=NodeLayer.SUBTASK
        )
        grandchild2 = create_test_node(
            "SUB-GRANDCHILD2", layer=NodeLayer.SUBTASK
        )

        # Set up relationships
        root.links.children = ["TSK-CHILD1", "TSK-CHILD2"]
        child1.links.parents = ["GOAL-ROOT"]
        child1.links.children = ["SUB-GRANDCHILD1"]
        child2.links.parents = ["GOAL-ROOT"]
        child2.links.children = ["SUB-GRANDCHILD2"]
        grandchild1.links.parents = ["TSK-CHILD1"]
        grandchild2.links.parents = ["TSK-CHILD2"]

        all_nodes = {
            "GOAL-ROOT": root,
            "TSK-CHILD1": child1,
            "TSK-CHILD2": child2,
            "SUB-GRANDCHILD1": grandchild1,
            "SUB-GRANDCHILD2": grandchild2,
        }

        descendants = get_all_descendants(root, all_nodes)
        assert len(descendants) == 4
        assert "TSK-CHILD1" in descendants
        assert "TSK-CHILD2" in descendants
        assert "SUB-GRANDCHILD1" in descendants
        assert "SUB-GRANDCHILD2" in descendants

    def test_get_all_ancestors(self):
        """Test getting all ancestors of a node."""
        root = create_test_node("GOAL-ROOT")
        child = create_test_node("TSK-CHILD")
        grandchild = create_test_node(
            "SUB-GRANDCHILD", layer=NodeLayer.SUBTASK
        )

        # Set up relationships
        root.links.children = ["TSK-CHILD"]
        child.links.parents = ["GOAL-ROOT"]
        child.links.children = ["SUB-GRANDCHILD"]
        grandchild.links.parents = ["TSK-CHILD"]

        all_nodes = {
            "GOAL-ROOT": root,
            "TSK-CHILD": child,
            "SUB-GRANDCHILD": grandchild,
        }

        ancestors = get_all_ancestors(grandchild, all_nodes)
        assert len(ancestors) == 2
        assert "GOAL-ROOT" in ancestors
        assert "TSK-CHILD" in ancestors

    def test_create_node_links(self):
        """Test creating node links."""
        # Empty links
        links = create_node_links()
        assert links["parents"] == []
        assert links["children"] == []

        # Links with values
        links = create_node_links(
            parent_ids=["GOAL-PARENT1", "GOAL-PARENT2"],
            child_ids=["TSK-CHILD1"],
        )
        assert len(links["parents"]) == 2
        assert len(links["children"]) == 1
        assert "GOAL-PARENT1" in links["parents"]


class TestSearchAndFilterUtilities:
    """Test search and filter utility functions."""

    def test_filter_nodes_by_layer(self):
        """Test filtering nodes by layer."""
        nodes = [
            create_test_node("GOAL-1", layer=NodeLayer.GOAL),
            create_test_node("TSK-1", layer=NodeLayer.TASK),
            create_test_node("GOAL-2", layer=NodeLayer.GOAL),
            create_test_node("CON-1", layer=NodeLayer.CONCEPT),
        ]

        goals = filter_nodes_by_layer(nodes, [NodeLayer.GOAL])
        assert len(goals) == 2
        assert all(node.layer == NodeLayer.GOAL for node in goals)

        tasks_and_concepts = filter_nodes_by_layer(
            nodes, [NodeLayer.TASK, NodeLayer.CONCEPT]
        )
        assert len(tasks_and_concepts) == 2

    def test_filter_nodes_by_status(self):
        """Test filtering nodes by status."""
        nodes = [
            create_test_node("TSK-1", NodeStatus.PLANNED),
            create_test_node("TSK-2", NodeStatus.COMPLETED),
            create_test_node("TSK-3", NodeStatus.IN_PROGRESS),
            create_test_node("TSK-4", NodeStatus.COMPLETED),
        ]

        completed = filter_nodes_by_status(nodes, [NodeStatus.COMPLETED])
        assert len(completed) == 2
        assert all(node.status == NodeStatus.COMPLETED for node in completed)

        planned_and_in_progress = filter_nodes_by_status(
            nodes, [NodeStatus.PLANNED, NodeStatus.IN_PROGRESS]
        )
        assert len(planned_and_in_progress) == 2

    def test_filter_nodes_by_assignee(self):
        """Test filtering nodes by assignee."""
        nodes = [
            create_test_node("TSK-1", NodeStatus.PLANNED, assignee="alice"),
            create_test_node("TSK-2", NodeStatus.COMPLETED, assignee="bob"),
            create_test_node("TSK-3", NodeStatus.PLANNED),  # No assignee
            create_test_node(
                "TSK-4", NodeStatus.IN_PROGRESS, assignee="alice"
            ),
        ]

        alice_tasks = filter_nodes_by_assignee(nodes, "alice")
        assert len(alice_tasks) == 2
        assert all(node.assignee == "alice" for node in alice_tasks)

    def test_filter_nodes_by_labels(self):
        """Test filtering nodes by labels."""
        nodes = [
            create_test_node("TSK-1", labels=["urgent", "bug"]),
            create_test_node("TSK-2", labels=["feature"]),
            create_test_node("TSK-3"),  # No labels
            create_test_node("TSK-4", labels=["urgent", "enhancement"]),
        ]

        urgent_tasks = filter_nodes_by_labels(nodes, ["urgent"])
        assert len(urgent_tasks) == 2

        bug_tasks = filter_nodes_by_labels(nodes, ["bug"])
        assert len(bug_tasks) == 1

    def test_search_nodes(self):
        """Test searching nodes."""
        nodes = [
            create_test_node(
                "GOAL-WEB1",
                NodeStatus.PLANNED,
                NodeLayer.GOAL,
                "Build web application",
            ),
            create_test_node(
                "TSK-SEARCH2",
                NodeStatus.PLANNED,
                NodeLayer.TASK,
                "Test Task",
                "Implement search functionality",
            ),
            create_test_node(
                "CON-UI3",
                NodeStatus.PLANNED,
                NodeLayer.CONCEPT,
                "User interface design",
            ),
            create_test_node(
                "TSK-DB4",
                NodeStatus.PLANNED,
                NodeLayer.TASK,
                "Database schema",
            ),
        ]

        # Search by title
        web_results = search_nodes(nodes, "web")
        assert len(web_results) == 1
        assert "web application" in web_results[0].title

        # Search by description
        search_results = search_nodes(nodes, "search")
        assert len(search_results) == 1
        assert "search functionality" in search_results[0].description

        # Search by ID
        goal_results = search_nodes(nodes, "GOAL-WEB1")
        assert len(goal_results) == 1
        assert goal_results[0].id == "GOAL-WEB1"

        # Case insensitive search
        ui_results = search_nodes(nodes, "interface")
        assert len(ui_results) == 1


class TestDateUtilities:
    """Test date-related utility functions."""

    def test_format_date(self):
        """Test date formatting."""
        test_date = datetime(2023, 12, 25, 14, 30, 0, tzinfo=UTC)
        assert format_date(test_date) == "2023-12-25"
        assert format_date(None) == ""

    def test_format_datetime(self):
        """Test datetime formatting."""
        test_datetime = datetime(2023, 12, 25, 14, 30, 45, tzinfo=UTC)
        formatted = format_datetime(test_datetime)
        assert "2023-12-25" in formatted
        assert "14:30:45" in formatted
        assert format_datetime(None) == ""

    def test_is_overdue(self):
        """Test overdue detection."""
        # Not started node
        not_started = create_test_node("TSK-NOTSTARTED")
        assert is_overdue(not_started) is False

        # Completed node
        completed_started = datetime.now(UTC) - timedelta(days=1)
        completed = Node(
            id="TSK-COMPLETED",
            layer=NodeLayer.TASK,
            title="Completed Task",
            description="A completed task",
            status=NodeStatus.COMPLETED,
            started_date=completed_started,
            links=NodeLinks(),
        )
        assert is_overdue(completed) is False

        # Overdue node (started in past, not completed)
        overdue_started = datetime.now(UTC) - timedelta(days=1)
        overdue = Node(
            id="TSK-OVERDUE",
            layer=NodeLayer.TASK,
            title="Overdue Task",
            description="An overdue task",
            status=NodeStatus.IN_PROGRESS,
            started_date=overdue_started,
            links=NodeLinks(),
        )
        assert is_overdue(overdue) is True

        # Not overdue node (started in future)
        not_overdue_started = datetime.now(UTC) + timedelta(hours=1)
        not_overdue = Node(
            id="TSK-NOTOVERDUE",
            layer=NodeLayer.TASK,
            title="Not Overdue Task",
            description="A task starting in the future",
            status=NodeStatus.IN_PROGRESS,
            started_date=not_overdue_started,
            links=NodeLinks(),
        )
        assert is_overdue(not_overdue) is False


class TestValidationUtilities:
    """Test validation utility functions."""

    def test_validate_node_structure_valid(self):
        """Test validation of valid node structure."""
        valid_node = {
            "id": "GOAL-VALID123",
            "layer": "Goal",
            "title": "Valid Goal",
            "description": "A valid goal node",
            "progress": 50,
        }

        is_valid, errors = validate_node_structure(valid_node)
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_node_structure_invalid_id(self):
        """Test validation of node with invalid ID."""
        invalid_node = {
            "id": "INVALID-ID",
            "layer": "Goal",
            "title": "Invalid Goal",
            "description": "Has invalid ID",
        }

        is_valid, errors = validate_node_structure(invalid_node)
        assert is_valid is False
        assert any("Invalid node ID format" in error for error in errors)

    def test_validate_node_structure_missing_required(self):
        """Test validation of node with missing required fields."""
        incomplete_node = {
            "id": "GOAL-INCOMPLETE123",
            "layer": "Goal",
            # Missing title and description
        }

        is_valid, errors = validate_node_structure(incomplete_node)
        assert is_valid is False
        assert any("Title is required" in error for error in errors)
        assert any("Description is required" in error for error in errors)

    def test_validate_node_structure_invalid_progress(self):
        """Test validation of node with invalid progress."""
        invalid_progress_node = {
            "id": "TSK-INVALID123",
            "layer": "Task",
            "title": "Invalid Progress",
            "description": "Has invalid progress",
            "progress": 150,  # Over 100
        }

        is_valid, errors = validate_node_structure(invalid_progress_node)
        assert is_valid is False
        assert any(
            "Progress must be an integer between 0 and 100" in error
            for error in errors
        )

    def test_validate_node_structure_command_validation(self):
        """Test command validation for different layers."""
        # Command node without command
        command_without_command = {
            "id": "CMD-INVALID123",
            "layer": "Command",
            "title": "Invalid Command",
            "description": "Missing command",
        }

        is_valid, errors = validate_node_structure(command_without_command)
        assert is_valid is False
        assert any(
            "Command layer nodes must have a command" in error
            for error in errors
        )

        # Non-command node with command
        goal_with_command = {
            "id": "GOAL-INVALID456",
            "layer": "Goal",
            "title": "Invalid Goal",
            "description": "Should not have command",
            "command": {"ac_ref": "AC-TEST123", "run": {"shell": "echo test"}},
        }

        is_valid, errors = validate_node_structure(goal_with_command)
        assert is_valid is False
        assert any(
            "Only Command layer nodes can have a command" in error
            for error in errors
        )


class TestExportUtilities:
    """Test export utility functions."""

    def test_export_to_json(self):
        """Test JSON export."""
        nodes = [
            create_test_node("GOAL-EXPORT1", title="Export Test Goal 1"),
            create_test_node("TSK-EXPORT2", title="Export Test Task 2"),
        ]

        json_str = export_to_json(nodes)
        exported_data = json.loads(json_str)

        assert len(exported_data) == 2
        assert exported_data[0]["id"] == "GOAL-EXPORT1"
        assert exported_data[1]["id"] == "TSK-EXPORT2"

    def test_export_to_csv(self):
        """Test CSV export."""
        test_date = datetime(2023, 12, 25, tzinfo=UTC)
        nodes = [
            Node(
                id="GOAL-CSV1",
                layer=NodeLayer.GOAL,
                title="CSV Test Goal",
                description="Testing CSV export",
                status=NodeStatus.COMPLETED,
                progress=100,
                assignee="test_user",
                started_date=test_date,
                links=NodeLinks(),
            ),
        ]

        csv_str = export_to_csv(nodes)
        csv_reader = csv.reader(StringIO(csv_str))
        rows = list(csv_reader)

        # Check header
        assert len(rows[0]) == 9
        assert "ID" in rows[0]
        assert "Title" in rows[0]

        # Check data row
        assert len(rows[1]) == 9
        assert rows[1][0] == "GOAL-CSV1"
        assert rows[1][2] == "CSV Test Goal"


class TestImportUtilities:
    """Test import utility functions."""

    def test_import_nodes_from_json_valid(self):
        """Test importing valid JSON data."""
        json_data = json.dumps(
            [
                {
                    "id": "GOAL-IMPORT1",
                    "layer": "Goal",
                    "title": "Import Test Goal",
                    "description": "Testing JSON import",
                    "status": "planned",
                },
                {
                    "id": "TSK-IMPORT2",
                    "layer": "Task",
                    "title": "Import Test Task",
                    "description": "Testing JSON import",
                    "status": "planned",
                    "progress": 0,
                },
            ]
        )

        nodes, errors = import_nodes_from_json(json_data)
        assert len(nodes) == 2
        assert len(errors) == 0
        assert nodes[0]["id"] == "GOAL-IMPORT1"
        assert nodes[1]["id"] == "TSK-IMPORT2"

    def test_import_nodes_from_json_invalid_json(self):
        """Test importing invalid JSON."""
        invalid_json = "{ invalid json }"

        nodes, errors = import_nodes_from_json(invalid_json)
        assert len(nodes) == 0
        assert len(errors) == 1
        assert "Invalid JSON" in errors[0]

    def test_import_nodes_from_json_invalid_structure(self):
        """Test importing JSON with invalid node structure."""
        json_data = json.dumps(
            [
                {
                    "id": "INVALID-ID",  # Invalid ID format
                    "layer": "Goal",
                    "title": "Invalid Goal",
                    "description": "Has invalid ID",
                }
            ]
        )

        nodes, errors = import_nodes_from_json(json_data)
        assert len(nodes) == 0
        assert len(errors) >= 1
        assert any("Invalid node ID format" in error for error in errors)

    def test_import_nodes_from_json_not_a_list(self):
        """Test importing JSON that's not a list."""
        json_data = json.dumps(
            {
                "id": "GOAL-NOTLIST",
                "layer": "Goal",
                "title": "Not a List",
                "description": "Should be in a list",
            }
        )

        nodes, errors = import_nodes_from_json(json_data)
        assert len(nodes) == 0
        assert len(errors) == 1
        assert "must be a list" in errors[0]


class TestMetadataUtilities:
    """Test metadata utility functions."""

    def test_merge_node_metadata_both_empty(self):
        """Test merging empty metadata."""
        result = merge_node_metadata(None, None)
        assert result == {}

    def test_merge_node_metadata_base_only(self):
        """Test merging with only base metadata."""
        base = {"owner": "alice", "labels": ["important"]}
        result = merge_node_metadata(base, None)
        assert result == base

    def test_merge_node_metadata_updates_only(self):
        """Test merging with only updates metadata."""
        updates = {"assignee": "bob", "severity": "high"}
        result = merge_node_metadata(None, updates)
        assert result == updates

    def test_merge_node_metadata_both_provided(self):
        """Test merging both base and updates metadata."""
        base = {
            "owner": "alice",
            "labels": ["important"],
            "priority": "medium",
        }
        updates = {"assignee": "bob", "priority": "high", "labels": ["urgent"]}

        result = merge_node_metadata(base, updates)
        assert result["owner"] == "alice"
        assert result["assignee"] == "bob"
        assert result["priority"] == "high"
        # Labels should be merged (order doesn't matter)
        assert set(result["labels"]) == {"important", "urgent"}

    def test_merge_node_metadata_label_merge(self):
        """Test specific label merging behavior."""
        base = {"labels": ["base1", "base2"]}
        updates = {
            "labels": ["update1", "base2"]
        }  # base2 should be deduplicated

        result = merge_node_metadata(base, updates)
        assert set(result["labels"]) == {"base1", "base2", "update1"}
        assert len(result["labels"]) == 3


# Helper function to create test nodes
def create_test_node(
    node_id: str,
    status: NodeStatus = NodeStatus.PLANNED,
    layer: NodeLayer = NodeLayer.TASK,
    title: str = "Test Node",
    description: str = "Test description",
    assignee: str | None = None,
    labels: list | None = None,
) -> Node:
    """Helper function to create test nodes."""
    metadata = None
    if assignee or labels:
        metadata = NodeMetadata(assignee=assignee, labels=labels)

    return Node(
        id=node_id,
        layer=layer,
        title=title,
        description=description,
        status=status,
        metadata=metadata,
        assignee=assignee,
        links=NodeLinks(),
    )
