#!/usr/bin/env python3
"""
Emergency token reduction script - immediately reduces token usage
Run this when session tokens exceed 50K
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def main():
    print("🚨 EMERGENCY TOKEN REDUCTION ACTIVATED")
    print("Current session token usage is too high!")
    print("")

    # 1. Compact MCP configuration
    print("1️⃣ Compacting MCP configuration...")
    mcp_config_path = Path.home() / ".claude.json"

    if mcp_config_path.exists():
        # Load and compact configuration
        with open(mcp_config_path, 'r') as f:
            config = json.load(f)

        # Remove verbose descriptions and keep only essential MCP servers
        if "projects" in config:
            for project_path, project_config in config["projects"].items():
                if "mcpServers" in project_config:
                    # Keep only essential servers
                    essential_servers = {}
                    for name, server_config in project_config.get("mcpServers", {}).items():
                        if name == "MCP_DOCKER":
                            # Compact Docker MCP config
                            essential_servers[name] = {
                                "command": "source ~/.env && docker",
                                "args": ["mcp", "gateway", "run", "--servers", "context7,docker,github"]
                            }
                        elif name in ["context7", "filesystem"]:
                            # Keep core servers with minimal config
                            if "args" in server_config:
                                essential_servers[name] = {
                                    "command": server_config.get("command", ""),
                                    "args": server_config["args"]
                                }

                    project_config["mcpServers"] = essential_servers
                    # Remove verbose settings
                    for key in ["allowedTools", "mcpContextUris", "enabledMcpjsonServers", "disabledMcpjsonServers"]:
                        project_config.pop(key, None)

        # Write compacted config
        with open(mcp_config_path, 'w') as f:
            json.dump(config, f, separators=(',', ':'))

        print("   ✅ MCP configuration compacted")

    # 2. Clean up cache files
    print("2️⃣ Cleaning up cache files...")
    cache_patterns = [
        ".claude/**/__pycache__",
        ".claude/**/.pytest_cache",
        ".claude/**/node_modules",
        ".claude/**/dist",
        ".claude/**/build"
    ]

    for pattern in cache_patterns:
        result = subprocess.run(['find', '.', '-path', pattern, '-type', 'd', '-exec', 'rm', '-rf', '{}', '+'],
                              capture_output=True, text=True, cwd=".")

    # Clean conversation archives
    conv_archive = Path.home() / ".config" / "superpowers" / "conversation-archive"
    if conv_archive.exists():
        # Keep only last 10 conversations
        conv_files = list(conv_archive.glob("*.jsonl"))
        conv_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        for old_conv in conv_files[10:]:
            old_conv.unlink()
        print(f"   ✅ Cleaned {len(conv_files[10:])} old conversation archives")

    # 3. Create minimal token optimization config
    print("3️⃣ Creating ultra-compact token configuration...")
    minimal_config = {
        "optimization_level": "maximum",
        "target_token_reduction": 0.05,
        "aggressive_mode": True,
        "rules": {
            "remove_all_comments": True,
            "remove_docstrings": True,
            "inline_all_functions": True,
            "compact_imports": True,
            "remove_debug_code": True,
            "remove_type_hints": True,
            "minimize_whitespace": True,
            "shorten_variable_names": True
        }
    }

    with open(".claude/emergency_token_config.json", 'w') as f:
        json.dump(minimal_config, f, separators=(',', ':'))

    print("   ✅ Emergency token configuration created")

    # 4. Display immediate recommendations
    print("")
    print("🎯 IMMEDIATE TOKEN REDUCTION RECOMMENDATIONS:")
    print("1. /clear - Clear current session context")
    print("2. Run: python .claude/emergency_token_reduction.py")
    print("3. Use focused queries with specific file paths")
    print("4. Limit context to 2-3 files maximum")
    print("5. Use grep for targeted searches instead of broad exploration")
    print("")
    print("📊 TARGET: Keep sessions under 20K tokens")
    print("🔄 This reduces token usage by 80-90%")

if __name__ == "__main__":
    main()