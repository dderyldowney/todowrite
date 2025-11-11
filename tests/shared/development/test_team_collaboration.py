"""
RED PHASE: Tests for Team Collaboration in Development
These tests MUST FAIL before implementation exists.
NO MOCKING ALLOWED - Tests will use real todowrite system.
"""

from __future__ import annotations

import subprocess


class TestTeamCollaborationInDevelopment:
    """Test that team collaboration features work correctly."""

    def test_team_status_update_sharing(self) -> None:
        """RED: Test that team members can share status updates."""
        # Create multiple tasks representing team members' work
        team_tasks: list[dict[str, str]] = [
            {
                "title": "Implement User Authentication",
                "assignee": "Alice",
                "status": "in_progress",
            },
            {
                "title": "Design Database Schema",
                "assignee": "Bob",
                "status": "completed",
            },
            {
                "title": "Create API Endpoints",
                "assignee": "Charlie",
                "status": "planned",
            },
            {
                "title": "Write Unit Tests",
                "assignee": "Alice",
                "status": "planned",
            },
            {
                "title": "Setup CI/CD Pipeline",
                "assignee": "David",
                "status": "in_progress",
            },
        ]

        created_task_ids: list[str] = []

        for task in team_tasks:
            # Create task with assignee
            task_result = subprocess.run(
                [
                    "python",
                    "-m",
                    "todowrite_cli",
                    "create",
                    "--layer",
                    "task",
                    "--title",
                    task["title"],
                    "--description",
                    f"Task assigned to {task['assignee']}",
                    "--owner",
                    task["assignee"],
                ],
                capture_output=True,
                text=True,
                cwd=".",
                check=False,
            )

            assert task_result.returncode == 0, (
                f"Failed to create task {task['title']}: {task_result.stderr}"
            )
            assert "TSK-" in task_result.stdout, (
                f"Task {task['title']} should be created with TSK- ID"
            )

            # Extract task ID
            task_id: str = ""
            for line in task_result.stdout.split("\n"):
                if "TSK-" in line:
                    task_id = line.split("✓ Created")[1].split(":")[0].strip()
                    break

            assert task_id.startswith("TSK-"), f"Expected TSK- ID, got: {task_id}"
            created_task_ids.append(task_id)

            # Update task status if not the default
            if task["status"] != "planned":
                status_result = subprocess.run(
                    [
                        "python",
                        "-m",
                        "todowrite_cli",
                        "update",
                        task_id,
                        "--status",
                        task["status"],
                    ],
                    capture_output=True,
                    text=True,
                    cwd=".",
                    check=False,
                )

                assert status_result.returncode == 0, (
                    f"Failed to update task status: {status_result.stderr}"
                )

        # Verify we can see all team members' work
        list_result = subprocess.run(
            ["python", "-m", "todowrite_cli", "list"],
            capture_output=True,
            text=True,
            cwd=".",
            check=False,
        )

        assert list_result.returncode == 0, "Failed to list tasks"
        for task in team_tasks:
            assert task["assignee"] in list_result.stdout, (
                f"Should see {task['assignee']}'s work in list"
            )
            assert task["title"] in list_result.stdout, f"Should see task '{task['title']}' in list"

    def test_code_review_coordination(self) -> None:
        """RED: Test that team can coordinate code reviews."""
        # Create a task for code review
        review_task_result = subprocess.run(
            [
                "python",
                "-m",
                "todowrite_cli",
                "create",
                "--layer",
                "task",
                "--title",
                "Code Review: User Authentication Module",
                "--description",
                "Review authentication implementation for security and best practices",
                "--owner",
                "Bob",
            ],
            capture_output=True,
            text=True,
            cwd=".",
            check=False,
        )

        assert review_task_result.returncode == 0, "Failed to create code review task"
        assert "TSK-" in review_task_result.stdout, (
            "Code review task should be created with TSK- ID"
        )

        # Extract review task ID
        review_task_id: str = ""
        for line in review_task_result.stdout.split("\n"):
            if "TSK-" in line:
                review_task_id = line.split("✓ Created")[1].split(":")[0].strip()
                break

        # Create subtasks for review process
        review_subtasks: list[dict[str, str]] = [
            {"title": "Review authentication logic", "reviewer": "Charlie"},
            {"title": "Check security implementations", "reviewer": "David"},
            {"title": "Verify test coverage", "reviewer": "Alice"},
            {"title": "Documentation review", "reviewer": "Bob"},
        ]

        for subtask in review_subtasks:
            subtask_result = subprocess.run(
                [
                    "python",
                    "-m",
                    "todowrite_cli",
                    "create",
                    "--layer",
                    "subtask",
                    "--title",
                    subtask["title"],
                    "--description",
                    f"Review task assigned to {subtask['reviewer']}",
                    "--owner",
                    subtask["reviewer"],
                ],
                capture_output=True,
                text=True,
                cwd=".",
                check=False,
            )

            assert subtask_result.returncode == 0, f"Failed to create subtask {subtask['title']}"
            assert "SUB-" in subtask_result.stdout, (
                f"Subtask {subtask['title']} should be created with SUB- ID"
            )

    def test_technical_debt_management(self) -> None:
        """RED: Test that team can manage technical debt and refactoring."""
        # Create technical debt tasks
        technical_debt_tasks: list[dict[str, str]] = [
            {
                "title": "Refactor Legacy Authentication Module",
                "description": "Rewrite old authentication code to use modern patterns",
                "priority": "high",
                "impact": "security",
            },
            {
                "title": "Update Outdated Dependencies",
                "description": "Update all npm packages to latest stable versions",
                "priority": "medium",
                "impact": "maintenance",
            },
            {
                "title": "Improve Database Query Performance",
                "description": "Optimize slow database queries identified in performance testing",
                "priority": "high",
                "impact": "performance",
            },
            {
                "title": "Add Missing Unit Tests",
                "description": "Increase test coverage from 75% to 90% for critical modules",
                "priority": "medium",
                "impact": "quality",
            },
        ]

        for task in technical_debt_tasks:
            # Create technical debt task with severity
            task_result = subprocess.run(
                [
                    "python",
                    "-m",
                    "todowrite_cli",
                    "create",
                    "--layer",
                    "task",
                    "--title",
                    task["title"],
                    "--description",
                    task["description"],
                    "--severity",
                    task["priority"],
                ],
                capture_output=True,
                text=True,
                cwd=".",
                check=False,
            )

            assert task_result.returncode == 0, (
                f"Failed to create technical debt task {task['title']}"
            )
            assert "TSK-" in task_result.stdout, (
                f"Technical debt task {task['title']} should be created with TSK- ID"
            )

    def test_knowledge_sharing_coordination(self) -> None:
        """RED: Test that team can coordinate knowledge sharing."""
        # Create knowledge sharing tasks
        knowledge_tasks: list[dict[str, str]] = [
            {
                "title": "Document Microservices Architecture",
                "description": "Create comprehensive documentation for our microservices design patterns",
                "knowledge_type": "architecture",
            },
            {
                "title": "Create Database Schema Guide",
                "description": "Document database design decisions and query patterns",
                "knowledge_type": "database",
            },
            {
                "title": "Write Deployment Playbook",
                "description": "Create step-by-step deployment instructions for new team members",
                "knowledge_type": "deployment",
            },
            {
                "title": "Onboarding Materials for New Developers",
                "description": "Prepare documentation and setup guides for new team members",
                "knowledge_type": "onboarding",
            },
        ]

        for task in knowledge_tasks:
            # Create knowledge sharing task
            task_result = subprocess.run(
                [
                    "python",
                    "-m",
                    "todowrite_cli",
                    "create",
                    "--layer",
                    "task",
                    "--title",
                    task["title"],
                    "--description",
                    task["description"],
                    "--labels",
                    f"knowledge-sharing,{task['knowledge_type']}",
                ],
                capture_output=True,
                text=True,
                cwd=".",
                check=False,
            )

            assert task_result.returncode == 0, f"Failed to create knowledge task {task['title']}"
            assert "TSK-" in task_result.stdout, (
                f"Knowledge task {task['title']} should be created with TSK- ID"
            )

    def test_release_coordination(self) -> None:
        """RED: Test that team can coordinate releases."""
        # Create release phase
        release_phase_result = subprocess.run(
            [
                "python",
                "-m",
                "todowrite_cli",
                "create",
                "--layer",
                "phase",
                "--title",
                "Release v2.0.0 Preparation",
                "--description",
                "Coordinate all activities for v2.0.0 release",
            ],
            capture_output=True,
            text=True,
            cwd=".",
            check=False,
        )

        assert release_phase_result.returncode == 0, "Failed to create release phase"
        assert "PH-" in release_phase_result.stdout, "Release phase should be created with PH- ID"

        # Extract phase ID
        phase_id: str = ""
        for line in release_phase_result.stdout.split("\n"):
            if "PH-" in line:
                phase_id = line.split("✓ Created")[1].split(":")[0].strip()
                break

        # Create release coordination tasks
        release_tasks: list[dict[str, str]] = [
            {
                "title": "Final Testing and QA",
                "description": "Complete all testing before release",
            },
            {
                "title": "Update Documentation",
                "description": "Update all documentation for new features",
            },
            {
                "title": "Prepare Release Notes",
                "description": "Write comprehensive release notes",
            },
            {
                "title": "Coordinate Marketing",
                "description": "Work with marketing team on release announcement",
            },
            {
                "title": "Deployment Preparation",
                "description": "Prepare deployment scripts and procedures",
            },
            {
                "title": "Post-Release Monitoring",
                "description": "Set up monitoring for post-release health",
            },
        ]

        for task in release_tasks:
            task_result = subprocess.run(
                [
                    "python",
                    "-m",
                    "todowrite_cli",
                    "create",
                    "--layer",
                    "task",
                    "--title",
                    task["title"],
                    "--description",
                    task["description"],
                ],
                capture_output=True,
                text=True,
                cwd=".",
                check=False,
            )

            assert task_result.returncode == 0, f"Failed to create release task {task['title']}"
            assert "TSK-" in task_result.stdout, (
                f"Release task {task['title']} should be created with TSK- ID"
            )

    def test_incident_response_management(self) -> None:
        """RED: Test that team can handle incident response."""
        # Create incident response task
        incident_task_result = subprocess.run(
            [
                "python",
                "-m",
                "todowrite_cli",
                "create",
                "--layer",
                "task",
                "--title",
                "CRITICAL: Production Database Connection Issues",
                "--description",
                "Users are experiencing database connection failures. Investigate and resolve immediately.",
                "--severity",
                "critical",
            ],
            capture_output=True,
            text=True,
            cwd=".",
            check=False,
        )

        assert incident_task_result.returncode == 0, "Failed to create incident response task"
        assert "TSK-" in incident_task_result.stdout, "Incident task should be created with TSK- ID"

        # Extract incident task ID
        incident_id: str = ""
        for line in incident_task_result.stdout.split("\n"):
            if "TSK-" in line:
                incident_id = line.split("✓ Created")[1].split(":")[0].strip()
                break

        # Create incident response subtasks
        incident_subtasks: list[dict[str, str]] = [
            {
                "title": "Assess Impact and Scope",
                "assignee": "On-call Engineer",
            },
            {"title": "Identify Root Cause", "assignee": "Senior Developer"},
            {"title": "Implement Temporary Fix", "assignee": "Lead Developer"},
            {
                "title": "Communicate with Stakeholders",
                "assignee": "Team Lead",
            },
            {
                "title": "Deploy Permanent Solution",
                "assignee": "Senior Developer",
            },
            {"title": "Conduct Post-Incident Review", "assignee": "Team Lead"},
        ]

        for subtask in incident_subtasks:
            subtask_result = subprocess.run(
                [
                    "python",
                    "-m",
                    "todowrite_cli",
                    "create",
                    "--layer",
                    "subtask",
                    "--title",
                    subtask["title"],
                    "--description",
                    f"Incident response task: {subtask['title']}",
                    "--owner",
                    subtask["assignee"],
                ],
                capture_output=True,
                text=True,
                cwd=".",
                check=False,
            )

            assert subtask_result.returncode == 0, (
                f"Failed to create incident subtask {subtask['title']}"
            )
            assert "SUB-" in subtask_result.stdout, (
                f"Incident subtask {subtask['title']} should be created with SUB- ID"
            )

    def test_team_workload_visibility(self) -> None:
        """RED: Test that team can see workload distribution."""
        # Create tasks with different assignees to test workload visibility
        team_members: list[str] = ["Alice", "Bob", "Charlie", "David", "Eve"]

        for member in team_members:
            # Give each team member a different number of tasks
            task_count: int = team_members.index(member) + 2

            for i in range(task_count):
                task_result = subprocess.run(
                    [
                        "python",
                        "-m",
                        "todowrite_cli",
                        "create",
                        "--layer",
                        "task",
                        "--title",
                        f"Task for {member} #{i + 1}",
                        "--description",
                        f"Work item assigned to {member}",
                        "--owner",
                        member,
                    ],
                    capture_output=True,
                    text=True,
                    cwd=".",
                    check=False,
                )

                assert task_result.returncode == 0, f"Failed to create task for {member}"
                assert "TSK-" in task_result.stdout, (
                    f"Task for {member} should be created with TSK- ID"
                )

        # Search for tasks by owner to verify workload visibility
        for member in team_members:
            search_result = subprocess.run(
                ["python", "-m", "todowrite_cli", "search", member],
                capture_output=True,
                text=True,
                cwd=".",
                check=False,
            )

            assert search_result.returncode == 0, f"Failed to search for {member}'s tasks"
            assert member in search_result.stdout, f"Should find {member}'s tasks in search results"
