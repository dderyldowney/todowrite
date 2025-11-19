#!/usr/bin/env python3
"""
Token Optimization and Reduction System

Comprehensive system for analyzing and optimizing token usage in code
to reduce AI model token consumption while maintaining functionality.
"""

import ast
import json
import re
import sys
from pathlib import Path
from typing import Any


class TokenOptimizer:
    """Analyzes and optimizes code for token efficiency."""

    def __init__(self, project_root: Path | None = None):
        self.project_root = project_root or Path.cwd()
        self.config_file = self.project_root / ".claude" / "token_optimization_config.json"
        self.load_config()

    def load_config(self):
        """Load token optimization configuration."""
        default_config = {
            "optimization_level": "aggressive",
            "target_token_reduction": 0.15,  # 15% reduction target
            "preserve_documentation": True,
            "preserve_error_handling": True,
            "preserve_security": True,
            "optimization_rules": {
                "remove_redundant_comments": True,
                "simplify_docstrings": True,
                "compact_imports": True,
                "inline_simple_functions": True,
                "remove_debug_code": True,
                "consolidate_string_operations": True,
                "optimize_data_structures": True,
                "remove_unused_imports": True,
                "simplify_conditionals": True,
                "compact_lists_dicts": True,
                "remove_redundant_type_hints": False,  # Keep type hints for clarity
                "consolidate_error_messages": True,
                "optimize_logging": True,
                "remove_test_boilerplate": True,
            },
            "excluded_files": [
                "tests/",
                "test_",
                "_test.py",
                "__init__.py",
                "conftest.py",
                ".hooks/",
                ".git/",
                "__pycache__/",
                ".pytest_cache/",
                "build/",
                "dist/",
            ],
            "excluded_patterns": [
                r"#.*TODO",
                r"#.*FIXME",
                r"#.*NOTE",
                r"#.*HACK",
                r"#.*XXX",
            ],
            "documentation_threshold": {
                "min_docstring_length": 20,
                "max_docstring_length": 200,
                "preserve_public_api_docs": True,
                "preserve_private_api_docs": False,
            }
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

    def analyze_file_tokens(self, file_path: Path) -> dict[str, Any]:
        """Analyze token usage in a Python file."""
        try:
            with open(file_path, encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')

            # Basic token estimation (rough approximation)
            total_tokens = len(content.split()) + len(lines)  # words + newlines

            analysis = {
                "file_path": str(file_path),
                "total_lines": len(lines),
                "total_tokens": total_tokens,
                "empty_lines": len([l for l in lines if not l.strip()]),
                "comment_lines": len([l for l in lines if l.strip().startswith('#')]),
                "docstring_lines": self._count_docstring_lines(content),
                "import_lines": len([l for l in lines if l.strip().startswith(('import ', 'from '))]),
                "function_count": content.count('def '),
                "class_count": content.count('class '),
                "optimization_opportunities": [],
            }

            # Analyze optimization opportunities
            if self.config["optimization_rules"]["remove_redundant_comments"]:
                redundant_comments = self._find_redundant_comments(lines)
                if redundant_comments:
                    analysis["optimization_opportunities"].append(f"Remove {len(redundant_comments)} redundant comments")
                    analysis["redundant_comments"] = redundant_comments

            if self.config["optimization_rules"]["simplify_docstrings"]:
                long_docstrings = self._find_long_docstrings(content)
                if long_docstrings:
                    analysis["optimization_opportunities"].append(f"Simplify {len(long_docstrings)} verbose docstrings")
                    analysis["long_docstrings"] = long_docstrings

            if self.config["optimization_rules"]["remove_unused_imports"]:
                unused_imports = self._find_unused_imports(file_path)
                if unused_imports:
                    analysis["optimization_opportunities"].append(f"Remove {len(unused_imports)} unused imports")
                    analysis["unused_imports"] = unused_imports

            if self.config["optimization_rules"]["inline_simple_functions"]:
                inline_candidates = self._find_inline_candidates(content)
                if inline_candidates:
                    analysis["optimization_opportunities"].append(f"Inline {len(inline_candidates)} simple functions")
                    analysis["inline_candidates"] = inline_candidates

            # Calculate potential savings
            potential_savings = self._calculate_potential_savings(analysis)
            analysis["potential_token_reduction"] = potential_savings["tokens"]
            analysis["potential_percentage_reduction"] = potential_savings["percentage"]

            return analysis

        except Exception as e:
            return {
                "file_path": str(file_path),
                "error": str(e),
                "total_tokens": 0,
                "optimization_opportunities": []
            }

    def _count_docstring_lines(self, content: str) -> int:
        """Count lines that are part of docstrings."""
        try:
            tree = ast.parse(content)
            docstring_lines = 0

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                    if ast.get_docstring(node):
                        docstring_lines += len(ast.get_docstring(node).split('\n'))

            return docstring_lines
        except:
            # Fallback: count triple-quoted strings
            return len(re.findall(r'""".*?"""', content, re.DOTALL))

    def _find_redundant_comments(self, lines: list[str]) -> list[str]:
        """Find comments that are redundant with obvious code."""
        redundant = []

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped.startswith('#'):
                continue

            comment = stripped[1:].strip().lower()

            # Skip important comments
            if any(pattern in comment for pattern in ['todo', 'fixme', 'note', 'hack', 'xxx', 'important', 'critical']):
                continue

            # Check for obviously redundant comments
            if comment in ['increment', 'decrement', 'return', 'break', 'continue'] or comment.startswith(('get ', 'set ', 'add ', 'remove ', 'create ', 'delete ')):
                redundant.append(f"Line {i+1}: {line}")

        return redundant

    def _find_long_docstrings(self, content: str) -> list[dict[str, Any]]:
        """Find docstrings that could be simplified."""
        try:
            tree = ast.parse(content)
            long_docstrings = []

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    docstring = ast.get_docstring(node)
                    if docstring and len(docstring) > self.config["documentation_threshold"]["max_docstring_length"]:
                        # Check if it's a public API that should preserve documentation
                        is_public = not node.name.startswith('_')
                        if is_public and self.config["documentation_threshold"]["preserve_public_api_docs"]:
                            continue

                        long_docstrings.append({
                            "name": node.name,
                            "type": "function" if isinstance(node, ast.FunctionDef) else "class",
                            "line": node.lineno,
                            "length": len(docstring),
                            "docstring": docstring[:100] + "..." if len(docstring) > 100 else docstring
                        })

            return long_docstrings
        except:
            return []

    def _find_unused_imports(self, file_path: Path) -> list[str]:
        """Find potentially unused imports (basic analysis)."""
        try:
            with open(file_path, encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)
            imported_names = set()
            used_names = set()

            # Collect imported names
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_names.add(alias.asname or alias.name)
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        if alias.name != '*':
                            imported_names.add(alias.asname or alias.name)

            # Collect used names (basic check)
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    used_names.add(node.id)
                elif isinstance(node, ast.Attribute):
                    # Get the base name for attribute access
                    if isinstance(node.value, ast.Name):
                        used_names.add(node.value.id)

            unused = imported_names - used_names
            return list(unused)
        except:
            return []

    def _find_inline_candidates(self, content: str) -> list[dict[str, Any]]:
        """Find simple functions that could be inlined."""
        try:
            tree = ast.parse(content)
            candidates = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Simple heuristics for inline candidates
                    if (len(node.body) == 1 and
                        isinstance(node.body[0], ast.Return) and
                        len(node.args.args) <= 2 and
                        not node.decorator_list):

                        candidates.append({
                            "name": node.name,
                            "line": node.lineno,
                            "args": [arg.arg for arg in node.args.args]
                        })

            return candidates
        except:
            return []

    def _calculate_potential_savings(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """Calculate potential token savings for a file."""
        potential_savings = 0

        # Savings from redundant comments
        if "redundant_comments" in analysis:
            potential_savings += len(analysis["redundant_comments"]) * 8  # avg 8 tokens per comment

        # Savings from long docstrings
        if "long_docstrings" in analysis:
            for docstring in analysis["long_docstrings"]:
                reduction = docstring["length"] * 0.6  # 60% reduction
                potential_savings += reduction

        # Savings from unused imports
        if "unused_imports" in analysis:
            potential_savings += len(analysis["unused_imports"]) * 12  # avg 12 tokens per import

        # Savings from inline candidates
        if "inline_candidates" in analysis:
            for _func in analysis["inline_candidates"]:
                potential_savings += 20  # avg 20 tokens per function definition

        percentage = (potential_savings / analysis["total_tokens"] * 100) if analysis["total_tokens"] > 0 else 0

        return {
            "tokens": int(potential_savings),
            "percentage": round(percentage, 2)
        }

    def analyze_project(self, directory: Path | None = None) -> dict[str, Any]:
        """Analyze entire project for token optimization opportunities."""
        if directory is None:
            directory = self.project_root

        python_files = list(directory.rglob("*.py"))

        # Filter out excluded files
        filtered_files = []
        for file_path in python_files:
            if self._should_exclude_file(file_path):
                continue
            filtered_files.append(file_path)

        analyses = []
        total_tokens = 0
        total_savings = 0

        for file_path in filtered_files:
            analysis = self.analyze_file_tokens(file_path)
            analyses.append(analysis)
            total_tokens += analysis["total_tokens"]
            total_savings += analysis.get("potential_token_reduction", 0)

        return {
            "project_root": str(directory),
            "total_files_analyzed": len(filtered_files),
            "total_tokens": total_tokens,
            "total_potential_savings": total_savings,
            "project_reduction_percentage": round((total_savings / total_tokens * 100), 2) if total_tokens > 0 else 0,
            "files": analyses,
            "top_optimization_candidates": sorted(
                [a for a in analyses if a.get("potential_percentage_reduction", 0) > 10],
                key=lambda x: x.get("potential_percentage_reduction", 0),
                reverse=True
            )[:10]
        }

    def _should_exclude_file(self, file_path: Path) -> bool:
        """Check if file should be excluded from analysis."""
        file_str = str(file_path)

        # Check excluded files/directories
        return any(excluded in file_str for excluded in self.config["excluded_files"])

    def generate_optimization_report(self, analysis: dict[str, Any]) -> str:
        """Generate a comprehensive optimization report."""
        report = []
        report.append("🔍 TOKEN OPTIMIZATION ANALYSIS REPORT")
        report.append("=" * 50)
        report.append(f"📁 Project: {analysis['project_root']}")
        report.append(f"📄 Files analyzed: {analysis['total_files_analyzed']}")
        report.append(f"🎯 Total tokens: {analysis['total_tokens']:,}")
        report.append(f"💰 Potential savings: {analysis['total_potential_savings']:,} tokens")
        report.append(f"📊 Reduction potential: {analysis['project_reduction_percentage']:.1f}%")
        report.append("")

        if analysis["top_optimization_candidates"]:
            report.append("🏆 TOP OPTIMIZATION CANDIDATES:")
            for i, file_analysis in enumerate(analysis["top_optimization_candidates"], 1):
                report.append(f"  {i}. {Path(file_analysis['file_path']).name}")
                report.append(f"     💾 Current: {file_analysis['total_tokens']:,} tokens")
                report.append(f"     ✂️  Can save: {file_analysis['potential_token_reduction']:,} tokens "
                            f"({file_analysis['potential_percentage_reduction']:.1f}%)")

                if file_analysis.get("optimization_opportunities"):
                    report.append("     🔧 Opportunities:")
                    for opportunity in file_analysis["optimization_opportunities"]:
                        report.append(f"        • {opportunity}")
                report.append("")

        # Summary by optimization type
        all_opportunities = []
        for file_analysis in analysis["files"]:
            all_opportunities.extend(file_analysis.get("optimization_opportunities", []))

        if all_opportunities:
            report.append("📈 OPTIMIZATION OPPORTUNITIES SUMMARY:")
            opportunity_counts = {}
            for opportunity in all_opportunities:
                # Extract the type of opportunity
                opp_type = opportunity.split(":")[0] if ":" in opportunity else opportunity
                opportunity_counts[opp_type] = opportunity_counts.get(opp_type, 0) + 1

            for opp_type, count in sorted(opportunity_counts.items(), key=lambda x: x[1], reverse=True):
                report.append(f"  • {opp_type}: {count} files")

        report.append("")
        report.append("💡 RECOMMENDATIONS:")
        report.append("  1. Focus on files with >10% reduction potential first")
        report.append("  2. Remove redundant comments and verbose docstrings")
        report.append("  3. Clean up unused imports")
        report.append("  4. Consider inlining very simple functions")
        report.append("  5. Preserve important documentation and error handling")
        report.append("")
        report.append("⚠️  Always review changes carefully to maintain code clarity!")

        return "\n".join(report)


def main():
    """Main entry point for token optimizer."""
    if len(sys.argv) == 2 and sys.argv[1] == "--help":
        print("Token Optimization and Reduction System")
        print("Usage: python token-optimizer.py [--analyze | --report]")
        print("  --analyze: Analyze project and show summary")
        print("  --report:  Generate detailed optimization report")
        print("  --help:    Show this help message")
        sys.exit(0)

    mode = "--analyze"
    if len(sys.argv) > 1:
        mode = sys.argv[1]

    optimizer = TokenOptimizer()
    analysis = optimizer.analyze_project()

    if mode == "--report":
        print(optimizer.generate_optimization_report(analysis))
    else:
        print("📊 Token Analysis Summary:")
        print(f"   Files analyzed: {analysis['total_files_analyzed']}")
        print(f"   Total tokens: {analysis['total_tokens']:,}")
        print(f"   Potential savings: {analysis['total_potential_savings']:,} tokens ({analysis['project_reduction_percentage']:.1f}%)")

        if analysis['top_optimization_candidates']:
            print("\n🎯 Top 5 files to optimize:")
            for i, file_analysis in enumerate(analysis['top_optimization_candidates'][:5], 1):
                filename = Path(file_analysis['file_path']).name
                reduction = file_analysis['potential_percentage_reduction']
                print(f"   {i}. {filename} ({reduction:.1f}% reduction)")

    sys.exit(0)


if __name__ == "__main__":
    main()