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

    def test_test_organization_rule(self) -> None:
        """Test that Rule #8 emphasizes component and subsystem test organization."""
        config_path = Path(".claude/CLAUDE.md")
        content = config_path.read_text()
        lines = content.split("\n")

        # Find Rule #8
        rule_8_found = False
        rule_8_content = ""
        for i, line in enumerate(lines):
            if line.strip().startswith("## 8."):
                rule_8_found = True
                # Get content of Rule #8 (until next rule or end)
                rule_lines = [line]
                for j in range(i + 1, len(lines)):
                    if lines[j].strip().startswith("## "):
                        break
                    rule_lines.append(lines[j])
                rule_8_content = "\n".join(rule_lines)
                break

        assert rule_8_found, "Rule #8 must exist"
        assert "component and subsystem" in rule_8_content, \
            "Rule #8 must be about component and subsystem organization"
        assert "SoC REQUIRED" in rule_8_content, \
            "Rule #8 must require Separation of Concerns"

        # Check for key test organization principles
        test_organization_principles = [
            "SEPARATION OF CONCERNS",
            "NO MONOLITHIC FILES",
            "COMPONENT-FIRST",
            "SUBSYSTEM-SPECIFIC",
            "MAINTAINABILITY",
            "SCALABILITY"
        ]

        for principle in test_organization_principles:
            assert principle in rule_8_content, \
                f"Rule #8 must include {principle}"

        # Check for directory structure examples
        directory_examples = [
            "lib/",
            "cli/",
            "web/",
            "features/",
            "unittests/",
            "shared/"
        ]

        for example in directory_examples:
            assert example in rule_8_content, \
                f"Rule #8 must include {example} directory example"

        # Check for monorepo package mapping
        package_mappings = [
            "MONOREPO PACKAGE MAPPING",
            "todowrite",
            "todowrite_cli",
            "todowrite_web"
        ]

        for mapping in package_mappings:
            assert mapping in rule_8_content, \
                f"Rule #8 must include {mapping} package reference"

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

    def test_never_fake_code_rule(self) -> None:
        """Test that Rule #4 prohibits fake code and mandates real implementations."""
        config_path = Path(".claude/CLAUDE.md")
        content = config_path.read_text()
        lines = content.split("\n")

        # Find Rule #4
        rule_4_found = False
        rule_4_content = ""
        for i, line in enumerate(lines):
            if line.strip().startswith("## 4."):
                rule_4_found = True
                # Get content of Rule #4 (until next rule or end)
                rule_lines = [line]
                for j in range(i + 1, len(lines)):
                    if lines[j].strip().startswith("## "):
                        break
                    rule_lines.append(lines[j])
                rule_4_content = "\n".join(rule_lines)
                break

        assert rule_4_found, "Rule #4 must exist"
        assert "NEVER fake code" in rule_4_content, \
            "Rule #4 must be about never faking code"
        assert "REAL implementations only" in rule_4_content, \
            "Rule #4 must require real implementations only"

        # Check for key anti-faking principles
        anti_faking_principles = [
            "use 'pass'",
            "fake implementations",
            "write actual",
            "NO TRICKS"
        ]

        for principle in anti_faking_principles:
            assert principle in rule_4_content, \
                f"Rule #4 must include {principle}"

    def test_always_test_actual_implementation_rule(self) -> None:
        """Test that Rule #5 requires testing actual implementation."""
        config_path = Path(".claude/CLAUDE.md")
        content = config_path.read_text()
        lines = content.split("\n")

        # Find Rule #5
        rule_5_found = False
        rule_5_content = ""
        for i, line in enumerate(lines):
            if line.strip().startswith("## 5."):
                rule_5_found = True
                # Get content of Rule #5 (until next rule or end)
                rule_lines = [line]
                for j in range(i + 1, len(lines)):
                    if lines[j].strip().startswith("## "):
                        break
                    rule_lines.append(lines[j])
                rule_5_content = "\n".join(rule_lines)
                break

        assert rule_5_found, "Rule #5 must exist"
        assert "test actual implementation" in rule_5_content, \
            "Rule #5 must be about testing actual implementation"
        assert "REAL testing only" in rule_5_content, \
            "Rule #5 must require real testing only"

        # Check for key real testing principles
        real_testing_principles = [
            "test the actual implementation",
            "REAL INTERACTIONS",
            "NO MOCKING",
            "VERIFIABLE BEHAVIOR"
        ]

        for principle in real_testing_principles:
            assert principle in rule_5_content, \
                f"Rule #5 must include {principle}"

    def test_simplicity_over_complexity_rule(self) -> None:
        """Test that Rule #11 emphasizes simplicity over complexity."""
        config_path = Path(".claude/CLAUDE.md")
        content = config_path.read_text()
        lines = content.split("\n")

        # Find Rule #11
        rule_11_found = False
        rule_11_content = ""
        for i, line in enumerate(lines):
            if line.strip().startswith("## 11."):
                rule_11_found = True
                # Get content of Rule #11 (until next rule or end)
                rule_lines = [line]
                for j in range(i + 1, len(lines)):
                    if lines[j].strip().startswith("## "):
                        break
                    rule_lines.append(lines[j])
                rule_11_content = "\n".join(rule_lines)
                break

        assert rule_11_found, "Rule #11 must exist"
        assert "Simplicity over complexity" in rule_11_content, \
            "Rule #11 must be about simplicity over complexity"
        assert "ALWAYS prefer" in rule_11_content, \
            "Rule #11 must emphasize ALWAYS preferring simplicity"

        # Check for key simplicity principles
        simplicity_principles = [
            "choose the simplest",
            "OVER-ENGINEERING",
            "DIRECT SOLUTIONS",
            "READABILITY FIRST"
        ]

        for principle in simplicity_principles:
            assert principle in rule_11_content, \
                f"Rule #11 must include {principle}"

    def test_natural_language_code_rule(self) -> None:
        """Test that Rule #12 emphasizes natural language code."""
        config_path = Path(".claude/CLAUDE.md")
        content = config_path.read_text()
        lines = content.split("\n")

        # Find Rule #12
        rule_12_found = False
        rule_12_content = ""
        for i, line in enumerate(lines):
            if line.strip().startswith("## 12."):
                rule_12_found = True
                # Get content of Rule #12 (until next rule or end)
                rule_lines = [line]
                for j in range(i + 1, len(lines)):
                    if lines[j].strip().startswith("## "):
                        break
                    rule_lines.append(lines[j])
                rule_12_content = "\n".join(rule_lines)
                break

        assert rule_12_found, "Rule #12 must exist"
        assert "read like natural language" in rule_12_content, \
            "Rule #12 must be about natural language code"
        assert "ALWAYS write naturally" in rule_12_content, \
            "Rule #12 must emphasize ALWAYS writing naturally"

        # Check for key natural language principles
        natural_language_principles = [
            "CONVERSATIONAL NAMING",
            "NATURAL FLOW",
            "SELF-DOCUMENTING",
            "TESTS TOO"
        ]

        for principle in natural_language_principles:
            assert principle in rule_12_content, \
                f"Rule #12 must include {principle}"

    def test_local_command_line_tools_rule(self) -> None:
        """Test that Rule #10 enforces local command-line tools preference."""
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
        assert "local command-line tools" in rule_10_content, \
            "Rule #10 must be about local command-line tools"
        assert "ALWAYS preferred" in rule_10_content, \
            "Rule #10 must emphasize ALWAYS preferring local tools"

        # Check for key local tool principles
        local_tool_principles = [
            "ALWAYS PREFER",
            "NO LIMITATIONS",
            "sed",
            "awk",
            "grep",
            "jq",
            "PIPELINES",
            "EFFICIENCY",
            "RELIABILITY"
        ]

        for principle in local_tool_principles:
            assert principle in rule_10_content, \
                f"Rule #10 must include {principle}"

    def test_working_directory_boundary_rule(self) -> None:
        """Test that Rule #16 clarifies working directory boundary for each project."""
        config_path = Path(".claude/CLAUDE.md")
        content = config_path.read_text()
        lines = content.split("\n")

        # Find Rule #16 section
        boundary_section_found = False
        boundary_content = ""
        in_boundary_section = False

        for line in lines:
            if "# 16. Working Directory Boundary" in line:
                boundary_section_found = True
                in_boundary_section = True
                boundary_content = line
                continue
            elif in_boundary_section:
                if line.startswith("# ") and "Working Directory Boundary" not in line:
                    break
                boundary_content += "\n" + line

        assert boundary_section_found, "Working Directory Boundary section must exist"

        # Check for key boundary principles
        boundary_principles = [
            "current project's root directory",
            "Each project has its own root directory boundary",
            "afs_fastapi",
            "todowrite",
            "NO CROSS-PROJECT",
            "RESPECT BOUNDARIES"
        ]

        for principle in boundary_principles:
            assert principle in boundary_content, \
                f"Working Directory Boundary must include {principle}"

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
