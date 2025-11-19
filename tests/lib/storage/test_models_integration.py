"""
Models Integration Tests

Tests for integrating ToDoWrite models with modern database operations.
Replaces the legacy todowrite storage backend functionality.
"""

import json
import tempfile
from pathlib import Path

import pytest
from sqlalchemy import and_, create_engine, func, or_
from sqlalchemy.orm import sessionmaker
from todowrite.core.models import (
    Base,
    Command,
    Goal,
    Label,
    Phase,
    Step,
    Task,
)


class TestModelsIntegration:
    """Test class for integrating ToDoWrite models with database operations."""

    @pytest.fixture
    def database_session(self):
        """Create a complete database session with all tables."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
            db_path = temp_file.name

        engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        yield session

        session.close()
        Path(db_path).unlink(missing_ok=True)

    def test_complete_workflow_creation(self, database_session):
        """Test complete workflow: Goal -> Phase -> Step -> Task -> Command."""
        # Create Goal
        goal = Goal(
            title="Launch New Product",
            description="Successfully launch the new product to market",
            owner="product-manager",
            severity="high",
            work_type="milestone"
        )
        database_session.add(goal)
        database_session.commit()

        # Create Phase
        phase = Phase(
            title="Development Phase",
            description="Core development work for the product",
            owner="tech-lead",
            severity="high",
            work_type="development"
        )
        database_session.add(phase)
        database_session.commit()

        # Create Step
        step = Step(
            title="Backend API Development",
            description="Develop the REST API backend services",
            owner="backend-lead",
            severity="medium",
            work_type="development"
        )
        database_session.add(step)
        database_session.commit()

        # Create Task
        task = Task(
            title="User Authentication Service",
            description="Implement user login, registration, and JWT handling",
            owner="backend-dev",
            severity="high",
            work_type="feature",
            assignee="senior-dev"
        )
        database_session.add(task)
        database_session.commit()

        # Create Command
        command = Command(
            title="Run Authentication Tests",
            description="Execute comprehensive authentication test suite",
            cmd="python -m pytest tests/auth/",
            cmd_params="--verbose --coverage",
            owner="qa-engineer",
            runtime_env=json.dumps({
                "PYTHONPATH": "/app/src",
                "DATABASE_URL": "sqlite:///test.db",
                "JWT_SECRET": "test-secret"
            }),
            artifacts=json.dumps([
                "test_report.xml",
                "coverage_report.html",
                "auth_test.log"
            ])
        )
        database_session.add(command)
        database_session.commit()

        # Verify all records were created
        assert database_session.query(Goal).count() == 1
        assert database_session.query(Phase).count() == 1
        assert database_session.query(Step).count() == 1
        assert database_session.query(Task).count() == 1
        assert database_session.query(Command).count() == 1

        # Verify data integrity
        retrieved_goal = database_session.query(Goal).first()
        assert retrieved_goal.title == "Launch New Product"
        assert retrieved_goal.severity == "high"

        retrieved_command = database_session.query(Command).first()
        assert retrieved_command.cmd == "python -m pytest tests/auth/"
        assert "test_report.xml" in json.loads(retrieved_command.artifacts)

    def test_complex_queries_and_relationships(self, database_session):
        """Test complex database queries and relationships."""
        # Create test data
        goals = [
            Goal(title="Project Alpha", description="Main project", severity="high", owner="alice"),
            Goal(title="Project Beta", description="Secondary project", severity="medium", owner="bob"),
            Goal(title="Project Gamma", description="Minor project", severity="low", owner="alice"),
        ]

        tasks = [
            Task(title="Frontend Development", description="Frontend development work", work_type="feature", owner="charlie", assignee="designer"),
            Task(title="Backend Development", description="Backend development work", work_type="feature", owner="charlie", assignee="backend-dev"),
            Task(title="Database Setup", description="Database setup work", work_type="infrastructure", owner="alice", assignee="dba"),
            Task(title="Testing Setup", description="Testing framework work", work_type="testing", owner="bob", assignee="qa-engineer"),
        ]

        labels = [
            Label(name="urgent"),
            Label(name="backend"),
            Label(name="frontend"),
            Label(name="infrastructure"),
            Label(name="testing"),
        ]

        database_session.add_all(goals + tasks + labels)
        database_session.commit()

        # Test complex queries
        # Query by severity and owner
        high_priority_alice_goals = database_session.query(Goal).filter(
            and_(Goal.severity == "high", Goal.owner == "alice")
        ).all()
        assert len(high_priority_alice_goals) == 1
        assert high_priority_alice_goals[0].title == "Project Alpha"

        # Query by work_type using OR condition
        feature_or_infrastructure = database_session.query(Task).filter(
            or_(Task.work_type == "feature", Task.work_type == "infrastructure")
        ).all()
        assert len(feature_or_infrastructure) == 3

        # Query using LIKE pattern matching
        dev_tasks = database_session.query(Task).filter(
            Task.description.ilike("%dev%")
        ).all()
        assert len(dev_tasks) == 2

        # Test aggregate functions
        task_count_by_work_type = database_session.query(
            Task.work_type,
            func.count(Task.id).label("count")
        ).group_by(Task.work_type).all()

        work_type_counts = {row.work_type: row.count for row in task_count_by_work_type}
        assert work_type_counts["feature"] == 2
        assert work_type_counts["infrastructure"] == 1
        assert work_type_counts["testing"] == 1

    def test_data_validation_and_constraints(self, database_session):
        """Test data validation and constraint enforcement."""
        # Test unique constraint on Label
        label1 = Label(name="unique-label")
        database_session.add(label1)
        database_session.commit()

        # Try to create duplicate label
        label2 = Label(name="unique-label")
        database_session.add(label2)

        # Should fail due to unique constraint
        with pytest.raises(Exception):  # Could be IntegrityError
            database_session.commit()

        database_session.rollback()

        # Test proper constraint handling
        assert database_session.query(Label).filter(Label.name == "unique-label").count() == 1

        # Test field length constraints (basic validation)
        # Create goal with very long title to test it doesn't break
        long_title = "A" * 255
        goal = Goal(title=long_title, description="Testing length constraints")
        database_session.add(goal)
        database_session.commit()

        retrieved_goal = database_session.query(Goal).filter(Goal.id == goal.id).first()
        assert len(retrieved_goal.title) == 255

    def test_json_field_operations(self, database_session):
        """Test JSON field operations with complex data structures."""
        # Create goal with complex extra_data
        complex_extra_data = {
            "project_metadata": {
                "version": "2.0.1",
                "release_date": "2025-06-01",
                "team": {
                    "lead": "project-manager",
                    "members": ["dev1", "dev2", "dev3"],
                    "skills": ["python", "javascript", "sql"]
                }
            },
            "requirements": {
                "functional": [
                    "User authentication",
                    "Data visualization",
                    "Reporting dashboard"
                ],
                "non_functional": [
                    "Performance: <2s response time",
                    "Security: OAuth2 implementation",
                    "Availability: 99.9% uptime"
                ]
            },
            "metrics": {
                "story_points": 120,
                "estimated_hours": 240,
                "complexity_score": 8.5,
                "risk_level": "medium"
            }
        }

        goal = Goal(
            title="Complex Data Test",
            description="Testing JSON field with complex nested data",
            owner="data-architect",
            extra_data=json.dumps(complex_extra_data)
        )

        database_session.add(goal)
        database_session.commit()

        # Retrieve and verify JSON data integrity
        retrieved_goal = database_session.query(Goal).filter(Goal.title == "Complex Data Test").first()
        assert retrieved_goal is not None

        # Parse and verify nested structure
        stored_data = json.loads(retrieved_goal.extra_data)

        # Verify deep nested data
        assert stored_data["project_metadata"]["version"] == "2.0.1"
        assert "dev1" in stored_data["project_metadata"]["team"]["members"]
        assert "python" in stored_data["project_metadata"]["team"]["skills"]

        assert "User authentication" in stored_data["requirements"]["functional"]
        assert stored_data["requirements"]["non_functional"][0].startswith("Performance:")

        assert stored_data["metrics"]["story_points"] == 120
        assert stored_data["metrics"]["complexity_score"] == 8.5

        # Test updating JSON data
        stored_data["metrics"]["story_points"] = 130
        stored_data["project_metadata"]["team"]["members"].append("dev4")

        goal.extra_data = json.dumps(stored_data)
        database_session.commit()

        # Verify update
        updated_goal = database_session.query(Goal).filter(Goal.id == goal.id).first()
        updated_data = json.loads(updated_goal.extra_data)
        assert updated_data["metrics"]["story_points"] == 130
        assert "dev4" in updated_data["project_metadata"]["team"]["members"]

    def test_transaction_and_error_handling(self, database_session):
        """Test transaction management and error handling."""
        # Start with clean database
        initial_goal_count = database_session.query(Goal).count()

        # Test successful transaction
        try:
            goal1 = Goal(title="Transaction Test 1", description="Testing transaction")
            goal2 = Goal(title="Transaction Test 2", description="Testing transaction")

            database_session.add_all([goal1, goal2])
            database_session.commit()

            assert database_session.query(Goal).count() == initial_goal_count + 2

        except Exception as e:
            database_session.rollback()
            pytest.fail(f"Successful transaction failed: {e}")

        # Test transaction rollback
        # First create a label to ensure uniqueness constraint will be violated
        existing_label = Label(name="unique-label-rollback")
        database_session.add(existing_label)
        database_session.commit()

        try:
            goal3 = Goal(title="Rollback Test", description="This should be rolled back")
            database_session.add(goal3)
            database_session.flush()  # Get ID but don't commit

            # Simulate error condition - duplicate label should cause integrity error
            bad_label = Label(name="unique-label-rollback")  # This already exists
            database_session.add(bad_label)
            database_session.commit()

        except Exception:
            database_session.rollback()

        # Verify rollback worked - goal3 should not be persisted
        rollback_goal_count = database_session.query(Goal).count()
        assert rollback_goal_count == initial_goal_count + 2  # Only the successful ones

    def test_performance_with_bulk_operations(self, database_session):
        """Test performance with bulk database operations."""
        import time

        # Test bulk insert performance
        start_time = time.time()

        # Create many records efficiently
        goals = [
            Goal(
                title=f"Bulk Goal {i}",
                description=f"Bulk insert test goal number {i}",
                owner=f"user{i % 5}",  # Rotate through 5 users
                severity=["low", "medium", "high"][i % 3]
            )
            for i in range(100)
        ]

        tasks = [
            Task(
                title=f"Bulk Task {i}",
                description=f"Bulk insert test task number {i}",
                owner=f"user{i % 5}",
                work_type=["feature", "bug-fix", "testing"][i % 3]
            )
            for i in range(100)
        ]

        labels = [
            Label(name=f"label{i}")
            for i in range(20)
        ]

        database_session.add_all(goals + tasks + labels)
        database_session.commit()

        bulk_insert_time = time.time() - start_time

        # Should complete reasonably fast
        assert bulk_insert_time < 5.0, f"Bulk insert took too long: {bulk_insert_time:.2f} seconds"

        # Verify all records were inserted
        assert database_session.query(Goal).filter(Goal.title.like("Bulk Goal%")).count() == 100
        assert database_session.query(Task).filter(Task.title.like("Bulk Task%")).count() == 100
        assert database_session.query(Label).filter(Label.name.like("label%")).count() == 20

        # Test bulk query performance
        start_time = time.time()

        all_bulk_goals = database_session.query(Goal).filter(Goal.title.like("Bulk Goal%")).all()
        all_bulk_tasks = database_session.query(Task).filter(Task.title.like("Bulk Task%")).all()

        bulk_query_time = time.time() - start_time

        # Should be fast for 200 records
        assert bulk_query_time < 1.0, f"Bulk query took too long: {bulk_query_time:.2f} seconds"
        assert len(all_bulk_goals) == 100
        assert len(all_bulk_tasks) == 100

    def test_database_integration_with_real_world_scenarios(self, database_session):
        """Test database integration with real-world project scenarios."""
        # Simulate a real software project hierarchy
        project_goal = Goal(
            title="E-commerce Platform Launch",
            description="Launch a complete e-commerce platform with payment processing, inventory management, and user accounts",
            owner="product-owner",
            severity="high",
            work_type="milestone",
            extra_data=json.dumps({
                "business_objectives": ["Revenue generation", "Market expansion"],
                "success_metrics": ["1000 daily active users", "$10k monthly revenue"],
                "timeline": "6 months"
            })
        )

        development_phase = Phase(
            title="Development Phase",
            description="Core development sprints",
            owner="tech-lead",
            severity="high",
            work_type="development",
            extra_data=json.dumps({
                "duration": "4 months",
                "team_size": 8,
                "methodology": "Agile/Scrum"
            })
        )

        # Create development tasks
        tasks = [
            Task(
                title="User Authentication System",
                description="Implement login, registration, password reset, and JWT token management",
                owner="backend-lead",
                severity="high",
                work_type="feature",
                assignee="senior-backend-dev",
                extra_data=json.dumps({
                    "technologies": ["Node.js", "Express", "JWT", "bcrypt"],
                    "acceptance_criteria": [
                        "Users can register with email",
                        "Users can login with email/password",
                        "JWT tokens are properly signed",
                        "Password reset functionality works"
                    ]
                })
            ),
            Task(
                title="Product Catalog API",
                description="RESTful API for product catalog with search, filtering, and pagination",
                owner="backend-lead",
                severity="high",
                work_type="feature",
                assignee="backend-dev",
                extra_data=json.dumps({
                    "endpoints": ["/api/products", "/api/products/:id", "/api/products/search"],
                    "features": ["search", "filtering", "sorting", "pagination"]
                })
            ),
            Task(
                title="Payment Integration",
                description="Integrate Stripe payment processing for credit cards and digital wallets",
                owner="backend-lead",
                severity="high",
                work_type="integration",
                assignee="backend-dev",
                extra_data=json.dumps({
                    "payment_providers": ["Stripe", "PayPal"],
                    "test_coverage": ["sandbox testing", "edge cases"]
                })
            )
        ]

        # Create database commands
        commands = [
            Command(
                title="Run Authentication Tests",
                description="Execute comprehensive authentication system test suite",
                cmd="python -m pytest tests/auth/ --cov=auth",
                cmd_params="--verbose --junitxml",
                owner="qa-lead",
                runtime_env=json.dumps({
                    "NODE_ENV": "test",
                    "TEST_DB": "sqlite:///:memory:",
                    "JWT_SECRET": "test-jwt-secret"
                }),
                artifacts=json.dumps(["test-results.xml", "coverage-report.html"])
            ),
            Command(
                title="Database Migration",
                description="Run database schema migrations",
                cmd="python manage.py migrate",
                cmd_params="--fake-initial",
                owner="devops",
                runtime_env=json.dumps({
                    "DATABASE_URL": "sqlite:///production.db",
                    "BACKUP_DB": "true"
                }),
                artifacts=json.dumps(["migration_log.txt", "backup.sql"])
            )
        ]

        # Create labels for categorization
        labels = [
            Label(name="authentication"),
            Label(name="api"),
            Label(name="payment"),
            Label(name="security"),
            Label(name="critical-path"),
            Label(name="integration"),
            Label(name="testing"),
        ]

        # Add all records to database
        database_session.add_all([
            project_goal, development_phase,
        ] + tasks + commands + labels)

        database_session.commit()

        # Verify the complete project structure
        assert database_session.query(Goal).count() == 1
        assert database_session.query(Phase).count() == 1
        assert database_session.query(Task).count() == 3
        assert database_session.query(Command).count() == 2
        assert database_session.query(Label).count() == 7

        # Verify real-world data integrity
        auth_task = database_session.query(Task).filter(Task.title == "User Authentication System").first()
        assert auth_task is not None
        assert auth_task.extra_data is not None

        auth_data = json.loads(auth_task.extra_data)
        assert "Node.js" in auth_data["technologies"]
        assert len(auth_data["acceptance_criteria"]) == 4

        # Test complex queries that would be used in real applications
        critical_path_tasks = database_session.query(Task).join(
            Label, Task.title.like("%Authentication%")
        ).filter(
            or_(Task.severity == "high", Task.work_type == "integration")
        ).all()
        assert len(critical_path_tasks) >= 1

        # Test aggregation queries for project management
        tasks_by_work_type = database_session.query(
            Task.work_type,
            func.count(Task.id).label("task_count")
        ).group_by(Task.work_type).all()

        work_type_distribution = {row.work_type: row.task_count for row in tasks_by_work_type}
        assert work_type_distribution["feature"] == 2
        assert work_type_distribution["integration"] == 1
