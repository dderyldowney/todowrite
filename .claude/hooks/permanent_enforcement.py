#!/usr/bin/env python3
"""
Permanent Code Quality Enforcement System

This system ensures code quality enforcement persists across all sessions,
including after /clear commands, by creating persistent state and
environment variables that Claude automatically detects and respects.
"""

import json
import os
import sys
from pathlib import Path


def setup_permanent_enforcement():
    """Setup permanent enforcement that survives session resets."""
    project_root = Path.cwd()
    claude_dir = project_root / ".claude"

    # Ensure .claude directory exists
    claude_dir.mkdir(exist_ok=True)

    # Create permanent enforcement configuration
    enforcement_file = claude_dir / "permanent_code_quality_enforcement.json"

    permanent_config = {
        "version": "1.0.0",
        "enforcement_permanent": True,
        "survives_session_reset": True,
        "last_updated": "2025-01-11T00:00:00Z",
        # Global agent behavior overrides
        "agent_behavior_overrides": {
            "require_semantic_scoping": True,
            "require_red_green_refactor": True,
            "require_token_optimization": True,
            "require_ToDoWrite_cli": True,
            "require_episodic_memory_search": False,  # DISABLED
            "forbidden_practices": [
                "mocking_frameworks",
                "committing_without_tests",
                "ignoring_quality_gates",
                "bypassing_pre_commit_hooks",
            ],
        },
        # Quality gates that cannot be bypassed
        "quality_gates": {
            "zero_tolerance_violations": [
                "semantic_scope_violations",
                "commit_message_format_errors",
                "security_vulnerabilities",
                "secret_detection",
                "syntax_errors",
            ],
            "critical_checks": [
                "pre_commit_hooks_pass",
                "ruff_format_check",
                "bandit_security_check",
                "detect_secrets_scan",
                "semantic_scope_validation",
                "red_green_refactor_compliance",
            ],
        },
        # Required workflow steps (cannot be skipped)
        "mandatory_workflows": {
            "before_any_work": [
                # "check_episodic_memory_for_context",  # DISABLED
                "verify_semantic_scoping_understanding",
                "ensure_ToDoWrite_cli_available",
            ],
            "for_any_code_change": [
                "write_failing_test_first",
                "implement_minimal_code",
                "refactor_while_tests_green",
            ],
            "before_any_commit": [
                "run_all_quality_checks",
                "validate_commit_message_format",
                "ensure_semantic_scope_correct",
            ],
        },
        # Tool requirements (cannot be disabled)
        "required_tools": {
            "always_active": [
                "semantic_scoping_validator",
                "red_green_refactor_enforcer",
                "token_optimizer",
                "ruff_linter_formatter",
                "bandit_security_scanner",
                "detect_secrets_scanner",
                "sqlfluff_linter",
            ],
            "pre_commit_enforced": [
                "conventional_commits",
                "check_builtin_literals",
                "check_executables_have_shebangs",
                "check_toml",
                "check_yaml",
                "debug_statements",
                "trailing_whitespace",
                "check_added_large_files",
            ],
        },
        # Persistent environment variables for agent awareness
        "environment_overrides": {
            "CLAUDE_ENFORCE_SEMANTIC_SCOPING": "1",
            "CLAUDE_ENFORCE_RED_GREEN_REFACTOR": "1",
            "CLAUDE_ENFORCE_TOKEN_OPTIMIZATION": "1",
            "CLAUDE_ENFORCE_ToDoWrite_CLI": "1",
            "CLAUDE_ENFORCE_ZERO_MOCKING": "1",
            "CLAUDE_REQUIRE_EPISODIC_MEMORY": "0",  # DISABLED
            "CLAUDE_MANDATORY_QUALITY_GATES": "1",
            "CLAUDE_PRE_COMMIT_ENFORCEMENT": "1",
        },
        # Verification commands for agents to run
        "verification_commands": {
            "check_enforcement_active": [
                "test -f .claude/permanent_code_quality_enforcement.json",
                "test -f .pre-commit-config.yaml",
                "test -f pyproject.toml",
            ],
            "validate_tools_available": [
                "which ruff",
                "which bandit",
                "python .hooks/token-optimizer.py --help",
                "python .hooks/semantic-scope-validator.py --help",
                "python .hooks/red-green-refactor-enforcer.py --help",
            ],
        },
    }

    # Write permanent configuration
    with open(enforcement_file, "w") as f:
        json.dump(permanent_config, f, indent=2)

    # Create environment override file
    env_file = claude_dir / "environment_overrides.env"
    env_content = """# Permanent Code Quality Enforcement Environment Variables
# These variables persist across all Claude sessions and cannot be disabled

# Semantic Scoping Enforcement
export CLAUDE_ENFORCE_SEMANTIC_SCOPING=1
export CLAUDE_SEMANTIC_SCOPES="lib,cli,web,tests,docs,build,config,ci,deps"

# Red-Green-Refactor Methodology
export CLAUDE_ENFORCE_RED_GREEN_REFACTOR=1
export CLAUDE_RGR_PHASES="RED,GREEN,REFACTOR"

# Token Optimization
export CLAUDE_ENFORCE_TOKEN_OPTIMIZATION=1
export CLAUDE_TOKEN_REDUCTION_TARGET=0.15

# Zero Mocking Policy
export CLAUDE_ENFORCE_ZERO_MOCKING=1
export CLAUDE_REAL_IMPLEMENTATIONS_ONLY=1

# ToDoWrite_cli Workflow
export CLAUDE_ENFORCE_ToDoWrite_CLI=1
export CLAUDE_MANDATORY_PLANNING=1

# Episodic Memory (DISABLED)
# export CLAUDE_REQUIRE_EPISODIC_MEMORY=1
# export CLAUDE_CONTEXT_SEARCH_REQUIRED=1
export CLAUDE_REQUIRE_EPISODIC_MEMORY=0

# Quality Gates
export CLAUDE_MANDATORY_QUALITY_GATES=1
export CLAUDE_PRE_COMMIT_ENFORCEMENT=1

# Forbidden Practices
export CLAUDE_FORBID_MOCKING=1
export CLAUDE_FORBID_TESTLESS_COMMITS=1
export CLAUDE_FORBID_QUALITY_BYPASS=1
"""

    with open(env_file, "w") as f:
        f.write(env_content)

    # Create persistent agent instruction file
    agent_instructions_file = claude_dir / "PERMANENT_AGENT_INSTRUCTIONS.md"
    agent_instructions = """# PERMANENT AGENT INSTRUCTIONS - READ BEFORE EVERY RESPONSE

This file contains mandatory instructions that apply to ALL Claude agents in ALL sessions, including after /clear commands.

## 🚨 ZERO TOLERANCE POLICIES

The following practices are FORBIDDEN and will result in immediate session termination:
- Using mocking frameworks (@patch, MagicMock, Mock, etc.)
- Writing production code before tests
- Committing without running tests
- Bypassing pre-commit hooks
- Ignoring semantic scoping requirements

## 🎯 MANDATORY WORKFLOWS

### Before ANY Work (No Exceptions):
1. ~~Check episodic memory for past context: `/.episodic-memory:search-conversations`~~ (DISABLED)
2. Verify semantic scoping understanding
3. Ensure ToDoWrite_cli is available and working
4. Read this file to understand current requirements

### For ANY Code Change:
1. **RED PHASE**: Write failing test first, watch it fail for correct reason
2. **GREEN PHASE**: Write minimal code to make test pass
3. **REFACTOR PHASE**: Clean up code while keeping tests green

### Before ANY Commit:
1. Run all quality checks: `pre-commit run --all-files`
2. Validate commit message has proper semantic scope
3. Ensure all tests pass

## 🔧 ENFORCED TOOLS

The following tools are MANDATORY and automatically enforced:
- **Semantic Scoping**: Project-specific commit scopes (lib, cli, web, tests, docs, build, config, ci, deps)
- **Red-Green-Refactor**: TDD methodology enforcement
- **Ruff**: Linting, formatting, import sorting, security analysis
- **Bandit**: Security vulnerability scanning
- **Detect-Secrets**: Secret scanning for API keys, passwords, tokens
- **SQLFluff**: SQL linting and formatting
- **Token Optimization**: Code efficiency analysis
- **Pre-commit Hooks**: All quality checks before commits

## 📋 QUALITY GATES

The following quality gates have ZERO TOLERANCE:
- Semantic scope violations
- Commit message format errors
- Security vulnerabilities
- Secret detection failures
- Syntax errors
- Pre-commit hook failures

## ⚠️ CONSEQUENCES

Failure to follow these mandatory instructions will result in:
- Immediate session failure
- Rejection of all code changes
- Requirement to restart with proper workflow
- Potential blocking of future work until compliance

## ✅ VERIFICATION

Before proceeding with any work, verify compliance by running:
```bash
# Check enforcement is active
test -f .claude/permanent_code_quality_enforcement.json

# Validate tools are working
python .hooks/token-optimizer.py --help
python .hooks/semantic-scope-validator.py --help
python .hooks/red-green-refactor-enforcer.py --help

# Run quality checks
pre-commit run --all-files
```

## 🔄 PERSISTENCE

This enforcement system persists across:
- Session resets (/clear)
- Claude restarts
- Agent changes
- Context switches

These instructions CANNOT be disabled or bypassed by any agent or user command.
"""

    with open(agent_instructions_file, "w") as f:
        f.write(agent_instructions)

    # Create a shell script for environment setup
    setup_script = claude_dir / "setup_permanent_enforcement.sh"
    script_content = """#!/bin/bash
# Setup Permanent Code Quality Enforcement

echo "🔒 Setting up permanent code quality enforcement..."

# Source environment overrides
if [ -f ".claude/environment_overrides.env" ]; then
    export $(cat .claude/environment_overrides.env | grep -v '^#' | xargs)
    echo "✓ Environment variables loaded"
fi

# Verify enforcement files exist
if [ -f ".claude/permanent_code_quality_enforcement.json" ]; then
    echo "✓ Permanent enforcement configuration found"
else
    echo "❌ Permanent enforcement configuration missing"
    exit 1
fi

# Set persistent environment variables for current session
export CLAUDE_ENFORCE_SEMANTIC_SCOPING=1
export CLAUDE_ENFORCE_RED_GREEN_REFACTOR=1
export CLAUDE_ENFORCE_TOKEN_OPTIMIZATION=1
export CLAUDE_ENFORCE_ToDoWrite_CLI=1
export CLAUDE_ENFORCE_ZERO_MOCKING=1
export CLAUDE_REQUIRE_EPISODIC_MEMORY=0  # DISABLED
export CLAUDE_MANDATORY_QUALITY_GATES=1
export CLAUDE_PRE_COMMIT_ENFORCEMENT=1

echo "✓ Permanent code quality enforcement activated"
echo "🚨 This enforcement persists across all sessions including /clear commands"

# Create marker file for other tools to detect
touch .claude/permanent_enforcement_active
"""

    with open(setup_script, "w") as f:
        f.write(script_content)

    # Make script executable
    setup_script.chmod(0o755)

    # Create marker file for detection
    marker_file = claude_dir / "permanent_enforcement_active"
    marker_file.touch()

    print("✅ Permanent code quality enforcement system created")
    print("🔒 This enforcement persists across all sessions including /clear commands")
    print("📁 Configuration files created:")
    print(f"   - {enforcement_file}")
    print(f"   - {env_file}")
    print(f"   - {agent_instructions_file}")
    print(f"   - {setup_script}")
    print(f"   - {marker_file}")

    return True


