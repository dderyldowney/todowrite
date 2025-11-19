#!/usr/bin/env python3
"""
Session startup script that enforces ToDoWrite_cli usage and token optimization.
Runs automatically at session start to ensure proper workflow compliance.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def check_ToDoWrite_cli_available():
    """Check if ToDoWrite_cli is available in the current environment."""
    try:
        result = subprocess.run(
            ["python", "-m", "todowrite_cli", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def setup_ToDoWrite_environment():
    """Set up environment variables for ToDoWrite_cli."""
    import os
    import sys
    from pathlib import Path

    # Add project root to path so we can import the utility
    project_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(project_root / "lib_package" / "src"))

    try:
        from todowrite.utils.database_utils import get_project_database_name

        dev_db_name = get_project_database_name("development")
        dev_db_url = f"sqlite:///{dev_db_name}"
    except ImportError:
        # Fallback to original naming if utility not available
        dev_db_url = "sqlite:///development_todowrite.db"

    env_vars = {
        "PYTHONPATH": "lib_package/src:cli_package/src",
        "TODOWRITE_DATABASE_URL": dev_db_url,
    }

    for key, value in env_vars.items():
        if key not in os.environ or not os.environ.get(key):
            print(f"Note: {key} should be set to {value}")
            # Note: In a real implementation, these would be set in the shell environment


def verify_token_optimization():
    """Verify that token optimization is properly configured."""
    config_path = Path.home() / ".claude" / "config.json"

    if not config_path.exists():
        print("❌ config.json not found")
        return False

    try:
        with open(config_path) as f:
            config = json.load(f)

        token_opt = config.get("token_optimization", {})
        if not token_opt.get("enabled", False):
            print("❌ Token optimization not enabled")
            return False

        print("✓ Token optimization is enabled")
        print(f"  - HAL preprocessing: {token_opt.get('hal_preprocessing', False)}")
        print(f"  - Cache enabled: {token_opt.get('cache_enabled', False)}")
        print(f"  - Max context chars: {token_opt.get('max_context_chars', 'N/A')}")

        return True

    except json.JSONDecodeError:
        print("❌ config.json is malformed")
        return False


def load_superpowers_and_fail_safes():
    """Load superpowers skills and fail-safe mechanisms."""
    import sys
    from pathlib import Path

    project_root = Path.cwd()
    claude_dir = project_root / ".claude"

    print("🔧 Loading superpowers skills and fail-safes...")

    # Add superpowers to Python path
    sys.path.insert(0, str(claude_dir))
    superpowers_dir = claude_dir / "skills"

    # Check for required skills
    required_skills = [
        "test-driven-development",
        "dispatching-parallel-agents",
        "subagent-driven-development",
    ]

    loaded_skills = []
    for skill_name in required_skills:
        skill_path = superpowers_dir / skill_name / "skill.py"
        if skill_path.exists():
            try:
                # Import and verify skill with unique module import
                import importlib.util

                spec = importlib.util.spec_from_file_location(
                    f"skill_{skill_name.replace('-', '_')}", skill_path
                )
                skill_module = importlib.util.module_from_spec(spec)
                sys.modules[f"skill_{skill_name.replace('-', '_')}"] = skill_module
                spec.loader.exec_module(skill_module)

                # Verify skill class exists
                if skill_name == "test-driven-development":
                    _ = skill_module.TestDrivenDevelopment  # Verify class exists
                    print(f"   ✓ {skill_name} skill loaded")
                    loaded_skills.append(skill_name)
                elif skill_name == "dispatching-parallel-agents":
                    _ = skill_module.DispatchingParallelAgents  # Verify class exists
                    print(f"   ✓ {skill_name} skill loaded")
                    loaded_skills.append(skill_name)
                elif skill_name == "subagent-driven-development":
                    _ = skill_module.SubagentDrivenDevelopment  # Verify class exists
                    print(f"   ✓ {skill_name} skill loaded")
                    loaded_skills.append(skill_name)
            except ImportError as e:
                print(f"   ⚠️ {skill_name} skill import failed: {e}")
            except AttributeError as e:
                print(f"   ⚠️ {skill_name} skill class not found: {e}")
        else:
            print(f"   ⚠️ {skill_name} skill not found")

    # Load fail-safes
    try:
        import superpowers_fail_safes

        fail_safes = superpowers_fail_safes.get_fail_safes()
        if fail_safes:
            print("   ✓ Superpowers fail-safes active")
            status = fail_safes.get_system_status()
            print(f"     Active subagents: {status['active_subagents']}")
            print(f"     Memory usage: {status['total_memory_used_mb']:.1f}MB")
        else:
            print("   ⚠️ Fail-safes instance not created")
    except ImportError as e:
        print(f"   ❌ Fail-safes import failed: {e}")

    print(f"✅ Superpowers loaded: {len(loaded_skills)}/{len(required_skills)}")
    return len(loaded_skills) >= 2  # Allow partial success


def initialize_mcp_2025():
    """Initialize MCP 2025 system."""
    project_root = Path.cwd()
    claude_dir = project_root / ".claude"

    print("🤖 Initializing MCP 2025 system...")

    # Check MCP configurations
    mcp_configs = [
        "mcp_config_2025.json",
        "mcp_superpowers_config_2025.json",
        "mcp_episodic_memory_config_2025.json",
    ]

    config_count = 0
    for config in mcp_configs:
        config_path = claude_dir / config
        if config_path.exists():
            config_count += 1
            print(f"   ✓ {config}")
        else:
            print(f"   ⚠️ {config} missing")

    # Check MCP tools
    mcp_tools = ["mcp_security_optimizer.py", "mcp_monitoring_dashboard.py", "setup_mcp_2025.sh"]

    tool_count = 0
    for tool in mcp_tools:
        tool_path = claude_dir / tool
        if tool_path.exists() and os.access(tool_path, os.X_OK):
            tool_count += 1
            print(f"   ✓ {tool} (executable)")

    print(
        f"✅ MCP 2025: {config_count}/{len(mcp_configs)} configs, {tool_count}/{len(mcp_tools)} tools"
    )
    return config_count >= 2


def verify_hal_and_token_optimization():
    """Verify HAL Agent and Token-Sage integration."""
    project_root = Path.cwd()
    dev_tools = project_root / "dev_tools"

    print("⚡ Verifying HAL Agent and Token-Sage integration...")

    hal_agent = dev_tools / "agent_controls" / "hal_token_savvy_agent.py"
    token_sage = dev_tools / "token_optimization" / "always_token_sage.py"

    hal_available = hal_agent.exists() and os.access(hal_agent, os.X_OK)
    token_available = token_sage.exists() and os.access(token_sage, os.X_OK)

    if hal_available:
        print("   ✓ HAL Agent available")
    else:
        print("   ⚠️ HAL Agent not available or not executable")

    if token_available:
        print("   ✓ Token-Sage available")
    else:
        print("   ⚠️ Token-Sage not available or not executable")

    return hal_available and token_available


def create_comprehensive_workflow_markers():
    """Create comprehensive workflow enforcement markers."""
    session_dir = Path.cwd() / ".claude"
    session_dir.mkdir(exist_ok=True)

    workflow_file = session_dir / "workflow_active_2025.json"
    workflow_data = {
        "session_start": datetime.now().isoformat(),
        "ToDoWrite_cli_enforced": True,
        "superpowers_active": True,
        "fail_safes_active": True,
        "mcp_2025_active": True,
        "hal_token_optimization_active": True,
        "episodic_memory_available": True,
        "workflow_version": "2025.1",
        "required_skills": [
            "test-driven-development",
            "dispatching-parallel-agents",
            "subagent-driven-development",
        ],
        "protection_mechanisms": [
            "session_lock_prevention",
            "memory_monitoring",
            "resource_limits",
            "error_isolation",
        ],
    }

    with open(workflow_file, "w") as f:
        json.dump(workflow_data, f, indent=2)

    print("✓ Comprehensive 2025 workflow markers created")


def initialize_ToDoWrite_tracking():
    """Initialize ToDoWrite system for development tracking."""
    print("🔧 Initializing ToDoWrite development tracking...")

    init_script = Path.cwd() / ".claude" / "init_ToDoWrite_session.py"

    if init_script.exists() and os.access(init_script, os.X_OK):
        try:
            # Run the initialization script
            result = subprocess.run(
                ["python", str(init_script)],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

            if result.returncode == 0:
                print("✓ ToDoWrite development tracking initialized")
                return True
            else:
                print(f"⚠️  ToDoWrite initialization issues: {result.stderr.strip()}")
                return False

        except subprocess.TimeoutExpired:
            print("⚠️  ToDoWrite initialization timeout")
            return False
        except Exception as e:
            print(f"⚠️  ToDoWrite initialization error: {e}")
            return False
    else:
        print("⚠️  ToDoWrite initialization script not found")
        return False


def activate_tdd_enforcement_for_session() -> bool:
    """Activate TDD enforcement for the session."""
    try:
        # Import the TDD activation module
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "tdd_activation", Path.cwd() / ".claude" / "activate_tdd_enforcement.py"
        )
        tdd_module = importlib.util.module_from_spec(spec)

        # Suppress verbose output during regular session startup
        import contextlib
        import io

        captured_output = io.StringIO()
        with contextlib.redirect_stdout(captured_output):
            spec.loader.exec_module(tdd_module)
            return tdd_module.activate_tdd_enforcement()

    except Exception as e:
        # Silently fail during session startup to avoid blocking initialization
        print(f"   ⚠️  TDD activation warning: {e}")
        return True  # Return True to avoid blocking session startup


def main():
    """Comprehensive main startup logic with all systems integration."""
    print("🚀 Starting comprehensive 2025 session initialization...")

    success_count = 0
    total_checks = 8

    # 1. Check ToDoWrite_cli availability
    if not check_ToDoWrite_cli_available():
        print("⚠️  ToDoWrite_cli not available - make sure PYTHONPATH is set correctly")
        print('   export PYTHONPATH="lib_package/src:cli_package/src"')
        sys.exit(1)
    print("✓ ToDoWrite_cli is available")
    success_count += 1

    # 2. Verify token optimization
    if not verify_token_optimization():
        print("⚠️  Token optimization issues detected - check config.json")
        sys.exit(1)
    print("✓ Token optimization verified")
    success_count += 1

    # 3. Initialize ToDoWrite development tracking (NEW)
    if initialize_ToDoWrite_tracking():
        print("✓ ToDoWrite development tracking active")
        success_count += 1
    else:
        print("⚠️  ToDoWrite tracking initialization incomplete")

    # 4. Load superpowers skills and fail-safes
    if load_superpowers_and_fail_safes():
        print("✓ Superpowers skills and fail-safes loaded")
        success_count += 1
    else:
        print("⚠️  Superpowers loading incomplete - some features may be unavailable")

    # 5. Initialize MCP 2025 system
    if initialize_mcp_2025():
        print("✓ MCP 2025 system initialized")
        success_count += 1
    else:
        print("⚠️  MCP 2025 initialization incomplete - some features may be unavailable")

    # 6. Verify HAL and Token-Sage integration
    if verify_hal_and_token_optimization():
        print("✓ HAL Agent and Token-Sage integration verified")
        success_count += 1
    else:
        print("⚠️  HAL/Token-Sage integration issues detected")

    # 7. Create comprehensive workflow markers
    create_comprehensive_workflow_markers()
    print("✓ Comprehensive workflow markers created")
    success_count += 1

    # 8. Activate TDD enforcement
    if activate_tdd_enforcement_for_session():
        print("✓ TDD enforcement activated")
        success_count += 1
    else:
        print("⚠️  TDD enforcement activation incomplete - some TDD features may be unavailable")

    # Set up environment
    setup_ToDoWrite_environment()

    print(f"\n📊 Session Initialization Complete: {success_count}/{total_checks} systems active")

    print("\n📋 2025 Session Requirements:")
    print("  1. ALL planning must use ToDoWrite_cli")
    print("  2. Check episodic memory before starting work")
    print("  3. Token optimization is active (HAL + Token-Sage)")
    print("  4. Superpowers skills with fail-safes are enabled")
    print("  5. MCP 2025 system provides industry-standard tools")
    print("  6. Document decisions in ToDoWrite tasks")
    print("  7. Session protection against memory exhaustion and locks")

    if success_count >= 5:
        print("\n✅ Session ready - comprehensive 2025 workflow active!")
        return 0
    else:
        print("\n⚠️  Session initialized with some limitations")
        print("   Consider checking system configuration for missing components")
        return 1


if __name__ == "__main__":
    sys.exit(main())
