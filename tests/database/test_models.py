"""
Database Models Tests

Tests for database models, relationships, and operations.
"""

import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todowrite.database.models import Artifact, Command, Label, Link, Node, node_labels


class TestDatabaseModels(unittest.TestCase):
    """Test database models and operations."""

    def setUp(self) -> None:
        """Set up test database."""
        self.test_db = Path("test_models.db")
        self.engine = create_engine(f"sqlite:///{self.test_db}")
        self.Session = sessionmaker(bind=self.engine)

        # Create tables
        from todowrite.database.models import Base

        Base.metadata.create_all(self.engine)

    def tearDown(self) -> None:
        """Clean up test database."""
        self.test_db.unlink(missing_ok=True)

    def test_node_model_creation(self) -> None:
        """Test Node model creation and basic properties."""
        with self.Session() as session:
            node = Node(
                id="GOAL-001",
                layer="Goal",
                title="Test Goal",
                description="Test goal description",
                status="planned",
                progress=0,
                owner="test-user",
                severity="med",
                work_type="architecture",
            )
            session.add(node)
            session.commit()

            # Verify node was created
            result = session.query(Node).filter(Node.id == "GOAL-001").first()
            self.assertIsNotNone(result)
            self.assertEqual(result.title, "Test Goal")
            self.assertEqual(result.layer, "Goal")
            self.assertEqual(result.status, "planned")

    def test_node_relationships(self) -> None:
        """Test node relationships with labels and links."""
        with self.Session() as session:
            # Create parent node
            parent = Node(
                id="GOAL-001",
                layer="Goal",
                title="Parent Goal",
                description="Parent goal",
            )
            session.add(parent)

            # Create child node
            child = Node(
                id="TSK-001",
                layer="Task",
                title="Child Task",
                description="Child task",
            )
            session.add(child)

            # Create link
            link = Link(parent_id="GOAL-001", child_id="TSK-001")
            session.add(link)

            # Create label
            label = Label(label="urgent")
            session.add(label)

            # Add label to child node
            child.labels.append(label)

            session.commit()

            # Verify relationships
            result = session.query(Node).filter(Node.id == "TSK-001").first()
            self.assertEqual(len(result.labels), 1)
            self.assertEqual(result.labels[0].label, "urgent")

            # Verify link
            link_result = (
                session.query(Link)
                .filter(Link.parent_id == "GOAL-001", Link.child_id == "TSK-001")
                .first()
            )
            self.assertIsNotNone(link_result)

    def test_command_model(self) -> None:
        """Test Command and Artifact models."""
        with self.Session() as session:
            # Create node with command
            node = Node(
                id="CMD-001",
                layer="Command",
                title="Test Command",
                description="Test command description",
            )
            session.add(node)

            # Create command
            import json

            command = Command(
                node_id="CMD-001",
                ac_ref="AC-001",
                run=json.dumps(
                    {"shell": "echo hello", "workdir": "/tmp", "env": {"DEBUG": "true"}}
                ),
            )
            session.add(command)

            # Create artifacts
            artifact1 = Artifact(command_id="CMD-001", artifact="output.txt")
            artifact2 = Artifact(command_id="CMD-001", artifact="log.txt")
            session.add(artifact1)
            session.add(artifact2)

            session.commit()

            # Verify command
            result = session.query(Command).filter(Command.node_id == "CMD-001").first()
            self.assertIsNotNone(result)
            self.assertEqual(result.ac_ref, "AC-001")

            # Verify artifacts
            artifacts = session.query(Artifact).filter(Artifact.command_id == "CMD-001").all()
            self.assertEqual(len(artifacts), 2)

    def test_node_labels_association(self) -> None:
        """Test many-to-many relationship between nodes and labels."""
        with self.Session() as session:
            # Create labels
            label1 = Label(label="urgent")
            label2 = Label(label="critical")
            session.add(label1)
            session.add(label2)

            # Create node with multiple labels
            node = Node(
                id="TSK-001",
                layer="Task",
                title="Task with Labels",
                description="Task description",
            )
            node.labels.extend([label1, label2])
            session.add(node)

            session.commit()

            # Verify association
            result = session.query(Node).filter(Node.id == "TSK-001").first()
            self.assertEqual(len(result.labels), 2)
            label_names = [label.label for label in result.labels]
            self.assertIn("urgent", label_names)
            self.assertIn("critical", label_names)

    def test_node_labels_table(self) -> None:
        """Test the association table between nodes and labels."""
        with self.Session() as session:
            # Create node and label
            node = Node(id="TSK-001", layer="Task", title="Test Task")
            label = Label(label="test-label")

            node.labels.append(label)
            session.add(node)
            session.add(label)

            session.commit()

            # Check association table
            result = (
                session.query(node_labels)
                .filter(
                    node_labels.c.node_id == "TSK-001",
                    node_labels.c.label == label.label,
                )
                .first()
            )
            self.assertIsNotNone(result)

    def test_cascade_delete(self) -> None:
        """Test cascade deletion of related records."""
        with self.Session() as session:
            # Create node with relationships
            node = Node(id="TSK-001", layer="Task", title="Test Task")
            label = Label(label="test")
            link = Link(parent_id="GOAL-001", child_id="TSK-001")

            node.labels.append(label)
            session.add(node)
            session.add(link)

            session.commit()

            # Delete node
            session.delete(node)
            session.commit()

            # Verify related records are deleted
            self.assertIsNone(session.query(Node).filter(Node.id == "TSK-001").first())
            # Link should still exist (we might want to handle this differently)


