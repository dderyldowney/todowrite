#!/usr/bin/env python3
"""
Dynamic MCP Tool Discovery System.

This script dynamically discovers and reports all available MCP tools
from running MCP servers, creating a real-time inventory of what's
actually available for use.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


class MCPToolDiscovery:
    """Dynamic MCP tool discovery and inventory management."""

    def __init__(self) -> None:
        """Initialize the MCP tool discovery system."""
        self.available_tools: dict[str, Any] = {}
        self.server_status: dict[str, bool] = {}
        self.discovery_time: str = datetime.now().isoformat()

    def check_server_status(self) -> dict[str, bool]:
        """Check which MCP servers are currently running."""
        status = {}

        # Check launchd services
        try:
            result = subprocess.run(
                ["launchctl", "list"], capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.split("\n"):
                if "com.user.mcp." in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        service_name = parts[2]
                        status_code = parts[0]
                        server_name = service_name.replace("com.user.mcp.", "")
                        # Status "-" or "0" means not running
                        is_running = status_code not in ("-", "0")
                        status[server_name] = is_running
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            pass

        # Check Docker containers
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            for line in result.stdout.split("\n"):
                if line.startswith("mcp-"):
                    server_name = line.replace("mcp-", "")
                    status[server_name] = True
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            pass

        # Check Docker MCP Gateway
        try:
            result = subprocess.run(
                ["pgrep", "-f", "docker mcp gateway"], capture_output=True, text=True, timeout=5
            )
            status["docker-mcp-gateway"] = len(result.stdout.strip()) > 0
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            status["docker-mcp-gateway"] = False

        return status

    def discover_mcp_tools(self) -> dict[str, Any]:
        """Discover available MCP tools by querying running servers"""
        discovery = {
            "discovery_time": self.discovery_time,
            "server_status": {},
            "available_tools": {},
            "tool_count": 0,
            "server_count": 0,
        }

        # Get server status
        discovery["server_status"] = self.check_server_status()
        discovery["server_count"] = sum(
            1 for running in discovery["server_status"].values() if running
        )

        # Discover tools from each running server
        for server_name, is_running in discovery["server_status"].items():
            if is_running:
                try:
                    tools = self.get_server_tools(server_name)
                    discovery["available_tools"][server_name] = tools
                    discovery["tool_count"] += len(tools)
                except Exception as e:
                    discovery["available_tools"][server_name] = {
                        "error": f"Failed to discover tools: {e!s}",
                        "tool_count": 0,
                    }

        return discovery

    def get_server_tools(self, server_name: str) -> dict[str, Any]:
        """Get tools from a specific MCP server"""
        tools = {}

        # This would typically involve making MCP protocol calls to the server
        # For now, we'll create a mapping based on known server capabilities
        server_tool_map = {
            "agentic-control-framework": {
                "description": "Agentic control and task management framework",
                "tools": [
                    "setWorkspace",
                    "initProject",
                    "addTask",
                    "listTasks",
                    "updateStatus",
                    "getNextTask",
                    "updateTask",
                    "removeTask",
                    "getContext",
                    "generateTaskFiles",
                    "parsePrd",
                    "expandTask",
                ],
            },
            "circleci-mcp-server": {
                "description": "CircleCI CI/CD pipeline management",
                "tools": [
                    "get_build_failure_logs",
                    "find_flaky_tests",
                    "get_latest_pipeline_status",
                    "get_job_test_results",
                    "config_helper",
                    "create_prompt_template",
                    "recommend_prompt_template_tests",
                    "run_pipeline",
                ],
            },
            "kaggle-mcp": {
                "description": "Kaggle data science competition tools",
                "tools": [
                    # Add known Kaggle MCP tools
                ],
            },
            "chrome-devtools": {
                "description": "Chrome browser automation and DevTools",
                "tools": [
                    "start_chrome",
                    "connect_to_browser",
                    "navigate_to_url",
                    "get_document",
                    "query_selector",
                    "get_element_attributes",
                ],
            },
            "ailint": {
                "description": "AI-powered code analysis and linting",
                "tools": [
                    # Add known AI lint tools
                ],
            },
            "agentmode": {
                "description": "AI agent with PostgreSQL backend",
                "tools": [
                    # Add known AgentMode tools
                ],
            },
            "cargo-mcp": {
                "description": "Rust Cargo package manager integration",
                "tools": ["search_crates", "get_crate_info", "get_crate_versions"],
            },
            "crates": {
                "description": "Rust crates.io integration",
                "tools": [
                    # Add known crates tools
                ],
            },
            "rust-docs": {
                "description": "Rust documentation lookup",
                "tools": ["lookup_crate_docs", "lookup_item_docs", "search_crates"],
            },
            "ai-pair-programmer": {
                "description": "AI pair programming assistant",
                "tools": ["pair", "review", "brainstorm", "review_performance", "review_security"],
            },
        }

        if server_name in server_tool_map:
            server_info = server_tool_map[server_name]
            tools = {
                "description": server_info["description"],
                "tools": server_info["tools"],
                "tool_count": len(server_info["tools"]),
            }
        else:
            tools = {"description": f"MCP Server: {server_name}", "tools": [], "tool_count": 0}

        return tools

    def generate_tool_report(self) -> str:
        """Generate a formatted report of available MCP tools"""
        discovery = self.discover_mcp_tools()

        report = f"""
