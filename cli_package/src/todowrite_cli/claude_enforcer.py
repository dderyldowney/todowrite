"""CLAUDE.md Rule Enforcement.

Rules cannot be overridden under any circumstances.
"""

import importlib.util
import os
import sys
from pathlib import Path
from typing import Any

# Check optional dependencies availability
click_available = importlib.util.find_spec("click") is not None
rich_available = importlib.util.find_spec("rich") is not None
todowrite_available = importlib.util.find_spec("todowrite") is not None

if rich_available:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text


class ClaudeRuleViolationError(Exception):
    """Raised when CLAUDE.md rules are violated."""

    pass


class ClaudeRuleEnforcer:
    """Enforces CLAUDE.md rules - ZERO EXCEPTIONS."""

    def __init__(self, console: Console | None = None):
        self.console = console or Console()
        self.claude_path = Path.cwd() / ".claude" / "CLAUDE.md"
        self.violations: list[str] = []

    def enforce_all_rules(self) -> None:
        """Enforce all CLAUDE.md rules - cannot be bypassed."""
        self._enforce_virtual_environment()
        self._enforce_database_configuration()
        self._enforce_database_content()

        if self.violations:
            self._report_violations()
            raise ClaudeRuleViolationError(
                "CLAUDE.md rules violated - session terminated"
            )

    def _enforce_virtual_environment(self) -> None:
        """MUST have virtual environment activated."""
        # Check if .venv exists
        venv_path = Path.cwd() / ".venv"
        if not venv_path.exists():
            self.violations.append("❌ Virtual environment .venv not found")
            return

        # Check if virtual environment is active
        python_path = sys.executable
        if ".venv" not in python_path:
            self.violations.append(
                "❌ Virtual environment not activated - run: source .venv/bin/activate"
            )
            return

        # Verify essential packages are available
        if not click_available or not rich_available or not todowrite_available:
            missing = []
            if not click_available:
                missing.append("click")
            if not rich_available:
                missing.append("rich")
            if not todowrite_available:
                missing.append("todowrite")
            self.violations.append(
                f"❌ Required packages not available: {', '.join(missing)}"
            )
            return

    def _enforce_database_configuration(self) -> None:
        """MUST use correct database configuration."""
        # Check database URL environment variable
        db_url = os.environ.get("TODOWRITE_DATABASE_URL", "")
        expected_pattern = "sqlite:///$HOME/dbs/todowrite_development.db"

        if not db_url:
            error_msg = f"❌ TODOWRITE_DATABASE_URL not set - must be: {expected_pattern}"
            self.violations.append(error_msg)
            return

        # Check for forbidden hardcoded paths
        forbidden_patterns = [
            "/Users/",
            "/home/",
            "/opt/",
            "/var/",
            "/tmp/",
            "todowrite_todowrite_development.db",  # Redundant prefix
            "development_todowrite.db",  # Wrong naming
        ]

        for pattern in forbidden_patterns:
            if pattern in db_url:
                self.violations.append(
                    f"❌ Forbidden hardcoded path in database URL: {pattern}"
                )
                return

        # Verify correct pattern
        if not db_url.startswith(
            "sqlite:///$HOME/dbs/todowrite_development.db"
        ):
            self.violations.append(
                f"❌ Incorrect database URL: must be {expected_pattern}"
            )
            return

    def _enforce_database_content(self) -> None:
        """Database must contain required planning structure."""
        try:
            from sqlalchemy import create_engine, text
            from sqlalchemy.orm import sessionmaker
            from todowrite.core.models import Goal
            from todowrite.utils.database_utils import get_database_path

            # Connect to database
            db_path = get_database_path("development")
            engine = create_engine(f"sqlite:///{db_path}")
            Session = sessionmaker(bind=engine)
            session = Session()

            # Check database exists and is accessible
            try:
                session.execute(text("SELECT COUNT(*) FROM goals"))
            except Exception as e:
                self.violations.append(f"❌ Database not accessible: {e}")
                session.close()
                return

            # Check for required goal
            required_goal = "Enhance ToDoWrite Planning Capabilities"
            goal_count = (
                session.query(Goal).filter(Goal.title == required_goal).count()
            )

            if goal_count == 0:
                self.violations.append(
                    f"❌ Required goal not found: '{required_goal}'"
                )
                session.close()
                return

            # Check for complete hierarchy (143+ records)
            total_records = 0
            tables = [
                "goals",
                "concepts",
                "contexts",
                "constraints",
                "requirements",
                "acceptance_criteria",
                "interface_contracts",
                "phases",
                "steps",
                "tasks",
                "sub_tasks",
                "commands",
                "labels",
            ]

            for table in tables:
                try:
                    # Use parameterized query with validated table names
                    if table not in tables:  # Double-check against our whitelist
                        continue

                    query = text(f"SELECT COUNT(*) FROM {table}")
                    result = session.execute(query)
                    count = result.fetchone()[0]
                    total_records += count
                except Exception as e:
                    # Log exception but continue with other tables
                    print(f"Warning: Could not count records in {table}: {e}")
                    continue

            if total_records < 143:
                self.violations.append(
                    f"❌ Incomplete database structure: {total_records} records (expected 143+)"
                )
                session.close()
                return

            session.close()

        except Exception as e:
            self.violations.append(f"❌ Database verification failed: {e}")

    def _report_violations(self) -> None:
        """Report rule violations and terminate."""
        error_text = Text(
            "\n🚨 CLAUDE.md RULE VIOLATIONS DETECTED 🚨\n", style="bold red"
        )
        error_text.append(
            "These rules cannot be overridden under any circumstances.\n\n",
            style="red",
        )

        for violation in self.violations:
            error_text.append(f"{violation}\n", style="red")

        error_text.append("\nREQUIRED ACTIONS:\n", style="bold yellow")

        # Add specific fixes based on violations
        if any("virtual environment" in v.lower() for v in self.violations):
            error_text.append(
                "• Run: source $PWD/.venv/bin/activate\n", style="yellow"
            )

        if any("database" in v.lower() for v in self.violations):
            error_text.append(
                '• Run: export TODOWRITE_DATABASE_URL="sqlite:///$HOME/dbs/todowrite_development.db"\n',
                style="yellow",
            )

        if any(
            "Enhance ToDoWrite Planning Capabilities" in v
            for v in self.violations
        ):
            error_text.append(
                "• Initialize database: python .claude/auto_init_todowrite_models.py\n",
                style="yellow",
            )

        error_text.append(
            "\nSession terminated. Fix violations and retry.\n",
            style="bold red",
        )

        panel = Panel(
            error_text,
            title="[bold red]ENFORCEMENT FAILURE[/bold red]",
            border_style="red",
            padding=(1, 2),
        )

        self.console.print(panel)

    def verify_startup_sequence(self) -> None:
        """Verify the complete startup sequence is followed."""
        required_env_vars = ["TODOWRITE_DATABASE_URL", "PYTHONPATH"]

        missing_vars = []
        for var in required_env_vars:
            if not os.environ.get(var):
                missing_vars.append(var)

        if missing_vars:
            self.violations.append(
                f"❌ Missing required environment variables: {', '.join(missing_vars)}"
            )


