"""
YAML Parsing Tests

Tests for YAML functionality using modern patterns with ToDoWrite models.
"""

import json
import tempfile
from pathlib import Path

import pytest
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from todowrite.core.models import (
    Base,
    Command,
    Goal,
    Label,
    Task,
)


class TestYAMLParsing:
    """Test class for YAML parsing with ToDoWrite models."""

    @pytest.fixture
    def temp_session(self):
        """Create a temporary database session."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
            db_path = temp_file.name

        engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        yield session

        session.close()
        Path(db_path).unlink(missing_ok=True)

    def test_parse_valid_goal_yaml(self, temp_session):
        """Test parsing valid YAML goal data."""
        yaml_content = """
title: "Implement User Authentication"
description: "Add user login and registration functionality"
owner: "backend-team"
severity: "high"
work_type: "feature"
assignee: "alice"
extra_data:
  priority: 1
  estimated_hours: 40
  dependencies: ["database-setup", "api-design"]
"""

        yaml_data = yaml.safe_load(yaml_content)

        # Create goal from YAML data
        goal = Goal(
            title=yaml_data["title"],
            description=yaml_data["description"],
            owner=yaml_data["owner"],
            severity=yaml_data["severity"],
            work_type=yaml_data["work_type"],
            assignee=yaml_data["assignee"],
            extra_data=json.dumps(yaml_data["extra_data"]),
        )

        temp_session.add(goal)
        temp_session.commit()

        # Verify goal was created correctly
        retrieved_goal = (
            temp_session.query(Goal).filter(Goal.title == "Implement User Authentication").first()
        )
        assert retrieved_goal is not None
        assert retrieved_goal.owner == "backend-team"
        assert retrieved_goal.severity == "high"

        # Verify extra data was preserved
        extra_data = json.loads(retrieved_goal.extra_data)
        assert extra_data["priority"] == 1
        assert extra_data["estimated_hours"] == 40

    def test_parse_task_yaml_with_command(self, temp_session):
        """Test parsing YAML task data with command information."""
        yaml_content = """
title: "Database Migration Script"
description: "Script to migrate database schema"
owner: "devops"
severity: "medium"
work_type: "automation"
assignee: "bob"
cmd: "python migrate_database.py"
cmd_params: "--env production --backup"
extra_data:
  runtime_env:
    PYTHONPATH: "/app/src"
    DATABASE_URL: "${DATABASE_URL}"
  artifacts:
    - "migration_log.txt"
    - "backup_file.sql"
"""

        yaml_data = yaml.safe_load(yaml_content)

        # Create task and command from YAML data
        task = Task(
            title=yaml_data["title"],
            description=yaml_data["description"],
            owner=yaml_data["owner"],
            severity=yaml_data["severity"],
            work_type=yaml_data["work_type"],
            assignee=yaml_data["assignee"],
        )

        command = Command(
            title=f"{yaml_data['title']} Command",
            description=yaml_data["description"],
            cmd=yaml_data["cmd"],
            cmd_params=yaml_data["cmd_params"],
            owner=yaml_data["owner"],
            runtime_env=json.dumps(yaml_data["extra_data"]["runtime_env"]),
            artifacts=json.dumps(yaml_data["extra_data"]["artifacts"]),
        )

        temp_session.add_all([task, command])
        temp_session.commit()

        # Verify task and command were created
        retrieved_task = (
            temp_session.query(Task).filter(Task.title == "Database Migration Script").first()
        )
        retrieved_command = (
            temp_session.query(Command)
            .filter(Command.title == "Database Migration Script Command")
            .first()
        )

        assert retrieved_task is not None
        assert retrieved_command is not None
        assert retrieved_command.cmd == "python migrate_database.py"
        assert retrieved_command.cmd_params == "--env production --backup"

    def test_parse_multiple_yaml_entries(self, temp_session):
        """Test parsing YAML file with multiple entries."""
        yaml_content = """
goals:
  - title: "Launch Product"
    description: "Successfully launch the product"
    owner: "product-manager"
    severity: "high"
    work_type: "milestone"
  - title: "Complete Documentation"
    description: "Write comprehensive documentation"
    owner: "tech-writer"
    severity: "medium"
    work_type: "documentation"

labels:
  - name: "urgent"
  - name: "backend"
  - name: "frontend"

tasks:
  - title: "Setup CI/CD Pipeline"
    description: "Automated deployment pipeline"
    owner: "devops"
    severity: "high"
    work_type: "infrastructure"
  - title: "Write Unit Tests"
    description: "Comprehensive test suite"
    owner: "qa-team"
    severity: "medium"
    work_type: "testing"
