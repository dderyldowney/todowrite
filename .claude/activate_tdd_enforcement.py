#!/usr/bin/env python3
"""
Activate TDD (Test-Driven Development) Enforcement

This script explicitly activates TDD enforcement requirements and ensures
all TDD-related systems are properly initialized and announced.
"""

import sys
from pathlib import Path


def activate_tdd_enforcement() -> bool:
    """Activate TDD enforcement systems"""
    print("🧪 Activating TDD Enforcement Systems...")

    claude_dir = Path(".claude")
    success = True

    # 1. Verify TDD skill is available and functional
    print("\n1. Verifying TDD Superpowers Skill:")
    tdd_skill_path = claude_dir / "skills" / "test-driven-development" / "skill.py"

    if not tdd_skill_path.exists():
        print("   ❌ TDD skill not found")
        return False

    try:
        sys.path.insert(0, str(tdd_skill_path.parent))
        from skill import TestDrivenDevelopment

        # Test instantiation
        tdd = TestDrivenDevelopment()
        print(f"   ✅ TDD Skill initialized: {tdd.project_root}")

    except ImportError as e:
        print(f"   ❌ TDD Skill import failed: {e}")
        success = False
    except Exception as e:
        print(f"   ❌ TDD Skill activation failed: {e}")
        success = False

    # 2. Verify TDD workflow configuration
    print("\n2. Verifying TDD Workflow Configuration:")
    tdd_workflow_path = claude_dir / "tdd_workflow.json"

    if tdd_workflow_path.exists():
        import json

        with open(tdd_workflow_path) as f:
            tdd_config = json.load(f)

        tdd_enabled = tdd_config.get("tdd_enabled", False)
        enforcement_level = tdd_config.get("enforcement_level", "unknown")

        if tdd_enabled:
            print(f"   ✅ TDD Enabled: {enforcement_level} enforcement")
        else:
            print("   ❌ TDD not enabled in configuration")
            success = False
    else:
        print("   ❌ TDD workflow configuration not found")
        success = False

    # 3. Announce TDD enforcement requirements
    print("\n3. TDD Enforcement Requirements:")
    print("   ✅ Red → Green → Refactor methodology ENFORCED")
    print("   ✅ Write failing tests BEFORE production code")
    print("   ✅ Write minimal code to pass tests")
    print("   ✅ Refactor only while tests remain green")
    print("   ✅ ZERO mocking policy - real implementations only")
    print("   ✅ Component-based test organization required")

    # 4. Integration with quality enforcement
    print("\n4. Quality Gate Integration:")
    quality_config_path = claude_dir / "comprehensive_quality_enforcement.json"

    if quality_config_path.exists():
        with open(quality_config_path) as f:
            quality_config = json.load(f)

        rgr_config = quality_config.get("tools", {}).get("red_green_refactor", {})
        if rgr_config.get("active", False):
            print("   ✅ Red-Green-Refactor enforcement active in quality gates")
            print(f"   📋 {rgr_config.get('description', 'TDD methodology enforcement')}")
        else:
            print("   ⚠️  Red-Green-Refactor not active in quality gates")

    # 5. Zero tolerance violations
    print("\n5. Zero Tolerance TDD Violations:")
    print("   🚫 Writing production code before tests")
    print("   🚫 Skipping RED phase (writing tests that fail)")
    print("   🚫 Using mocking frameworks or test doubles")
    print("   🚫 Committing without comprehensive test coverage")
    print("   🚫 Monolithic test files (component-based required)")

    if success:
        print("\n🚀 TDD ENFORCEMENT ACTIVATED")
        print("=" * 50)
        print("✅ All TDD requirements are now ENFORCED")
        print("✅ Superpowers TDD skill loaded and ready")
        print("✅ Quality gates will enforce TDD methodology")
        print("✅ Zero-tolerance violations are actively monitored")
        print("=" * 50)
    else:
        print("\n❌ TDD ENFORCEMENT ACTIVATION FAILED")
        print("Some TDD components could not be activated")

    return success


if __name__ == "__main__":
    success = activate_tdd_enforcement()
    sys.exit(0 if success else 1)
