#!/usr/bin/env python3
"""
Clear Context Enforcement - Must re-verify all rules before clearing.

This script enforces CLAUDE.md rules when /clear command is used.
"""

import sys
from pathlib import Path

# Import from the startup script to avoid duplication
sys.path.insert(0, str(Path(__file__).parent))

try:
    from rich.console import Console
    from rich.panel import Panel
    from startup_enforcement import ClaudeRuleEnforcer, ClaudeRuleViolationError
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def enforce_clear_context_rules() -> bool:
    """Enforce CLAUDE.md rules when clearing context."""
    console = Console()

    console.print(Panel(
        "[bold yellow]🔄 RE-VERIFYING RULES BEFORE CLEARING CONTEXT[/bold yellow]",
        title="CLEAR CONTEXT ENFORCEMENT",
        border_style="yellow"
    ))

    enforcer = ClaudeRuleEnforcer(console)

    try:
        enforcer.enforce_all_rules()

        console.print(Panel(
            "[bold green]✅ Rules re-verified - Context can be cleared[/bold green]",
            title="CLEAR APPROVED",
            border_style="green"
        ))

        return True

    except ClaudeRuleViolationError:
        console.print(Panel(
            "[bold red]❌ Cannot clear context - Rules violated[/bold red]",
            title="CLEAR BLOCKED",
            border_style="red"
        ))
        return False
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        return False


if __name__ == "__main__":
    success = enforce_clear_context_rules()
    sys.exit(0 if success else 1)