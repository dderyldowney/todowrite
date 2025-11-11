"""
Debug database operations to understand isolation issues.
"""

import uuid

from todowrite.core.app import (
    create_node,
    get_node,
    list_nodes,
)


def test_debug_database_operations():
    """Debug database operations step by step."""
    # Create unique test data
    unique_id = uuid.uuid4().hex[:8].upper()
    test_node_data = {
        "id": f"GOAL-{unique_id}",
        "title": f"Debug Goal {unique_id}",
        "description": f"Debug goal {unique_id}",
        "layer": "Goal",
        "status": "planned",
        "metadata": {
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "version": 1,
        },
        "links": {"parents": [], "children": []},
    }

    print(f"Creating node with ID: {test_node_data['id']}")

    # Create node
    created_node = create_node(test_node_data)
    print(f"Created node: {created_node}")

    # Try to retrieve it immediately
    retrieved_node = get_node(created_node.id)
    print(f"Retrieved node: {retrieved_node}")

    # List all nodes
    nodes_list = list_nodes()
    print(f"All nodes: {nodes_list}")

    # Debug info
    print(f"Created node ID: {created_node.id}")
    print(f"Retrieved node exists: {retrieved_node is not None}")
    print(f"Number of nodes in list: {len(nodes_list.get('nodes', []))}")

    # Basic assertions
    assert created_node is not None
    assert retrieved_node is not None
    assert created_node.id == retrieved_node.id