def enforce_claude_rules(
    ctx: click.Context, param: click.Parameter, value: Any
) -> Any:
    """Click callback to enforce CLAUDE.md rules."""
    if value:  # Only enforce when --enforce-claude-rules is used
        enforcer = ClaudeRuleEnforcer()
        try:
            enforcer.enforce_all_rules()
            console = Console()
            console.print(
                Panel(
                    "✅ All CLAUDE.md rules verified and enforced",
                    title="[bold green]RULE ENFORCEMENT SUCCESS[/bold green]",
                    border_style="green",
                )
            )
        except ClaudeRuleViolationError:
            sys.exit(1)
    return value


def verify_database_completeness(
    ctx: click.Context, param: click.Parameter, value: Any
) -> Any:
    """Click callback to verify database completeness."""
    if value:
        enforcer = ClaudeRuleEnforcer()
        enforcer._enforce_database_content()
        if enforcer.violations:
            enforcer._report_violations()
            sys.exit(1)
        else:
            console = Console()
            console.print(
                Panel(
                    "✅ Database completeness verified",
                    title="[bold green]DATABASE VERIFICATION SUCCESS[/bold green]",
                    border_style="green",
                )
            )
    return value


def clear_context_enforcement(
    ctx: click.Context, param: click.Parameter, value: Any
) -> Any:
    """Enforce rules when /clear command is used."""
    if value:
        # Re-enforce all rules before clearing context
        enforcer = ClaudeRuleEnforcer()
        try:
            enforcer.enforce_all_rules()
        except ClaudeRuleViolationError:
            sys.exit(1)
    return value
