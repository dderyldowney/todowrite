"""Tests for Claude configuration validation.

Tests that .claude/CLAUDE.md contains mandatory documentation loading requirements
and follows the project's configuration standards.
"""

from pathlib import Path


class TestClaudeConfigValidation:
    """Test suite for Claude configuration file validation."""

    def test_claude_md_exists(self) -> None:
        """Test that .claude/CLAUDE.md file exists."""
        config_path = Path(".claude/CLAUDE.md")
        assert config_path.exists(), ".claude/CLAUDE.md must exist"

    def test_claude_md_contains_documentation_loading_rule(self) -> None:
        """Test that CLAUDE.md contains mandatory documentation loading requirements."""
        config_path = Path(".claude/CLAUDE.md")
        content = config_path.read_text()

        # Check for rule that requires documentation loading
        assert "read and load documentation files IN ORDER" in content, (
            "Must require documentation loading in order"
        )

        # Check for the three required files
        assert "CLAUDE.md" in content, "Must reference CLAUDE.md"
        assert "ToDoWrite.md" in content, "Must reference ToDoWrite.md"
        assert "BUILD_SYSTEM.md" in content, "Must reference BUILD_SYSTEM.md"

    def test_documentation_loading_is_rule_2(self) -> None:
        """Test that documentation loading is specifically Rule #2."""
        config_path = Path(".claude/CLAUDE.md")
        content = config_path.read_text()
        lines = content.split("\n")

        # Find Rule #2
        rule_2_found = False
        rule_2_content = ""
        for i, line in enumerate(lines):
            if line.strip().startswith("## 2."):
                rule_2_found = True
                # Get content of Rule #2 (until next rule or end)
                rule_lines = [line]
                for j in range(i + 1, len(lines)):
                    if lines[j].strip().startswith("## "):
                        break
                    rule_lines.append(lines[j])
                rule_2_content = "\n".join(rule_lines)
                break

        assert rule_2_found, "Rule #2 must exist"
        assert "documentation files" in rule_2_content, "Rule #2 must be about documentation files"
        assert "IN ORDER" in rule_2_content, "Rule #2 must require loading in order"

    def test_claude_md_clear_quit_handling(self) -> None:
        """Test that CLAUDE.md handles /clear and /quit scenarios."""
        config_path = Path(".claude/CLAUDE.md")
        content = config_path.read_text()

        # Check for explicit /clear and /quit handling
        assert "/clear" in content, "Must handle /clear scenarios"
        assert "/quit" in content, "Must handle /quit scenarios"

    def test_claude_md_no_bypass_clauses(self) -> None:
        """Test that CLAUDE.md contains no-bypassing clauses."""
        config_path = Path(".claude/CLAUDE.md")
        content = config_path.read_text()

        # Check for no-bypassing language
        assert "NO EXCEPTIONS" in content, "Must have no-exceptions clause"
        assert any(
            bypass in content for bypass in ["NO BYPASSING", "no bypass", "cannot bypass"]
        ), "Must have no-bypassing clause"

    def test_claude_md_emergency_verification(self) -> None:
        """Test that CLAUDE.md contains emergency verification procedures."""
        config_path = Path(".claude/CLAUDE.md")
        content = config_path.read_text()

        # Check for emergency verification section
        assert "Emergency" in content, "Must have emergency verification procedures"
        assert "verification" in content.lower(), "Must have verification procedures"

    def test_documentation_files_exist(self) -> None:
        """Test that all required documentation files exist."""
        # Check main documentation files
        assert Path("docs/ToDoWrite.md").exists(), "docs/ToDoWrite.md must exist"
        assert Path("BUILD_SYSTEM.md").exists(), "BUILD_SYSTEM.md must exist"
        assert Path(".claude/CLAUDE.md").exists(), ".claude/CLAUDE.md must exist"

    def test_rule_numbering_consistency(self) -> None:
        """Test that rule numbering is consistent without gaps."""
        config_path = Path(".claude/CLAUDE.md")
        content = config_path.read_text()
        lines = content.split("\n")

        # Find all rule numbers
        rule_numbers = []
        for line in lines:
            if line.strip().startswith("## ") and ". " in line:
                # Extract rule number from "## X. description"
                try:
                    num_str = line.strip()[3:].split(". ")[0]
                    rule_numbers.append(int(num_str))
                except (ValueError, IndexError):
                    continue

        # Verify we have rules and they start at 1
        assert rule_numbers, "Must have numbered rules"
        assert rule_numbers[0] == 1, "Rules must start at 1"

        # Verify no gaps in numbering
        for i, expected in enumerate(rule_numbers, start=1):
            assert expected == i, f"Rule gap detected: expected {i}, found {expected}"
