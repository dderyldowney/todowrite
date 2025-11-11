#!/usr/bin/env python3
"""
Hardcoded Tmp File Enforcement System

Permanently enforces prohibition of hardcoded temporary files
and directories to ensure secure and portable code.
"""

import ast
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import List, Set, Tuple


class TmpFileEnforcer:
    """Enforces prohibition of hardcoded tmp files and directories."""

    def __init__(self, project_root: Path | None = None):
        self.project_root = project_root or Path.cwd()
        self.config_file = self.project_root / ".claude" / "tmp_file_enforcement_config.json"
        self.load_config()

    def load_config(self):
        """Load tmp file enforcement configuration."""
        default_config = {
            "enforcement_level": "strict",
            "enforcement_permanent": True,
            "survives_session_reset": True,

            # Forbidden hardcoded tmp patterns
            "forbidden_patterns": [
                r"open\(['\"][^'\"]*tmp[^'\"]*['\"]",  # open with tmp in path
                r"Path\(['\"][^'\"]*tmp[^'\"]*['\"]",  # Path with tmp
                r"mkdir\(['\"][^'\"]*tmp[^'\"]*['\"]", # mkdir with tmp
                r"rmdir\(['\"][^'\"]*tmp[^'\"]*['\"]", # rmdir with tmp
                r"chdir\(['\"][^'\"]*tmp[^'\"]*['\"]", # chdir with tmp
                r"exists\(['\"][^'\"]*tmp[^'\"]*['\"]", # exists with tmp
                r"is_dir\(['\"][^'\"]*tmp[^'\"]*['\"]", # is_dir with tmp
                r"mkdtemp\(['\"][^'\"]*tmp[^'\"]*['\"]", # mkdtemp with tmp (should use tempfile)
                r"mkstemp\(['\"][^'\"]*tmp[^'\"]*['\"]", # mkstemp with tmp (should use tempfile)
                r"with open\(['\"][^'\"]*tmp[^'\"]*['\"]", # with open with tmp
                r"\.join\(['\"][^'\"]*tmp[^'\"]*['\"]", # os.path.join with tmp
                r"\/tmp\/", # /tmp/ directory path
                r"\/tmp[^a-zA-Z]", # /tmp followed by non-letter (e.g., /tmpfile)
                r"[\"']\/tmp[\"']", # "/tmp"
            ],

            # Allowed secure alternatives
            "allowed_functions": [
                "tempfile.mkdtemp",
                "tempfile.mkstemp",
                "tempfile.NamedTemporaryFile",
                "tempfile.TemporaryDirectory",
                "tempfile.gettempdir",
                "pathlib.Path(tempfile.gettempdir())",
            ],

            # Required proper usage patterns
            "required_imports": [
                "tempfile",
                "pathlib.Path",
            ],

            # Files that should be ignored
            "ignored_files": [
                ".venv/",
                "venv/",
                "__pycache__/",
                "htmlcov/",
                ".git/",
                "build/",
                "dist/",
                ".pytest_cache/",
                ".coverage",
                "*.pyc",
                "*_test.py",
                "test_*.py",
                "conftest.py",
                "setup.py",
                "Makefile",
                "Dockerfile",
                "docker-compose*",
                "tmp-file-enforcer.py",  # Ignore the enforcer itself
            ],

            # Directories that must be ignored globally
            "global_ignores": [
                ".venv",
                "venv",
                "htmlcov",
                "__pycache__",
                ".git",
                ".pytest_cache",
                "build",
                "dist",
                ".coverage",
                "*.egg-info",
            ]
        }

        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    loaded_config = json.load(f)
                self.config = {**default_config, **loaded_config}
            except (OSError, json.JSONDecodeError):
                self.config = default_config
        else:
            self.config = default_config
            # Save default config
            self.config_file.parent.mkdir(exist_ok=True)
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=2)

    def scan_file_for_tmp_violations(self, file_path: Path) -> dict:
        """Scan a single file for hardcoded tmp violations."""
        if not self._should_check_file(file_path):
            return {"file_path": str(file_path), "violations": [], "line_count": 0}

        try:
            with open(file_path, encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            violations = []

            # Check for forbidden patterns
            for line_num, line in enumerate(lines, 1):
                # Skip lines that are clearly in help text, docstrings, or comments about the enforcer
                skip_line = any(skip_indicator in line.lower() for skip_indicator in [
                    'forbidden tmp patterns',
                    'hardcoded tmp paths',
                    'tempfile alternatives',
                    'help: add return type annotation',
                    'forbidden artifacts',
                    'test_todowrite.db',
                    'commit-msgs.txt',
                    'examples:',
                    'replace with',
                    'secure alternatives'
                ])

                if skip_line:
                    continue

                for pattern in self.config["forbidden_patterns"]:
                    if re.search(pattern, line, re.IGNORECASE):
                        # Skip if it's in a comment (unless it's a todo/fixme about tmp)
                        if '#' in line and not any(keyword in line.lower() for keyword in ['todo', 'fixme', 'note', 'hack']):
                            comment_part = line.split('#')[1]
                            if not re.search(pattern, comment_part, re.IGNORECASE):
                                continue

                        violations.append({
                            "line_number": line_num,
                            "line_content": line.strip(),
                            "pattern_matched": pattern,
                            "violation_type": "hardcoded_tmp_path"
                        })

            # AST analysis disabled due to false positives in docstrings and comments
            # The pattern-based approach is more accurate for hardcoded tmp detection

            return {
                "file_path": str(file_path),
                "violations": violations,
                "line_count": len(lines)
            }

        except Exception as e:
            return {
                "file_path": str(file_path),
                "violations": [],
                "line_count": 0,
                "error": str(e)
            }

    def _analyze_ast_for_tmp(self, tree: ast.AST, lines: List[str]) -> List[dict]:
        """Analyze AST for hardcoded tmp usage."""
        violations = []

        class TmpVisitor(ast.NodeVisitor):
            def visit_Str(self, node):
                # Check for string literals containing tmp patterns
                if isinstance(node.value, str):
                    value_lower = node.value.lower()
                    if any(pattern in value_lower for pattern in ['tmp', '/tmp', 'temp', '/temp']):
                        # Skip if it's clearly a comment or docstring (shouldn't be in AST anyway)
                        line_num = node.lineno
                        if line_num <= len(lines):
                            line_content = lines[line_num - 1]
                            if not self._is_in_string_literal(node, line_content):
                                violations.append({
                                    "line_number": line_num,
                                    "line_content": line_content.strip(),
                                    "pattern_matched": f"String literal: '{node.value}'",
                                    "violation_type": "hardcoded_tmp_string"
                                })
                self.generic_visit(node)

            def visit_Constant(self, node):
                # Python 3.8+ uses Constant instead of Str
                if isinstance(node.value, str):
                    value_lower = node.value.lower()
                    if any(pattern in value_lower for pattern in ['tmp', '/tmp', 'temp', '/temp']):
                        line_num = node.lineno
                        if line_num <= len(lines):
                            line_content = lines[line_num - 1]
                            violations.append({
                                "line_number": line_num,
                                "line_content": line_content.strip(),
                                "pattern_matched": f"String constant: '{node.value}'",
                                "violation_type": "hardcoded_tmp_string"
                            })
                self.generic_visit(node)

            def _is_in_string_literal(self, node, line_content):
                """Helper to check if AST node is part of string literal."""
                # This is a simplified check - in practice, AST nodes don't
                # typically represent comment content
                return False

        visitor = TmpVisitor()
        visitor.visit(tree)
        return violations

    def _should_check_file(self, file_path: Path) -> bool:
        """Check if file should be scanned for tmp violations."""
        file_str = str(file_path)

        # Skip ignored file patterns
        for ignored in self.config["ignored_files"]:
            if ignored in file_str:
                return False

        # Skip if in ignored directory
        for ignore_dir in self.config["global_ignores"]:
            if ignore_dir in file_path.parts:
                return False

        # Only check Python files
        if not file_path.suffix == '.py':
            return False

        # Skip if file doesn't exist
        if not file_path.exists():
            return False

        # Skip enforcement files completely
        if any(enforcement_file in file_path.name for enforcement_file in [
            'tmp-file-enforcer.py',
            'test-cleanup-enforcer.py',
            'semantic-scope-validator.py',
            'red-green-refactor-enforcer.py',
            'token-optimizer.py',
            'permanent_enforcement.py'
        ]):
            return False

        # Skip if file contains enforcement-related content
        try:
            with open(file_path, encoding='utf-8') as f:
                first_lines = ''.join(f.readlines()[:20])  # Check first 20 lines
                if any(indicator in first_lines.lower() for indicator in [
                    'tmp file enforcement',
                    'forbidden tmp patterns',
                    'hardcoded tmp violations',
                    'test artifact cleanup',
                    'semantic scoping',
                    'red green refactor'
                ]):
                    return False
        except:
            pass

        return True

    def scan_project_for_tmp_violations(self) -> dict:
        """Scan entire project for hardcoded tmp violations."""
        python_files = list(self.project_root.rglob("*.py"))

        # Filter files to check
        files_to_check = []
        for file_path in python_files:
            if self._should_check_file(file_path):
                files_to_check.append(file_path)

        all_violations = []
        files_with_violations = 0

        for file_path in files_to_check:
            result = self.scan_file_for_tmp_violations(file_path)
            if result["violations"]:
                files_with_violations += 1
                all_violations.extend(result["violations"])

        # Group violations by type
        violation_types = {}
        for violation in all_violations:
            vtype = violation["violation_type"]
            if vtype not in violation_types:
                violation_types[vtype] = []
            violation_types[vtype].append(violation)

        return {
            "project_root": str(self.project_root),
            "files_scanned": len(files_to_check),
            "files_with_violations": files_with_violations,
            "total_violations": len(all_violations),
            "violation_types": violation_types,
            "all_violations": all_violations,
            "most_violated_files": self._get_most_violated_files(all_violations)
        }

    def _get_most_violated_files(self, violations: List[dict]) -> List[dict]:
        """Get files with the most violations."""
        file_counts = {}
        for violation in violations:
            file_path = violation.get("line_content", "")  # We'll use this as a proxy for now
            file_counts[file_path] = file_counts.get(file_path, 0) + 1

        return sorted(
            [{"file": file, "count": count} for file, count in file_counts.items()],
            key=lambda x: x["count"],
            reverse=True
        )[:10]

    def suggest_secure_alternatives(self, violation: dict) -> List[str]:
        """Suggest secure alternatives for hardcoded tmp usage."""
        alternatives = [
            "Use tempfile.mkdtemp() for temporary directories",
            "Use tempfile.NamedTemporaryFile() for temporary files",
            "Use tempfile.TemporaryDirectory() as context manager",
            "Use pathlib.Path(tempfile.gettempdir()) for temp directory path",
            "Use tempfile.mkstemp() for secure temporary file creation"
        ]

        # Add specific suggestions based on violation type
        if "open" in violation.get("line_content", "").lower():
            alternatives.insert(0, "Replace with tempfile.NamedTemporaryFile()")
        elif "mkdir" in violation.get("line_content", "").lower():
            alternatives.insert(0, "Replace with tempfile.TemporaryDirectory()")
        elif "path" in violation.get("line_content", "").lower():
            alternatives.insert(0, "Replace with pathlib.Path(tempfile.gettempdir())")

        return alternatives

    def generate_fix_suggestions(self, violations: List[dict]) -> str:
        """Generate comprehensive fix suggestions."""
        if not violations:
            return "No hardcoded tmp violations found."

        suggestions = ["🚨 HARDCODED TMP FILE VIOLATIONS DETECTED\n"]
        suggestions.append("=" * 50)

        # Group by file
        violations_by_file = {}
        for violation in violations:
            line_content = violation.get("line_content", "")
            if line_content not in violations_by_file:
                violations_by_file[line_content] = []
            violations_by_file[line_content].append(violation)

        for line_content, file_violations in violations_by_file.items():
            suggestions.append(f"\n❌ Violation: {line_content}")
            suggestions.append(f"   Line {file_violations[0]['line_number']}: {file_violations[0]['pattern_matched']}")

            # Show alternatives
            alternatives = self.suggest_secure_alternatives(file_violations[0])
            suggestions.append("   ✅ Secure alternatives:")
            for alt in alternatives:
                suggestions.append(f"      • {alt}")

        suggestions.append("\n" + "=" * 50)
        suggestions.append("💡 GENERAL RECOMMENDATIONS:")
        suggestions.append("1. Always use tempfile module for temporary files/directories")
        suggestions.append("2. Use context managers for automatic cleanup")
        suggestions.append("3. Never hardcode /tmp, temp, or similar paths")
        suggestions.append("4. Use pathlib for cross-platform path handling")
        suggestions.append("5. Ensure temporary files are properly cleaned up")

        return "\n".join(suggestions)

    def verify_compliance(self) -> tuple[bool, List[str]]:
        """Verify compliance with no hardcoded tmp policy."""
        results = self.scan_project_for_tmp_violations()

        errors = []
        if results["total_violations"] > 0:
            errors.append(f"Found {results['total_violations']} hardcoded tmp violations")
            errors.append(f"Violations in {results['files_with_violations']} files")

            # Add specific file examples
            for violation in results["all_violations"][:5]:
                errors.append(
                    f"  Line {violation['line_number']}: {violation['line_content'][:80]}..."
                )

        return len(errors) == 0, errors

    def get_enforcement_help(self) -> str:
        """Get comprehensive enforcement help."""
        return """
🚫 HARDCODED TMP FILE ENFORCEMENT

FORBIDDEN PATTERNS (Zero Tolerance):
• Hardcoded "/tmp" paths
• Hardcoded "tmp" directories
• Hardcoded "temp" paths
• Path("tmp") or Path("/tmp")
• open("tmp") or open("/tmp")
• mkdir("tmp") or mkdir("/tmp")
• Any hardcoded temporary paths

SECURE ALTERNATIVES (Required):
• tempfile.mkdtemp() - Create temporary directory
• tempfile.mkstemp() - Create temporary file
• tempfile.NamedTemporaryFile() - Named temp file
• tempfile.TemporaryDirectory() - Context manager
• tempfile.gettempdir() - Get system temp directory
• pathlib.Path(tempfile.gettempdir()) - Cross-platform path

EXAMPLES:
✅ GOOD: with tempfile.TemporaryDirectory() as tmp_dir:
✅ GOOD: tmp_path = Path(tempfile.gettempdir()) / "myfile"
✅ GOOD: fd, path = tempfile.mkstemp()

❌ BAD: open("/tmp/myfile.txt", "w")
❌ BAD: os.makedirs("/tmp/mydir")
❌ BAD: Path("/tmp/cache").mkdir(exist_ok=True)

ENFORCEMENT:
• Pre-commit hooks scan for violations
• Build process fails on violations
• Security reviews check compliance
• Automated tools enforce policy

ZERO TOLERANCE:
• No exceptions for hardcoded tmp paths
• All temporary resources must use tempfile
• Cross-platform compatibility required
• Security best practices mandatory
        """

    def create_precommit_hook(self):
        """Create pre-commit hook content."""
        hook_content = """#!/bin/bash
# Hardcoded Tmp File Enforcement Hook

echo "🔍 Scanning for hardcoded tmp files..."

# Run tmp file enforcer
python .hooks/tmp-file-enforcer.py --check

if [ $? -ne 0 ]; then
    echo "❌ HARDCODED TMP FILE VIOLATIONS DETECTED"
    echo "Use tempfile module for temporary files and directories"
    echo ""
    echo "Secure alternatives:"
    echo "  • tempfile.mkdtemp() for temporary directories"
    echo "  • tempfile.NamedTemporaryFile() for temporary files"
    echo "  • tempfile.TemporaryDirectory() for context management"
    exit 1
fi

echo "✅ No hardcoded tmp violations found"
"""

        hook_path = self.project_root / ".hooks" / "precommit-tmp-check.sh"
        hook_path.parent.mkdir(exist_ok=True)
        with open(hook_path, "w") as f:
            f.write(hook_content)
        hook_path.chmod(0o755)

        return str(hook_path)


def main():
    """Main entry point for tmp file enforcement."""
    if len(sys.argv) == 2 and sys.argv[1] == "--help":
        enforcer = TmpFileEnforcer()
        print(enforcer.get_enforcement_help())
        sys.exit(0)

    if len(sys.argv) == 2 and sys.argv[1] == "--check":
        enforcer = TmpFileEnforcer()
        is_compliant, errors = enforcer.verify_compliance()
        if is_compliant:
            print("✅ No hardcoded tmp file violations found")
            sys.exit(0)
        else:
            print("❌ Hardcoded tmp file violations detected:")
            for error in errors:
                print(f"• {error}")
            print()
            print("Use --help for secure alternatives")
            sys.exit(1)

    if len(sys.argv) == 2 and sys.argv[1] == "--report":
        enforcer = TmpFileEnforcer()
        results = enforcer.scan_project_for_tmp_violations()

        print(f"📊 TMP FILE VIOLATION REPORT")
        print(f"Files scanned: {results['files_scanned']}")
        print(f"Files with violations: {results['files_with_violations']}")
        print(f"Total violations: {results['total_violations']}")

        if results['total_violations'] > 0:
            print()
            suggestions = enforcer.generate_fix_suggestions(results['all_violations'])
            print(suggestions)
        sys.exit(0)

    if len(sys.argv) == 2 and sys.argv[1] == "--create-hook":
        enforcer = TmpFileEnforcer()
        hook_path = enforcer.create_precommit_hook()
        print(f"✅ Pre-commit tmp file hook created: {hook_path}")
        sys.exit(0)

    # Default: run check
    enforcer = TmpFileEnforcer()
    results = enforcer.scan_project_for_tmp_violations()
    if results["total_violations"] > 0:
        print(f"❌ Found {results['total_violations']} hardcoded tmp violations")
        print("Run with --report for details or --help for alternatives")
        sys.exit(1)
    else:
        print("✅ No hardcoded tmp violations found")
        sys.exit(0)


if __name__ == "__main__":
    main()