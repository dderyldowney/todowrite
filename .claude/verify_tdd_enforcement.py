#!/usr/bin/env python3
"""
Verify TDD (Test-Driven Development) enforcement status

This script checks if TDD requirements are properly activated and persistent
in the current session, including superpowers skills and enforcement mechanisms.
"""

import json
import sys
from pathlib import Path
from typing import Any


def load_json_file(file_path: Path) -> dict[str, Any] | None:
    """Load and parse JSON file"""
    try:
        if file_path.exists():
            with open(file_path) as f:
                return json.load(f)
        return None
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return None


def check_tdd_enforcement() -> None:
    """Check TDD enforcement status"""
    print("🧪 TDD Enforcement Status Check")
    print("=" * 50)

    claude_dir = Path(".claude")

    # Check 1: TDD workflow configuration
    print("\n1. TDD Workflow Configuration:")
    tdd_workflow = load_json_file(claude_dir / "tdd_workflow.json")
    if tdd_workflow:
        enabled = tdd_workflow.get("tdd_enabled", False)
        enforcement = tdd_workflow.get("enforcement_level", "unknown")
        print(f"   ✅ TDD Enabled: {enabled}")
        print(f"   ✅ Enforcement Level: {enforcement}")

        mandatory_skills = tdd_workflow.get("mandatory_skills", [])
        print(f"   ✅ Mandatory Skills: {mandatory_skills}")
    else:
        print("   ❌ TDD workflow configuration not found")

    # Check 2: Superpowers configuration
    print("\n2. Superpowers Configuration:")
    superpowers_config = load_json_file(claude_dir / "mcp_superpowers_config_2025.json")
    if superpowers_config:
        skill_categories = superpowers_config.get("skill_categories", {})
        dev_skills = skill_categories.get("development", [])
        tdd_included = "test-driven-development" in dev_skills
        print(f"   {'✅' if tdd_included else '❌'} TDD in Development Skills: {tdd_included}")
        print(f"   📋 All Development Skills: {dev_skills}")
    else:
        print("   ❌ Superpowers configuration not found")

    # Check 3: Comprehensive quality enforcement
    print("\n3. Quality Enforcement Configuration:")
    quality_config = load_json_file(claude_dir / "comprehensive_quality_enforcement.json")
    if quality_config:
        tools = quality_config.get("tools", {})
        rgr = tools.get("red_green_refactor", {})
        rgr_active = rgr.get("active", False)
        print(f"   {'✅' if rgr_active else '❌'} Red-Green-Refactor Active: {rgr_active}")
        if rgr:
            print(f"   📋 Description: {rgr.get('description', 'N/A')}")
    else:
        print("   ❌ Quality enforcement configuration not found")

    # Check 4: TDD skill availability
    print("\n4. TDD Skill Availability:")
    tdd_skill_path = claude_dir / "skills" / "test-driven-development" / "skill.py"
    if tdd_skill_path.exists():
        print(f"   ✅ TDD Skill File: {tdd_skill_path}")

        # Check if skill can be imported
        try:
            sys.path.insert(0, str(tdd_skill_path.parent))
            from skill import TestDrivenDevelopment
            print("   ✅ TDD Skill Import: SUCCESS")

            # Test skill instantiation
            tdd = TestDrivenDevelopment()
            print("   ✅ TDD Skill Instantiation: SUCCESS")
            print(f"   📁 Project Root: {tdd.project_root}")
            print(f"   📁 Test Directory: {tdd.test_dir}")
            print(f"   📁 Source Directory: {tdd.source_dir}")

        except ImportError as e:
            print(f"   ❌ TDD Skill Import Failed: {e}")
        except Exception as e:
            print(f"   ❌ TDD Skill Instantiation Failed: {e}")
    else:
        print(f"   ❌ TDD Skill File Not Found: {tdd_skill_path}")

    # Check 5: Session startup integration
    print("\n5. Session Startup Integration:")
    autorun_file = claude_dir / "autorun.py"
    if autorun_file.exists():
        content = autorun_file.read_text()
        tdd_in_required_skills = "test-driven-development" in content
        print(f"   {'✅' if tdd_in_required_skills else '❌'} TDD in Required Skills: {tdd_in_required_skills}")
    else:
        print("   ❌ Autorun script not found")

    # Check 6: Permanent enforcement
    print("\n6. Permanent Enforcement:")
    permanent_enforcement = claude_dir / "hooks" / "permanent_enforcement.py"
    if permanent_enforcement.exists():
        content = permanent_enforcement.read_text()
        rgr_enforced = "red_green_refactor" in content
        print(f"   {'✅' if rgr_enforced else '❌'} Red-Green-Refactor Enforced: {rgr_enforced}")
    else:
        print("   ❌ Permanent enforcement script not found")

    # Summary
    print("\n" + "=" * 50)
    print("🎯 TDD Enforcement Summary:")

    all_checks = [
        tdd_workflow is not None and tdd_workflow.get("tdd_enabled", False),
        superpowers_config is not None and "test-driven-development" in superpowers_config.get("skill_categories", {}).get("development", []),
        quality_config is not None and quality_config.get("tools", {}).get("red_green_refactor", {}).get("active", False),
        tdd_skill_path.exists(),
        autorun_file.exists() and "test-driven-development" in autorun_file.read_text()
    ]

    passed_checks = sum(all_checks)
    total_checks = len(all_checks)

    if passed_checks == total_checks:
        print("   ✅ ALL TDD ENFORCEMENT SYSTEMS ACTIVE")
        print("   🚀 TDD requirements are properly enforced")
    else:
        print(f"   ⚠️  {passed_checks}/{total_checks} TDD systems active")
        print("   🔧 Some TDD enforcement components may need attention")

    return passed_checks == total_checks


if __name__ == "__main__":
    success = check_tdd_enforcement()
    sys.exit(0 if success else 1)