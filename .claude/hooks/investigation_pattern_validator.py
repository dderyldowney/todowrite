#!/usr/bin/env python3
"""Universal investigation pattern validator for ALL AI agents.

Validates that AI agent responses follow the mandatory structured
investigation pattern for safety-critical agricultural robotics development.

Agent-Agnostic Enforcement:
- Applies to Claude Code, GitHub Copilot, ChatGPT, Gemini Code Assist
- Validates ALL AI-generated analysis and troubleshooting responses
- Ensures safety-critical transparency requirements are met

Pattern Requirements:
1. Investigation Steps - Numbered systematic methodology
2. Files Examined - File paths with examination rationale
3. Evidence Collected - Factual findings with pass/fail indicators
4. Final Analysis - Root cause, mechanism, and solutions

Reference: .claude/INVESTIGATION_PATTERN_MANDATORY.md
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class PatternValidationResult:
    """Results from investigation pattern validation."""

    has_investigation_steps: bool
    has_files_examined: bool
    has_evidence_collected: bool
    has_final_analysis: bool
    is_substantive_response: bool
    validation_passed: bool
    missing_sections: list[str]
    agent_type: str = "unknown"


class InvestigationPatternValidator:
    """Validates AI agent responses against investigation pattern requirements.

    Universal validator for ALL AI development assistants including:
    - Claude Code (Anthropic)
    - GitHub Copilot (Microsoft/OpenAI)
    - ChatGPT Code Interpreter (OpenAI)
    - Gemini Code Assist (Google)
    - Amazon CodeWhisperer (AWS)
    - Any future AI agent
    """

    # Pattern markers for substantive responses requiring investigation pattern
    SUBSTANTIVE_INDICATORS = [
        r"bug",
        r"error",
        r"issue",
        r"problem",
        r"fail",
        r"debug",
        r"investigate",
        r"analyze",
        r"why\s+(is|does|did|doesn't)",
        r"root\s+cause",
        r"performance",
        r"optimization",
        r"security",
        r"safety",
    ]

    # Pattern section markers
    INVESTIGATION_STEPS_MARKERS = [
        r"##\s*Investigation\s+Steps",
        r"##\s*Methodology",
        r"##\s*Analysis\s+Steps",
    ]

    FILES_EXAMINED_MARKERS = [
        r"##\s*Files\s+Examined",
        r"##\s*Files\s+Reviewed",
        r"##\s*Code\s+Examined",
    ]

    EVIDENCE_COLLECTED_MARKERS = [
        r"##\s*Evidence\s+Collected",
        r"##\s*Findings",
        r"##\s*Data\s+Collected",
    ]

    FINAL_ANALYSIS_MARKERS = [
        r"##\s*Final\s+Analysis",
        r"##\s*Conclusion",
        r"##\s*Root\s+Cause\s+Analysis",
    ]

    def __init__(self) -> None:
        """Initialize investigation pattern validator."""
        self.project_root = self._find_project_root()

    def _find_project_root(self) -> Path:
        """Find project root by locating CLAUDE.md."""
        current = Path.cwd()
        while current != current.parent:
            if (current / "CLAUDE.md").exists():
                return current
            current = current.parent
        return Path.cwd()

    def _is_substantive_response(self, content: str) -> bool:
        """Check if response is substantive and requires investigation pattern.

        Args:
            content: AI agent response content

        Returns:
            True if response requires investigation pattern
        """
        content_lower = content.lower()

        # Check for substantive indicators
        for indicator_pattern in self.SUBSTANTIVE_INDICATORS:
            if re.search(indicator_pattern, content_lower):
                return True

        # Check for code analysis patterns
        if re.search(r"```\w+", content):  # Contains code blocks
            if len(content) > 500:  # Longer analysis
                return True

        return False

    def _check_section_present(self, content: str, markers: list[str]) -> bool:
        """Check if any section marker is present in content.

        Args:
            content: AI agent response content
            markers: List of regex patterns for section markers

        Returns:
            True if any marker found
        """
        for marker in markers:
            if re.search(marker, content, re.IGNORECASE | re.MULTILINE):
                return True
        return False

    def validate_response(
        self, content: str, agent_type: str = "unknown"
    ) -> PatternValidationResult:
        """Validate AI agent response against investigation pattern requirements.

        Args:
            content: AI agent response content
            agent_type: Type of AI agent (claude, copilot, gpt, gemini, etc.)

        Returns:
            PatternValidationResult with validation details
        """
        is_substantive = self._is_substantive_response(content)

        # Check for required sections
        has_investigation_steps = self._check_section_present(
            content, self.INVESTIGATION_STEPS_MARKERS
        )
        has_files_examined = self._check_section_present(content, self.FILES_EXAMINED_MARKERS)
        has_evidence_collected = self._check_section_present(
            content, self.EVIDENCE_COLLECTED_MARKERS
        )
        has_final_analysis = self._check_section_present(content, self.FINAL_ANALYSIS_MARKERS)

        # Determine missing sections
        missing_sections = []
        if is_substantive:
            if not has_investigation_steps:
                missing_sections.append("Investigation Steps")
            if not has_files_examined:
                missing_sections.append("Files Examined")
            if not has_evidence_collected:
                missing_sections.append("Evidence Collected")
            if not has_final_analysis:
                missing_sections.append("Final Analysis")

        # Validation passes if non-substantive OR all sections present
        validation_passed = not is_substantive or len(missing_sections) == 0

        return PatternValidationResult(
            has_investigation_steps=has_investigation_steps,
            has_files_examined=has_files_examined,
            has_evidence_collected=has_evidence_collected,
            has_final_analysis=has_final_analysis,
            is_substantive_response=is_substantive,
            validation_passed=validation_passed,
            missing_sections=missing_sections,
            agent_type=agent_type,
        )

    def format_validation_message(self, result: PatternValidationResult) -> str:
        """Format validation result as user-friendly message.

        Args:
            result: Validation result

        Returns:
            Formatted validation message
        """
        if result.validation_passed:
            return (
                "✅ Investigation pattern validation PASSED\n"
                f"   Agent: {result.agent_type}\n"
                "   Response meets structured investigation requirements"
            )

        message = (
            "❌ INVESTIGATION PATTERN VIOLATION\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Agent: {result.agent_type}\n"
            "This substantive response is missing required sections:\n\n"
        )

        for section in result.missing_sections:
            message += f"  ❌ {section}\n"

        message += (
            "\n"
            "REQUIRED: All substantive AI agent responses MUST include:\n"
            "  1. Investigation Steps (methodology)\n"
            "  2. Files Examined (audit trail)\n"
            "  3. Evidence Collected (factual findings)\n"
            "  4. Final Analysis (root cause and solutions)\n"
            "\n"
            "Reference: .claude/INVESTIGATION_PATTERN_MANDATORY.md\n"
            "\n"
            "This requirement applies to ALL AI agents:\n"
            "  • Claude Code, GitHub Copilot, ChatGPT, Gemini, CodeWhisperer\n"
            "  • Safety-critical agricultural robotics demands verifiable reasoning\n"
            "  • ISO compliance requires transparent decision auditing\n"
        )

        return message


def validate_agent_response_hook(tool_name: str, tool_input: dict[str, Any]) -> dict[str, Any]:
    """Hook function to validate AI agent responses for investigation pattern.

    Args:
        tool_name: Name of tool being invoked
        tool_input: Tool input parameters

    Returns:
        Hook result with validation status and message
    """
    validator = InvestigationPatternValidator()

    # Extract response content (agent-specific)
    content = ""
    agent_type = "unknown"

    # Claude Code format
    if "content" in tool_input:
        content = str(tool_input["content"])
        agent_type = "claude"

    # GitHub Copilot format
    elif "message" in tool_input:
        content = str(tool_input["message"])
        agent_type = "copilot"

    # Generic format
    elif "response" in tool_input:
        content = str(tool_input["response"])

    if not content:
        return {"status": "skipped", "message": "No content to validate"}

    # Validate response
    result = validator.validate_response(content, agent_type)

    if result.validation_passed:
        return {"status": "approved", "message": validator.format_validation_message(result)}

    # Validation failed - return warning (not blocking for now)
    return {
        "status": "warning",
        "message": validator.format_validation_message(result),
    }


def main() -> int:
    """Main entry point for standalone validation.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    if len(sys.argv) < 2:
        print("Usage: investigation_pattern_validator.py <response_file>")
        return 1

    response_file = Path(sys.argv[1])
    if not response_file.exists():
        print(f"Error: Response file not found: {response_file}")
        return 1

    content = response_file.read_text()
    agent_type = sys.argv[2] if len(sys.argv) > 2 else "unknown"

    validator = InvestigationPatternValidator()
    result = validator.validate_response(content, agent_type)

    print(validator.format_validation_message(result))

    return 0 if result.validation_passed else 1


if __name__ == "__main__":
    sys.exit(main())
