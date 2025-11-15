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

    def test_authoritative_sources_rule(self) -> None:
        """Test that Rule #3 requires authoritative sources consultation."""
        config_path = Path(".claude/CLAUDE.md")
        content = config_path.read_text()
        lines = content.split("\n")

        # Find Rule #3
        rule_3_found = False
        rule_3_content = ""
        for i, line in enumerate(lines):
            if line.strip().startswith("## 3."):
                rule_3_found = True
                # Get content of Rule #3 (until next rule or end)
                rule_lines = [line]
                for j in range(i + 1, len(lines)):
                    if lines[j].strip().startswith("## "):
                        break
                    rule_lines.append(lines[j])
                rule_3_content = "\n".join(rule_lines)
                break

        assert rule_3_found, "Rule #3 must exist"
        assert "Authoritative sources" in rule_3_content, (
            "Rule #3 must be about authoritative sources"
        )
        assert "MUST be consulted" in rule_3_content, (
            "Rule #3 must require consultation of authoritative sources"
        )

        # Check for specific authoritative sites
        authoritative_sites = [
            "python.org",
            "docs.python.org/3/library/typing.html",
            "docs.python.org/3/library/asyncio.html",
            "docs.astral.sh/uv",
            "docs.astral.sh/ruff",
            "bandit.readthedocs.io",
            "conventionalcommits.org",
            "docs.pytest.org/en/stable",
            "docs.pypi.org",
            "git-scm.com/docs",
            "docs.github.com/en",
            "packaging.python.org",
            "docs.python.org/3/library/sqlite3.html",
            "sqlite.org/docs.html",
            "postgresql.org/docs/current",
            "yaml.org/spec/1.2.2",
            "pypi.org/project/hatchling",
            "twine-bhrutledge.readthedocs.io/en/stable",
            "tddbuddy.com/references/tdd-cycle.html",
            "ibm.com/think/topics/test-driven-development",
        ]

        for site in authoritative_sites:
            assert site in rule_3_content, f"Rule #3 must reference {site} as authoritative source"

    def test_simplicity_over_complexity_rule(self) -> None:
        """Test that Rule #9 emphasizes simplicity over complexity."""
        config_path = Path(".claude/CLAUDE.md")
        content = config_path.read_text()
        lines = content.split("\n")

        # Find Rule #9
        rule_9_found = False
        rule_9_content = ""
        for i, line in enumerate(lines):
            if line.strip().startswith("## 9."):
                rule_9_found = True
                # Get content of Rule #9 (until next rule or end)
                rule_lines = [line]
                for j in range(i + 1, len(lines)):
                    if lines[j].strip().startswith("## "):
                        break
                    rule_lines.append(lines[j])
                rule_9_content = "\n".join(rule_lines)
                break

        assert rule_9_found, "Rule #9 must exist"
        assert "Simplicity over complexity" in rule_9_content, \
            "Rule #9 must be about simplicity over complexity"
        assert "ALWAYS prefer" in rule_9_content, \
            "Rule #9 must emphasize ALWAYS preferring simplicity"

        # Check for key simplicity principles
        simplicity_principles = [
            "choose the simplest",
            "OVER-ENGINEERING",
            "DIRECT SOLUTIONS",
            "READABILITY FIRST"
        ]

        for principle in simplicity_principles:
            assert principle in rule_9_content, \
                f"Rule #9 must include {principle}"

    def test_natural_language_code_rule(self) -> None:
        """Test that Rule #10 emphasizes natural language code."""
        config_path = Path(".claude/CLAUDE.md")
        content = config_path.read_text()
        lines = content.split("\n")

        # Find Rule #10
        rule_10_found = False
        rule_10_content = ""
        for i, line in enumerate(lines):
            if line.strip().startswith("## 10."):
                rule_10_found = True
                # Get content of Rule #10 (until next rule or end)
                rule_lines = [line]
                for j in range(i + 1, len(lines)):
                    if lines[j].strip().startswith("## "):
                        break
                    rule_lines.append(lines[j])
                rule_10_content = "\n".join(rule_lines)
                break

        assert rule_10_found, "Rule #10 must exist"
        assert "read like natural language" in rule_10_content, \
            "Rule #10 must be about natural language code"
        assert "ALWAYS write naturally" in rule_10_content, \
            "Rule #10 must emphasize ALWAYS writing naturally"

        # Check for key natural language principles
        natural_language_principles = [
            "CONVERSATIONAL NAMING",
            "NATURAL FLOW",
            "SELF-DOCUMENTING",
            "TESTS TOO"
        ]

        for principle in natural_language_principles:
            assert principle in rule_10_content, \
                f"Rule #10 must include {principle}"

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
