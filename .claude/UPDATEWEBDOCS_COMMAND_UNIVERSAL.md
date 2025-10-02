# Universal AI Agent Access: updatewebdocs Command

**Requirement**: The `updatewebdocs` command must be available to ALL AI agents (see [SESSION_SUMMARY.md](../SESSION_SUMMARY.md#universal-ai-agents)) and executed whenever README.md changes.

---

## Command Overview

**Purpose**: Converts README.md to docs/index.html with professional styling, ensuring web documentation synchronization.

**Usage**: MANDATORY when README.md changes.

**Access**: Universal across all AI agents.

---

## Command Execution

```bash
./bin/updatewebdocs                # Convert README.md → docs/index.html
./bin/updatewebdocs --test-mode    # Test mode (no git staging)
```

**Output**: Professional HTML with agricultural robotics styling, syntax-highlighted code blocks, preserved terminology (ISOBUS, ISO 11783, ISO 18497, vector clocks), GFM extensions (tables, task lists, strikethrough), automatic git staging.

---

## Mandatory README.md Update Protocol

**EVERY README.md change workflow MUST follow**:

1. Edit README.md → make documentation changes
2. Regenerate HTML → execute updatewebdocs
3. Validate output → verify docs/index.html generated
4. Stage both files → include README.md and docs/index.html
5. Commit together → ensure web docs synchronized

**Example**:
```bash
# After editing README.md
vim README.md

# Regenerate HTML
./bin/updatewebdocs

# Stage both files
git add README.md docs/index.html

# Commit together
git commit -m "docs(docs): update ISO compliance documentation

Adds comprehensive ISO 11783 ISOBUS compliance status for regulatory auditing."
```

---

## Implementation Architecture

**Executable Script**: bin/updatewebdocs (132 lines) with colored output, error handling, automatic git staging

**Python Converter**: docs/convert_readme_to_index_html.py converts markdown using CommonMark parser, GFM extensions, professional agricultural robotics styling

**Test Coverage**: 11 tests (100% passing)
- Command Execution (3): Existence, permissions, help output
- HTML Generation (4): Conversion accuracy, formatting, code blocks, terminology
- Git Integration (2): Automatic staging, commit guidance
- Agricultural Context (2): ISO terminology, technical specifications

**Test File**: [tests/unit/commands/test_updatewebdocs.py](tests/unit/commands/test_updatewebdocs.py)

---

## Usage Patterns

**ISO Compliance Update**: Add ISO 11783 compliance details to README.md, regenerate HTML for auditor access

**Test Suite Metrics Update**: Update test counts (195→214), synchronize web documentation with current metrics

**Stakeholder Presentation**: Ensure web docs current for executive presentations, professional HTML for procurement meetings

---

## Troubleshooting

**README.md not found**: Verify README.md location (`ls -la README.md`)

**Converter script not found**: Check docs/convert_readme_to_index_html.py exists, restore from git if missing

**HTML conversion failed**: Verify Python markdown library installed (`pip install markdown`), run converter directly for detailed error

**docs/index.html not staged**: Manual staging (`git add docs/index.html`), verify git repository

**Agricultural terminology not preserved**: Review README.md formatting, regenerate, verify in HTML with grep

**Permission denied**: `chmod +x bin/updatewebdocs`

---

## Integration

**Related Commands**:
- `updatechangelog` - Similar mandatory pre-commit requirement
- `updatedocs` - Meta-command orchestrating updatewebdocs with other doc commands
- `runtests` - Validates platform before documentation updates
- `whereweare` - Shows synchronized documentation status

**Session Architecture Role**: Phase 6 (Helper Commands) with Phase 4 (Enforcement) integration

---

## HTML Generation Details

**Professional Styling**: Agricultural robotics theme, responsive design, print-friendly formatting, syntax-highlighted code blocks

**Technical Preservation**: ISO terminology exactly preserved, test count accuracy maintained, performance metrics correct, equipment specifications professional

**GFM Extensions**: Tables, footnotes, task lists, strikethrough for comprehensive markdown support

**CommonMark Compliance**: Python markdown library with fenced_code, tables, footnotes, sane_lists, nl2br extensions

---

## Summary

**Requirement**: ALL AI agents must execute updatewebdocs WHENEVER README.md changes to maintain documentation synchronization required for stakeholder communication and regulatory compliance.

**Rationale**: Unsynchronized README.md/docs/index.html compromises stakeholder communication (executives viewing outdated HTML), ISO compliance presentation (auditors seeing incorrect status), equipment operator access (field operators missing safety updates), and professional standards (documentation drift demonstrates poor quality control).

---

**Version**: 1.0.0 | **Updated**: October 2, 2025 | **Status**: MANDATORY
