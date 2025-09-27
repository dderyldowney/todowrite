# Claude Code Configuration for AFS FastAPI

This file contains project-specific instructions for Claude Code sessions working on the AFS FastAPI robotic agriculture platform.

## Code Documentation Requirements

**Educational Code Explanations**: All code generated must be explained both overall and individually. Explanations should be concise with the dual purpose of teaching while building this real-world professional project.

### Explanation Structure
- **Architecture Level**: Explain design patterns, system integration, and why specific approaches were chosen
- **Implementation Level**: Detail how individual components work, function purposes, and technical specifics
- **Professional Context**: Cover industry best practices, domain-specific concepts (ISOBUS, ISO 18497 safety, agricultural robotics), and enterprise development standards

### Educational Focus Areas
- Modern Python patterns (type hints, dataclasses, ABC inheritance)
- Agricultural technology standards (ISOBUS communication, safety compliance)
- Distributed systems concepts (CRDTs, vector clocks, fleet coordination)
- API design and serialization best practices
- Enterprise testing strategies and code quality

## Project Context

AFS FastAPI is an enterprise-grade robotic agriculture platform implementing:
- Multi-tractor fleet coordination and synchronization
- Professional agricultural interface compliance (ISO 11783, ISO 18497)
- Enhanced robotic interfaces (6 major categories: ISOBUS, Safety, Motor Control, Data Management, Power Management, Vision/Sensors)
- Modern Python development practices with comprehensive testing

## Code Quality Standards

- All formatting tools aligned: Black, ruff, isort with consistent configuration
- Comprehensive testing: unit, integration, and feature tests
- Zero linting warnings maintained
- Modern Python syntax (3.12+, union types, proper type annotations)

## Development Workflow

- Work on `develop` branch for new features
- Use semantic versioning and proper Git workflow
- Document technical decisions and architectural changes
- Maintain comprehensive test coverage for all new functionality

This ensures knowledge transfer alongside deliverable code, making the codebase both functional and instructional for professional agricultural technology development.
