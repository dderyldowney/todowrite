"""
Comprehensive PostgreSQL API Test Suite

Extensive testing of the new ToDoWrite Models API using PostgreSQL as the backend.
This suite tests the full functionality of the library including:
- CRUD operations with all model types
- Complex relationships and queries
- Schema import/export functionality
- YAML data processing with PostgreSQL backend
- Performance and scalability testing
- Data integrity and validation
- Advanced PostgreSQL features (JSON, indexing, etc.)
"""

from __future__ import annotations

import json
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List

import pytest
import yaml
from sqlalchemy import create_engine, text, and_, or_, func
from sqlalchemy.orm import sessionmaker

from todowrite.core.models import (
    Goal,
    Task,
    Phase,
    Step,
    Label,
    Command,
    Base,
    Concept,
    Context,
    Constraints,
    Requirements,
    AcceptanceCriteria,
    InterfaceContract,
    SubTask,
)

try:
    from .docker_utils import docker_manager, TestPostgreSQLConfig
except ImportError:
    # Fallback for when running directly
    import sys
    from pathlib import Path

    # Add the parent directory to path so we can import docker_utils
    parent_dir = Path(__file__).parent.parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))

    from tests.lib.docker.docker_utils import docker_manager, TestPostgreSQLConfig


@pytest.mark.requires_docker
class TestComprehensivePostgreSQLAPI:
    """Comprehensive API testing with PostgreSQL backend."""

    @pytest.fixture(scope="class")
    def postgresql_url(self: "TestComprehensivePostgreSQLAPI") -> str:
        """Start PostgreSQL container and return connection URL."""
        if not docker_manager.start_postgresql_container("docker-compose"):
            pytest.skip("Failed to start PostgreSQL container")

        yield TestPostgreSQLConfig.get_connection_url()

        docker_manager.stop_postgresql_container("docker-compose")

    @pytest.fixture
    def session(self: "TestComprehensivePostgreSQLAPI", postgresql_url: str):
        """Create database session for testing."""
        engine = create_engine(postgresql_url)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        yield session

        session.close()

    def test_full_crud_operations_all_models(self: "TestComprehensivePostgreSQLAPI", session: Any) -> None:
        """Test comprehensive CRUD operations for all model types."""
        # Test all model types creation
        goal = Goal(
            title="Comprehensive Test Goal",
            description="Testing all model types with PostgreSQL",
            owner="test-user",
            severity="high",
            work_type="feature",
            assignee="developer",
            extra_data=json.dumps({
                "priority": 1,
                "estimated_complexity": "high",
                "tags": ["comprehensive", "postgresql", "testing"]
            })
        )

        task = Task(
            title="Core Task Implementation",
            description="Main task for comprehensive testing",
            owner="test-user",
            severity="medium",
            work_type="development",
            assignee="backend-developer",
            extra_data=json.dumps({
                "complexity_score": 8,
                "dependencies": ["database-setup", "api-design"],
                "estimated_hours": 40
            })
        )

        phase = Phase(
            title="Development Phase",
            description="Main development phase",
            owner="project-manager",
            severity="high",
            work_type="development"
        )

        step = Step(
            title="Database Setup",
            description="Initialize database schema",
            owner="database-admin",
            severity="high",
            work_type="infrastructure"
        )

        subtask = SubTask(
            title="Create Migration Scripts",
            description="SQL migration scripts",
            owner="database-admin",
            severity="high",
            work_type="database"
        )

        label1 = Label(name="postgresql")
        label2 = Label(name="comprehensive")
        label3 = Label(name="api-testing")

        command = Command(
            title="Database Migration Command",
            description="Run database migrations",
            cmd="python manage.py migrate",
            cmd_params="--env=production",
            owner="devops",
            runtime_env=json.dumps({
                "DATABASE_URL": "${DATABASE_URL}",
                "PYTHONPATH": "/app/src"
            })
        )

        concept = Concept(
            title="Database Architecture Concept",
            description="Overall database design concept",
            owner="architect",
            severity="high",
            work_type="design"
        )

        context = Context(
            title="Project Context",
            description="Overall project context and goals",
            owner="product-manager",
            severity="high",
            work_type="planning"
        )

        constraints = Constraints(
            title="Performance Constraints",
            description="Performance and scalability constraints",
            owner="architect",
            severity="high",
            work_type="architecture"
        )

        requirements = Requirements(
            title="Functional Requirements",
            description="Core functional requirements",
            owner="product-manager",
            severity="high",
            work_type="requirements"
        )

        acceptance_criteria = AcceptanceCriteria(
            title="User Story Acceptance",
            description="Acceptance criteria for user stories",
            owner="qa-lead",
            severity="high",
            work_type="testing"
        )

        interface_contract = InterfaceContract(
            title="API Contract",
            description="REST API interface contract",
            owner="api-architect",
            severity="high",
            work_type="api"
        )

        # Add all to session
        all_models = [
            goal, task, phase, step, subtask, label1, label2, label3, command,
            concept, context, constraints, requirements, acceptance_criteria, interface_contract
        ]
        session.add_all(all_models)
        session.commit()

        # Verify all were created with IDs
        for model in all_models:
            assert model.id is not None

        # Test relationships - add labels to goal
        goal.labels.extend([label1, label2, label3])
        session.commit()

        # Test READ operations with complex queries
        retrieved_goal = session.query(Goal).filter(
            Goal.title == "Comprehensive Test Goal"
        ).first()
        assert retrieved_goal is not None
        assert len(retrieved_goal.labels) == 3

        # Test JSON field queries
        complex_tasks = session.query(Task).filter(
            Task.extra_data.contains('complexity_score')
        ).all()
        assert len(complex_tasks) == 1

        # Test UPDATE operations
        goal.severity = "critical"
        goal.extra_data = json.dumps({
            "priority": 1,
            "estimated_complexity": "very-high",
            "tags": ["comprehensive", "postgresql", "testing", "updated"],
            "last_updated": time.time()
        })
        session.commit()

        updated_goal = session.query(Goal).filter(Goal.id == goal.id).first()
        assert updated_goal.severity == "critical"
        updated_data = json.loads(updated_goal.extra_data)
        assert "updated" in updated_data["tags"]

        # Test DELETE operations with cascading
        session.delete(label3)
        session.commit()

        # Verify relationship is maintained
        remaining_goal = session.query(Goal).filter(Goal.id == goal.id).first()
        assert len(remaining_goal.labels) == 2

    def test_complex_relationship_patterns(self: "TestComprehensivePostgreSQLAPI", session: Any) -> None:
        """Test complex relationship patterns and queries."""
        # Create hierarchical data structure
        main_goal = Goal(
            title="E-commerce Platform",
            description="Complete e-commerce solution",
            owner="product-owner",
            severity="critical"
        )

        development_phase = Phase(
            title="Core Development",
            description="Main development phase",
            owner="tech-lead",
            severity="high"
        )

        # Create tasks for the phase
        auth_task = Task(
            title="User Authentication",
            description="Implement login/registration system",
            owner="backend-lead",
            severity="high",
            work_type="feature"
        )

        api_task = Task(
            title="REST API Development",
            description="Build comprehensive REST API",
            owner="backend-lead",
            severity="high",
            work_type="feature"
        )

        # Create steps for tasks
        auth_steps = [
            Step(title="Design Auth Schema", owner="database-admin", severity="high"),
            Step(title="Implement JWT Tokens", owner="backend-dev", severity="high"),
            Step(title="Build Auth Endpoints", owner="backend-dev", severity="medium")
        ]

        # Create labels
        labels = [
            Label(name="e-commerce"),
            Label(name="authentication"),
            Label(name="api"),
            Label(name="security"),
            Label(name="backend")
        ]

        session.add_all([
            main_goal, development_phase, auth_task, api_task,
            *auth_steps, *labels
        ])
        session.commit()

        # Establish relationships
        main_goal.labels.extend([labels[0], labels[3], labels[4]])  # e-commerce, security, backend
        auth_task.labels.extend([labels[1], labels[2], labels[3]])  # authentication, api, security
        api_task.labels.extend([labels[2], labels[4]])  # api, backend

        # Add steps to task (relationship would be implemented in real app)
        for step in auth_steps:
            step.extra_data = json.dumps({"parent_task_id": auth_task.id})

        session.commit()

        # Test complex queries
        # Find all high-priority backend work
        high_priority_backend = session.query(Task).join(Task.labels).filter(
            Task.severity == "high",
            Label.name == "backend"
        ).all()
        assert len(high_priority_backend) == 2

        # Find security-related items across all models
        security_items = session.query(Label).filter(
            Label.name == "security"
        ).first()
        assert security_items is not None

        # Test JSON queries for hierarchical data
        auth_related_steps = session.query(Step).filter(
            Step.extra_data.contains('parent_task_id')
        ).all()
        assert len(auth_related_steps) == 3

    def test_yaml_import_export_functionality(self: "TestComprehensivePostgreSQLAPI", session: Any) -> None:
        """Test comprehensive YAML import/export with PostgreSQL backend."""
        # Create complex YAML data structure
        yaml_content = """
project:
  name: "Comprehensive API Test"
  description: "Testing full API functionality with PostgreSQL"
  version: "1.0.0"

goals:
  - title: "Launch E-commerce Platform"
    description: "Complete e-commerce solution with all features"
    owner: "product-owner"
    severity: "critical"
    work_type: "milestone"
    extra_data:
      business_value: "high"
      revenue_impact: "$1M+"
      customer_count: 10000

  - title: "Mobile Application"
    description: "Native mobile apps for iOS and Android"
    owner: "mobile-lead"
    severity: "high"
    work_type: "feature"
    extra_data:
      platforms: ["ios", "android"]
      target_users: 50000
      launch_date: "Q3 2025"

phases:
  - title: "Discovery & Planning"
    description: "Initial discovery and detailed planning"
    owner: "project-manager"
    severity: "high"
    work_type: "planning"
    duration_weeks: 4

  - title: "Core Development"
    description: "Main development work"
    owner: "tech-lead"
    severity: "high"
    work_type: "development"
    duration_weeks: 12

tasks:
  - title: "Database Design"
    description: "Design comprehensive database schema"
    owner: "database-architect"
    severity: "high"
    work_type: "design"
    extra_data:
      tables: 25
      relationships: "complex"
      estimated_hours: 40
      technologies: ["postgresql", "redis"]

  - title: "Payment Gateway Integration"
    description: "Integrate multiple payment providers"
    owner: "backend-lead"
    severity: "high"
    work_type: "integration"
    extra_data:
      providers: ["stripe", "paypal", "square"]
      compliance: "pci-dss"
      testing_required: true

  - title: "User Authentication System"
    description: "Complete user authentication and authorization"
    owner: "security-lead"
    severity: "critical"
    work_type: "feature"
    extra_data:
      methods: ["email", "social", "sso"]
      security_level: "high"
      mfa_required: true

labels:
  - name: "e-commerce"
  - name: "payment"
  - name: "security"
  - name: "mobile"
  - name: "database"
  - name: "api"

commands:
  - title: "Database Migration"
    description: "Run database schema migrations"
    cmd: "python manage.py migrate"
    cmd_params: "--env=production --backup"
    owner: "devops"
    runtime_env:
      DATABASE_URL: "${DATABASE_URL}"
      BACKUP_PATH: "/backups/database"

  - title: "Payment Processing Test"
    description: "Test payment gateway integration"
    cmd: "python -m tests.payment.test_providers"
    cmd_params: "--sandbox --verbose"
    owner: "qa-engineer"
    runtime_env:
      PAYMENT_ENV: "sandbox"
      LOG_LEVEL: "debug"
"""

        # Parse YAML and import to PostgreSQL
        yaml_data = yaml.safe_load(yaml_content)

        # Process and create all models
        created_models = []

        # Process goals
        for goal_data in yaml_data["goals"]:
            goal = Goal(
                title=goal_data["title"],
                description=goal_data["description"],
                owner=goal_data["owner"],
                severity=goal_data["severity"],
                work_type=goal_data["work_type"],
                extra_data=json.dumps(goal_data.get("extra_data", {}))
            )
            created_models.append(goal)

        # Process phases
        for phase_data in yaml_data["phases"]:
            phase = Phase(
                title=phase_data["title"],
                description=phase_data["description"],
                owner=phase_data["owner"],
                severity=phase_data["severity"],
                work_type=phase_data["work_type"],
                extra_data=json.dumps({
                    "duration_weeks": phase_data.get("duration_weeks")
                })
            )
            created_models.append(phase)

        # Process tasks
        for task_data in yaml_data["tasks"]:
            task = Task(
                title=task_data["title"],
                description=task_data["description"],
                owner=task_data["owner"],
                severity=task_data["severity"],
                work_type=task_data["work_type"],
                extra_data=json.dumps(task_data.get("extra_data", {}))
            )
            created_models.append(task)

        # Process labels
        labels = []
        for label_data in yaml_data["labels"]:
            label = Label(name=label_data["name"])
            labels.append(label)
        created_models.extend(labels)

        # Process commands
        for command_data in yaml_data["commands"]:
            command = Command(
                title=command_data["title"],
                description=command_data["description"],
                cmd=command_data["cmd"],
                cmd_params=command_data["cmd_params"],
                owner=command_data["owner"],
                runtime_env=json.dumps(command_data.get("runtime_env", {}))
            )
            created_models.append(command)

        # Save to PostgreSQL
        session.add_all(created_models)
        session.commit()

        # Verify data integrity
        assert session.query(Goal).count() == 2
        assert session.query(Phase).count() == 2
        assert session.query(Task).count() == 3
        assert session.query(Label).count() == 6
        assert session.query(Command).count() == 2

        # Test complex JSON data preservation
        payment_task = session.query(Task).filter(
            Task.title == "Payment Gateway Integration"
        ).first()
        assert payment_task is not None

        payment_extra = json.loads(payment_task.extra_data)
        assert "stripe" in payment_extra["providers"]
        assert payment_extra["compliance"] == "pci-dss"

        # Test export functionality
        exported_data = self._export_database_to_yaml(session)

        # Verify export contains all expected data
        assert len(exported_data["goals"]) == 2
        assert len(exported_data["phases"]) == 2
        assert len(exported_data["tasks"]) == 3
        assert len(exported_data["labels"]) == 6
        assert len(exported_data["commands"]) == 2

        # Verify data consistency
        exported_goals = {g["title"]: g for g in exported_data["goals"]}
        assert "Launch E-commerce Platform" in exported_goals
        assert exported_goals["Launch E-commerce Platform"]["severity"] == "critical"

    def _export_database_to_yaml(self: "TestComprehensivePostgreSQLAPI", session: Any) -> Dict[str, Any]:
        """Export all database data to YAML-compatible format."""
        export_data = {
            "goals": [],
            "phases": [],
            "tasks": [],
            "labels": [],
            "commands": []
        }

        # Export goals
        for goal in session.query(Goal).all():
            goal_data = {
                "title": goal.title,
                "description": goal.description,
                "owner": goal.owner,
                "severity": goal.severity,
                "work_type": goal.work_type,
                "extra_data": json.loads(goal.extra_data) if goal.extra_data else {}
            }
            export_data["goals"].append(goal_data)

        # Export phases
        for phase in session.query(Phase).all():
            phase_data = {
                "title": phase.title,
                "description": phase.description,
                "owner": phase.owner,
                "severity": phase.severity,
                "work_type": phase.work_type,
                "extra_data": json.loads(phase.extra_data) if phase.extra_data else {}
            }
            export_data["phases"].append(phase_data)

        # Export tasks
        for task in session.query(Task).all():
            task_data = {
                "title": task.title,
                "description": task.description,
                "owner": task.owner,
                "severity": task.severity,
                "work_type": task.work_type,
                "extra_data": json.loads(task.extra_data) if task.extra_data else {}
            }
            export_data["tasks"].append(task_data)

        # Export labels
        for label in session.query(Label).all():
            label_data = {"name": label.name}
            export_data["labels"].append(label_data)

        # Export commands
        for command in session.query(Command).all():
            command_data = {
                "title": command.title,
                "description": command.description,
                "cmd": command.cmd,
                "cmd_params": command.cmd_params,
                "owner": command.owner,
                "runtime_env": json.loads(command.runtime_env) if command.runtime_env else {}
            }
            export_data["commands"].append(command_data)

        return export_data

    def test_postgresql_advanced_features(self: "TestComprehensivePostgreSQLAPI", session: Any) -> None:
        """Test advanced PostgreSQL features and optimizations."""
        # Test JSON field operations
        complex_goals = []
        for i in range(100):
            goal = Goal(
                title=f"Complex Goal {i}",
                description=f"Goal with complex JSON data {i}",
                owner=f"user-{i % 10}",
                severity=["low", "medium", "high", "critical"][i % 4],
                work_type=["feature", "bug-fix", "documentation"][i % 3],
                extra_data=json.dumps({
                    "metadata": {
                        "created_by": f"user-{i % 10}",
                        "batch_id": i // 10,
                        "complexity_score": i % 100,
                        "tags": [f"tag-{j}" for j in range(i % 5)],
                        "nested": {
                            "level1": {
                                "level2": {
                                    "value": i,
                                    "active": i % 2 == 0
                                }
                            }
                        }
                    },
                    "performance_metrics": {
                        "estimated_hours": i * 2,
                        "confidence": 0.5 + (i % 50) / 100
                    }
                })
            )
            complex_goals.append(goal)

        session.add_all(complex_goals)
        session.commit()

        # Test JSON field queries
        # Query nested JSON properties
        active_goals = session.query(Goal).filter(
            Goal.extra_data.contains('active')
        ).all()
        assert len(active_goals) == 50  # Half should be active

        # Query specific JSON paths (PostgreSQL-specific)
        batch_goals = session.query(Goal).filter(
            Goal.extra_data.like('%"batch_id"%')
        ).all()
        assert len(batch_goals) == 100

        # Test complex queries with ordering and limits
        high_complexity_goals = session.query(Goal).filter(
            Goal.extra_data.contains('complexity_score')
        ).order_by(Goal.created_at.desc()).limit(10).all()
        assert len(high_complexity_goals) == 10

        # Test aggregation queries
        goal_counts_by_owner = session.query(
            Goal.owner,
            func.count(Goal.id).label('goal_count')
        ).group_by(Goal.owner).all()

        # Should have 10 different users
        assert len(goal_counts_by_owner) == 10

        # Each user should have exactly 10 goals
        for owner, count in goal_counts_by_owner:
            assert count == 10

    def test_database_performance_and_scalability(self: "TestComprehensivePostgreSQLAPI", postgresql_url: str) -> None:
        """Test database performance characteristics and scalability."""
        # Create performance test engine
        perf_engine = create_engine(postgresql_url)
        perf_session = sessionmaker(bind=perf_engine)()

        try:
            # Bulk insert performance test
            start_time = time.time()

            bulk_data = []
            for i in range(5000):  # 5000 records
                bulk_data.append(Goal(
                    title=f"Performance Goal {i}",
                    description=f"Performance testing goal number {i}",
                    owner=f"user-{i % 20}",
                    severity=["low", "medium", "high", "critical"][i % 4],
                    work_type=["feature", "bug-fix", "documentation", "testing", "infrastructure"][i % 5],
                    extra_data=json.dumps({
                        "batch_id": i // 100,
                        "performance_test": True,
                        "timestamp": time.time(),
                        "metadata": {
                            "index": i,
                            "checksum": f"hash-{i}",
                            "tags": [f"perf-tag-{j}" for j in range(i % 10)]
                        }
                    })
                ))

            perf_session.add_all(bulk_data)
            perf_session.commit()

            bulk_insert_time = time.time() - start_time
            print(f"Bulk insert of 5000 records took: {bulk_insert_time:.2f} seconds")

            # Should complete within reasonable time (under 30 seconds for 5000 records)
            assert bulk_insert_time < 30.0, f"Bulk insert too slow: {bulk_insert_time:.2f}s"

            # Query performance test
            start_time = time.time()

            # Complex query with JSON filtering and ordering
            complex_results = perf_session.query(Goal).filter(
                Goal.severity.in_(["high", "critical"]),
                Goal.extra_data.contains('performance_test'),
                Goal.title.like("%Performance Goal%")
            ).order_by(Goal.created_at.desc()).limit(1000).all()

            query_time = time.time() - start_time
            print(f"Complex query of {len(complex_results)} records took: {query_time:.2f} seconds")

            # Should complete complex query quickly
            assert query_time < 2.0, f"Complex query too slow: {query_time:.2f}s"
            assert len(complex_results) == 1000

            # Index utilization test
            start_time = time.time()

            # Query that should use index on title
            indexed_result = perf_session.query(Goal).filter(
                Goal.title == "Performance Goal 2500"
            ).first()

            index_query_time = time.time() - start_time
            print(f"Indexed query took: {index_query_time:.4f} seconds")

            # Should be extremely fast with proper indexing
            assert index_query_time < 0.01, f"Indexed query too slow: {index_query_time:.4f}s"
            assert indexed_result is not None

            # Pagination performance test
            start_time = time.time()

            page_size = 100
            total_pages = 10

            for page in range(total_pages):
                offset = page * page_size
                page_results = perf_session.query(Goal).order_by(Goal.id).offset(offset).limit(page_size).all()
                assert len(page_results) == page_size

            pagination_time = time.time() - start_time
            print(f"Pagination of {total_pages} pages took: {pagination_time:.2f} seconds")

            # Pagination should be efficient
            assert pagination_time < 1.0, f"Pagination too slow: {pagination_time:.2f}s"

        finally:
            perf_session.close()
            perf_engine.dispose()

    def test_data_integrity_and_validation(self: "TestComprehensivePostgreSQLAPI", session: Any) -> None:
        """Test data integrity, constraints, and validation with PostgreSQL."""
        # Test unique constraints
        label1 = Label(name="unique-test")
        session.add(label1)
        session.commit()

        # Try to create duplicate - should fail
        label2 = Label(name="unique-test")
        session.add(label2)

        with pytest.raises(Exception):  # IntegrityError
            session.commit()

        session.rollback()

        # Test foreign key relationships through association tables
        goal = Goal(title="Relationship Test", description="Testing relationships")
        label3 = Label(name="relationship-test")

        session.add_all([goal, label3])
        session.commit()

        # Add label to goal
        goal.labels.append(label3)
        session.commit()

        # Verify relationship exists
        retrieved_goal = session.query(Goal).filter(Goal.title == "Relationship Test").first()
        assert len(retrieved_goal.labels) == 1
        assert retrieved_goal.labels[0].name == "relationship-test"

        # Test JSON field validation
        valid_json_data = {
            "complex": {
                "nested": {
                    "arrays": [1, 2, 3],
                    "objects": {"key": "value"},
                    "boolean": True,
                    "null": None,
                    "number": 42.5
                }
            },
            "tags": ["postgresql", "testing", "json"],
            "config": {
                "enabled": True,
                "timeout": 30,
                "nested_config": {
                    "deep": True
                }
            }
        }

        goal_with_json = Goal(
            title="JSON Validation Test",
            description="Testing JSON field validation",
            extra_data=json.dumps(valid_json_data)
        )
        session.add(goal_with_json)
        session.commit()

        # Verify JSON data integrity
        retrieved_json_goal = session.query(Goal).filter(
            Goal.title == "JSON Validation Test"
        ).first()
        assert retrieved_json_goal is not None

        retrieved_data = json.loads(retrieved_json_goal.extra_data)
        assert retrieved_data == valid_json_data
        assert retrieved_data["complex"]["nested"]["arrays"] == [1, 2, 3]
        assert retrieved_data["config"]["nested_config"]["deep"] is True

        # Test large JSON data handling
        large_json_data = {
            "big_array": list(range(1000)),
            "large_text": "x" * 10000,
            "nested_structure": {
                f"level_{i}": {f"key_{j}": f"value_{i}_{j}" for j in range(10)}
                for i in range(20)
            }
        }

        goal_with_large_json = Goal(
            title="Large JSON Test",
            description="Testing large JSON data handling",
            extra_data=json.dumps(large_json_data)
        )
        session.add(goal_with_large_json)
        session.commit()

        # Verify large JSON data was stored and can be retrieved
        retrieved_large_goal = session.query(Goal).filter(
            Goal.title == "Large JSON Test"
        ).first()
        assert retrieved_large_goal is not None

        retrieved_large_data = json.loads(retrieved_large_goal.extra_data)
        assert len(retrieved_large_data["big_array"]) == 1000
        assert len(retrieved_large_data["large_text"]) == 10000

    def test_transaction_and_concurrency_handling(self: "TestComprehensivePostgreSQLAPI", postgresql_url: str) -> None:
        """Test transaction isolation and concurrent access patterns."""
        # Create multiple sessions for concurrency testing
        engines = [create_engine(postgresql_url) for _ in range(3)]
        sessions = [sessionmaker(bind=engine)() for engine in engines]

        try:
            # Test concurrent writes with different isolation levels
            def concurrent_goal_create(session_num: int, session: Any) -> int:
                """Create a goal in a specific session."""
                goal = Goal(
                    title=f"Concurrent Goal {session_num}",
                    description=f"Created by session {session_num}",
                    owner=f"user-{session_num}",
                    severity="medium",
                    work_type="feature",
                    extra_data=json.dumps({
                        "session_id": session_num,
                        "created_at": time.time(),
                        "concurrent_test": True
                    })
                )
                session.add(goal)
                session.commit()
                return goal.id

            # Create goals concurrently
            goal_ids = []
            for i, session in enumerate(sessions):
                goal_id = concurrent_goal_create(i + 1, session)
                goal_ids.append(goal_id)

            # Verify all goals were created with unique IDs
            assert len(set(goal_ids)) == 3, "Concurrent goals should have unique IDs"

            # Test transaction isolation
            # Start transaction in session 0
            test_goal = Goal(
                title="Isolation Test",
                description="Testing transaction isolation",
                owner="test-user"
            )
            sessions[0].add(test_goal)
            sessions[0].flush()  # Get ID but don't commit yet

            # Other sessions should not see uncommitted data
            for i in range(1, 3):
                invisible_goal = sessions[i].query(Goal).filter(
                    Goal.title == "Isolation Test"
                ).first()
                assert invisible_goal is None, "Uncommitted data should not be visible"

            # Commit and verify visibility across sessions
            sessions[0].commit()

            # Explicitly refresh other sessions to see committed data
            for i in range(1, 3):
                sessions[i].expire_all()
                visible_goal = sessions[i].query(Goal).filter(
                    Goal.title == "Isolation Test"
                ).first()
                assert visible_goal is not None, "Committed data should be visible"

            # Test rollback scenarios
            try:
                # Start transaction that will be rolled back
                rollback_goal = Goal(
                    title="Rollback Test",
                    description="This should be rolled back",
                    owner="test-user"
                )
                sessions[1].add(rollback_goal)
                sessions[1].flush()

                # Simulate error condition
                duplicate_label = Label(name="rollback-test-label")
                sessions[1].add(duplicate_label)
                sessions[1].commit()

                # Try to create same label again (should fail)
                duplicate_label2 = Label(name="rollback-test-label")
                sessions[1].add(duplicate_label2)
                sessions[1].commit()

            except Exception:
                # Rollback on error
                sessions[1].rollback()

            # Verify rollback worked
            sessions[1].expire_all()
            rolled_back_goal = sessions[1].query(Goal).filter(
                Goal.title == "Rollback Test"
            ).first()
            assert rolled_back_goal is None, "Rolled back data should not exist"

        finally:
            # Clean up all sessions
            for session in sessions:
                try:
                    session.close()
                except:
                    pass
            for engine in engines:
                try:
                    engine.dispose()
                except:
                    pass