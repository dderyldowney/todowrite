# ChatGPT Configuration for AFS FastAPI

This file contains project-specific instructions for ChatGPT sessions working on the **AFS FastAPI robotic agriculture platform** via the `chatgpt4-cli` pip package.

## AI Agent Integration

**CHATGPT.md** serves as the **authoritative instruction file** for ChatGPT interactions with this codebase. This complements the Claude Code configuration (`.claude/CLAUDE.md`) to provide consistent AI assistance across different platforms.

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

- **Modern Python Patterns**
  - Type hints, dataclasses, ABC inheritance
  - Python 3.12+ features (union types, pattern matching)

- **Agricultural Technology Standards**
  - ISOBUS communication protocols (ISO 11783)
  - Safety compliance systems (ISO 18497)
  - Professional agricultural equipment interfaces

- **Distributed Systems Concepts**
  - Conflict-Free Replicated Data Types (CRDTs)
  - Vector clocks for operation ordering
  - Multi-tractor fleet coordination and synchronization

- **Enterprise Development Practices**
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

**Important**: Always reference WORKFLOW.md when working with tests, understanding test patterns, or explaining the testing strategy. This document captures the sophisticated testing approach used in this enterprise-grade agricultural robotics platform.

## Development Workflow

- **Branch Strategy**: Work on `develop` branch for new features
- **Version Control**: Use semantic versioning and proper Git workflow
- **Documentation**: Document technical decisions and architectural changes
- **Testing**: Maintain comprehensive test coverage (see WORKFLOW.md for complete reference)
- **Code Review**: All changes reviewed for educational value and professional standards

## ChatGPT-Specific Guidelines

### Session Context Awareness
- Always check SESSION_SUMMARY.md for project evolution and current state
- Reference existing documentation files for consistency
- Maintain awareness of enterprise-grade standards and agricultural domain expertise

### Command-Line Integration
- When working via `chatgpt4-cli`, maintain consistency with project standards
- Follow the same educational framework as defined for other AI agents
- Ensure all code suggestions align with the dual-purpose educational mission

### Agricultural Domain Expertise
- Prioritize industry-standard agricultural robotics patterns
- Explain ISOBUS and safety compliance concepts when relevant
- Connect code implementations to real-world farming automation scenarios

### Code Generation Standards
- Generate production-ready code that meets enterprise standards
- Include comprehensive type hints and documentation
- Follow existing architectural patterns established in the codebase
- Maintain zero-warning code quality standards

## Multi-Agent Coordination

This configuration works alongside:
- **Claude Code** (`.claude/CLAUDE.md`): Primary development and educational framework
- **Other AI Tools**: Consistent standards across all AI interactions

### Consistency Requirements
- Maintain the same educational explanations approach
- Follow identical code quality standards
- Reference the same authoritative documents (WORKFLOW.md, SESSION_SUMMARY.md)
- Preserve the dual-purpose functional/educational mission

## Key References

- **WORKFLOW.md**: Complete testing architecture documentation
- **SESSION_SUMMARY.md**: Project evolution and current session context
- **README.md**: Project overview and build instructions
- **docs/index.html**: Comprehensive API documentation

---

**Purpose**: This ensures consistent, high-quality AI assistance for the AFS FastAPI agricultural robotics platform across different AI agents and interfaces, maintaining the educational framework while delivering enterprise-grade agricultural technology solutions.

**Agent Integration**: ChatGPT via `chatgpt4-cli` package provides complementary AI assistance alongside Claude Code, ensuring consistent project standards and educational value across all AI interactions.
