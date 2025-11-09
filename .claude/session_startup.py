#!/usr/bin/env python3
"""
Claude Code Session Startup Script

This script is automatically loaded at the beginning of every Claude Code session.
It initializes token optimization and agent control processes to ensure
maximum efficiency and proper development environment setup.

This script is called automatically by Claude Code CLI for every session,
including after '/clear' commands and when starting new conversations.
"""

import os
import sys
from pathlib import Path


def setup_token_optimization():
    """Initialize token optimization environment and processes"""
    print("🚀 Initializing Token Optimization Environment...")

    # Add dev_tools to Python path for token optimization tools
    project_root = Path(__file__).parent.parent
    dev_tools_path = project_root / "dev_tools"

    if dev_tools_path.exists():
        sys.path.insert(0, str(dev_tools_path))
        print(f"✅ Added dev_tools to Python path: {dev_tools_path}")

        # Set environment variables for token optimization
        os.environ["CLAUDE_TOKEN_OPTIMIZATION"] = "enabled"
        os.environ["CLAUDE_DEFAULT_AGENT"] = "token-sage"
        os.environ["CLAUDE_HAL_AGENTS"] = "enabled"

        # Try to import and initialize token optimization tools
        try:
            # Import the main token optimization agent
            from token_optimization import (
                always_token_sage,
                token_optimized_agent,
            )

            # Initialize token-sage agent
            if hasattr(always_token_sage, "initialize_token_sage"):
                result = always_token_sage.initialize_token_sage()
                if result:
                    print("✅ Token-sage agent initialized successfully")
                else:
                    print(
                        "⚠️ Token-sage initialization completed with warnings"
                    )

            # Initialize HAL token-savvy agent
            try:
                from agent_controls import hal_token_savvy_agent

                # Enable HAL agents by running initialization
                if hasattr(hal_token_savvy_agent, "initialize_hal_agents"):
                    hal_result = hal_token_savvy_agent.initialize_hal_agents()
                    if hal_result:
                        print("✅ HAL token-savvy agents ENABLED and ready")
                        print("🤖 HAL agent loop and controls active")
                    else:
                        print(
                            "⚠️ HAL agents initialization completed with warnings"
                        )

                # Run initial HAL agent loop to ensure controls are active
                if hasattr(hal_token_savvy_agent, "start_hal_loop"):
                    print("🔄 Starting HAL agent control loop...")
                    # Note: This runs in background to enable persistent control
                    # The actual loop management is handled by the HAL agent system
                    control_result = hal_token_savvy_agent.start_hal_loop()
                    if control_result:
                        print("✅ HAL agent control loop started successfully")

            except ImportError as e:
                print(f"⚠️ Could not initialize HAL agents: {e}")

            print("📊 Token optimization environment ready")
            print("💰 Local preprocessing available (0 tokens for filtering)")
            print("🔧 Token-sage and HAL agents ENABLED")
            print("🤖 Agentic controls ACTIVE and ready")

        except ImportError as e:
            print(f"⚠️ Token optimization tools not fully available: {e}")
            print("💡 Run './run_token_tools.sh list' to see available tools")

    else:
        print(f"⚠️ dev_tools directory not found at: {dev_tools_path}")


def setup_project_environment():
    """Setup project-specific environment variables and paths"""
    print("\n🔧 Setting up ToDoWrite Project Environment...")

    project_root = Path(__file__).parent.parent

    # Set PYTHONPATH for project packages
    lib_path = project_root / "lib_package" / "src"
    cli_path = project_root / "cli_package" / "src"

    python_paths = [str(lib_path), str(cli_path)]
    existing_paths = [p for p in python_paths if Path(p).exists()]

    if existing_paths:
        current_pythonpath = os.environ.get("PYTHONPATH", "")
        new_pythonpath = ":".join(existing_paths)
        if current_pythonpath:
            new_pythonpath = f"{new_pythonpath}:{current_pythonpath}"

        os.environ["PYTHONPATH"] = new_pythonpath
        print(f"✅ PYTHONPATH updated: {new_pythonpath}")

    # Set project root environment variable
    os.environ["TODOWRITE_PROJECT_ROOT"] = str(project_root)
    print(f"✅ Project root set: {project_root}")

    # Check if todowrite database exists
    db_files = list(project_root.glob("*.db"))
    if db_files:
        print(f"✅ Found ToDoWrite databases: {[f.name for f in db_files]}")
    else:
        print(
            "ℹ️ No ToDoWrite databases found - run 'todowrite init' to create one"
        )