class TestDatabaseIntegration(unittest.TestCase):
    """Integration tests for database operations."""

    def setUp(self) -> None:
        """Set up test database."""
        self.test_db = Path("test_integration.db")
        self.engine = create_engine(f"sqlite:///{self.test_db}")
        self.Session = sessionmaker(bind=self.engine)

        # Create tables
        from todowrite.database.models import Base

        Base.metadata.create_all(self.engine)

    def tearDown(self) -> None:
        """Clean up test database."""
        self.test_db.unlink(missing_ok=True)

    def test_complex_hierarchy(self) -> None:
        """Test creating a complex node hierarchy."""
        with self.Session() as session:
            # Create goal
            goal = Node(
                id="GOAL-001",
                layer="Goal",
                title="Main Goal",
                description="Main project goal",
            )
            session.add(goal)

            # Create concepts
            concept1 = Node(
                id="CON-001",
                layer="Concept",
                title="Concept 1",
                description="First concept",
            )
            concept2 = Node(
                id="CON-002",
                layer="Concept",
                title="Concept 2",
                description="Second concept",
            )
            session.add(concept1)
            session.add(concept2)

            # Create tasks
            task1 = Node(
                id="TSK-001",
                layer="Task",
                title="Task 1",
                description="First task",
                owner="user1",
            )
            task2 = Node(
                id="TSK-002",
                layer="Task",
                title="Task 2",
                description="Second task",
                owner="user2",
            )
            session.add(task1)
            session.add(task2)

            # Create links
            goal_link1 = Link(parent_id="GOAL-001", child_id="CON-001")
            goal_link2 = Link(parent_id="GOAL-001", child_id="CON-002")
            goal_link3 = Link(parent_id="GOAL-001", child_id="TSK-001")
            goal_link4 = Link(parent_id="GOAL-001", child_id="TSK-002")

            session.add_all([goal_link1, goal_link2, goal_link3, goal_link4])

            session.commit()

            # Verify hierarchy
            goal_result = session.query(Node).filter(Node.id == "GOAL-001").first()
            self.assertEqual(len(goal_result.children), 4)  # 2 concepts + 2 tasks

    def test_command_artifacts_integration(self) -> None:
        """Test command and artifact integration."""
        with self.Session() as session:
            # Create command node
            command_node = Node(
                id="CMD-001",
                layer="Command",
                title="Build Command",
                description="Build the project",
            )
            session.add(command_node)

            # Create command with artifacts
            import json

            command = Command(
                node_id="CMD-001",
                ac_ref="AC-001",
                run=json.dumps(
                    {
                        "shell": "make build",
                        "workdir": "/project",
                        "env": {"TARGET": "production"},
                    }
                ),
            )

            artifacts = [
                Artifact(command_id="CMD-001", artifact="build.log"),
                Artifact(command_id="CMD-001", artifact="dist/"),
                Artifact(command_id="CMD-001", artifact="reports/"),
            ]

            session.add(command)
            session.add_all(artifacts)
            session.commit()

            # Verify command with artifacts
            result = session.query(Command).filter(Command.node_id == "CMD-001").first()
            self.assertIsNotNone(result)

            db_artifacts = session.query(Artifact).filter(Artifact.command_id == "CMD-001").all()
            self.assertEqual(len(db_artifacts), 3)


if __name__ == "__main__":
    unittest.main()