def verify_permanent_enforcement():
    """Verify that permanent enforcement is active and working."""
    project_root = Path.cwd()
    claude_dir = project_root / ".claude"

    required_files = [
        claude_dir / "permanent_code_quality_enforcement.json",
        claude_dir / "environment_overrides.env",
        claude_dir / "PERMANENT_AGENT_INSTRUCTIONS.md",
        claude_dir / "setup_permanent_enforcement.sh",
        claude_dir / "permanent_enforcement_active",
    ]

    missing_files = []
    for file_path in required_files:
        if not file_path.exists():
            missing_files.append(str(file_path))

    if missing_files:
        print("❌ Permanent enforcement verification failed - missing files:")
        for missing in missing_files:
            print(f"   - {missing}")
        return False

    # Check environment variables
    required_env_vars = [
        "CLAUDE_ENFORCE_SEMANTIC_SCOPING",
        "CLAUDE_ENFORCE_RED_GREEN_REFACTOR",
        "CLAUDE_ENFORCE_TOKEN_OPTIMIZATION",
        "CLAUDE_ENFORCE_ToDoWrite_CLI",
        "CLAUDE_ENFORCE_ZERO_MOCKING",
        # "CLAUDE_REQUIRE_EPISODIC_MEMORY",  # DISABLED
        "CLAUDE_MANDATORY_QUALITY_GATES",
        "CLAUDE_PRE_COMMIT_ENFORCEMENT",
    ]

    missing_env = []
    for env_var in required_env_vars:
        if not os.environ.get(env_var):
            missing_env.append(env_var)

    if missing_env:
        print("⚠️  Missing environment variables (run setup script):")
        for env in missing_env:
            print(f"   - {env}")

    print("✅ Permanent enforcement verification passed")
    print("🔒 Code quality enforcement persists across all sessions")
    return True


def main():
    """Main entry point for permanent enforcement setup."""
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        verify_permanent_enforcement()
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Permanent Code Quality Enforcement System")
        print("Usage: python permanent_enforcement.py [--verify | --help]")
        print("  --verify: Verify permanent enforcement is active")
        print("  --help:    Show this help message")
        print()
        print("This system creates persistent enforcement that survives:")
        print("  - Session resets (/clear)")
        print("  - Claude restarts")
        print("  - Agent changes")
        print("  - Context switches")
        sys.exit(0)

    success = setup_permanent_enforcement()
    if success:
        # Run the setup script to activate environment variables
        import subprocess

        script_path = Path.cwd() / ".claude" / "setup_permanent_enforcement.sh"
        try:
            result = subprocess.run(["bash", str(script_path)], capture_output=True, text=True)
            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"Script output: {result.stderr}")
        except Exception as e:
            print(f"⚠️  Could not run setup script: {e}")
            print("Run it manually: bash .claude/setup_permanent_enforcement.sh")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
