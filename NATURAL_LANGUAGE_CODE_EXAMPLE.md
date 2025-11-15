# Natural Language Code Examples

This document demonstrates how AI-generated code should always be written with full typing and natural language constructs.

## Example 1: Business Logic Function

```python
def create_user_workspace(
    database_url: str,
    user_identifier: str,
    workspace_name: str
) -> dict[str, Any]:
    """Create a new workspace for the specified user.

    This function sets up a complete workspace environment including:
    - Database connection validation
    - Initial node creation
    - Workspace metadata setup
    - Proper error handling

    Args:
        database_url: Connection string for the database
        user_identifier: Unique identifier for the user
        workspace_name: Human-readable name for the workspace

    Returns:
        Dictionary containing workspace details and creation status

    Raises:
        DatabaseConnectionError: If database connection fails
        WorkspaceCreationError: If workspace cannot be created
    """
    try:
        # Connect to the database first to ensure it's valid
        todowrite_app = ToDoWrite(database_url=database_url)

        # Create the main workspace goal with natural description
        workspace_goal = todowrite_app.create_node(
            layer="Goal",
            title=workspace_name,
            description=f"Personal workspace for {user_identifier}",
            metadata={
                "owner": user_identifier,
                "created_by": "system",
                "workspace_type": "personal"
            }
        )

        return {
            "workspace_id": workspace_goal["id"],
            "user_id": user_identifier,
            "name": workspace_name,
            "status": "created_successfully",
            "database_url": database_url
        }

    except Exception as error:
        raise WorkspaceCreationError(
            f"Failed to create workspace '{workspace_name}' for user '{user_identifier}': {error}"
        )
```

## Example 2: Data Processing Pipeline

```python
def process_user_task_hierarchy(
    todowrite_app: ToDoWrite,
    parent_goal_id: str
    task_descriptions: list[str]
    priority_weights: dict[str, int] | None = None
) -> list[dict[str, Any]]:
    """Process a list of task descriptions into a structured hierarchy.

    This function takes simple text descriptions and creates a properly
    structured task hierarchy under the specified parent goal, using
    natural language processing to understand task relationships.

    Args:
        todowrite_app: Active ToDoWrite application instance
        parent_goal_id: ID of the parent goal to attach tasks to
        task_descriptions: List of task descriptions in plain English
        priority_weights: Optional mapping of task types to priority levels

    Returns:
        List of created task dictionaries with their IDs and metadata

    Raises:
        HierarchyValidationError: If parent goal is not found
        TaskCreationError: If any task cannot be created
    """
    if priority_weights is None:
        priority_weights = {
            "implement": 1,
            "design": 2,
            "test": 3,
            "document": 4
        }

    created_tasks: list[dict[str, Any]] = []

    # Verify parent goal exists before creating tasks
    parent_goal = todowrite_app.get_node(parent_goal_id)
    if not parent_goal:
        raise HierarchyValidationError(f"Parent goal '{parent_goal_id}' not found")

    for task_description in task_descriptions:
        # Extract task type and intent from natural language description
        task_type = extract_task_type_from_description(task_description)
        priority_level = priority_weights.get(task_type, 2)

        # Create the task with meaningful metadata
        task_node = todowrite_app.create_node(
            layer="Task",
            title=task_description,
            description=f"Implementation of: {task_description}",
            metadata={
                "task_type": task_type,
                "priority_level": priority_level,
                "parent_goal": parent_goal_id,
                "estimated_complexity": estimate_task_complexity(task_description)
            }
        )

        # Link the task to its parent goal
        todowrite_app.link_nodes(
            source_id=parent_goal_id,
            target_id=task_node["id"],
            link_type="contains"
        )

        created_tasks.append({
            "task_id": task_node["id"],
            "description": task_description,
            "type": task_type,
            "priority": priority_level,
            "parent_goal": parent_goal_id
        })

    return created_tasks

def extract_task_type_from_description(description: str) -> str:
    """Extract the task type from a natural language description.

    This function analyzes the description to determine what kind of work
    the task represents, using keyword patterns and natural language
    understanding.

    Args:
        description: Natural language description of the task

    Returns:
        The identified task type as a string

    Examples:
        >>> extract_task_type_from_description("Implement user authentication")
        'implement'
        >>> extract_task_type_from_description("Design the database schema")
        'design'
        >>> extract_task_type_from_description("Write test cases for login")
        'test'
    """
    description_lower = description.lower()

    # Pattern matching for different task types
    task_patterns = {
        "implement": ["implement", "code", "program", "build", "create function"],
        "design": ["design", "schema", "architecture", "plan", "blueprint"],
        "test": ["test", "verify", "check", "validate", "ensure"],
        "document": ["document", "write", "explain", "describe", "manual"],
        "review": ["review", "audit", "inspect", "check over"]
    }

    for task_type, keywords in task_patterns.items():
        if any(keyword in description_lower for keyword in keywords):
            return task_type

    return "general"

def estimate_task_complexity(description: str) -> str:
    """Estimate the complexity level of a task from its description.

    This function analyzes the task description to provide a rough
    complexity estimate, considering factors like task scope, dependencies,
    and technical complexity.

    Args:
        description: Natural language description of the task

    Returns:
        Complexity level as a string: "simple", "moderate", "complex", or "unknown"
    """
    # Simple heuristic based on description length and complexity indicators
    complexity_indicators = ["multiple", "system", "integrate", "architecture"]

    if len(description) > 100:
        return "complex"
    elif any(indicator in description.lower() for indicator in complexity_indicators):
        return "moderate"
    elif len(description) < 30:
        return "simple"
    else:
        return "unknown"
```

