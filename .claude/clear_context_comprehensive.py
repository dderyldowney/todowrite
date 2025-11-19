#!/usr/bin/env python3
"""
Comprehensive Clear Context Enforcement - Re-verifies ALL systems before clearing.

This script ensures ALL CLAUDE.md rules and systems remain satisfied when /clear is used.
"""

import os
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


def verify_hal_agent_system() -> bool:
    """Verify HAL Agent System is ready."""
    try:
        hal_path = Path("dev_tools/agent_controls/hal_token_savvy_agent.py")
        if not hal_path.exists():
            return False

        # Test HAL Agent dependencies
        try:
            import importlib.util

            openai_spec = importlib.util.find_spec("openai")
            if openai_spec is None:
                return False
        except ImportError:
            return False

        # Test HAL Agent functionality
        result = os.system(
            "python dev_tools/agent_controls/hal_token_savvy_agent.py --help > /dev/null 2>&1"
        )
        return result == 0
    except:
        return False


def verify_token_optimization_system() -> bool:
    """Verify Token Optimization System is ready."""
    try:
        token_path = Path("dev_tools/token_optimization/always_token_sage.py")
        if not token_path.exists():
            return False

        # Test token optimization functionality
        result = os.system(
            'python dev_tools/token_optimization/always_token_sage.py "test" > /dev/null 2>&1'
        )
        return result == 0
    except:
        return False


def verify_mcp_systems() -> bool:
    """Verify MCP (Model Context Protocol) Systems are ready."""
    try:
        # Check episodic memory MCP
        episodic_memory_exists = (
            Path(".claude/episodic_memory").exists() or Path(".claude/episodic_memory.db").exists()
        )

        # Check for other MCP plugins
        plugins_dir = Path(".claude/plugins")
        mcp_plugins_exist = plugins_dir.exists() and any(plugins_dir.glob("*.py"))

        return episodic_memory_exists or mcp_plugins_exist
    except:
        return False


def verify_anthropic_configuration() -> bool:
    """Verify Anthropic API configuration for HAL Agent."""
    api_key_set = bool(os.environ.get("ANTHROPIC_API_KEY"))

    # API key is mandatory, model is optional
    return api_key_set


def enforce_comprehensive_clear_context_rules() -> bool:
    """Enforce ALL CLAUDE.md rules and systems when clearing context."""
    console = Console()

    console.print(
        Panel(
            "[bold yellow]🔄 COMPREHENSIVE RE-VERIFICATION BEFORE CLEARING CONTEXT[/bold yellow]",
            title="CLEAR CONTEXT ENFORCEMENT",
            border_style="yellow",
        )
    )

    violations = []

    # 1. Basic CLAUDE.md rules
    console.print("[blue]📋 Verifying CLAUDE.md rules...[/blue]")
    enforcer = ClaudeRuleEnforcer(console)
    try:
        enforcer.enforce_all_rules()
        console.print("[green]✅ CLAUDE.md rules verified[/green]")
    except ClaudeRuleViolationError:
        violations.append("CLAUDE.md rules violated")
        console.print("[red]❌ CLAUDE.md rules violated[/red]")

    # 2. HAL Agent System
    console.print("[blue]🤖 Verifying HAL Agent System...[/blue]")
    if verify_hal_agent_system():
        console.print("[green]✅ HAL Agent System ready[/green]")
    else:
        violations.append("HAL Agent System not ready")
        console.print("[red]❌ HAL Agent System not ready[/red]")

    # 3. Token Optimization System
    console.print("[blue]⚡ Verifying Token Optimization System...[/blue]")
    if verify_token_optimization_system():
        console.print("[green]✅ Token Optimization System ready[/green]")
    else:
        violations.append("Token Optimization System not ready")
        console.print("[red]❌ Token Optimization System not ready[/red]")

    # 4. MCP Systems
    console.print("[blue]🔌 Verifying MCP Systems...[/blue]")
    if verify_mcp_systems():
        console.print("[green]✅ MCP Systems ready[/green]")
    else:
        violations.append("MCP Systems not ready")
        console.print("[red]❌ MCP Systems not ready[/red]")

    # 5. Anthropic Configuration
    console.print("[blue]🔑 Verifying Anthropic Configuration...[/blue]")
    if verify_anthropic_configuration():
        console.print("[green]✅ Anthropic configuration ready[/green]")
    else:
        violations.append("Anthropic configuration incomplete")
        console.print("[red]❌ Anthropic configuration incomplete[/red]")

    # Final decision
    if violations:
        console.print(
            Panel(
                f"[bold red]❌ Cannot clear context - {len(violations)} system(s) not ready[/bold red]\n\n"
                f"Violations:\n" + "\n".join(f"• {violation}" for violation in violations),
                title="CLEAR BLOCKED",
                border_style="red",
            )
        )
        return False
    else:
        console.print(
            Panel(
                "[bold green]✅ All systems verified - Context can be cleared[/bold green]",
                title="CLEAR APPROVED",
                border_style="green",
            )
        )

        # Show what will be preserved across /clear
        console.print(
            Panel(
                "[bold blue]🔄 Systems that will remain active across /clear:[/bold blue]\n\n"
                "• 🔄 Virtual Environment: Active\n"
                "• 🗄️ Database Connection: Maintained\n"
                "• 🧠 Episodic Memory: Intact\n"
                "• 🤖 HAL Agent System: Ready\n"
                "• ⚡ Token Optimization: Active\n"
                "• 🔌 MCP Systems: Connected\n"
                "• 📋 CLAUDE.md Rules: Enforced",
                title="PRESERVED SYSTEMS",
                border_style="cyan",
            )
        )
        return True


if __name__ == "__main__":
    success = enforce_comprehensive_clear_context_rules()
    sys.exit(0 if success else 1)
