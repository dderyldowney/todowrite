# Universal AI Agent Access: whereweare Command

**Requirement**: The `whereweare` command must be available to ALL AI agents (see [SESSION_SUMMARY.md](../SESSION_SUMMARY.md#universal-ai-agents)) for strategic assessment.

---

## Command Overview

**Purpose**: Displays or generates comprehensive platform state assessment (480+ lines) for ISO compliance planning and stakeholder communication.

**Usage**: ISO compliance auditing, stakeholder presentations, development planning.

**Access**: Universal across all AI agents.

---

## Dual-Mode Operation

### Display Mode (Default)

```bash
./bin/whereweare              # Display existing WHERE_WE_ARE.md
/whereweare                   # Claude Code slash command
```

**Output**: 480+ line document with executive summary, strategic positioning, current release status, architectural overview, testing architecture, strategic roadmap.

### Generation Mode

```bash
./bin/whereweare --generate   # Regenerate from current platform state
```

**Sources**: README.md, SESSION_SUMMARY.md, git metrics (tags, branch), test metrics (pytest --collect-only)

**Purpose**: Synthesize WHERE_WE_ARE.md ensuring documentation synchronized with actual platform state.

---

## Implementation Architecture

**Executable Script**: bin/whereweare (215 lines) with colored output, dual-mode support, error handling

**Document Generator**: docs/generate_where_we_are.py (357 lines) extracts git metrics, collects test counts, parses documentation

**Test Coverage**: 13 tests (100% passing)
- Display Tests (9): Existence, permissions, sections, error handling, colored output
- Generation Tests (4): Creation, metrics inclusion, updates, source requirements

**Test File**: [tests/unit/test_whereweare.py](../tests/unit/test_whereweare.py)

---

## Usage Patterns

**ISO Compliance Audit**: Display current ISO 11783/ISO 18497 compliance status for auditors

**Stakeholder Presentation**: Generate updated assessment with current version, test counts, capabilities for procurement meetings

**Development Planning**: Review current focus, next phase priorities, foundation readiness for team planning

---

## Troubleshooting

**Document missing**: Run `--generate` to create WHERE_WE_ARE.md

**Permission denied**: `chmod +x bin/whereweare`

**Generation fails**: Verify README.md, SESSION_SUMMARY.md exist; check git repository status

**Outdated metrics**: Use `--generate` to regenerate from current platform state

---

## Integration

**Related Commands**:
- `loadsession` - Loads context including whereweare documentation
- `updatedocs` - Orchestrates whereweare --generate with other doc commands
- `savesession` - Records strategic assessment status
- `updatechangelog` - Documents version history

**Session Architecture Role**: Phase 6 (Helper Commands) for strategic visibility

---

## Summary

**Requirement**: ALL AI agents must remember and utilize whereweare for strategic assessment access, ISO compliance support, stakeholder communication, and development planning.

**Rationale**: Essential for farm equipment safety engineering, autonomous tractor fleet management, and ISO compliance in safety-critical multi-tractor coordination systems.

---

**Version**: 1.0.0 | **Updated**: October 1, 2025 | **Status**: MANDATORY
