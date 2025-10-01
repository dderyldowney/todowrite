# Claude Code Configuration for AFS FastAPI

This file contains project-specific instructions for Claude Code sessions working on the **AFS FastAPI robotic agriculture platform**.

## MANDATORY: Test-First Development for ALL Code Generation

**ABSOLUTE REQUIREMENT**: ALL development—Human AND AI/Agent/ML/LLM—MUST start with tests. Testing drives ALL implementation.

### Universal Test-First Protocol

**EVERY code implementation session MUST begin with:**

1. **RED Phase FIRST**: Write failing test that describes desired behavior BEFORE any implementation code
2. **GREEN Phase Implementation**: Write minimal code to satisfy test requirements only
3. **REFACTOR Phase Enhancement**: Improve code quality while maintaining test coverage

### Zero Exceptions Policy

- **NO CODE WITHOUT TESTS**: No functions, classes, modules, or features implemented without failing tests first
- **Human Developers**: Must follow Red-Green-Refactor methodology for all implementation
- **AI/Agent/ML/LLM**: Cannot generate implementation code without corresponding test coverage
- **Documentation Exception**: Tests not required for documentation, comments, HEREDOCs, code examples in docs

### Enforcement Mechanisms

- **Pre-commit hooks**: Validate test-first compliance for all code changes
- **Cross-session persistence**: Requirement embedded permanently in project configuration
- **Automated rejection**: Non-test-first code blocked from entering codebase
- **Agricultural context**: All tests must include relevant agricultural robotics scenarios

### Claude Code Specific Requirements

- **Session Start**: Must acknowledge test-first requirement immediately
- **Code Generation**: MUST write failing tests before generating any implementation
- **Agricultural Context**: Tests must include safety-critical agricultural scenarios
- **Performance Constraints**: Tests must validate embedded equipment limitations

### Universal Application

- **All Contributors**: Human developers, AI assistants, and automated systems
- **All Code Types**: Equipment control, API endpoints, coordination systems, monitoring
- **All Sessions**: Requirement persists across all development sessions
- **Safety Critical**: Essential for ISO 18497 and ISO 11783 compliance

**RATIONALE**: Agricultural robotics demands bulletproof reliability. Test-First Development ensures ALL code—human or AI-generated—meets rigorous standards for safety-critical multi-tractor coordination systems where failures can cause equipment damage or safety incidents.

## MANDATORY: Cross-Agent Infrastructure Sharing

**ABSOLUTE REQUIREMENT**: ANY changes to session management infrastructure MUST be automatically accessible to ALL AI agents.

### Universal Infrastructure Policy

**EVERY infrastructure change MUST ensure:**

1. **Automatic Cross-Agent Availability**: Commands, hooks, validation scripts, and configuration files added to ALL agent configurations
2. **Universal Documentation**: Changes reflected in CLAUDE.md, AGENTS.md, SESSION_SUMMARY.md, and .claude/commands/
3. **Agent-Agnostic Access**: Infrastructure usable by Claude, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer
4. **Cross-Session Memory**: All agents MUST remember and use shared infrastructure across ALL sessions

### Enforcement and Scope

- **Universal Application**: Applies to ALL session management tools, commands, hooks, and configurations
- **Mandatory Synchronization**: Changes cannot be completed until all agent configurations updated
- **Quality Assurance**: Ensures consistent capabilities across all development assistants
- **Agricultural Context**: Essential for maintaining continuity in safety-critical platform development

**RATIONALE**: Safety-critical agricultural robotics requires ALL development assistants to use identical session management infrastructure. Without automatic cross-agent sharing, configuration drift creates inconsistent development experiences and risks losing critical session context across different AI platforms.

## MANDATORY: Structured Investigation Pattern for ALL AI Agent Responses

**ABSOLUTE REQUIREMENT**: ALL AI agent responses (Claude, GPT, Gemini, Copilot, etc.) must follow a structured investigation pattern providing complete transparency into analysis methodology.

### Universal Investigation Protocol

**EVERY substantive response MUST include:**

1. **Investigation Steps**: Numbered list documenting systematic methodology
2. **Files Examined**: Bulleted list with file paths and examination rationale
3. **Evidence Collected**: Factual findings grouped by category with pass/fail indicators
4. **Final Analysis**: Root cause identification, mechanism explanation, and solution options

### Enforcement and Scope