"""

        yaml_data = yaml.safe_load(yaml_content)

        # Create goals from YAML
        for goal_data in yaml_data["goals"]:
            goal = Goal(**goal_data)
            temp_session.add(goal)

        # Create labels from YAML
        for label_data in yaml_data["labels"]:
            label = Label(**label_data)
            temp_session.add(label)

        # Create tasks from YAML
        for task_data in yaml_data["tasks"]:
            task = Task(**task_data)
            temp_session.add(task)

        temp_session.commit()

        # Verify all records were created
        assert temp_session.query(Goal).count() == 2
        assert temp_session.query(Label).count() == 3
        assert temp_session.query(Task).count() == 2

        # Verify specific data
        launch_goal = temp_session.query(Goal).filter(Goal.title == "Launch Product").first()
        assert launch_goal.severity == "high"
        assert launch_goal.work_type == "milestone"

    def test_yaml_error_handling(self):
        """Test YAML parsing error handling."""
        invalid_yaml_content = """
title: "Invalid YAML"
description: "This has invalid syntax
  missing quotes: "unclosed string
  - wrong indentation:
     - this is wrong
"""

        with pytest.raises(yaml.YAMLError):
            yaml.safe_load(invalid_yaml_content)

    def test_yaml_validation_with_models(self, temp_session):
        """Test YAML validation against ToDoWrite model constraints."""
        yaml_content = """
title: "Valid Model Data"
description: "Testing model validation"
owner: "test-user"
severity: "critical"
work_type: "feature"
assignee: "developer"
extra_data:
  priority: 1
  tags: ["backend", "api"]
  metadata:
    complex: true
    nested:
      level1:
        level2: "value"