## Example 3: Test with Natural Language Readability

```python
def test_user_workspace_creation_with_valid_database():
    """Test workspace creation succeeds when database connection is working.

    This test verifies that a user can successfully create a workspace
    when the database is properly configured and accessible. It checks that
    the returned workspace contains all expected fields and that the database
    properly stores the workspace information.
    """
    # Use a temporary database for isolated testing
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_db:
        database_url = f"sqlite:///{temp_db.name}"

        # Test data
        test_user_id = "test_user_123"
        test_workspace_name = "My Test Workspace"

        # Execute the function being tested
        result = create_user_workspace(
            database_url=database_url,
            user_identifier=test_user_id,
            workspace_name=test_workspace_name
        )

        # Verify the workspace was created successfully
        assert result["status"] == "created_successfully"
        assert result["workspace_id"].startswith("GOAL-")
        assert result["user_id"] == test_user_id
        assert result["name"] == test_workspace_name
        assert result["database_url"] == database_url

        # Verify the workspace actually exists in the database
        todowrite_app = ToDoWrite(database_url=database_url)
        retrieved_workspace = todowrite_app.get_node(result["workspace_id"])

        assert retrieved_workspace is not None
        assert retrieved_workspace["title"] == test_workspace_name
        assert retrieved_workspace["metadata"]["owner"] == test_user_id

def test_workspace_creation_fails_with_invalid_database():
    """Test workspace creation raises appropriate error with invalid database.

    This test ensures that the function properly handles database connection
    failures and raises a meaningful exception instead of silently failing or
    returning incorrect results.
    """
    invalid_database_url = "sqlite:///nonexistent/path/database.db"

    # The function should raise the appropriate exception type
    with pytest.raises(WorkspaceCreationError) as exception_info:
        create_user_workspace(
            database_url=invalid_database_url,
            user_identifier="test_user",
            workspace_name="Test Workspace"
        )

    # Verify the error message contains useful information
    error_message = str(exception_info.value)
    assert "test_user" in error_message
    assert "Test Workspace" in error_message
    assert "Failed to create workspace" in error_message
```

## Key Principles Demonstrated:

1. **Full Type Hints**: Every parameter, return value, and variable is typed
2. **Natural Function Names**: Functions describe what they do in plain English
3. **Clear Docstrings**: Human-readable documentation that explains purpose and behavior
4. **Contextual Variable Names**: Variable names that tell a story (user_identifier, workspace_name)
5. **Natural Flow**: Code reads like logical sentences and follows business logic
6. **Self-Documenting**: Code structure makes the purpose clear without excessive comments
7. **Readable Tests**: Test names describe behavior in plain English with clear assertion messages
8. **Error Handling**: Meaningful exceptions with helpful error messages
9. **Business Logic**: Code follows natural business workflows and contexts

This is the standard of code quality that all AI-generated code must meet.