- **Universal Application**: Applies to ALL AI agents (Claude Code, GitHub Copilot, ChatGPT, Gemini, etc.)
- **Cross-Session Persistence**: Requirement embedded permanently in project configuration
- **Agent Agnostic**: Pattern applies regardless of AI platform or implementation
- **Quality Assurance**: Enables verification, auditing, and knowledge transfer
- **Agricultural Context**: Essential for safety-critical system transparency

### Complete Specification

**Reference**: [.claude/INVESTIGATION_PATTERN_MANDATORY.md](.claude/INVESTIGATION_PATTERN_MANDATORY.md)

**RATIONALE**: Safety-critical agricultural robotics demands verifiable reasoning from ALL development assistants (human or AI). Structured investigation patterns enable safety validation, decision auditing, reproducible analysis, and educational knowledge transfer—essential for ISO compliance and bulletproof multi-tractor coordination systems.

## MANDATORY: Standardized Test Reporting for ALL AI Agents

**ABSOLUTE REQUIREMENT**: ALL AI agents must use standardized test reporting format when executing test suites.

### Universal Test Reporting Protocol

**EVERY test execution response MUST include:**

1. **Executive Summary Block**: High-level results with pass/fail status
2. **Insight Block**: Educational analysis of test suite architecture (required when Explanatory style active)
3. **Test Distribution Analysis**: Breakdown by category and domain coverage
4. **Platform Health Indicators**: Checklist of key quality metrics
5. **Agricultural Context**: Safety-critical and ISO compliance highlights
6. **Advisory Notes**: Warnings, deprecations, or recommended improvements

### Enforcement and Scope

- **Universal Application**: Applies to ALL AI agents (Claude Code, GitHub Copilot, ChatGPT, Gemini, CodeWhisperer, etc.)
- **Cross-Session Persistence**: Requirement embedded permanently in project configuration
- **Agent Agnostic**: Pattern applies regardless of AI platform or implementation
- **Test Commands**: Applies to `pytest`, `pytest -v`, `pytest --cov`, and all testing variations
- **Educational Integration**: Enhanced insights when Explanatory output style active

### Complete Specification

**Reference**: [.claude/TEST_REPORTING_MANDATORY.md](.claude/TEST_REPORTING_MANDATORY.md)

**RATIONALE**: Safety-critical agricultural robotics demands consistent, comprehensive test analysis from ALL development assistants (human or AI). Standardized test reporting enables quality validation, safety assurance, educational value, decision support, and cross-session continuity—essential for maintaining enterprise-grade reliability in multi-tractor coordination systems.

## MANDATORY: Format-First Generation Standards

**ABSOLUTE REQUIREMENT**: ALL generated content must emerge in final quality-controlled form.

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

### MANDATORY: CHANGELOG.md Maintenance

**ABSOLUTE REQUIREMENT**: CHANGELOG.md must be regenerated, formatted, and included in every git commit.

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

### MANDATORY: Web Documentation Synchronization

**ABSOLUTE REQUIREMENT**: When README.md changes, docs/index.html must be regenerated and included in the same commit.

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

The platform includes authoritative ISO 11783 technical specifications that MUST be referenced for all ISOBUS-related work:

- **[docs/iso11783-11-online_data_base.pdf](docs/iso11783-11-online_data_base.pdf)**: Complete ISO 11783-11 specifications
- **[docs/isoExport_csv.zip](docs/isoExport_csv.zip)**: Machine-readable protocol definitions
- **[docs/isobus-osi-model-layer-iso-11783.svg](docs/isobus-osi-model-layer-iso-11783.svg)**: OSI model architecture diagram

**Mandatory Reference Requirements**:
- ALL ISOBUS implementation decisions must cite specific sections from authoritative documentation
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

**MANDATORY: Git Commit Separation of Concerns**:
- **CRITICAL REQUIREMENT**: All commits must follow strict separation of concerns methodology
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

**POLICY**: ALL future development on AFS FastAPI MUST follow Test-Driven Development methodology:

1. **RED Phase**: Write failing test describing agricultural robotics behavior
2. **GREEN Phase**: Implement minimal code meeting performance and safety requirements
3. **REFACTOR Phase**: Enhance code quality while maintaining enterprise standards

**ENFORCEMENT**: Automated pre-commit hooks validate TDD compliance before any code changes are accepted.

