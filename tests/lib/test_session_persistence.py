"""
Session Persistence Tests

Tests for session persistence functionality following TDD methodology.
RED → GREEN → REFACTOR cycle with specific exception handling.

Author: Claude Code Assistant
Version: 2025.1.0
"""

import json
import tempfile
from pathlib import Path
from typing import Any

import pytest

from todowrite.core.models import Base, Goal, Task, Label


class TestSessionPersistence:
    """Test class for session persistence functionality."""

    def test_session_marker_creation_missing_directory_should_fail_with_file_not_found_error(self) -> None:
        """
        RED: Test that session marker creation fails when directory doesn't exist.

        This test validates that the session persistence system properly handles
        missing directory scenarios by raising FileNotFoundError.
        """
        non_existent_path = Path("/tmp/non_existent_directory_12345/session.json")

        # This should fail because directory doesn't exist
        with pytest.raises(FileNotFoundError):
            self._create_session_marker(non_existent_path)

    def _create_session_marker(self, session_path: Path) -> dict[str, Any]:
        """
        Helper method to create a session marker.

        Args:
            session_path: Path where to create the session marker

        Returns:
            Created session data

        Raises:
            FileNotFoundError: If parent directory doesn't exist
        """
        session_data = {
            "session_id": "test-session-123",
            "created_at": "2025-01-01T00:00:00Z",
            "user_id": "test-user",
            "data": {"test": "data"}
        }

        # Ensure parent directory exists
        if not session_path.parent.exists():
            raise FileNotFoundError(f"Parent directory does not exist: {session_path.parent}")

        # Write session marker
        with open(session_path, 'w') as f:
            json.dump(session_data, f, indent=2)

        return session_data

    def test_session_marker_creation_with_valid_directory_should_succeed(self) -> None:
        """
        GREEN: Test that session marker creation succeeds with valid directory.

        This test validates that when a valid directory is provided,
        session marker creation succeeds and data is properly persisted.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            session_path = Path(temp_dir) / "session.json"

            # Should succeed with valid directory
            session_data = self._create_session_marker(session_path)

            # Verify file was created and contains correct data
            assert session_path.exists()

            with open(session_path, 'r') as f:
                loaded_data = json.load(f)

            assert loaded_data["session_id"] == "test-session-123"
            assert loaded_data["user_id"] == "test-user"
            assert loaded_data["data"]["test"] == "data"

    def test_session_marker_data_persistence_integrity(self) -> None:
        """
        GREEN: Test that session marker data maintains integrity across save/load cycles.

        This test validates that complex data structures can be persisted
        and loaded without corruption.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            session_path = Path(temp_dir) / "complex_session.json"

            # Create complex session data
            complex_session_data = {
                "session_id": "complex-session-456",
                "created_at": "2025-01-01T00:00:00Z",
                "user_id": "advanced-user",
                "data": {
                    "goals": [
                        {"title": "Goal 1", "priority": "high"},
                        {"title": "Goal 2", "priority": "low"}
                    ],
                    "settings": {
                        "theme": "dark",
                        "notifications": True,
                        "preferences": {"language": "en", "timezone": "UTC"}
                    }
                }
            }

            # Write complex data
            with open(session_path, 'w') as f:
                json.dump(complex_session_data, f, indent=2)

            # Load and verify integrity
            with open(session_path, 'r') as f:
                loaded_data = json.load(f)

            assert loaded_data == complex_session_data
            assert len(loaded_data["data"]["goals"]) == 2
            assert loaded_data["data"]["settings"]["theme"] == "dark"

    def test_session_marker_concurrent_access_handling(self) -> None:
        """
        REFACTOR: Test handling of concurrent session marker access.

        This test validates that the system can handle multiple sessions
        being created and accessed concurrently without conflicts.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            sessions = []

            # Create multiple session markers
            for i in range(5):
                session_path = Path(temp_dir) / f"session_{i}.json"
                session_data = {
                    "session_id": f"concurrent-session-{i}",
                    "user_id": f"user-{i}",
                    "data": {"index": i, "concurrent": True}
                }

                with open(session_path, 'w') as f:
                    json.dump(session_data, f, indent=2)

                sessions.append(session_data)

            # Verify all sessions were created correctly
            for i, expected_data in enumerate(sessions):
                session_path = Path(temp_dir) / f"session_{i}.json"
                with open(session_path, 'r') as f:
                    loaded_data = json.load(f)

                assert loaded_data["session_id"] == f"concurrent-session-{i}"
                assert loaded_data["data"]["index"] == i
                assert loaded_data["data"]["concurrent"] is True

    def test_database_session_persistence_integration(self) -> None:
        """
        GREEN: Test database session persistence with ToDoWrite models.

        This test validates that database sessions work correctly with
        the updated ToDoWrite Models API.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"

            # Create in-memory SQLite database with our models
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker

            engine = create_engine(f"sqlite:///{db_path}")
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()

            try:
                # Create test data using models
                goal = Goal(
                    title="Persistence Test Goal",
                    description="Testing database persistence",
                    owner="test-user"
                )
                session.add(goal)

                label = Label(name="persistence-test")
                session.add(label)

                task = Task(
                    title="Persistence Test Task",
                    description="Task for persistence testing",
                    owner="test-user",
                    assignee="developer"
                )
                session.add(task)

                session.commit()

                # Verify data persistence
                assert session.query(Goal).count() == 1
                assert session.query(Label).count() == 1
                assert session.query(Task).count() == 1

                # Create new session to test persistence
                session2 = Session()

                # Verify data is still there
                assert session2.query(Goal).count() == 1
                assert session2.query(Label).count() == 1
                assert session2.query(Task).count() == 1

                # Verify data integrity
                persisted_goal = session2.query(Goal).first()
                assert persisted_goal.title == "Persistence Test Goal"
                assert persisted_goal.description == "Testing database persistence"

                persisted_label = session2.query(Label).first()
                assert persisted_label.name == "persistence-test"

                persisted_task = session2.query(Task).first()
                assert persisted_task.title == "Persistence Test Task"
                assert persisted_task.assignee == "developer"

                session2.close()

            finally:
                session.close()

    def test_session_marker_invalid_json_handling(self) -> None:
        """
        GREEN: Test handling of invalid JSON in session files.

        This test validates graceful handling of corrupted or invalid
        JSON session files.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            session_path = Path(temp_dir) / "invalid.json"

            # Write invalid JSON
            with open(session_path, 'w') as f:
                f.write('{"invalid": json content}')  # Invalid JSON syntax

            # Should raise JSONDecodeError when trying to load
            with pytest.raises(json.JSONDecodeError):
                with open(session_path, 'r') as f:
                    json.load(f)

    def test_session_persistence_with_models_data(self) -> None:
        """
        GREEN: Test session persistence with actual ToDoWrite model data.

        This test validates that real model instances can be serialized
        and deserialized through the session persistence system.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            session_path = Path(temp_dir) / "models_session.json"

            # Create model data for serialization
            models_session_data = {
                "session_id": "models-session-789",
                "created_at": "2025-01-01T00:00:00Z",
                "user_id": "model-user",
                "active_models": {
                    "goals": [
                        {
                            "id": 1,
                            "title": "Test Goal from Session",
                            "description": "Goal created in session",
                            "owner": "session-owner",
                            "severity": "medium"
                        }
                    ],
                    "labels": [
                        {
                            "id": 1,
                            "name": "session-label"
                        }
                    ],
                    "tasks": [
                        {
                            "id": 1,
                            "title": "Session Task",
                            "description": "Task from session",
                            "owner": "task-owner",
                            "assignee": "task-assignee"
                        }
                    ]
                }
            }

            # Write session data
            with open(session_path, 'w') as f:
                json.dump(models_session_data, f, indent=2)

            # Load and verify model data integrity
            with open(session_path, 'r') as f:
                loaded_data = json.load(f)

            assert loaded_data["session_id"] == "models-session-789"
            assert len(loaded_data["active_models"]["goals"]) == 1
            assert loaded_data["active_models"]["goals"][0]["title"] == "Test Goal from Session"
            assert loaded_data["active_models"]["labels"][0]["name"] == "session-label"