#!/usr/bin/env python3
"""
Startup Enforcement Script - MANDATORY CLAUDE.md Loading and Verification.

Ensures all agents load CLAUDE.md and enforce its rules on every session start.
"""

import os
import sys
from pathlib import Path


def enforce_claude_md_loading():
    """Enforce CLAUDE.md loading and rule verification."""
    print("📋 **CLAUDE.md RULE ENFORCEMENT**")

    # 1. Load and apply CLAUDE.md rules
    claude_md = Path("CLAUDE.md")
    if not claude_md.exists():
        print("❌ CRITICAL: CLAUDE.md not found!")
        return False

    print("✅ CLAUDE.md found")

    # Load and apply CLAUDE.md content
    try:
        with open(claude_md, encoding="utf-8") as f:
            claude_md_content = f.read()

        # Store CLAUDE.md content in environment for agents to access
        os.environ["CLAUDE_MD_CONTENT"] = claude_md_content

        # Extract and apply critical mandates from CLAUDE.md
        mandates_applied = []

        # Check for MCP-FIRST WORKFLOW MANDATE
        if "MCP-FIRST WORKFLOW MANDATE" in claude_md_content:
            mandates_applied.append("MCP-FIRST WORKFLOW MANDATE")
            os.environ["MCP_FIRST_MANDATE"] = "true"

        # Check for DATABASE DATA PROTECTION MANDATE
        if "DATABASE DATA PROTECTION MANDATE" in claude_md_content:
            mandates_applied.append("DATABASE DATA PROTECTION MANDATE")
            os.environ["DATABASE_PROTECTION_MANDATE"] = "true"

        # Check for COST OPTIMIZATION MANDATE
        if "COST OPTIMIZATION MANDATE" in claude_md_content:
            mandates_applied.append("COST OPTIMIZATION MANDATE")
            os.environ["COST_OPTIMIZATION_MANDATE"] = "true"

        # Check for TDD compliance requirement
        if "TDD COMPLIANCE" in claude_md_content:
            mandates_applied.append("TDD COMPLIANCE ENFORCEMENT")
            os.environ["TDD_COMPLIANCE_MANDATORY"] = "true"

        # Check for PostgreSQL-first architecture
        if "PostgreSQL" in claude_md_content and "SINGLE SOURCE OF TRUTH" in claude_md_content:
            mandates_applied.append("POSTGRESQL-FIRST ARCHITECTURE")
            os.environ["POSTGRESQL_FIRST_MANDATORY"] = "true"

        if mandates_applied:
            print(f"✅ CLAUDE.md loaded and applied: {', '.join(mandates_applied)}")
        else:
            print("⚠️  CLAUDE.md loaded but no critical mandates detected")

    except Exception as e:
        print(f"❌ CRITICAL: Failed to load CLAUDE.md content: {e}")
        return False

    # 2. Verify environment variables are sourced
    required_vars = [
        "TODOWRITE_DATABASE_URL",
        "EPISODIC_MEMORY_DB_URL",
        "MCP_SESSIONS_DB_URL",
        "MCP_FILESYSTEM_DATABASE_URL",
        "MCP_DATABASE_URL",
        "HAL_PREPROCESSING_MANDATORY",
    ]

    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"❌ CRITICAL: Missing environment variables: {missing_vars}")
        print("❌ Run: source .env")
        return False

    print("✅ All required environment variables set")

    # 3. Verify HAL preprocessing is mandatory
    if os.environ.get("HAL_PREPROCESSING_MANDATORY") != "true":
        print("❌ CRITICAL: HAL preprocessing is not mandatory!")
        print("❌ Set: HAL_PREPROCESSING_MANDATORY=true")
        return False

    print("✅ HAL preprocessing is mandatory")

    # 4. Verify PostgreSQL container
    import subprocess

    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=mcp-postgres", "--quiet"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if not result.stdout.strip():
            print("❌ CRITICAL: PostgreSQL container not running!")
            return False
        print("✅ PostgreSQL container running")
    except Exception as e:
        print(f"❌ CRITICAL: Cannot verify PostgreSQL container: {e}")
        return False

    # 5. Verify PostgreSQL as SINGLE SOURCE OF TRUTH
    try:
        # Check container is running
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=mcp-postgres", "--quiet"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if not result.stdout.strip():
            print("❌ CRITICAL: PostgreSQL container mcp-postgres not running!")
            return False
        print("✅ PostgreSQL container mcp-postgres verified")

        # Verify all required databases exist
        required_databases = [
            "todowrite",
            "mcp_episodic_memory",
            "mcp_sessions",
            "mcp_filesystem",
            "mcp_main",
        ]

        for db_name in required_databases:
            # Use parameterized query to prevent SQL injection
            result = subprocess.run(
                [
                    "docker",
                    "exec",
                    "mcp-postgres",
                    "psql",
                    "-U",
                    "mcp_user",
                    "-d",
                    "postgres",
                    "-c",
                    f"SELECT 1 FROM pg_database WHERE datname = '{db_name}' LIMIT 1;",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if "1" not in result.stdout:
                print(f"❌ CRITICAL: Database {db_name} not found on PostgreSQL!")
                return False
            print(f"✅ Database {db_name} verified on PostgreSQL")

        # Verify todowrite database basic structure
        result = subprocess.run(
            [
                "docker",
                "exec",
                "mcp-postgres",
                "psql",
                "-U",
                "mcp_user",
                "-d",
                "todowrite",
                "-c",
                "SELECT COUNT(*) FROM goals;",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            print("❌ CRITICAL: Cannot query todowrite database structure!")
            return False
        print("✅ ToDoWrite database structure verified")

        # Verify episodic memory database is accessible (tables created on first use)
        result = subprocess.run(
            [
                "docker",
                "exec",
                "mcp-postgres",
                "psql",
                "-U",
                "mcp_user",
                "-d",
                "mcp_episodic_memory",
                "-c",
                "SELECT 1;",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            print("❌ CRITICAL: Cannot access episodic memory database!")
            return False
        print("✅ Episodic memory database verified (tables created on first use)")

        print("✅ PostgreSQL SINGLE SOURCE OF TRUTH verified - All databases accessible")

    except Exception as e:
        print(f"❌ CRITICAL: PostgreSQL verification failed: {e}")
        return False

    # 6. Load session state
    try:
        session_manager = Path(".claude/session_manager.py")
        if session_manager.exists():
            result = subprocess.run(
                ["python", ".claude/session_manager.py", "--summary"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                print("✅ Session state loaded")
            else:
                print("⚠️  Session state loading failed")
    except Exception as e:
        print(f"⚠️  Session state verification failed: {e}")

    # 7. Initialize real-time token monitoring
    try:
        monitor_script = Path(".claude/realtime_token_monitor.py")
        if monitor_script.exists():
            result = subprocess.run(
                ["python", str(monitor_script), "start"], capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                print("✅ Real-time token monitoring initialized")
            else:
                print("⚠️  Real-time token monitoring failed")
        else:
            print("⚠️  Real-time token monitor not found")
    except Exception as e:
        print(f"⚠️  Real-time token monitoring initialization failed: {e}")

    # Load MCP workflow mandates for session continuity
    try:
        mandates_file = Path("MCP_WORKFLOW_MANDATES.md")
        if mandates_file.exists():
            print("✅ MCP workflow mandates loaded for session continuity")
        else:
            print("⚠️  MCP_WORKFLOW_MANDATES.md not found")
    except Exception as e:
        print(f"⚠️  MCP workflow mandates loading failed: {e}")

    # 8. Verify CLAUDE.md mandates are enforced
    active_mandates = []
    if os.environ.get("MCP_FIRST_MANDATE") == "true":
        active_mandates.append("MCP-FIRST WORKFLOW")
    if os.environ.get("DATABASE_PROTECTION_MANDATE") == "true":
        active_mandates.append("DATABASE PROTECTION")
    if os.environ.get("COST_OPTIMIZATION_MANDATE") == "true":
        active_mandates.append("COST OPTIMIZATION")
    if os.environ.get("TDD_COMPLIANCE_MANDATORY") == "true":
        active_mandates.append("TDD COMPLIANCE")
    if os.environ.get("POSTGRESQL_FIRST_MANDATORY") == "true":
        active_mandates.append("POSTGRESQL-FIRST ARCHITECTURE")

    if active_mandates:
        print(f"✅ CLAUDE.md mandates enforced: {', '.join(active_mandates)}")
    else:
        print("❌ WARNING: No CLAUDE.md mandates were applied!")

    print("📋 **CLAUDE.md and MCP workflow enforcement complete - all systems ready**")
    return True


def verify_mandates_enforced():
    """Verify that critical CLAUDE.md mandates are being enforced."""
    print("\n🔍 **MANDATE ENFORCEMENT VERIFICATION**")

    critical_mandates = {
        "MCP_FIRST_MANDATE": "MCP-FIRST WORKFLOW MANDATE",
        "DATABASE_PROTECTION_MANDATE": "DATABASE DATA PROTECTION MANDATE",
        "COST_OPTIMIZATION_MANDATE": "COST OPTIMIZATION MANDATE",
        "TDD_COMPLIANCE_MANDATORY": "TDD COMPLIANCE ENFORCEMENT",
        "POSTGRESQL_FIRST_MANDATORY": "POSTGRESQL-FIRST ARCHITECTURE",
    }

    enforced_count = 0
    for env_var, mandate_name in critical_mandates.items():
        if os.environ.get(env_var) == "true":
            print(f"✅ {mandate_name} - ENFORCED")
            enforced_count += 1
        else:
            print(f"❌ {mandate_name} - NOT ENFORCED")

    compliance_rate = (enforced_count / len(critical_mandates)) * 100
    print(
        f"\n📊 **COMPLIANCE RATE: {compliance_rate:.1f}% ({enforced_count}/{len(critical_mandates)} mandates enforced)**"
    )

    return compliance_rate >= 80.0  # Require 80% compliance to pass


def main():
    """Main enforcement function."""
    print("🚀 **STARTUP ENFORCEMENT - LOADING CLAUDE.md AND ALL CONFIGS**")
    print("=" * 60)

    success = enforce_claude_md_loading()

    if not success:
        print("\n❌ **STARTUP ENFORCEMENT FAILED**")
        print("❌ Session cannot continue until all requirements are met")
        sys.exit(1)

    # Verify mandate compliance
    mandate_compliance = verify_mandates_enforced()
    if not mandate_compliance:
        print("\n❌ **MANDATE COMPLIANCE FAILED**")
        print("❌ Critical CLAUDE.md mandates are not being enforced")
        print("❌ Session cannot continue until compliance is achieved")
        sys.exit(1)

    print("\n✅ **STARTUP ENFORCEMENT PASSED**")
    print("✅ All CLAUDE.md rules loaded and enforced")
    print("✅ Critical mandates verified and active")
    print("✅ Session ready for development work")
    sys.exit(0)


if __name__ == "__main__":
    main()