**Reference Documentation**:
- TDD_WORKFLOW.md: Complete Test-First development guide with agricultural domain examples
- TDD_FRAMEWORK_MANDATORY.md: Comprehensive mandatory TDD framework and enforcement policies

## Session Initialization Architecture

**Complete Execution Order**: [docs/EXECUTION_ORDER.md](docs/EXECUTION_ORDER.md)

The platform uses a sophisticated 6-phase session initialization architecture with 28+ files working together to establish conceptual, contextual, and functional session state for ALL AI agents.

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

The project includes a **.claude/commands/** directory containing reusable command triggers for consistent documentation and workflow execution:

**Available Commands**:
- **loadsession**: Loads and applies SESSION_SUMMARY.md for complete project context restoration
  - **CRITICAL**: Must be executed immediately after `/new` completes for all AFS FastAPI sessions
  - Restores v0.1.3 platform state, enterprise foundation, and strategic development priorities
  - Ensures continuity of Test-First Development methodology and synchronization infrastructure focus
  - Maintains dual-purpose educational and functional mission across sessions
  - **Architecture**: See [docs/EXECUTION_ORDER.md](docs/EXECUTION_ORDER.md) for complete execution flow
- **savesession**: Saves complete session state (conceptual, contextual, functional) with mandatory compaction
  - **CRITICAL**: Session state MUST be compacted into SESSION_SUMMARY.md before applying new changes
  - Creates dated snapshot: `docs/monitoring/SESSION_STATE_YYYY_MM_DD.md`
  - Captures: Platform metrics, git status, mandatory requirements, enforcement mechanisms
  - **Universal Access**: ALL humans and AI agents (Claude, GPT, Gemini, Copilot, CodeWhisperer)
  - **Compaction Protocol**: Prevents knowledge fragmentation, ensures SESSION_SUMMARY.md remains authoritative
  - **Cross-Session Memory**: Command MUST be remembered by all agents across all sessions
  - **Complete Specification**: See [.claude/commands/savesession.md](.claude/commands/savesession.md)
- **runtests**: Executes comprehensive test suite with standardized reporting format
  - **MANDATORY**: ALL AI agents must provide standardized test analysis (Executive Summary, Insight Block, Test Distribution, Platform Health Indicators, Agricultural Context, Advisory Notes)
  - Colored output with platform health assessment and reporting reminders
  - Command variations: `./bin/runtests`, `./bin/runtests --coverage`, `./bin/runtests -q`, `./bin/runtests tests/unit/equipment/`
  - **Universal Access**: ALL humans and AI agents (Claude, GPT, Gemini, Copilot, CodeWhisperer)
  - **Cross-Session Memory**: Command MUST be remembered by all agents across all sessions
  - **Complete Specification**: See [.claude/commands/runtests.md](.claude/commands/runtests.md)
- **whereweare**: Display or generate comprehensive WHERE_WE_ARE.md strategic assessment
  - **Display Mode**: `./bin/whereweare` shows existing 480+ line strategic documentation
  - **Generation Mode**: `./bin/whereweare --generate` synthesizes from current platform state
  - Extracts live metrics (git tags, test counts, README.md, SESSION_SUMMARY.md)
  - Essential for ISO compliance planning and stakeholder communication
  - **Command variations**: `./bin/whereweare`, `./bin/whereweare --generate`, `/whereweare` (Claude Code)
  - **Universal Access**: ALL humans and AI agents (Claude, GPT, Gemini, Copilot, CodeWhisperer)
  - **Cross-Session Memory**: Command MUST be remembered by all agents across all sessions
  - **Complete Specification**: See [.claude/commands/whereweare.md](.claude/commands/whereweare.md)

**Command Usage**:
- Commands are documented with complete specifications including purpose, expected output, and usage context
- Professional standards maintained across all command triggers
- Version-controlled for team collaboration and consistency
- Educational integration preserves dual-purpose functional and instructional mission

**Integration Benefits**:
- **Consistent Documentation**: Repeatable processes for strategic assessment generation
- **Quality Assurance**: Standardized documentation structure and professional formatting
- **Team Enablement**: Clear specifications for collaborative documentation creation
- **Workflow Enhancement**: Structured approach to maintaining current project documentation

---

**Purpose**: This ensures knowledge transfer alongside deliverable code, making the codebase both functional and instructional for professional agricultural technology development.
