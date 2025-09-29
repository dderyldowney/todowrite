#!/usr/bin/env python3
"""
Agricultural Safety Standards Validation Hook for AFS FastAPI

This pre-commit hook validates ISO 18497 safety compliance and agricultural
equipment standards for the AFS FastAPI robotic agriculture platform.

Safety Standards Enforced:
- ISO 18497 (Agricultural machinery safety)
- ISO 11783 (ISOBUS communication safety)
- Performance Level compliance (PLc, PLd, PLe)
- Emergency stop validation
- Multi-tractor coordination safety

Agricultural Context:
- Equipment operates in safety-critical environments
- Multi-tractor coordination requires collision avoidance
- Emergency stop systems must function across entire fleet
- Autonomous operations require comprehensive safety validation
"""

import ast
import re
import sys


class AgriculturalSafetyValidator:
    """
    Validates agricultural safety compliance for equipment and services modules.

    Ensures that safety-critical components meet ISO 18497 standards and
    implement proper safety patterns for agricultural robotics operations.
    """

    def __init__(self):
        self.safety_critical_patterns = {
            "emergency_stop": r"emergency_stop|e_stop|emergency_halt",
            "collision_avoidance": r"collision|obstacle|avoidance|proximity",
            "safety_level": r"PLc|PLd|PLe|performance_level|safety_level",
            "iso_compliance": r"ISO\s*18497|ISO\s*11783|ISOBUS.*safety",
            "autonomous_safety": r"autonomous.*safety|safety.*autonomous",
            "power_management": r"power_off|shutdown|safe_state",
        }

        self.required_safety_methods = {
            "equipment": ["emergency_stop", "enter_safe_state", "validate_operation"],
            "services": ["handle_emergency", "validate_coordination", "check_safety_constraints"],
            "coordination": ["emergency_broadcast", "collision_check", "safe_distance_validation"],
        }

    def validate_safety_compliance(self, files: list[str]) -> tuple[bool, list[str]]:
        """
        Validate safety compliance for agricultural robotics files.

        Args:
            files: List of modified Python files

        Returns:
            Tuple of (is_compliant, error_messages)
        """
        errors = []

        for file_path in files:
            if not self._is_safety_critical_file(file_path):
                continue

            try:
                with open(file_path) as f:
                    content = f.read()
            except Exception as e:
                errors.append(f"Cannot read safety-critical file {file_path}: {e}")
                continue

            # Validate safety patterns
            safety_errors = self._validate_safety_patterns(file_path, content)
            errors.extend(safety_errors)

            # Validate required safety methods
            method_errors = self._validate_required_methods(file_path, content)
            errors.extend(method_errors)

            # Validate safety documentation
            doc_errors = self._validate_safety_documentation(file_path, content)
            errors.extend(doc_errors)

        return len(errors) == 0, errors

    def _is_safety_critical_file(self, file_path: str) -> bool:
        """
        Determine if file contains safety-critical agricultural functionality.

        Args:
            file_path: Path to source file

        Returns:
            True if file requires safety validation
        """
        safety_paths = [
            "equipment/",
            "services/synchronization",
            "services/coordination",
            "monitoring/",
        ]

        safety_keywords = [
            "motor",
            "power",
            "emergency",
            "safety",
            "collision",
            "autonomous",
            "coordination",
            "synchronization",
        ]

        # Check file path
        for path in safety_paths:
            if path in file_path:
                return True

        # Check filename for safety keywords
        filename = file_path.lower()
        for keyword in safety_keywords:
            if keyword in filename:
                return True

        return False

    def _validate_safety_patterns(self, file_path: str, content: str) -> list[str]:
        """
        Validate required safety patterns in code.

        Args:
            file_path: Path to source file
            content: File content

        Returns:
            List of safety validation errors
        """
        errors = []

        # Equipment files must have emergency stop capability
        if "equipment/" in file_path:
            if not re.search(
                self.safety_critical_patterns["emergency_stop"], content, re.IGNORECASE
            ):
                errors.append(
                    f"Equipment module {file_path} missing emergency stop implementation "
                    f"(ISO 18497 requirement)"
                )

        # Autonomous components must have collision avoidance
        if "autonomous" in content.lower():
            if not re.search(
                self.safety_critical_patterns["collision_avoidance"], content, re.IGNORECASE
            ):
                errors.append(
                    f"Autonomous component {file_path} missing collision avoidance "
                    f"(ISO 18497 safety requirement)"
                )

        # Coordination services must handle safety constraints
        if "coordination" in file_path or "synchronization" in file_path:
            required_patterns = ["emergency_stop", "collision_avoidance"]
            for pattern_name in required_patterns:
                pattern = self.safety_critical_patterns[pattern_name]
                if not re.search(pattern, content, re.IGNORECASE):
                    errors.append(
                        f"Coordination module {file_path} missing {pattern_name} handling "
                        f"(Multi-tractor safety requirement)"
                    )

        return errors

    def _validate_required_methods(self, file_path: str, content: str) -> list[str]:
        """
        Validate required safety methods are implemented.

        Args:
            file_path: Path to source file
            content: File content

        Returns:
            List of method validation errors
        """
        errors = []

        try:
            tree = ast.parse(content)
        except SyntaxError:
            # If file has syntax errors, let other tools catch it
            return []

        # Extract all method names
        method_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                method_names.add(node.name)

        # Check required methods based on file type
        for module_type, required_methods in self.required_safety_methods.items():
            if module_type in file_path:
                for required_method in required_methods:
                    # Check for exact match or pattern match
                    found = any(
                        required_method in method
                        or re.search(required_method.replace("_", ".*"), method, re.IGNORECASE)
                        for method in method_names
                    )

                    if not found:
                        errors.append(
                            f"Safety-critical module {file_path} missing required method: {required_method} "
                            f"(Agricultural safety standards requirement)"
                        )

        return errors

    def _validate_safety_documentation(self, file_path: str, content: str) -> list[str]:
        """
        Validate safety documentation requirements.

        Args:
            file_path: Path to source file
            content: File content

        Returns:
            List of documentation validation errors
        """
        errors = []

        # Safety-critical files must have safety documentation
        safety_doc_patterns = [
            r"ISO\s*18497",  # Safety standard reference
            r"safety.*level|performance.*level",  # Safety level documentation
            r"emergency.*stop|emergency.*procedure",  # Emergency procedures
            r"agricultural.*safety|farm.*safety",  # Agricultural safety context
        ]

        has_safety_docs = any(
            re.search(pattern, content, re.IGNORECASE) for pattern in safety_doc_patterns
        )

        if not has_safety_docs:
            errors.append(
                f"Safety-critical file {file_path} missing required safety documentation "
                f"(Must reference ISO 18497, safety levels, or emergency procedures)"
            )

        # Class docstrings should mention safety for critical components
        if "class " in content and "equipment/" in file_path:
            class_pattern = r'class\s+\w+.*?:\s*"""(.*?)"""'
            class_docs = re.findall(class_pattern, content, re.DOTALL | re.IGNORECASE)

            for doc in class_docs:
                if not re.search(r"safety|emergency|ISO", doc, re.IGNORECASE):
                    errors.append(
                        f"Equipment class in {file_path} missing safety information in docstring "
                        f"(Agricultural equipment must document safety considerations)"
                    )

        return errors


def main():
    """
    Main safety validation entry point for pre-commit hook.
    """
    if len(sys.argv) < 2:
        print("Safety Validation: No files to validate")
        return 0

    files = sys.argv[1:]
    validator = AgriculturalSafetyValidator()

    is_compliant, errors = validator.validate_safety_compliance(files)

    if not is_compliant:
        print("🚨 AGRICULTURAL SAFETY STANDARDS VIOLATIONS DETECTED")
        print("=" * 65)
        print("AFS FastAPI requires ISO 18497 safety compliance for agricultural robotics.")
        print("Safety-critical components must implement comprehensive safety measures.")
        print()

        for error in errors:
            print(f"⚠️  {error}")

        print()
        print("🛡️  Agricultural Safety Requirements:")
        print("• Emergency stop systems (ISO 18497)")
        print("• Collision avoidance for autonomous operations")
        print("• Multi-tractor coordination safety")
        print("• Performance Level compliance (PLc/PLd/PLe)")
        print("• Comprehensive safety documentation")
        print()
        print("📖 Reference: ROBOTIC_INTERFACES_FARM_TRACTORS.md for safety standards")

        return 1

    print("✅ Agricultural Safety Standards Compliance Validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
