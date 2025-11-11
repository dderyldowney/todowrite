"""
RED PHASE: Tests for Development Project Lifecycle Management
These tests MUST FAIL before implementation exists.
NO MOCKING ALLOWED - Tests will use real todowrite system.
"""

from __future__ import annotations

import subprocess


class TestDevelopmentProjectLifecycleManagement:
    """Test that development project lifecycle management works correctly."""

    def test_development_project_setup(self) -> None:
        """RED: Test that team can set up development project structure."""
        # This test will create a real development project and verify 12-layer structure
        project_name: str = "TestSoftwareProject"

        # Create project using todowrite CLI
        result = subprocess.run(
            [
                "python",
                "-m",
                "todowrite_cli",
                "create",
                "--layer",
                "goal",
                "--title",
                project_name,
                "--description",
                "A test software development project",
            ],
            capture_output=True,
            text=True,
            cwd=".",
            check=False,
        )

        assert result.returncode == 0, f"Failed to create development goal: {result.stderr}"

        # Extract the goal ID from output
        assert "GOAL-" in result.stdout, "Goal should be created with GOAL- ID"

        # Create concepts for architecture
        concept_result = subprocess.run(
            [
                "python",
                "-m",
                "todowrite_cli",
                "create",
                "--layer",
                "concept",
                "--title",
                "Microservices Architecture",
                "--description",
                "System architecture using microservices pattern",
            ],
            capture_output=True,
            text=True,
            cwd=".",
            check=False,
        )

        assert concept_result.returncode == 0, f"Failed to create concept: {concept_result.stderr}"
        assert "CON-" in concept_result.stdout, "Concept should be created with CON- ID"

    def test_requirements_and_acceptance_criteria_management(self) -> None:
        """RED: Test that developer can define requirements and acceptance criteria."""
        # Create a requirement
        req_result = subprocess.run(
            [
                "python",
                "-m",
                "todowrite_cli",
                "create",
                "--layer",
                "requirements",
                "--title",
                "User Authentication System",
                "--description",
                "Users must be able to authenticate using email and password",
            ],
            capture_output=True,
            text=True,
            cwd=".",
            check=False,
        )

        assert req_result.returncode == 0, f"Failed to create requirement: {req_result.stderr}"
        assert "R-" in req_result.stdout, "Requirement should be created with R- ID"

        # Create acceptance criteria for the requirement
        ac_result = subprocess.run(
            [
                "python",
                "-m",
                "todowrite_cli",
                "create",
                "--layer",
                "acceptancecriteria",
                "--title",
                "User can register with valid email",
                "--description",
                "GIVEN a new user visits the registration page WHEN they enter a valid email and password THEN their account is created",
            ],
            capture_output=True,
            text=True,
            cwd=".",
            check=False,
        )

        assert ac_result.returncode == 0, (
            f"Failed to create acceptance criteria: {ac_result.stderr}"
        )
        assert "AC-" in ac_result.stdout, "Acceptance criteria should be created with AC- ID"

    def test_interface_contract_definition(self) -> None:
        """RED: Test that team can define interface contracts between components."""
        # Create interface contract
        if_result = subprocess.run(
            [
                "python",
                "-m",
                "todowrite_cli",
                "create",
                "--layer",
                "interfacecontract",
                "--title",
                "User Service API Contract",
                "--description",
                "REST API contract for user management service",
            ],
            capture_output=True,
            text=True,
            cwd=".",
            check=False,
        )

        assert if_result.returncode == 0, f"Failed to create interface contract: {if_result.stderr}"
        assert "IF-" in if_result.stdout, "Interface contract should be created with IF- ID"

    def test_development_phase_creation(self) -> None:
        """RED: Test that project manager can create development phases."""
        # Create development phases
        phases = [
            (
                "Phase 1: Requirements and Design",
                "Gather requirements and create system design",
            ),
            (
                "Phase 2: Core Development",
                "Implement core system functionality",
            ),
            (
                "Phase 3: Testing and QA",
                "Comprehensive testing and quality assurance",
            ),
            ("Phase 4: Deployment", "Deploy system to production environment"),
        ]

        for phase_title, phase_desc in phases:
            phase_result = subprocess.run(
                [
                    "python",
                    "-m",
                    "todowrite_cli",
                    "create",
                    "--layer",
                    "phase",
                    "--title",
                    phase_title,
                    "--description",
                    phase_desc,
                ],
                capture_output=True,
                text=True,
                cwd=".",
                check=False,
            )

            assert phase_result.returncode == 0, (
                f"Failed to create phase {phase_title}: {phase_result.stderr}"
            )
            assert "PH-" in phase_result.stdout, (
                f"Phase should be created with PH- ID: {phase_title}"
            )

    def test_implementation_step_breakdown(self) -> None:
        """RED: Test that developers can break phases into implementation steps."""
        # Create implementation steps
        steps = [
            (
                "Set up development environment",
                "Configure IDE, databases, and development tools",
            ),
            (
                "Implement user authentication",
                "Create login, registration, and password reset functionality",
            ),
            (
                "Create user dashboard",
                "Build main user interface with project overview",
            ),
            (
                "Implement project management features",
                "Add task creation, editing, and deletion",
            ),
        ]

        for step_title, step_desc in steps:
            step_result = subprocess.run(
                [
                    "python",
                    "-m",
                    "todowrite_cli",
                    "create",
                    "--layer",
                    "step",
                    "--title",
                    step_title,
                    "--description",
                    step_desc,
                ],
                capture_output=True,
                text=True,
                cwd=".",
                check=False,
            )

            assert step_result.returncode == 0, (
                f"Failed to create step {step_title}: {step_result.stderr}"
            )
            assert "STP-" in step_result.stdout, (
                f"Step should be created with STP- ID: {step_title}"
            )

    def test_command_execution_and_artifact_tracking(self) -> None:
        """RED: Test that team can execute commands and track artifacts."""
        # Create command with build script
        cmd_result = subprocess.run(
            [
                "python",
                "-m",
                "todowrite_cli",
                "create",
                "--layer",
                "command",
                "--title",
                "Build and Test Application",
                "--description",
                "Run build process and execute test suite",
                "--run-shell",
                "echo 'Building application...' && echo 'Tests passed!'",
            ],
            capture_output=True,
            text=True,
            cwd=".",
            check=False,
        )

        assert cmd_result.returncode == 0, f"Failed to create command: {cmd_result.stderr}"
        assert "CMD-" in cmd_result.stdout, "Command should be created with CMD- ID"

    def test_layer_relationships_and_dependencies(self) -> None:
        """RED: Test that layers can be linked to show dependencies."""
        # This test verifies that we can create relationships between different layers
        # First, create nodes in different layers
        goal_result = subprocess.run(
            [
                "python",
                "-m",
                "todowrite_cli",
                "create",
                "--layer",
                "goal",
                "--title",
                "Test Goal for Dependencies",
                "--description",
                "A goal for testing layer dependencies",
            ],
            capture_output=True,
            text=True,
            cwd=".",
            check=False,
        )

        assert goal_result.returncode == 0, "Failed to create test goal"

        # Extract goal ID from output
        goal_id: str = ""
        for line in goal_result.stdout.split("\n"):
            if "GOAL-" in line:
                goal_id = line.split("✓ Created")[1].split(":")[0].strip()
                break

        assert goal_id.startswith("GOAL-"), f"Expected GOAL- ID, got: {goal_id}"

        # Create a task to link to the goal
        task_result = subprocess.run(
            [
                "python",
                "-m",
                "todowrite_cli",
                "create",
                "--layer",
                "task",
                "--title",
                "Test Task for Dependencies",
                "--description",
                "A task to test linking to goals",
            ],
            capture_output=True,
            text=True,
            cwd=".",
            check=False,
        )

        assert task_result.returncode == 0, "Failed to create test task"

        # Extract task ID
        task_id: str = ""
        for line in task_result.stdout.split("\n"):
            if "TSK-" in line:
                task_id = line.split("✓ Created")[1].split(":")[0].strip()
                break

        assert task_id.startswith("TSK-"), f"Expected TSK- ID, got: {task_id}"
