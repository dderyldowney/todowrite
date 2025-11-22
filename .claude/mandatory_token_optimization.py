#!/usr/bin/env python3
"""
Mandatory Token Optimization Enforcement
Enforces HAL preprocessing, CLI tool usage, and adaptive limits across all packages
"""

import json
import os
import sys
from pathlib import Path


class MandatoryTokenOptimization:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.config = self._load_config()

    def _load_config(self):
        """Load mandatory optimization configuration"""
        config_file = (
            self.project_root / "dev_tools" / "token_optimization" / ".token_optimized_config.yaml"
        )

        # Default configuration with mandatory settings
        return {
            "max_allowed_tokens": 40000,
            "hal_preprocessing_mandatory": True,
            "cli_tools_mandatory": True,
            "adaptive_limits_enabled": True,
            "package_limits": {
                "lib_package": {"max_files": 150, "max_context_chars": 3000, "context_lines": 5},
                "cli_package": {"max_files": 100, "max_context_chars": 2000, "context_lines": 3},
                "web_package": {"max_files": 120, "max_context_chars": 2500, "context_lines": 4},
                "root": {"max_files": 100, "max_context_chars": 2000, "context_lines": 3},
            },
            "mandatory_cli_tools": [
                # File Reading/Viewing
                "cat",
                "head",
                "tail",
                "less",
                "more",
                "bat",
                "tac",
                "nl",
                # File Searching/Filtering
                "grep",
                "egrep",
                "fgrep",
                "rg",
                "ag",
                "find",
                "locate",
                "which",
                "awk",
                "sed",
                "sort",
                "uniq",
                "cut",
                "tr",
                "wc",
                "ls",
                "tree",
                # File Manipulation
                "touch",
                "mkdir",
                "rm",
                "rmdir",
                "mv",
                "cp",
                "ln",
                "chmod",
                "chown",
                "dd",
                "split",
                "csplit",
                "fmt",
                "fold",
                "pr",
                "expand",
                "unexpand",
                # Text Processing
                "awk",
                "sed",
                "tr",
                "cut",
                "paste",
                "join",
                "comm",
                "diff",
                "patch",
                "cmp",
                "sdiff",
                "vimdiff",
                "iconv",
                "dos2unix",
                "unix2dos",
                # Data Processing
                "jq",
                "yq",
                "xmlstarlet",
                "tidy",
                "csvkit",
                "mlr",
                "datamash",
                # Archive Tools
                "tar",
                "gzip",
                "gunzip",
                "zip",
                "unzip",
                "compress",
                "uncompress",
                "bzip2",
                "bunzip2",
                "xz",
                "unxz",
                "7z",
                "ar",
                "cpio",
                # System Tools
                "ps",
                "top",
                "htop",
                "lsof",
                "netstat",
                "ss",
                "df",
                "du",
                "free",
                "uptime",
                "date",
                "who",
                "w",
                "id",
                "uname",
                "env",
                "printenv",
                # Process Management
                "kill",
                "killall",
                "pkill",
                "jobs",
                "bg",
                "fg",
                "nohup",
                "nice",
                "renice",
                "time",
                "timeout",
                "watch",
                "screen",
                "tmux",
                # Network Tools
                "curl",
                "wget",
                "nc",
                "telnet",
                "ssh",
                "scp",
                "rsync",
                "ping",
                "traceroute",
                "dig",
                "nslookup",
                "host",
                "nmap",
                # Development Tools
                "git",
                "make",
                "cmake",
                "gcc",
                "g++",
                "clang",
                "python",
                "python3",
                "pip",
                "pip3",
                "npm",
                "yarn",
                "node",
                "cargo",
                "rustc",
                "go",
                "java",
                "javac",
                "mvn",
                "gradle",
                "docker",
                "kubectl",
                "helm",
                # Filesystem Tools
                "mount",
                "umount",
                "fsck",
                "e2fsck",
                "xfs_repair",
                "fdisk",
                "parted",
                "lsblk",
                "blkid",
                "file",
                "stat",
                "du",
                "df",
                "quota",
                "repquota",
                # Text Editors (when Edit tool would be used)
                "vim",
                "vi",
                "emacs",
                "nano",
                "micro",
                "code",
                "subl",
                "atom",
                # Shell Programming
                "bash",
                "zsh",
                "fish",
                "sh",
                "dash",
                "ksh",
                "tcsh",
                "csh",
                # Miscellaneous
                "tee",
                "xargs",
                "parallel",
                "script",
                "scriptreplay",
                "tput",
                "stty",
                "tty",
                "mesg",
                "write",
                "wall",
                "logger",
                "logrotate",
            ],
        }

    def enforce_mandatory_optimization(self):
        """Enforce all mandatory optimization settings"""
        print("🔧 ENFORCING MANDATORY TOKEN OPTIMIZATION")

        # 1. Set MAX ALLOWED TOKENS to 40000
        self._enforce_token_limit()

        # 2. Enable HAL preprocessing system-wide
        self._enable_hal_preprocessing()

        # 3. Mandate CLI tools over internal operations
        self._mandate_cli_tools()

        # 4. Apply adaptive package limits
        self._apply_adaptive_limits()

        print("✅ All mandatory optimizations enforced")

    def _enforce_token_limit(self):
        """Set max allowed tokens to 40000"""
        print("📊 Setting MAX ALLOWED TOKENS to 40000...")

        # Update environment
        os.environ["CLAUDE_MAX_TOKENS"] = "40000"
        os.environ["MAX_ALLOWED_TOKENS"] = "40000"

        # Update configuration files
        self._update_token_configs()

    def _enable_hal_preprocessing(self):
        """Enable HAL preprocessing for all file operations"""
        print("🔧 Enabling HAL preprocessing system-wide...")

        os.environ["HAL_PREPROCESSING_MANDATORY"] = "true"
        os.environ["HAL_PREPROCESSING_ENABLED"] = "true"

        # Create HAL preprocessing wrapper for common operations
        self._create_hal_wrapper()

    def _mandate_cli_tools(self):
        """Make CLI tools mandatory over internal Read/Edit operations"""
        print("⚡ Mandating CLI tools over internal operations...")

        os.environ["CLI_TOOLS_MANDATORY"] = "true"
        os.environ["READ_TOOL_RESTRICTED"] = "true"
        os.environ["EDIT_TOOL_RESTRICTED"] = "true"

        # Create CLI tool enforcement scripts
        self._create_cli_enforcement()

    def _apply_adaptive_limits(self):
        """Apply adaptive limits based on package context"""
        print("📦 Applying adaptive package limits...")

        current_dir = Path.cwd()
        package_context = self._detect_package_context(current_dir)

        limits = self.config["package_limits"][package_context]
        print(f"🎯 Package: {package_context}, Limits: {limits}")

        # Set environment variables for current package
        os.environ["PACKAGE_CONTEXT"] = package_context
        os.environ["MAX_FILES"] = str(limits["max_files"])
        os.environ["MAX_CONTEXT_CHARS"] = str(limits["max_context_chars"])
        os.environ["CONTEXT_LINES"] = str(limits["context_lines"])

    def _detect_package_context(self, cwd):
        """Detect which package context we're in"""
        if "lib_package" in cwd.parts:
            return "lib_package"
        elif "cli_package" in cwd.parts:
            return "cli_package"
        elif "web_package" in cwd.parts:
            return "web_package"
        else:
            return "root"

    def _update_token_configs(self):
        """Update all relevant configuration files with new token limits"""
        config_updates = [
            ".claude/mcp_config_2025.json",
            ".claude/mcp_superpowers_config_2025.json",
            "dev_tools/token_optimization/.token_optimized_config.yaml",
        ]

        for config_file in config_updates:
            config_path = self.project_root / config_file
            if config_path.exists():
                self._update_json_config(config_path, "max_allowed_tokens", 40000)

    def _update_json_config(self, config_path, key, value):
        """Update a JSON configuration file"""
        try:
            with open(config_path) as f:
                config = json.load(f)

            # Handle nested keys
            if "." in key:
                keys = key.split(".")
                current = config
                for k in keys[:-1]:
                    if k not in current:
                        current[k] = {}
                    current = current[k]
                current[keys[-1]] = value
            else:
                config[key] = value

            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)

            print(f"  ✅ Updated {config_path}")
        except Exception as e:
            print(f"  ❌ Failed to update {config_path}: {e}")

    def _create_hal_wrapper(self):
        """Create HAL preprocessing wrapper script"""
        wrapper_content = """#!/bin/bash
# HAL Preprocessing Wrapper - MANDATORY for all file operations

# Check if HAL preprocessing is enabled
if [[ "$HAL_PREPROCESSING_MANDATORY" != "true" ]]; then
    echo "❌ HAL preprocessing is MANDATORY. Enable with HAL_PREPROCESSING_MANDATORY=true"
    exit 1
fi

# Detect package context
PACKAGE_CONTEXT=${PACKAGE_CONTEXT:-root}
MAX_FILES=${MAX_FILES:-100}
MAX_CONTEXT_CHARS=${MAX_CONTEXT_CHARS:-2000}

# Run HAL preprocessor
python3 .claude/hal_preprocessor.py "$@" --package-context "$PACKAGE_CONTEXT" --max-files "$MAX_FILES" --max-chars "$MAX_CONTEXT_CHARS"
"""

        wrapper_path = self.project_root / ".claude" / "hal_wrapper.sh"
        with open(wrapper_path, "w") as f:
            f.write(wrapper_content)

        # Make executable
        wrapper_path.chmod(0o755)
        print("  ✅ Created HAL preprocessing wrapper")

    def _create_cli_enforcement(self):
        """Create CLI tool enforcement configuration"""
        enforcement_config = {
            "mandatory_cli_tools": self.config["mandatory_cli_tools"],
            "restricted_tools": ["Read", "Edit"],
            "cli_tool_preferences": {
                "file_reading": ["cat", "head", "tail", "less", "more", "bat"],
                "file_searching": ["grep", "find", "rg", "ag", "locate"],
                "file_editing": ["sed", "awk", "vim", "nano", "micro"],
                "file_analysis": ["wc", "sort", "uniq", "cut", "tr"],
                "archive_operations": ["tar", "zip", "unzip", "gzip", "gunzip"],
                "process_management": ["ps", "top", "htop", "kill", "killall"],
                "network_operations": ["curl", "wget", "nc", "ping", "dig"],
                "development_operations": ["git", "make", "gcc", "python", "docker"],
            },
            "enforcement_rules": [
                "ALWAYS prefer CLI tools over Read tool",
                "ALWAYS use sed/awk/vim for simple edits over Edit tool",
                "ONLY use Read/Edit when CLI tools cannot accomplish the task",
                "HAL preprocessing MUST run before any file operations",
                "Use appropriate CLI tools for specific tasks (grep for search, sed for edit)",
                "Leverage specialized tools (jq for JSON, xmlstarlet for XML)",
                "Use process management tools (ps, top) instead of internal monitoring",
                "Utilize network tools (curl, wget) for HTTP operations",
            ],
        }

        config_path = self.project_root / ".claude" / "mandatory_cli_enforcement.json"
        with open(config_path, "w") as f:
            json.dump(enforcement_config, f, indent=2)

        print("  ✅ Created CLI enforcement configuration")


def main():
    """Main enforcement function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        # Check if optimizations are properly enforced
        required_vars = [
            "CLAUDE_MAX_TOKENS",
            "MAX_ALLOWED_TOKENS",
            "HAL_PREPROCESSING_MANDATORY",
            "CLI_TOOLS_MANDATORY",
        ]

        missing = [var for var in required_vars if var not in os.environ]
        if missing:
            print(f"❌ Missing mandatory environment variables: {missing}")
            sys.exit(1)

        expected_tokens = "40000"
        actual_tokens = os.environ.get("CLAUDE_MAX_TOKENS", "")
        if actual_tokens != expected_tokens:
            print(
                f"❌ Token limit not set correctly: expected {expected_tokens}, got {actual_tokens}"
            )
            sys.exit(1)

        print("✅ All mandatory optimizations are properly enforced")
        return

    # Run enforcement
    enforcer = MandatoryTokenOptimization()
    enforcer.enforce_mandatory_optimization()


if __name__ == "__main__":
    main()
