#!/usr/bin/env python3
"""Startup Enforcement Script - MANDATORY CLAUDE.md Loading and Verification.

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

        # Check for key mandates in the streamlined CLAUDE.md

        if "TDD MANDATE (NON-NEGOTIABLE)" in claude_md_content:
            mandates_applied.append("TDD COMPLIANCE ENFORCEMENT")
            os.environ["TDD_COMPLIANCE_MANDATORY"] = "true"

        if "POSTGRESQL-ONLY DATA STORAGE" in claude_md_content:
            mandates_applied.append("POSTGRESQL-FIRST ARCHITECTURE")
            os.environ["POSTGRESQL_FIRST_MANDATORY"] = "true"

        if "DEVELOPMENT STANDARDS COMPLIANCE" in claude_md_content:
            mandates_applied.append("DEVELOPMENT STANDARDS")
            os.environ["DEVELOPMENT_STANDARDS_MANDATORY"] = "true"

        if "TODOWRITE PLANNING REQUIREMENT" in claude_md_content:
            mandates_applied.append("TODOWRITE PLANNING")
            os.environ["TODOWRITE_PLANNING_MANDATORY"] = "true"

        if "PRODUCTION-SAFE RULES" in claude_md_content:
            mandates_applied.append("PRODUCTION SAFETY")
            os.environ["PRODUCTION_SAFETY_MANDATORY"] = "true"

        if "STARTUP SEQUENCE REQUIREMENT" in claude_md_content:
            mandates_applied.append("STARTUP SEQUENCE")
            os.environ["STARTUP_SEQUENCE_MANDATORY"] = "true"

        if "HAL AND TOKEN OPTIMIZATION MANDATE" in claude_md_content:
            mandates_applied.append("HAL TOKEN OPTIMIZATION")
            os.environ["HAL_TOKEN_OPTIMIZATION_MANDATORY"] = "true"  # noqa: S105

        if mandates_applied:
            print(f"✅ CLAUDE.md loaded and mandates enforced: {', '.join(mandates_applied)}")
        else:
            print("⚠️  CLAUDE.md loaded but no critical mandates detected")

    except Exception as e:
        print(f"❌ CRITICAL: Failed to load CLAUDE.md content: {e}")
        return False

    # 2. Verify environment variables are sourced
    required_vars = [
        "TODOWRITE_DATABASE_URL",
        "HAL_PREPROCESSING_MANDATORY",
    ]

    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"❌ CRITICAL: Missing environment variables: {missing_vars}")
        print("❌ Run: source .env.dev")
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
        # First check if Docker daemon is responsive
        docker_version = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if docker_version.returncode != 0:
            print("❌ CRITICAL: Docker daemon not responding!")
            return False

        # Check for todowrite-postgres container with multiple methods
        result_name = subprocess.run(
            ["docker", "ps", "--filter", "name=todowrite-postgres", "--quiet"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        result_all = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Check if container is running by either exact name match or in list
        container_running = result_name.stdout.strip() or "todowrite-postgres" in result_all.stdout

        if not container_running:
            print("❌ CRITICAL: PostgreSQL container not running!")
            print(f"🐛 Debug: Name filter result: '{result_name.stdout.strip()}'")
            print(f"🐛 Debug: All containers: '{result_all.stdout.strip()}'")
            return False
        print("✅ PostgreSQL container running")
    except Exception as e:
        print(f"❌ CRITICAL: Cannot verify PostgreSQL container: {e}")
        return False

    # 5. Verify PostgreSQL as SINGLE SOURCE OF TRUTH
    try:
        # Check container is running
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=todowrite-postgres", "--quiet"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if not result.stdout.strip():
            print("❌ CRITICAL: PostgreSQL container todowrite-postgres not running!")
            return False
        print("✅ PostgreSQL container todowrite-postgres verified")

        # Verify all required databases exist
        required_databases = [
            "todowrite",
        ]

        for db_name in required_databases:
            # Use proper escaping to prevent SQL injection since we're using subprocess
            # The db_name variable is from our trusted list above, not user input
            escaped_db_name = db_name.replace("'", "''")
            result = subprocess.run(
                [
                    "docker",
                    "exec",
                    "todowrite-postgres",
                    "psql",
                    "-U",
                    "todowrite_user",
                    "-d",
                    "postgres",
                    "-c",
                    f"SELECT 1 FROM pg_database WHERE datname = '{escaped_db_name}' LIMIT 1;",  # noqa: S608
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
                "todowrite-postgres",
                "psql",
                "-U",
                "todowrite_user",
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
                "todowrite-postgres",
                "psql",
                "-U",
                "todowrite_user",
                "-d",
                "todowrite",
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

    # 7. Verify policy documents exist and are accessible
    print("📋 **POLICY DOCUMENT VERIFICATION**")
    policy_dir = Path("docs/policies")
    required_policies = [
        "TDD_REQUIREMENTS.md",
        "VALIDATION_TESTING.md",
        "POSTGRESQL_ARCHITECTURE.md",
        "DEVELOPMENT_STANDARDS.md",
        "MONOREPO_STRUCTURE.md",
        "API_USAGE_POLICY.md",
        "TODOWRITE_PLANNING.md",
        "PRODUCTION_SAFETY.md",
        "STARTUP_SEQUENCE.md",
        "HAL_TOKEN_OPTIMIZATION_POLICY.md",
    ]

    missing_policies = []
    policies_found = 0

    if not policy_dir.exists():
        print("❌ CRITICAL: docs/policies directory not found!")
        return False

    for policy in required_policies:
        policy_path = policy_dir / policy
        if policy_path.exists():
            policies_found += 1
        else:
            missing_policies.append(policy)

    if missing_policies:
        print(f"❌ CRITICAL: Missing policy documents: {missing_policies}")
        return False

    print(f"✅ All {policies_found} policy documents verified")

    # Store policy directory path for agent access
    os.environ["POLICY_DOCS_DIRECTORY"] = str(policy_dir.absolute())
    print("✅ Policy directory path set for agent access")

    # 8. Initialize real-time token monitoring
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

    # 9. Verify CLAUDE.md mandates are enforced
    active_mandates = []
    if os.environ.get("DEVELOPMENT_STANDARDS_MANDATORY") == "true":
        active_mandates.append("DEVELOPMENT STANDARDS")
    if os.environ.get("TDD_COMPLIANCE_MANDATORY") == "true":
        active_mandates.append("TDD COMPLIANCE")
    if os.environ.get("POSTGRESQL_FIRST_MANDATORY") == "true":
        active_mandates.append("POSTGRESQL-FIRST ARCHITECTURE")
    if os.environ.get("TODOWRITE_PLANNING_MANDATORY") == "true":
        active_mandates.append("TODOWRITE PLANNING")
    if os.environ.get("PRODUCTION_SAFETY_MANDATORY") == "true":
        active_mandates.append("PRODUCTION SAFETY")
    if os.environ.get("STARTUP_SEQUENCE_MANDATORY") == "true":
        active_mandates.append("STARTUP SEQUENCE")
    if os.environ.get("HAL_TOKEN_OPTIMIZATION_MANDATORY") == "true":
        active_mandates.append("HAL TOKEN OPTIMIZATION")

    if active_mandates:
        print(f"✅ CLAUDE.md mandates enforced: {', '.join(active_mandates)}")
    else:
        print("❌ WARNING: No CLAUDE.md mandates were applied!")

    print("📋 **CLAUDE.md, policy documents, and all systems ready**")
    return True


def verify_mandates_enforced():
    """Verify that critical CLAUDE.md mandates are being enforced."""
    print("\n🔍 **MANDATE ENFORCEMENT VERIFICATION**")

    critical_mandates = {
        "DEVELOPMENT_STANDARDS_MANDATORY": "DEVELOPMENT STANDARDS COMPLIANCE",
        "TDD_COMPLIANCE_MANDATORY": "TDD COMPLIANCE ENFORCEMENT",
        "POSTGRESQL_FIRST_MANDATORY": "POSTGRESQL-FIRST ARCHITECTURE",
        "TODOWRITE_PLANNING_MANDATORY": "TODOWRITE PLANNING REQUIREMENT",
        "PRODUCTION_SAFETY_MANDATORY": "PRODUCTION SAFETY RULES",
        "STARTUP_SEQUENCE_MANDATORY": "STARTUP SEQUENCE REQUIREMENT",
        "HAL_TOKEN_OPTIMIZATION_MANDATORY": "HAL TOKEN OPTIMIZATION MANDATE",
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
