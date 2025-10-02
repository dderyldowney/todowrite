# Universal AI Agent Access: savesession Command

**Requirement**: The `savesession` command must be available to ALL AI agents (see [SESSION_SUMMARY.md](../SESSION_SUMMARY.md#universal-ai-agents)) across all development sessions.

---

## Command Overview

**Purpose**: Captures complete session state with mandatory compaction protocol to prevent knowledge fragmentation.

**Usage**: End-of-session state preservation with SESSION_SUMMARY.md compaction.

**Access**: Universal across all AI agents.

---

## Command Execution

```bash
./bin/savesession              # Create dated session state snapshot
```

**Output**: Creates `docs/monitoring/SESSION_STATE_YYYY_MM_DD.md` containing platform metrics, git state, mandatory requirements, and development priorities.

---

## Mandatory Compaction Protocol

**Why Required**: Without compaction, session knowledge fragments across dated snapshots, making SESSION_SUMMARY.md stale and degrading cross-agent accessibility.

**Workflow**:
1. Execute savesession → creates dated snapshot
2. Review snapshot achievements and metrics
3. Update SESSION_SUMMARY.md with critical changes
4. Commit compacted state with CHANGELOG.md
5. Archive old snapshots (optional)
6. Verify with loadsession

**Compaction Trigger**: After significant features, before major work, at session end.

---

## Implementation Architecture

**Executable Script**: bin/savesession (165 lines) with colored output, git state collection, platform metrics capture

**State Storage**:
- Dated snapshots: `docs/monitoring/SESSION_STATE_YYYY_MM_DD.md`
- Compacted state: `docs/monitoring/SESSION_SUMMARY.md` (authoritative)

**Test Coverage**: Manual validation (bash script - no dedicated test suite)

---

## Usage Pattern

**End-of-Session**: Execute savesession, review snapshot, compact into SESSION_SUMMARY.md, commit with CHANGELOG.md

**Pre-Push**: Capture state before pushing commits to remote

**Cross-Agent Handoff**: Save state when switching AI assistants (Claude → Copilot)

---

## Troubleshooting

**Snapshot exists**: Type 'y' to overwrite or 'n' to cancel

**Permission denied**: `chmod +x bin/savesession`

**Directory missing**: `mkdir -p docs/monitoring`

**Multiple snapshots accumulating**: Batch review, compact to SESSION_SUMMARY.md, archive processed snapshots

---

## Integration

**Related Commands**:
- `loadsession` - Restores compacted context
- `updatechangelog` - Run during compaction
- `whereweare` - Verify current status
- `updatedocs` - Comprehensive doc refresh

**Session Architecture Role**: Phase 3 (Conceptual Context Loading) input via SESSION_SUMMARY.md

---

## Summary

**Requirement**: ALL AI agents must execute savesession at end of sessions and assist with SESSION_SUMMARY.md compaction.

**Rationale**: Complete change history essential for ISO compliance auditing (ISO 18497, ISO 11783) and emergency incident investigation in safety-critical agricultural robotics.

---

**Version**: 1.0.0 | **Updated**: October 2, 2025 | **Status**: MANDATORY
