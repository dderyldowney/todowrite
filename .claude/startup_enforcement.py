#!/usr/bin/env python3
"""
AI CLI Startup Enforcement - Cannot be overridden under any circumstances.

This script enforces CLAUDE.md rules for AI agents working on this project.
It MUST be run before any development work can proceed.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
except ImportError:
    print("❌ Missing rich library. Please run: pip install rich")
    sys.exit(1)


class ClaudeRuleViolationError(Exception):
    """Raised when CLAUDE.md rules are violated."""
    pass


class ClaudeRuleEnforcer:
    """Enforces CLAUDE.md rules - ZERO EXCEPTIONS."""

    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
        self.violations: List[str] = []

    def enforce_all_rules(self) -> None:
        """Enforce all CLAUDE.md rules - cannot be bypassed."""
        self._enforce_virtual_environment()
        self._enforce_database_configuration()
        self._enforce_database_content()

        if self.violations:
            self._report_violations()
            raise ClaudeRuleViolationError("CLAUDE.md rules violated - session terminated")

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
            self.violations.append("❌ Virtual environment not activated - run: source .venv/bin/activate")
            return

        # Verify essential packages are available
        try:
            import todowrite
            import click
            import rich
        except ImportError as e:
            self.violations.append(f"❌ Required package not available in virtual environment: {e}")
            return

    def _enforce_database_configuration(self) -> None:
        """MUST use correct database configuration."""
        # Check database URL environment variable
        db_url = os.environ.get("TODOWRITE_DATABASE_URL", "")
        expected_pattern = "sqlite:///$HOME/dbs/todowrite_development.db"

        if not db_url:
            self.violations.append(f"❌ TODOWRITE_DATABASE_URL not set - must be: {expected_pattern}")
            return

        # Normalize the database URL to check pattern
        expanded_db_url = db_url.replace(os.path.expanduser("~"), "$HOME")

        # Check for forbidden hardcoded paths (after expansion)
        forbidden_patterns = [
            "/opt/", "/var/", "/tmp/",
            "todowrite_todowrite_development.db",  # Redundant prefix
            "development_todowrite.db",           # Wrong naming
        ]

        for pattern in forbidden_patterns:
            if pattern in expanded_db_url:
                self.violations.append(f"❌ Forbidden hardcoded path in database URL: {pattern}")
                return

        # Verify correct pattern
        if not expanded_db_url.startswith("sqlite:///$HOME/dbs/todowrite_development.db"):
            self.violations.append(f"❌ Incorrect database URL: must be {expected_pattern}")
            return

    def _enforce_database_content(self) -> None:
        """Database must contain required planning structure."""
        try:
            from todowrite.utils.database_utils import get_database_path
            from sqlalchemy import create_engine, select, text
            from sqlalchemy.orm import sessionmaker
            from todowrite.core.models import Goal

            # Connect to database
            db_path = get_database_path('development')
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
            goal_count = session.query(Goal).filter(Goal.title == required_goal).count()

            if goal_count == 0:
                self.violations.append(f"❌ Required goal not found: '{required_goal}'")
                session.close()
                return

            # Check for complete hierarchy (143+ records)
            total_records = 0
            tables = ['goals', 'concepts', 'contexts', 'constraints', 'requirements',
                     'acceptance_criteria', 'interface_contracts', 'phases', 'steps',
                     'tasks', 'sub_tasks', 'commands', 'labels']

            for table in tables:
                try:
                    result = session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    total_records += count
                except:
                    pass

            if total_records < 143:
                self.violations.append(f"❌ Incomplete database structure: {total_records} records (expected 143+)")
                session.close()
                return

            session.close()

        except Exception as e:
            self.violations.append(f"❌ Database verification failed: {e}")

    def _report_violations(self) -> None:
        """Report rule violations and terminate."""
        error_text = Text("\n🚨 CLAUDE.md RULE VIOLATIONS DETECTED 🚨\n", style="bold red")
        error_text.append("These rules cannot be overridden under any circumstances.\n\n", style="red")

        for violation in self.violations:
            error_text.append(f"{violation}\n", style="red")

        error_text.append("\nREQUIRED ACTIONS:\n", style="bold yellow")

        # Add specific fixes based on violations
        if any("virtual environment" in v.lower() for v in self.violations):
            error_text.append("• Run: source $PWD/.venv/bin/activate\n", style="yellow")

        if any("database" in v.lower() for v in self.violations):
            error_text.append("• Run: export TODOWRITE_DATABASE_URL=\"sqlite:///$HOME/dbs/todowrite_development.db\"\n", style="yellow")

        if any("Enhance ToDoWrite Planning Capabilities" in v for v in self.violations):
            error_text.append("• Initialize database: python .claude/auto_init_todowrite_models.py\n", style="yellow")

        error_text.append("\nSession terminated. Fix violations and retry.\n", style="bold red")

        panel = Panel(
            error_text,
            title="[bold red]ENFORCEMENT FAILURE[/bold red]",
            border_style="red",
            padding=(1, 2)
        )

        self.console.print(panel)


def enforce_startup_rules() -> bool:
    """Enforce CLAUDE.md rules on startup."""
    console = Console()

    console.print(Panel(
        "[bold blue]🚀 ENFORCING CLAUDE.md RULES FOR AI CLI[/bold blue]",
        title="STARTUP VERIFICATION",
        border_style="blue"
    ))

    enforcer = ClaudeRuleEnforcer(console)

    try:
        enforcer.enforce_all_rules()

        console.print(Panel(
            "[bold green]✅ ALL RULES VERIFIED - AI CLI READY[/bold green]",
            title="ENFORCEMENT SUCCESS",
            border_style="green"
        ))

        # Print current environment status
        env_info = Text()
        env_info.append("📍 Current Environment:\n", style="bold")
        env_info.append(f"• Virtual Environment: {'.venv' in sys.executable}\n", style="green" if '.venv' in sys.executable else "red")
        env_info.append(f"• Database URL: {os.environ.get('TODOWRITE_DATABASE_URL', 'NOT SET')}\n", style="green" if os.environ.get('TODOWRITE_DATABASE_URL') else "red")
        env_info.append(f"• PYTHONPATH: {os.environ.get('PYTHONPATH', 'NOT SET')}\n", style="green" if os.environ.get('PYTHONPATH') else "red")

        console.print(Panel(env_info, title="ENVIRONMENT STATUS", border_style="cyan"))

        return True

    except ClaudeRuleViolationError:
        console.print(Panel(
            "[bold red]❌ RULE ENFORCEMENT FAILED[/bold red]",
            title="ENFORCEMENT FAILURE",
            border_style="red"
        ))
        return False
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")
        return False


if __name__ == "__main__":
    success = enforce_startup_rules()
    sys.exit(0 if success else 1)