#!/usr/bin/env python3
"""
Development tools runner for ToDoWrite project.

This module provides backward-compatible access to token optimization
and agent control tools that have been moved to dev_tools/.
"""

import sys
from pathlib import Path

# Add dev_tools to Python path
current_dir = Path(__file__).parent
dev_tools_path = current_dir / "dev_tools"
if dev_tools_path.exists():
    sys.path.insert(0, str(dev_tools_path))


def run_token_optimization_tool(tool_name, *args):
    """Run a token optimization tool"""
    tool_path = dev_tools_path / "token_optimization" / f"{tool_name}.py"

    if not tool_path.exists():
        available_tools = list(dev_tools_path.glob("token_optimization/*.py"))
        tool_names = [t.stem for t in available_tools]
        msg = f"Tool '{tool_name}' not found. Available: {tool_names}"
        raise FileNotFoundError(msg)

    # Execute the tool
    exec_globals = {}
    with open(tool_path) as f:
        exec(f.read(), exec_globals)

    # Look for main function or if __name__ == "__main__"
    if "main" in exec_globals and callable(exec_globals["main"]):
        return exec_globals["main"](*args)
    print(f"Tool '{tool_name}' executed (no main function found)")
    return None


def run_agent_control_tool(tool_name, *args):
    """Run an agent control tool"""
    tool_path = dev_tools_path / "agent_controls" / f"{tool_name}.py"

    if not tool_path.exists():
        available_tools = list(dev_tools_path.glob("agent_controls/*.py"))
        tool_names = [t.stem for t in available_tools]
        msg = f"Agent tool '{tool_name}' not found. Available: {tool_names}"
        raise FileNotFoundError(msg)

    # Execute the tool
    exec_globals = {}
    with open(tool_path) as f:
        exec(f.read(), exec_globals)

    # Look for main function or if __name__ == "__main__"
    if "main" in exec_globals and callable(exec_globals["main"]):
        return exec_globals["main"](*args)
    print(f"Agent tool '{tool_name}' executed (no main function found)")
    return None


def list_available_tools():
    """List all available development tools"""

    print("🚀 Token Optimization Tools:")
    token_tools = list(dev_tools_path.glob("token_optimization/*.py"))
    for tool in token_tools:
        if tool.stem != "__init__":
            print(f"  - {tool.stem}")

    print("\n🤖 Agent Control Tools:")
    agent_tools = list(dev_tools_path.glob("agent_controls/*.py"))
    for tool in agent_tools:
        if tool.stem != "__init__":
            print(f"  - {tool.stem}")


# Backward compatibility functions
def token_optimized_agent(*args):
    """Backward compatibility wrapper"""
    return run_token_optimization_tool("token_optimized_agent", *args)


def always_token_sage(*args):
    """Backward compatibility wrapper"""
    return run_token_optimization_tool("always_token_sage", *args)


def auto_agent(*args):
    """Backward compatibility wrapper"""
    return run_token_optimization_tool("auto_agent", *args)


def hal_agent_loop(*args):
    """Backward compatibility wrapper"""
    return run_agent_control_tool("hal_agent_loop", *args)


def hal_token_savvy_agent(*args):
    """Backward compatibility wrapper"""
    return run_agent_control_tool("hal_token_savvy_agent", *args)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dev_tools_runner.py <tool_name> [args...]")
        print("Use 'list' to see available tools")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "list":
        list_available_tools()
    elif command in [
        "token_optimized_agent",
        "always_token_sage",
        "auto_agent",
    ]:
        run_token_optimization_tool(command, *args)
    elif command in ["hal_agent_loop", "hal_token_savvy_agent"]:
        run_agent_control_tool(command, *args)
    else:
        print(f"Unknown tool: {command}")
        print("Available tools:")
        list_available_tools()
        sys.exit(1)
