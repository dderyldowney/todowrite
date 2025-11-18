#!/usr/bin/env python3
"""
Session initialization hook for agricultural robotics development.

Manages session markers and agent registry for coordinated
multi-agent development sessions with ISO compliance tracking.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path


def get_session_root():
    """Get the session root directory."""
    return Path.cwd()


def create_session_markers():
    """Create session markers for new session detection."""
    session_root = get_session_root()
    session_dir = session_root / ".claude"
    session_dir.mkdir(exist_ok=True)

    # Create session start marker
    start_marker = session_dir / "session_start.json"
    session_data = {
        "start_time": datetime.now().isoformat(),
        "agent": "claude-code",
        "session_type": "development",
    }

    with open(start_marker, "w") as f:
        json.dump(session_data, f, indent=2)

    # Create session heartbeat marker
    heartbeat_marker = session_dir / "session_heartbeat.json"
    heartbeat_data = {
        "last_heartbeat": datetime.now().isoformat(),
        "agent": "claude-code",
        "status": "active",
    }

    with open(heartbeat_marker, "w") as f:
        json.dump(heartbeat_data, f, indent=2)


def check_session_freshness():
    """Check if session markers are fresh (within 5 minutes)."""
    session_root = get_session_root()
    session_dir = session_root / ".claude"

    heartbeat_marker = session_dir / "session_heartbeat.json"

    if not heartbeat_marker.exists():
        return False

    try:
        with open(heartbeat_marker) as f:
            heartbeat_data = json.load(f)

        last_heartbeat = datetime.fromisoformat(heartbeat_data["last_heartbeat"])
        time_diff = datetime.now() - last_heartbeat

        return time_diff < timedelta(minutes=5)

    except (json.JSONDecodeError, KeyError, ValueError):
        return False


def update_heartbeat():
    """Update the session heartbeat."""
    session_root = get_session_root()
    session_dir = session_root / ".claude"
    heartbeat_marker = session_dir / "session_heartbeat.json"

    heartbeat_data = {
        "last_heartbeat": datetime.now().isoformat(),
        "agent": "claude-code",
        "status": "active",
    }

    with open(heartbeat_marker, "w") as f:
        json.dump(heartbeat_data, f, indent=2)


def register_agent():
    """Register agent in the agent registry."""
    session_root = get_session_root()
    session_dir = session_root / ".claude"
    registry_file = session_dir / "agent_registry.json"

    registry = {}
    if registry_file.exists():
        try:
            with open(registry_file) as f:
                registry = json.load(f)
        except json.JSONDecodeError:
            registry = {}

    registry["claude-code"] = {
        "last_seen": datetime.now().isoformat(),
        "agent_type": "development",
        "capabilities": ["code-generation", "test-fixing", "documentation"],
        "workflow_enforcement": {
            "requires_ToDoWrite_cli": True,
            "planning_required": True,
            "token_optimization": True,
        },
    }

    with open(registry_file, "w") as f:
        json.dump(registry, f, indent=2)


def enforce_ToDoWrite_cli_workflow():
    """Enforce ToDoWrite_cli usage for all planning and implementation."""
    session_root = get_session_root()
    session_dir = session_root / ".claude"
    workflow_file = session_dir / "workflow_enforcement.json"

    workflow_config = {
        "ToDoWrite_cli_required": True,
        "planning_steps": [
            "Use ToDoWrite_cli to create tasks for all work",
            "Check episodic memory for past context",
            "Plan implementation using ToDoWrite_cli",
            "Execute work with ToDoWrite_cli tracking",
        ],
        "enforcement_time": datetime.now().isoformat(),
        "token_optimization_active": True,
    }

    with open(workflow_file, "w") as f:
        json.dump(workflow_config, f, indent=2)

    print("✓ ToDoWrite_cli workflow enforcement activated")
    return True


def enforce_comprehensive_code_quality():
    """Activate comprehensive code quality enforcement across all tools."""
    session_root = get_session_root()
    session_dir = session_root / ".claude"
    quality_config_file = session_dir / "comprehensive_quality_enforcement.json"

    # Updated comprehensive quality configuration with all new tools
    quality_config = {
        "enforcement_level": "strict",
        "enforcement_time": datetime.now().isoformat(),
        "tools": {
            "semantic_scoping": {
                "active": True,
                "enforced_via": "pre_commit_hooks",
                "configuration": ".hooks/semantic-scope-validator.py",
                "description": "Project-specific commit message scoping (lib, cli, web, tests, docs, build, config, ci, deps)",
            },
            "red_green_refactor": {
                "active": True,
                "enforced_via": "pre_commit_hooks",
                "configuration": ".hooks/red-green-refactor-enforcer.py",
                "description": "TDD methodology enforcement (RED test, GREEN code, REFACTOR clean)",
            },
            "ruff": {
                "active": True,
                "enforced_via": "pre_commit_hooks",
                "configuration": "pyproject.toml",
                "description": "Comprehensive Python linting, formatting, import sorting, security analysis",
                "features": [
                    "Linting with comprehensive rule set",
                    "Code formatting with consistent style",
                    "Import sorting and organization",
                    "Security vulnerability detection",
                    "E402: module import enforcement",
                    "PLC0415: import location enforcement",
                ],
            },
            "bandit": {
                "active": True,
                "enforced_via": "pre_commit_hooks",
                "configuration": "pyproject.toml",
                "description": "Security-focused static analysis for common vulnerabilities",
            },
            "detect_secrets": {
                "active": True,
                "enforced_via": "pre_commit_hooks",
                "configuration": ".secrets.baseline",
                "description": "Secret scanning to prevent API keys, passwords, tokens from being committed",
            },
            "sqlfluff": {
                "active": True,
                "enforced_via": "pre_commit_hooks",
                "configuration": ".sqlfluff-config",
                "description": "SQL linting and formatting for database consistency",
            },
            "token_optimization": {
                "active": True,
                "enforced_via": "pre_commit_hooks",
                "configuration": ".hooks/token-optimizer.py",
                "description": "Token usage analysis and optimization for AI model efficiency",
                "features": [
                    "Redundant comment removal",
                    "Verbose docstring simplification",
                    "Unused import detection",
                    "Simple function inlining opportunities",
                    "Code structure optimization",
                ],
            },
            "conventional_commits": {
                "active": True,
                "enforced_via": "pre_commit_hooks",
                "configuration": "commitizen + custom validators",
                "description": "Standardized commit message format (type(scope): description)",
            },
            "pre_commit_hooks": {
                "active": True,
                "enforced_via": "git_hooks",
                "configuration": ".pre-commit-config.yaml",
                "description": "Automated code quality checks before commits",
                "hooks": [
                    "check-builtin-literals",
                    "check-executables-have-shebangs",
                    "check-toml",
                    "check-yaml",
                    "debug-statements",
                    "trailing-whitespace",
                    "end-of-file-fixer",
                    "check-added-large-files",
                    "check-json",
                    "check-xml",
                    "check-ast",
                    "check-case-conflict",
                    "check-docstring-first",
                    "check-shebang-scripts-are-executable",
                ],
            },
        },
        "quality_gates": {
            "zero_tolerance_violations": [
                "semantic_scope_violations",
                "commit_message_format_errors",
                "security_vulnerabilities",
                "secret_detection",
                "syntax_errors",
            ],
            "warning_thresholds": {
                "token_inefficiency": 0.15,  # 15% threshold for token optimization
                "code_complexity": 10,
                "file_size_mb": 1.0,
            },
        },
        "agent_requirements": {
            "mandatory_workflows": [
                "episodic_memory_search_before_work",
                "semantic_scoping_awareness",
                "red_green_refactor_methodology",
                "token_optimization_consideration",
                "ToDoWrite_cli_usage",
            ],
            "forbidden_practices": [
                "mocking_frameworks",
                "committing_without_tests",
                "ignoring_quality_gates",
                "bypassing_pre_commit_hooks",
            ],
        },
        "verification_commands": {
            "pre_commit_install": "pre-commit install",
            "run_all_checks": "pre-commit run --all-files",
            "token_analysis": ".hooks/token-optimizer.py --report",
            "secret_scan": "detect-secrets scan --baseline .secrets.baseline",
            "sql_linting": "sqlfluff lint",
            "security_audit": "bandit -r .",
            "code_quality": "ruff check . && ruff format .",
        },
    }

    with open(quality_config_file, "w") as f:
        json.dump(quality_config, f, indent=2)

    print("✓ Comprehensive code quality enforcement activated")
    print("  - Semantic scoping: ENFORCED")
    print("  - Red-Green-Refactor: ENFORCED")
    print("  - Ruff (lint/format/sort): ENFORCED")
    print("  - Bandit (security): ENFORCED")
    print("  - Detect-secrets: ENFORCED")
    print("  - SQLFluff: ENFORCED")
    print("  - Token optimization: ENFORCED")
    print("  - Conventional commits: ENFORCED")
    print("  - All pre-commit hooks: ENFORCED")
    return True


def activate_permanent_enforcement():
    """Activate permanent enforcement that survives /clear commands."""
    project_root = get_session_root()
    autorun_script = project_root / ".claude" / "autorun.py"

    if autorun_script.exists():
        try:
            import subprocess

            result = subprocess.run(
                ["python", str(autorun_script)], capture_output=True, text=True, cwd=project_root
            )
            if result.stdout:
                print(result.stdout.strip())
        except Exception as e:
            print(f"⚠️  Could not activate permanent enforcement: {e}")


def main():
    """Main session initialization logic."""
    # Always activate permanent enforcement first
    activate_permanent_enforcement()

    if check_session_freshness():
        update_heartbeat()
        print("Session active - heartbeat updated")
        enforce_ToDoWrite_cli_workflow()
        enforce_comprehensive_code_quality()
        return 0
    create_session_markers()
    register_agent()
    enforce_ToDoWrite_cli_workflow()
    enforce_comprehensive_code_quality()
    print("New session initialized with comprehensive code quality enforcement")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