"""

        yaml_data = yaml.safe_load(yaml_content)

        # Validate data against model constraints
        assert yaml_data["severity"] in ["low", "medium", "high", "critical"]
        assert yaml_data["work_type"] in ["feature", "bug-fix", "documentation", "testing"]
        assert isinstance(yaml_data["extra_data"], dict)

        # Create model and verify it persists
        goal = Goal(
            title=yaml_data["title"],
            description=yaml_data["description"],
            owner=yaml_data["owner"],
            severity=yaml_data["severity"],
            work_type=yaml_data["work_type"],
            assignee=yaml_data["assignee"],
            extra_data=json.dumps(yaml_data["extra_data"]),
        )

        temp_session.add(goal)
        temp_session.commit()

        # Verify model creation and data integrity
        retrieved_goal = temp_session.query(Goal).filter(Goal.title == "Valid Model Data").first()
        assert retrieved_goal is not None

        extra_data = json.loads(retrieved_goal.extra_data)
        assert extra_data["priority"] == 1
        assert extra_data["tags"] == ["backend", "api"]
        assert "metadata" in extra_data
        assert "nested" in extra_data["metadata"]

    def test_yaml_serialization_from_models(self, temp_session):
        """Test serializing models back to YAML format."""
        # Create test data
        goal = Goal(
            title="Serialization Test",
            description="Testing model to YAML conversion",
            owner="test-user",
            severity="high",
            work_type="feature",
            assignee="developer",
            extra_data='{"priority": 1, "complex": true}',
        )
        temp_session.add(goal)
        temp_session.commit()

        # Serialize to YAML format
        yaml_data = {
            "title": goal.title,
            "description": goal.description,
            "owner": goal.owner,
            "severity": goal.severity,
            "work_type": goal.work_type,
            "assignee": goal.assignee,
            "extra_data": json.loads(goal.extra_data) if goal.extra_data else {},
            "created_at": goal.created_at,
            "updated_at": goal.updated_at,
            "id": goal.id,
        }

        yaml_output = yaml.dump(yaml_data, default_flow_style=False)

        # Verify YAML can be parsed back
        parsed_data = yaml.safe_load(yaml_output)
        assert parsed_data["title"] == "Serialization Test"
        assert parsed_data["severity"] == "high"
        assert parsed_data["extra_data"]["priority"] == 1

    def test_yaml_file_operations(self, temp_session):
        """Test reading and writing YAML files."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as temp_file:
            yaml_file_path = temp_file.name

            # Write YAML file
            yaml_content = """
goals:
  - title: "File Test Goal"
    description: "Testing file operations"
    owner: "file-user"
    severity: "low"
    work_type: "feature"

labels:
  - name: "file-test"
"""

            temp_file.write(yaml_content)

        # Read YAML file
        with open(yaml_file_path) as f:
            yaml_data = yaml.safe_load(f)

        # Create models from file data
        for goal_data in yaml_data["goals"]:
            goal = Goal(**goal_data)
            temp_session.add(goal)

        for label_data in yaml_data["labels"]:
            label = Label(**label_data)
            temp_session.add(label)

        temp_session.commit()

        # Verify data was created
        assert temp_session.query(Goal).count() == 1
        assert temp_session.query(Label).count() == 1

        # Clean up
        Path(yaml_file_path).unlink(missing_ok=True)

    def test_yaml_complex_nested_structures(self, temp_session):
        """Test parsing complex nested YAML structures."""
        yaml_content = """
project:
  name: "Complex Project"
  description: "Testing complex YAML structures"

phases:
  - name: "Planning Phase"
    description: "Initial planning and design"
    owner: "project-manager"
    severity: "high"
    tasks:
      - title: "Requirements Analysis"
        description: "Analyze and document requirements"
        owner: "business-analyst"
        severity: "high"
        work_type: "documentation"
        extra_data:
          stakeholders: ["product", "engineering", "sales"]
          deliverables: ["requirements-doc", "user-stories"]
      - title: "Technical Design"
        description: "Design technical architecture"
        owner: "tech-lead"
        severity: "high"
        work_type: "design"
        extra_data:
          architecture_diagrams: ["system-design", "database-design"]
          technology_stack: ["python", "postgresql", "react"]
  - name: "Implementation Phase"
    description: "Core implementation work"
    owner: "tech-lead"
    severity: "high"
    tasks:
      - title: "Backend Development"
        description: "Implement backend services"
        owner: "backend-dev"
        severity: "high"
        work_type: "feature"
        extra_data:
          services: ["auth", "api", "database"]
          frameworks: ["fastapi", "sqlalchemy"]

labels:
  - name: "planning"
  - name: "design"
  - name: "architecture"
"""

        yaml_data = yaml.safe_load(yaml_content)

        # Process complex structure - create models
        created_goals = []
        created_tasks = []
        created_labels = []

        # Process phases and tasks
        for phase_data in yaml_data["phases"]:
            # Create phase as goal (for this example)
            goal = Goal(
                title=phase_data["name"],
                description=phase_data["description"],
                owner=phase_data["owner"],
                severity=phase_data["severity"],
                work_type="phase",
            )
            created_goals.append(goal)

            # Create tasks
            for task_data in phase_data.get("tasks", []):  # Use .get() to avoid KeyError
                task = Task(
                    title=task_data["title"],
                    description=task_data["description"],
                    owner=task_data["owner"],
                    severity=task_data["severity"],
                    work_type=task_data["work_type"],
                    extra_data=json.dumps(
                        task_data.get("extra_data", {})
                    ),  # Use .get() to avoid KeyError
                )
                created_tasks.append(task)  # In real app, would link to phase

        # Create labels
        for label_data in yaml_data.get("labels", []):  # Use .get() to avoid KeyError
            label = Label(name=label_data["name"])
            created_labels.append(label)

        # Save to database
        temp_session.add_all(created_goals + created_tasks + created_labels)
        temp_session.commit()

        # Verify complex data was processed correctly
        assert temp_session.query(Goal).count() >= 2  # 2 phases
        assert temp_session.query(Task).count() >= 3  # 3 tasks
        assert temp_session.query(Label).count() == 3

        # Verify task with complex extra_data
        design_task = temp_session.query(Task).filter(Task.title == "Technical Design").first()
        if design_task:
            extra_data = json.loads(design_task.extra_data)
            assert "technology_stack" in extra_data
            assert "python" in extra_data["technology_stack"]

    def test_yaml_type_conversions(self, temp_session):
        """Test proper type conversions from YAML to Python types."""
        yaml_content = """
title: "Type Conversion Test"
description: "Testing various data type conversions"
priority: 1
estimated_hours: 42.5
is_active: true
tags: ["tag1", "tag2", "tag3"]
metadata:
  created_by: "test-user"
  timestamps:
    created: "2025-01-01T00:00:00Z"
    updated: "2025-01-02T12:30:00Z"
  config:
    debug: true
    max_connections: 100
    timeout: null
"""

        yaml_data = yaml.safe_load(yaml_content)

        # Verify type conversions
        assert isinstance(yaml_data["priority"], int)
        assert isinstance(yaml_data["estimated_hours"], float)
        assert isinstance(yaml_data["is_active"], bool)
        assert isinstance(yaml_data["tags"], list)
        assert isinstance(yaml_data["metadata"], dict)
        assert isinstance(yaml_data["metadata"]["config"]["debug"], bool)
        assert isinstance(yaml_data["metadata"]["config"]["max_connections"], int)
        assert yaml_data["metadata"]["config"]["timeout"] is None

        # Store in model (convert complex data to JSON)
        goal = Goal(
            title=yaml_data["title"],
            description=yaml_data["description"],
            owner="conversion-test",
            extra_data=json.dumps(yaml_data),
        )

        temp_session.add(goal)
        temp_session.commit()

        # Retrieve and verify type preservation
        retrieved_goal = (
            temp_session.query(Goal).filter(Goal.title == "Type Conversion Test").first()
        )
        assert retrieved_goal is not None

        stored_data = json.loads(retrieved_goal.extra_data)
        assert isinstance(stored_data["priority"], int)
        assert isinstance(stored_data["estimated_hours"], float)
        assert isinstance(stored_data["is_active"], bool)
        assert isinstance(stored_data["tags"], list)
