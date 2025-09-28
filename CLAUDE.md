# Claude Code Configuration for AFS FastAPI

This file contains project-specific instructions for Claude Code sessions working on the **AFS FastAPI robotic agriculture platform**.

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

- **118 tests** across 3-layer architecture (Feature, Unit, Root-level tests)
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

### Test-First Methodology for Synchronization Infrastructure

**Strategic Priority**: All distributed systems components (vector clocks, CRDTs, ISOBUS message queuing) must follow Test-Driven Development:

1. **RED Phase**: Write failing test describing agricultural robotics behavior
2. **GREEN Phase**: Implement minimal code meeting performance and safety requirements
3. **REFACTOR Phase**: Enhance code quality while maintaining enterprise standards

**Reference Documentation**: TDD_WORKFLOW.md provides complete Test-First development guide with agricultural domain examples.

## Claude Command Integration

### Command Trigger Framework

The project includes a **.claude/commands/** directory containing reusable command triggers for consistent documentation and workflow execution:

**Available Commands**:
- **loadsession**: Loads and applies SESSION_SUMMARY.md for complete project context restoration
  - **CRITICAL**: Must be executed immediately after `/new` completes for all AFS FastAPI sessions
  - Restores v0.1.3 platform state, enterprise foundation, and strategic development priorities
  - Ensures continuity of Test-First Development methodology and synchronization infrastructure focus
  - Maintains dual-purpose educational and functional mission across sessions
- **whereweare**: Generates comprehensive WHERE_WE_ARE.md project state assessment
  - Creates 475-line strategic documentation from overarching vision to implementation details
  - Captures live metrics (tests, code quality, release status)
  - Provides enterprise-grade stakeholder communication documentation

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
