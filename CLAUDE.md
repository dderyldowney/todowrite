# Claude Code Configuration for AFS FastAPI

This file contains project-specific instructions for Claude Code sessions working on the **AFS FastAPI robotic agriculture platform**.

## Mandatory Requirements for All AI Agents

> **See Authoritative Reference**: [SESSION_SUMMARY.md](SESSION_SUMMARY.md#mandatory-requirements-for-all-ai-agents)
>
> All mandatory requirements are documented in SESSION_SUMMARY.md to maintain a single source of truth and avoid duplication.

**Six Universal Requirements** (enforced via pre-commit hooks):

1. **Test-First Development** - RED-GREEN-REFACTOR methodology drives all implementation
2. **Structured Investigation Pattern** - Investigation steps, files examined, evidence, analysis
3. **Standardized Test Reporting** - Executive summary, insights, distribution, health indicators
4. **CHANGELOG Triple-Layer Loop Protection** - Included in every commit with hash-range protection
5. **Git Commit Separation** - Single concern rule with proper type(scope) format
6. **Cross-Agent Infrastructure Sharing** - Automatic updates to all agent configurations

**Claude Code Specific Notes**:
- Session initialization via `loadsession` command loads all mandatory requirements
- Pre-commit hooks validate compliance automatically
- Agricultural context required for safety-critical code (ISO 18497, ISO 11783)

## Format-First Generation Standards

**Requirement**: All generated content must emerge in final quality-controlled form.

### Format-First Protocol

**NO FORMATTING CYCLES**: Generate all code, tests, and documentation pre-formatted to quality standards.

1. **Code Generation**: Apply Black, isort, Ruff compliance during creation
2. **Type Safety**: Include proper type annotations from initial generation
3. **Agricultural Context**: Embed domain-specific examples and scenarios
4. **Quality Standards**: Meet enterprise-grade requirements immediately

### Pre-Formatted Generation Templates

**Python Code Template**:
```python
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

class AgriculturalComponent:
    """Agricultural robotics component for tractor coordination.

    Provides functionality for multi-tractor field operations with
    safety compliance and performance optimization.
    """

    def __init__(self, equipment_id: str) -> None:
        """Initialize agricultural equipment interface."""
        self.equipment_id = equipment_id
        self.operational_status = "ready"

    def coordinate_field_operation(self, operation_data: Dict[str, Any]) -> bool:
        """Execute coordinated field operation with fleet synchronization."""
        return True
```

**Test Generation Template**:
```python
import pytest
from afs_fastapi.equipment.farm_tractors import FarmTractor

class TestAgriculturalOperation:
    """Test agricultural equipment operations for field coordination."""

    def test_tractor_field_coordination(self) -> None:
        """Test multi-tractor coordination during field cultivation."""
        # RED: Describe desired agricultural behavior
        tractor = FarmTractor(equipment_id="FIELD_CULTIVATOR_01")

        # Test agricultural operation
        result = tractor.execute_cultivation_pattern()

        assert result is True
        assert tractor.field_status == "cultivation_complete"
```

### Error Monitoring Integration

**Common Error Solutions**:
- **Module Imports**: Use `fixmodules` command for package installation
- **Type Issues**: Apply proper annotations during generation
- **Formatting**: Pre-format all content to prevent cycles
- **Commit Violations**: Follow `committemplate` for separation compliance

**Error Prevention**:
- Monitor patterns across sessions
- Store solutions in SESSION_SUMMARY.md
- Create reusable commands for common fixes
- Apply quality standards from initial generation

### CHANGELOG.md Maintenance

**Requirement**: CHANGELOG.md must be regenerated, formatted, and included in every git commit.

**Before Every Commit Protocol**:
1. **Regenerate CHANGELOG.md**: Use `updatechangelog` command to include all changes
2. **Format according to standards**: Keep a Changelog format with agricultural context
3. **Add to git staging**: Include CHANGELOG.md alongside other changes
4. **Commit with complete changelog**: Ensure changelog reflects all changes up to and including that commit

**Cross-Session Enforcement**:
- CHANGELOG.md updates mandatory before all commits
- Agricultural context required for safety-critical entries
- Keep a Changelog formatting standards applied
- Version history completeness validated

### Web Documentation Synchronization

**Requirement**: When README.md changes, docs/index.html must be regenerated and included in the same commit.

**README.md Update Protocol**:
1. **Edit README.md**: Make documentation changes to markdown source
2. **Regenerate HTML**: Use `updatewebdocs` command to convert README.md → docs/index.html
3. **Validate output**: Verify docs/index.html generated correctly
4. **Stage both files**: Include both README.md and docs/index.html in git staging
5. **Commit together**: Ensure web documentation stays synchronized with markdown

**Command Usage**:
```bash
# After editing README.md
./bin/updatewebdocs

# Command automatically:
# - Converts README.md to HTML with professional styling
# - Creates docs/ directory if missing
# - Adds docs/index.html to git staging
# - Preserves agricultural terminology and technical specs
```

**Cross-Session Enforcement**:
- HTML updates mandatory when README.md changes
- Prevents documentation drift between markdown and web formats
- Professional presentation critical for stakeholder communication
- ISO compliance auditing requires synchronized documentation
- Command documented in .claude/commands/updatewebdocs.md

**Agricultural Context**: Web documentation essential for equipment operators, safety engineers, and compliance auditors who access project information via browsers. Automated HTML generation ensures stakeholders see current documentation without viewing raw markdown.

## Code Documentation Requirements

**Educational Code Explanations**: All code generated must be explained both **overall** and **individually**. Explanations should be concise with the dual purpose of teaching while building this real-world professional project.

### Explanation Structure

1. **Architecture Level**
   - Explain design patterns, system integration, and why specific approaches were chosen
   - Cover how components fit into the broader agricultural robotics ecosystem

2. **Implementation Level**
   - Detail how individual components work, function purposes, and technical specifics
   - Include code-level explanations for complex algorithms or business logic

3. **Professional Context**
   - Cover industry best practices and enterprise development standards
   - Explain domain-specific concepts (ISOBUS, ISO 18497 safety, agricultural robotics)

### Educational Focus Areas

#### Modern Python Patterns

- Type hints, dataclasses, ABC inheritance
- Python 3.12+ features (union types, pattern matching)

#### Agricultural Technology Standards

- ISOBUS communication protocols (ISO 11783)
- Safety compliance systems (ISO 18497)
- Professional agricultural equipment interfaces

**Authoritative ISO 11783 Reference Documentation**:

The platform includes authoritative ISO 11783 technical specifications that must be referenced for all ISOBUS-related work:

- **[docs/iso11783-11-online_data_base.pdf](docs/iso11783-11-online_data_base.pdf)**: Complete ISO 11783-11 specifications
- **[docs/isoExport_csv.zip](docs/isoExport_csv.zip)**: Machine-readable protocol definitions
- **[docs/isobus-osi-model-layer-iso-11783.svg](docs/isobus-osi-model-layer-iso-11783.svg)**: OSI model architecture diagram

**Mandatory Reference Requirements**:
- All ISOBUS implementation decisions must cite specific sections from authoritative documentation
- Educational explanations about ISOBUS must reference official specifications
- Compliance validation requires verification against ISO 11783 standards
- Code generation for ISOBUS features must align with specification requirements

#### Distributed Systems Concepts

- Conflict-Free Replicated Data Types (CRDTs)
- Vector clocks for operation ordering
- Multi-tractor fleet coordination and synchronization

#### Enterprise Development Practices

- API design and serialization best practices
- Comprehensive testing strategies (unit, integration, feature)
- Code quality automation and CI/CD workflows

## Project Context

**AFS FastAPI** is an enterprise-grade robotic agriculture platform implementing:

- **Fleet Coordination**: Multi-tractor synchronization with conflict resolution
- **Industry Compliance**: Professional agricultural interface compliance (ISO 11783, ISO 18497)
- **Robotic Interfaces**: Six major categories of enhanced interfaces:
  - ISOBUS Communication
  - Safety & Compliance Systems
  - Motor Control Interfaces
  - Data Management Systems
  - Power Management
  - Vision & Sensor Systems
- **Modern Development**: Python 3.12+ with comprehensive testing and code quality standards

## Code Quality Standards

- **Formatting Tools**: Black, ruff, isort aligned with consistent configuration
- **Testing Coverage**: Comprehensive unit, integration, and feature tests
- **Code Quality**: Zero linting warnings maintained across all modules
- **Modern Syntax**: Python 3.12+ features, union types, proper type annotations
- **Documentation**: Inline documentation for complex agricultural domain logic

## Testing Documentation

**WORKFLOW.md** is the **complete authoritative reference** for the AFS FastAPI testing architecture:

 - **161 tests** across 3-layer architecture (Feature, Unit, Root-level tests, plus enforcement hooks)
- **Professional agricultural standards** compliance (ISOBUS ISO 11783, Safety ISO 18497)
- **Complete test flow patterns** and execution commands
- **Domain coverage analysis** for Equipment, Monitoring, API, and Infrastructure
- **Performance metrics** and quality assurance framework

> **Important**: Always reference WORKFLOW.md when working with tests, understanding test patterns, or explaining the testing strategy. This document captures the sophisticated testing approach used in this enterprise-grade agricultural robotics platform.

## Development Workflow

- **Test-First Development**: Use Red-Green-Refactor methodology for all synchronization infrastructure (see TDD_WORKFLOW.md)
- **Branch Strategy**: Work on `develop` branch for new features
- **Version Control**: Use semantic versioning and proper Git workflow
- **Documentation**: Document technical decisions and architectural changes
- **Testing**: Maintain comprehensive test coverage (see WORKFLOW.md for complete reference)
- **Code Review**: All changes reviewed for educational value and professional standards

### Environment Sanity (pyenv)

- Verify pyenv is healthy before development:
  - `pyenv --version` prints a version with no errors
  - `pyenv rehash` runs clean (no “shims isn’t writable”)
- If you see the shims error, run: `chmod u+rwx ~/.pyenv/shims && pyenv rehash`.
- Keep zsh init in `~/.zshrc`; ensure `~/.bash_profile` is bash-safe, for example:
  - `export PYENV_ROOT="$HOME/.pyenv"`
  - `[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"`
  - `eval "$(pyenv init -)"`
  - Optionally: `eval "$(pyenv virtualenv-init -)"` if plugin installed
- See the Quick Verification Checklist in `CONTRIBUTING.md` for full details.

### Documentation and Commit Message Standards

**Professional Tone Requirements**:
- Use clear, factual language without marketing superlatives
- Avoid excessive capitalization, emojis, or promotional rhetoric
- Focus on what was accomplished rather than subjective assessments
- Write commit messages using standard conventions (type(scope): description)

**Git Commit Separation of Concerns**:
- **Critical requirement**: All commits must follow strict separation of concerns methodology
- **Single Concern Rule**: Each commit addresses exactly one logical concern (feat, fix, docs, refactor, test, config, perf, security)
- **Automated Enforcement**: Pre-commit hooks validate separation compliance and reject non-compliant commits
- **Cross-Session Persistence**: Requirements embedded permanently in project configuration

**Commit Message Format (ENFORCED)**:
```
type(scope): brief description of change

Optional detailed explanation focusing on:
- What was changed and why (single concern only)
- Technical implementation details
- Agricultural robotics context when applicable

Valid types: feat, fix, refactor, docs, test, config, perf, security
Required scope: equipment, coordination, api, monitoring, safety, etc.
Agricultural context: Required for feat, fix, refactor, perf, security types
```

**Examples of Proper Separation**:
```
feat(equipment): add multi-tractor synchronization capability
fix(coordination): resolve vector clock synchronization race condition
refactor(api): consolidate equipment status endpoints
docs(safety): add comprehensive emergency stop procedures
test(integration): enhance multi-field operation validation
config(hooks): add commit separation enforcement
```

**Separation Enforcement**:
- **Pre-commit validation**: `.claude/hooks/commit_separation_enforcement.py`
- **Documentation reference**: `GIT_COMMIT_SEPARATION_MANDATORY.md`
- **Quality gates**: Prevents commits addressing multiple concerns
- **Agricultural context**: Required for safety-critical agricultural robotics development

**Documentation Style**:
- Technical accuracy over promotional language
- Measured descriptions of capabilities and status
- Professional terminology appropriate for engineering teams
- Educational content without excessive emphasis

### Mandatory Test-Driven Development for All Components

**Policy**: All future development on AFS FastAPI must follow Test-Driven Development methodology:

1. **RED Phase**: Write failing test describing agricultural robotics behavior
2. **GREEN Phase**: Implement minimal code meeting performance and safety requirements
3. **REFACTOR Phase**: Enhance code quality while maintaining enterprise standards

**ENFORCEMENT**: Automated pre-commit hooks validate TDD compliance before any code changes are accepted.

**Reference Documentation**:
- TDD_WORKFLOW.md: Complete Test-First development guide with agricultural domain examples
- TDD_FRAMEWORK_MANDATORY.md: Comprehensive mandatory TDD framework and enforcement policies

## Session Initialization Architecture

**Complete Execution Order**: [docs/EXECUTION_ORDER.md](docs/EXECUTION_ORDER.md)

The platform uses a sophisticated 6-phase session initialization architecture with 28+ files working together to establish conceptual, contextual, and functional session state for all AI agents.

**Key Phases**:
1. **Automatic Hook-Based Initialization** - Claude Code hooks detect new sessions
2. **Manual Session Loading** - `bin/loadsession` provides fallback context restoration
3. **Conceptual Context Loading** - CLAUDE.md, SESSION_SUMMARY.md, AGENTS.md define requirements
4. **Enforcement & Validation** - Hooks validate compliance with mandatory requirements
5. **Mandatory Requirement References** - Complete specifications for universal AI agents
6. **Helper Commands & Utilities** - Additional session-related documentation and tools

**Session Initialization Execution**:
- **Automatic**: [.claude/hooks/session_initialization.py](.claude/hooks/session_initialization.py) detects new sessions via 5-minute staleness detection
- **Manual**: `bin/loadsession` command explicitly loads context
- **Documentation**: SESSION_SUMMARY.md provides primary session state (578 lines)
- **Test Coverage**: 10 tests validate automatic initialization logic

## Claude Command Integration

### Command Trigger Framework

The platform provides 7 universal session management commands available to all AI agents:

**Available Commands** (complete specifications in [SESSION_SUMMARY.md](SESSION_SUMMARY.md#universal-session-management-commands)):
- **loadsession** - Restore complete project context (execute after `/new`)
- **savesession** - Capture session state with mandatory compaction
- **runtests** - Execute test suite with standardized reporting
- **whereweare** - Display/generate strategic assessment
- **updatedocs** - Regenerate all 6 core documentation files
- **updatechangelog** - Regenerate CHANGELOG.md with loop protection
- **updatewebdocs** - Convert README.md → docs/index.html

**Detailed Documentation**: See [SESSION_SUMMARY.md - Universal Session Management Commands](SESSION_SUMMARY.md#universal-session-management-commands) for complete usage, functionality, and references.

**Claude Code Integration**:
- Commands executable via bash: `./bin/commandname`
- Select commands available as slash commands: `/loadsession`, `/whereweare`, `/updatedocs`
- Command triggers stored in `.claude/commands/` with complete specifications

---

**Purpose**: This ensures knowledge transfer alongside deliverable code, making the codebase both functional and instructional for professional agricultural technology development.
