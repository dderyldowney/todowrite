# Universal AI Agent Access: updatedocs Command

**Requirement**: The `updatedocs` command must be available to ALL AI agents (see [SESSION_SUMMARY.md](../SESSION_SUMMARY.md#universal-ai-agents)) for unified documentation synchronization.

---

## Command Overview

**Purpose**: Meta-command orchestrating regeneration of all 6 core documentation files ensuring synchronized platform state for ISO compliance auditing and stakeholder communication.

**Usage**: After major development work, before releases, targeted updates.

**Access**: Universal across all AI agents.

---

## Three Operational Modes

### 1. Update All Mode (Default)

```bash
./bin/updatedocs                  # Regenerate all 6 core documents
```

**6 Core Documents**:
1. WHERE_WE_ARE.md (Strategic assessment)
2. docs/index.html (Web documentation)
3. CHANGELOG.md (Version history)
4. Test reports (Platform health)
5. Session state (Development metrics)
6. Documentation statistics (Status dashboard)

### 2. Dry-Run Mode

```bash
./bin/updatedocs --dry-run        # Preview without executing
```

**Purpose**: Display planned updates without making changes.

### 3. Selective Update Mode

```bash
./bin/updatedocs --only=whereweare,changelog    # Update specific documents
```

**Valid Names**: whereweare, webdocs, changelog, tests, session, stats

---

## Implementation Architecture

**Primary Script**: bin/updatedocs (267 lines) with argument parsing, update orchestration, colored output, error handling

**Orchestrated Commands**:
1. `whereweare --generate` - Strategic assessment
2. `updatewebdocs` - README.md → docs/index.html
3. `updatechangelog` - Git commits → CHANGELOG.md
4. `runtests -q` - Platform health validation
5. Session state tracking
6. Documentation statistics

**Test Suite**: tests/unit/test_updatedocs.py (231 lines, 13 tests)
- Existence Tests (2): Script exists, executable permissions
- Functionality Tests (6): Help, WHERE_WE_ARE, CHANGELOG, web docs, colored output, summary
- Mode Tests (3): Dry-run, selective update, agricultural context
- Error Handling (2): Sub-command failures, 6 documents reference

---

## Usage Patterns

**After Major Work**: Complete development, commit changes, run updatedocs, verify synchronization

**Before Release/Tagging**: Ensure all docs current, review strategic assessment, tag release

**Targeted Updates**: After README.md changes (--only=webdocs), after git commits (--only=changelog)

**Documentation Review**: Preview with --dry-run, execute specific updates

---

## Integration Workflow

```bash
# Standard workflow
./bin/loadsession              # 1. Load session context
./bin/whereweare               # 2. View current assessment
# ... development work ...
./bin/updatedocs               # 3. Update all docs
./bin/savesession              # 4. Save session state
```

**Related Commands**:
- `loadsession` - Loads context including updatedocs documentation
- `whereweare` - Strategic assessment (orchestrated by updatedocs)
- `updatewebdocs` - Web docs (orchestrated by updatedocs)
- `updatechangelog` - Version history (orchestrated by updatedocs)

---

## Troubleshooting

**Sub-command failures**: Check docs/strategic/ exists (`mkdir -p docs/strategic`), retry updatedocs

**Permission denied**: `chmod +x bin/updatedocs`

**Missing dependencies**: Verify all command scripts exist (`ls bin/whereweare bin/updatewebdocs bin/updatechangelog`)

**Validation**: After execution, check WHERE_WE_ARE.md updated, verify web docs generated, confirm CHANGELOG.md current

---

## Summary

**Requirement**: ALL AI agents must execute updatedocs for unified documentation synchronization ensuring ISO compliance materials audit-ready and stakeholder communication materials current.

**Rationale**: Safety-critical agricultural robotics demands synchronized documentation across all core documents to prevent documentation drift compromising ISO compliance auditing (ISO 11783, ISO 18497) and stakeholder communication.

---

**Version**: 1.0.0 | **Updated**: October 01, 2025 | **Status**: MANDATORY
