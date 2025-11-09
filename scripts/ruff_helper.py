#!/usr/bin/env python3
"""
Ruff Helper - Proper parsing and analysis of ruff linting results
Fixes the display/parsing issues with arrow formats and error detection.
"""

import re
import subprocess
import sys
from pathlib import Path


class RuffHelper:
    """Helper class for properly parsing ruff output and managing linting."""

    def __init__(self, root_path: str | None = None):
        self.root_path = Path(root_path) if root_path else Path.cwd()

    def run_ruff_check(
        self, with_statistics: bool = False
    ) -> tuple[int, str, str]:
        """Run ruff check and return proper results with correct error parsing."""
        cmd = [sys.executable, "-m", "ruff", "check", "."]
        if with_statistics:
            cmd.append("--statistics")

        result = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
            cwd=str(self.root_path),
        )

        return result.returncode, result.stdout, result.stderr

    def parse_ruff_output(self, stdout: str) -> dict:
        """Properly parse ruff output to extract errors and statistics."""
        lines = stdout.strip().split("\n") if stdout.strip() else []

        # Parse summary
        total_errors = 0
        for line in lines:
            match = re.search(r"Found (\d+) errors?", line)
            if match:
                total_errors = int(match.group(1))
                break

        # Parse individual errors - ruff format is:
        # ERROR_DESCRIPTION
        #   --> FILE_PATH:LINE:COL
        #   | CONTEXT...
        errors = []

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Skip empty lines, context markers, and statistics
            if (
                not line
                or line.startswith(("|", "-", "-->"))
                or re.match(r"^\d+\s+[A-Z]\d+", line)
            ):
                i += 1
                continue

            # Error description line (like "S105 Possible hardcoded password")
            if re.match(r"^[A-Z]\d+", line):
                error_code_match = re.match(r"^([A-Z]\d+)\s+(.+)", line)
                if error_code_match:
                    error_code = error_code_match.group(1)
                    description = error_code_match.group(2)

                    # Look for file location in next few lines
                    file_info = None
                    j = i + 1
                    while (
                        j < len(lines) and j <= i + 3
                    ):  # Look ahead up to 3 lines
                        next_line = lines[j].strip()
                        if next_line.startswith("-->"):
                            # Extract file info from arrow line
                            match = re.search(
                                r"-->\s*([^:]+):(\d+):(\d+)", next_line
                            )
                            if match:
                                file_info = {
                                    "file": match.group(1),
                                    "line": int(match.group(2)),
                                    "col": int(match.group(3)),
                                }
                                break
                        j += 1

                    if file_info:
                        errors.append(
                            {
                                "code": error_code,
                                "description": description,
                                **file_info,
                            }
                        )

                    # Skip to after the file location we found
                    i = j if file_info else i + 1
                else:
                    i += 1
            else:
                i += 1

        return {
            "total_errors": total_errors,
            "error_count": len(errors),
            "errors": errors,
        }

    def get_error_summary(self, parsed_output: dict) -> dict[str, int]:
        """Get a summary of errors by type."""
        error_counts = {}
        for error in parsed_output["errors"]:
            code = error.get("code", "UNKNOWN")
            error_counts[code] = error_counts.get(code, 0) + 1
        return dict(
            sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
        )

    def format_error_report(self, parsed_output: dict, limit: int = 10) -> str:
        """Format a readable error report."""
        summary = self.get_error_summary(parsed_output)

        report = [
            "🔍 Ruff Linting Report",
            f"Total Errors: {parsed_output['total_errors']}",
            f"Parsed Errors: {parsed_output['error_count']}",
            "",
            "📊 Top Error Types:",
        ]

        for i, (code, count) in enumerate(list(summary.items())[:limit]):
            report.append(f"  {i + 1}. {code}: {count} errors")

        if parsed_output["errors"]:
            report.extend(
                [
                    "",
                    f"🔧 First {min(5, len(parsed_output['errors']))} errors:",
                ]
            )

            for i, error in enumerate(parsed_output["errors"][:5]):
                file_name = Path(error["file"]).name
                report.append(
                    f"  {i + 1}. {error['code']}: {file_name}:{error['line']} - {error['description']}"
                )

        return "\n".join(report)


def main():
    """Test the ruff helper to verify it works correctly."""
    helper = RuffHelper()

    print("🔧 Testing Ruff Helper...")

    # Run ruff check
    _returncode, stdout, _stderr = helper.run_ruff_check()

    # Parse output
    parsed = helper.parse_ruff_output(stdout)

    # Generate report
    report = helper.format_error_report(parsed)
    print(report)

    # Verify we're getting the right count
    if parsed["total_errors"] > 0:
        print(f"\n✅ Successfully parsed {parsed['total_errors']} errors!")
    else:
        print("\n✅ No errors found!")


if __name__ == "__main__":
    main()