def load_project_context():
    """Load project context from ToDoWrite.md for Claude understanding"""
    print("\n📖 Loading Project Context...")

    project_root = Path(__file__).parent.parent
    todowrite_md_path = project_root / "ToDoWrite.md"

    if todowrite_md_path.exists():
        print(f"✅ Found ToDoWrite.md at {todowrite_md_path}")
        print("📋 Project Layers (12-level hierarchy):")
        print("   1. Goal (GOAL-*) - High-level project objectives")
        print(
            "   2. Concept (CON-*) - Design concepts and architectural patterns"
        )
        print("   3. Context (CTX-*) - Environmental and project context")
        print(
            "   4. Constraints (CST-*) - Project constraints and limitations"
        )
        print("   5. Requirements (R-*) - Functional requirements")
        print(
            "   6. AcceptanceCriteria (AC-*) - Acceptance conditions and criteria"
        )
        print(
            "   7. InterfaceContract (IF-*) - Interface specifications and contracts"
        )
        print("   8. Phase (PH-*) - Project phases and milestones")
        print("   9. Step (STP-*) - Implementation steps")
        print("   10. Task (TSK-*) - Specific tasks with progress tracking")
        print(
            "   11. SubTask (SUB-*) - Sub-tasks that break down larger tasks"
        )
        print(
            "   12. Command (CMD-*) - Executable commands with run instructions"
        )
        print(
            "💡 Claude should reference these layers when organizing development work"
        )
        print(
            "🔄 Use 'todowrite' CLI for managing development tasks hierarchically"
        )

        # Store context for Claude
        os.environ["TODOWRITE_LAYERS_LOADED"] = "true"
        return True
    print(f"⚠️ ToDoWrite.md not found at {todowrite_md_path}")
    return False


def display_session_info():
    """Display session initialization summary"""
    print("\n" + "=" * 70)
    print("🤖 CLAUDE CODE SESSION INITIALIZED")
    print("=" * 70)
    print("📁 Project: ToDoWrite Hierarchical Task Management")
    print("🚀 Token Optimization: ENABLED")
    print("🤖 Agent Controls: ACTIVE")
    print("💰 Efficiency Mode: MAXIMUM")
    print("📖 Project Context: LOADED")
    print("=" * 70)
    print("\n🛠️ Available Commands:")
    print(
        "  • ./run_token_tools.sh list                    - List all optimization tools"
    )
    print(
        "  • ./run_token_tools.sh token_optimized_agent  - Run token optimizer"
    )
    print(
        "  • ./run_token_tools.sh hal_agent_loop         - Run HAL agent loop"
    )
    print("  • todowrite --help                          - ToDoWrite CLI help")
    print(
        "  • todowrite init                            - Initialize development DB"
    )
    print(
        "  • todowrite list                            - List all development tasks"
    )
    print("\n📚 Documentation:")
    print(
        "  • ToDoWrite.md                               - Project layers and system overview"
    )
    print(
        "  • dev_tools/README.md                       - Development tools guide"
    )
    print(
        "  • docs/                                    - Project documentation"
    )
    print("  • README.md                                - Project overview")
    print("\n💻 Development Tools:")
    print(
        "  • ruff format, ruff check                   - Linting and formatting"
    )
    print("  • uv                                        - Package management")
    print("  • todowrite CLI                             - Task management")
    print("=" * 70 + "\n")


def main():
    """Main session initialization function"""
    try:
        # Initialize token optimization first
        setup_token_optimization()

        # Setup project environment
        setup_project_environment()

        # Load project context from ToDoWrite.md
        load_project_context()

        # Display session information
        display_session_info()

        return True

    except Exception as e:
        print(f"❌ Session initialization error: {e}")
        print("⚠️ Continuing with limited functionality")
        return False


# Auto-execute when imported
if __name__ == "__main__":
    main()
else:
    # When imported, automatically run initialization
    main()