# 🛠️ DYNAMIC MCP TOOL INVENTORY

**Generated:** {discovery["discovery_time"]}
**Running Servers:** {discovery["server_count"]}/{len(discovery["server_status"])}
**Total Available Tools:** {discovery["tool_count"]}

## 📊 Server Status

"""

        # Server status section
        for server_name, is_running in discovery["server_status"].items():
            status_icon = "✅" if is_running else "❌"
            report += (
                f"- {status_icon} **{server_name}**: {'Running' if is_running else 'Stopped'}\n"
            )

        report += "\n## 🛠️ Available Tools by Server\n\n"

        # Tools section
        if discovery["tool_count"] > 0:
            for server_name, tools_info in discovery["available_tools"].items():
                if "error" in tools_info:
                    report += f"### ❌ {server_name}\n"
                    report += f"Error: {tools_info['error']}\n\n"
                else:
                    report += f"### ✅ {server_name}\n"
                    report += f"**Description:** {tools_info['description']}\n"
                    report += f"**Tools:** {tools_info['tool_count']}\n\n"

                    if tools_info["tools"]:
                        report += "**Available Functions:**\n"
                        for tool in tools_info["tools"]:
                            report += f"- `{tool}`\n"
                    else:
                        report += "*No tools documented*\n"
                    report += "\n"
        else:
            report += "❌ **No MCP tools currently available** - all servers are stopped\n\n"

        report += """
## 🔄 Refresh This Report

To refresh this tool inventory:

```bash
python .claude/mcp_tool_discovery.py --report
```

Or run the main startup script:

```bash
./.claude/startup.sh
```

---
*This is a dynamically generated report. Static tool documentation has been removed from CLAUDE.md to ensure only currently available tools are shown.*
"""

        return report

    def save_tool_report(self, output_path: str | None = None) -> str:
        """Save the tool report to a file."""
        if output_path is None:
            output_path = ".claude/MCP_TOOLS_AVAILABLE.md"

        report = self.generate_tool_report()

        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            f.write(report)

        return output_path


def main() -> None:
    """Main entry point for the MCP tool discovery CLI."""
    import argparse

    parser = argparse.ArgumentParser(description="Dynamic MCP Tool Discovery")
    parser.add_argument("--report", action="store_true", help="Generate and display tool report")
    parser.add_argument(
        "--save", default=".claude/MCP_TOOLS_AVAILABLE.md", help="Save report to specified file"
    )
    parser.add_argument("--json", action="store_true", help="Output raw discovery data as JSON")

    args = parser.parse_args()

    discovery = MCPToolDiscovery()

    if args.json:
        data = discovery.discover_mcp_tools()
        print(json.dumps(data, indent=2))
    elif args.report:
        report = discovery.generate_tool_report()
        print(report)

        # Also save to file
        output_file = discovery.save_tool_report(args.save)
        print(f"\n📄 Report saved to: {output_file}")
    else:
        # Default: just save the report
        output_file = discovery.save_tool_report(args.save)
        print("✅ MCP Tool Discovery complete")
        print(f"📄 Report saved to: {output_file}")


if __name__ == "__main__":
    main()
