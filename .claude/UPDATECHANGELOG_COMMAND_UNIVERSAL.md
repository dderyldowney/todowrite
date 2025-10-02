# Universal AI Agent Access: updatechangelog Command

**Requirement**: The `updatechangelog` command must be available to ALL AI agents (see [SESSION_SUMMARY.md](../SESSION_SUMMARY.md#universal-ai-agents)) and executed before EVERY git commit.

---

## Command Overview

**Purpose**: Regenerates CHANGELOG.md from git commit history following Keep a Changelog format, essential for ISO compliance auditing and emergency incident investigation.

**Usage**: MANDATORY before every git commit.

**Access**: Universal across all AI agents.

---

## Command Execution

```bash
./bin/updatechangelog              # Regenerate CHANGELOG.md from git history
```

**Output**: Regenerated CHANGELOG.md with [Unreleased] section, categorized changes (Added, Changed, Fixed, Security, Documentation, Configuration), Keep a Changelog formatting.

---

## Mandatory Pre-Commit Protocol

**EVERY commit workflow MUST follow**:

1. Make code changes
2. Run updatechangelog → regenerate CHANGELOG.md
3. Review CHANGELOG.md → verify categorization
4. Stage all files → include CHANGELOG.md
5. Commit together → ensure changelog reflects all changes

**Example**:
```bash
# After code changes
./bin/updatechangelog

# Stage everything
git add CHANGELOG.md src/afs_fastapi/equipment/farm_tractor.py

# Commit with both
git commit -m "feat(equipment): add multi-tractor synchronization capability

Implements vector clock-based coordination for autonomous field operations
with ISO 18497 safety compliance."
```

---

## Implementation Architecture

**Executable Script**: bin/updatechangelog (56 lines) bash wrapper with colored output

**Python Generator**: afs_fastapi/scripts/updatechangelog.py extracts git history, categorizes commits, applies Keep a Changelog formatting

**Test Coverage**: 13 tests validating automation and loop protection
- Baseline Functionality (3): Execution, unreleased section, categorization
- Loop Protection (6): Triple-layer breaking, recursive prevention, safety guards
- Agricultural Context (4): ISO terminology, safety highlighting, professional tone

**Test File**: [tests/unit/test_changelog_automation.py](tests/unit/test_changelog_automation.py)

---

## Triple-Layer Loop Protection

**Layer 1**: Skip changelog updates in changelog-specific commits (`if "changelog" in commit_message.lower()`)

**Layer 2**: Skip if ONLY CHANGELOG.md changed (`if changed_files == ["CHANGELOG.md"]`)

**Layer 3**: Skip if recently updated (`if time.time() - changelog_mtime < 300`)

**Purpose**: Prevents infinite regeneration loops during commit automation.

---

## Usage Patterns

**Feature Implementation**: Update changelog, stage with code, commit with agricultural context

**Safety-Critical Bug Fix**: Document emergency stop fixes, ISO 18497 impact, validation results

**Documentation Update**: Include README.md changes, ISO compliance info, specification references

---

## Troubleshooting

**CHANGELOG.md not found**: Script automatically creates with proper format

**No commits to add**: Normal if no commits since last update, proceed with commit

**Agricultural context missing**: Manually edit CHANGELOG.md to add ISO compliance details

**Keep a Changelog format incorrect**: Re-run updatechangelog or fix manually following keepachangelog.com

**CHANGELOG.md not staged**: `git add CHANGELOG.md` before committing

---

## Integration

**Related Commands**:
- `updatewebdocs` - Similar mandatory requirement for README.md changes
- `runtests` - Validate platform health before changelog generation
- `savesession` - Captures changelog automation status
- `whereweare` - Shows CHANGELOG.md in documentation status

**Session Architecture Role**: Phase 6 (Helper Commands) with Phase 4 (Enforcement) integration

---

## Summary

**Requirement**: ALL AI agents must execute updatechangelog BEFORE EVERY git commit to maintain complete change tracking required for safety-critical agricultural equipment certification.

**Rationale**: Missing or incomplete CHANGELOG.md compromises ISO 18497 safety certification, ISO 11783 ISOBUS compliance auditing, emergency incident investigation, regulatory reporting, and liability protection. Complete audit trails essential for autonomous multi-tractor coordination systems.

---

**Version**: 1.0.0 | **Updated**: October 2, 2025 | **Status**: MANDATORY
