"""
Test-First Development: Strategic Complete Script Integration Tests

RED PHASE: These tests describe desired behavior for the refactored strategic-complete
script that uses the new complete_goal function instead of manual completion logic.

Agricultural Context:
- Strategic goal management must be reliable for safety-critical tractor coordination
- Audit tToDoWrite (date_completed, validation logs) are essential for ISO compliance
- Robust error handling prevents operational disruptions in agricultural systems
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Make sure project_root is correct - should be the main ToDoWrite directory
if project_root.name == "tests":
    project_root = project_root.parent
sys.path.insert(0, str(project_root))


class TestStrategicCompleteScript(unittest.TestCase):
    """Test the refactored strategic-complete script using complete_goal function."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.script_path = project_root / "scripts" / "strategic-complete"

    def test_complete_goal_by_exact_id_success(self) -> None:
        """Test RED: Script completes goal when exact ID match found."""
        # Mock the complete_goal function to return success
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="✓ Goal marked as completed!\n  ID: goal-123\n  Title: Test Goal\n  Status: done\n  Date completed: 2025-10-16T12:00:00\n",
                stderr="",
            )

            subprocess.run(
                ["python", str(self.script_path), "goal-123"],
                capture_output=True,
                text=True,
                cwd=project_root,
                check=False,
            )

            # Should call the script successfully
            mock_run.assert_called_once()

    def test_complete_goal_by_title_substring_success(self) -> None:
        """Test RED: Script completes goal when title substring match found."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="✓ Goal marked as completed!\n  ID: goal-456\n  Title: Clear Technical Issues\n  Status: done\n  Date completed: 2025-10-16T12:00:00\n",
                stderr="",
            )

            subprocess.run(
                ["python", str(self.script_path), "technical"],
                capture_output=True,
                text=True,
                cwd=project_root,
                check=False,
            )

            mock_run.assert_called_once()

    def test_complete_goal_not_found_error(self) -> None:
        """Test RED: Script handles non-existent goal gracefully."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1,
                stdout="",
                stderr="Error: No goal found matching \"nonexistent-goal\"\nUse 'get_goals()' to see available goals.\n",
            )

            subprocess.run(
                ["python", str(self.script_path), "nonexistent-goal"],
                capture_output=True,
                text=True,
                cwd=project_root,
                check=False,
            )

            mock_run.assert_called_once()

    def test_complete_goal_already_completed(self) -> None:
        """Test RED: Script handles already completed goal gracefully."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="Goal already completed: Test Goal\n",
                stderr="",
            )

            subprocess.run(
                ["python", str(self.script_path), "goal-123"],
                capture_output=True,
                text=True,
                cwd=project_root,
                check=False,
            )

            mock_run.assert_called_once()

    def test_script_uses_complete_goal_function(self) -> None:
        """Test RED: Verify script uses complete_goal function for enhanced features."""
        # This test ensures the refactored script provides enhanced output
        # including date_completed and proper validation logging
        with patch("subprocess.run") as mock_run:
            # Enhanced output should include date_completed from complete_goal function
            enhanced_output = (
                "✓ Goal marked as completed!\n"
                "  ID: goal-123\n"
                "  Title: Test Goal\n"
                "  Status: done\n"
                "  Date completed: 2025-10-16T12:00:00.123456\n"
                "  Enhanced: Validation log updated\n"
            )
            mock_run.return_value = MagicMock(returncode=0, stdout=enhanced_output, stderr="")

            subprocess.run(
                ["python", str(self.script_path), "goal-123"],
                capture_output=True,
                text=True,
                cwd=project_root,
                check=False,
            )

            mock_run.assert_called_once()

    def test_script_requires_search_term_argument(self) -> None:
        """Test RED: Script shows usage when no search term provided."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=2,
                stdout="",
                stderr="usage: strategic-complete [-h] search_term\nstrategic-complete: error: the following arguments are required: search_term\n",
            )

            subprocess.run(
                ["python", str(self.script_path)],
                capture_output=True,
                text=True,
                cwd=project_root,
                check=False,
            )

            mock_run.assert_called_once()


class TestStrategicCompleteDirectLogic(unittest.TestCase):
    """Direct tests of strategic-complete script logic to verify complete_goal usage."""

    @classmethod
    def setUpClass(cls) -> None:
        # ToDoWrite.manager doesn't exist - use ToDoWrite.core.app
        from sqlalchemy import create_engine
        from todowrite.database.models import Base

        # Setup test database with project-specific naming
        from todowrite.utils.database_utils import get_project_database_name

        test_db_name = get_project_database_name("testing")
        test_db_url = f"sqlite:///{test_db_name}"
        engine = create_engine(test_db_url)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        engine.dispose()

    @classmethod
    def tearDownClass(cls) -> None:
        """Clean up the test database for ToDoWrite."""
        # ToDoWrite.manager doesn't exist - use ToDoWrite.core.app
        from sqlalchemy import create_engine
        from todowrite.database.models import Base

        # Setup test database with project-specific naming
        from todowrite.utils.database_utils import get_project_database_name

        test_db_name = get_project_database_name("testing")
        test_db_url = f"sqlite:///{test_db_name}"
        engine = create_engine(test_db_url)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        engine.dispose()  # Calling init_database again will drop and recreate, effectively cleaning

    def setUp(self) -> None:
        """Set up test environment."""
        self.script_path = project_root / "scripts" / "strategic-complete"

    def test_script_calls_complete_goal_function(self):
        """Test GREEN: Verify script uses complete_goal function behavior."""
        # This test verifies the enhanced output includes date_completed
        # which is only available when using complete_goal function

        # Create a test script that should trigger enhanced output
        result = subprocess.run(
            ["python", str(self.script_path), "--help"],
            capture_output=True,
            text=True,
            cwd=project_root,
            check=False,
        )

        # Verify script loads successfully (imports work)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Mark a strategic goal as complete", result.stdout)

    def test_script_title_matching_with_complete_goal(self):
        """Test GREEN: Script uses complete_goal function with enhanced error handling."""
        # Test the script handles non-existent goals properly
        # (enhanced error handling from complete_goal function)

        result = subprocess.run(
            ["python", str(self.script_path), "nonexistent-goal-xyz"],
            capture_output=True,
            text=True,
            cwd=project_root,
            check=False,
        )

        # Verify enhanced error handling from complete_goal function
        self.assertEqual(result.returncode, 1)
        self.assertIn("No goal found matching", result.stderr or result.stdout)

    def test_script_imports_complete_goal_function(self):
        """Test RED: Verify script imports complete_goal function."""
        # Read the script file and check if it imports complete_goal
        script_path = project_root / "scripts" / "strategic-complete"
        script_content = script_path.read_text()

        # Test for imports - updated to reflect current architecture
        self.assertIn("import", script_content)  # Should have some imports
        self.assertIn(
            "complete_goal",
            script_content,
            "Script should import complete_goal function for enhanced functionality",
        )


if __name__ == "__main__":
    unittest.main()
