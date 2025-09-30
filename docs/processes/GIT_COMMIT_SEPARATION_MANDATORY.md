# Git Commit Separation of Concerns - MANDATORY Policy

> **Navigation**: [📚 DOCS Index](../README.md) | [🏠 Project Root](../../) | [🔄 Development Processes](../processes/) | [📋 Strategic](../strategic/) | [🔧 Implementation](../implementation/)
>
> **Reading Order**: **Current Document** → [Git Commit Documentation](GIT_COMMIT_DOCUMENTATION.md) → [Bin Directory Reorganization](BIN_DIRECTORY_REORGANIZATION.md) → [Changelog Generation](CHANGELOG_GENERATION.md)

---

## Overview

**MANDATORY REQUIREMENT**: All git commits in the AFS FastAPI agricultural robotics platform must follow strict separation of concerns methodology. Each commit must address exactly one logical concern, enabling precise change tracking, efficient code reviews, and reliable rollback capabilities essential for safety-critical agricultural systems.

**UNIVERSAL APPLICATION**: This requirement applies to ALL contributors—human developers AND all AI agents (Claude Code, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer, and any future AI development assistant).

**INVESTIGATION PATTERN**: All commit messages explaining complex changes SHOULD reference structured investigation pattern when applicable (see [INVESTIGATION_PATTERN_MANDATORY.md](../../.claude/INVESTIGATION_PATTERN_MANDATORY.md)).

## Separation Categories

### 1. Feature Implementation (`feat`)
**Purpose**: New functionality or capability additions
**Scope**: Single feature implementation with complete functionality
**Examples**:
- `feat(equipment): add multi-tractor synchronization capability`
- `feat(api): implement field allocation endpoint with ISOBUS integration`
- `feat(monitoring): add soil composition sensor interface`

**Requirements**:
- Must include corresponding test updates
- Documentation updates included only if directly related
- Configuration changes only if feature-specific

### 2. Bug Fixes (`fix`)
**Purpose**: Correcting defects or unexpected behavior
**Scope**: Single bug resolution with minimal scope
**Examples**:
- `fix(coordination): resolve vector clock synchronization race condition`
- `fix(api): correct equipment status validation logic`
- `fix(safety): ensure emergency stop triggers across all tractors`

**Requirements**:
- Must include test that reproduces the bug
- Fix must be minimal and targeted
- No unrelated changes or improvements

### 3. Refactoring (`refactor`)
**Purpose**: Code structure improvements without behavior changes
**Scope**: Single architectural or structural improvement
**Examples**:
- `refactor(equipment): extract tractor interface into abstract base class`
- `refactor(services): consolidate ISOBUS message handling logic`
- `refactor(monitoring): simplify sensor data aggregation pipeline`

**Requirements**:
- No functional behavior changes
- All tests must continue passing unchanged
- Performance improvements documented if applicable

### 4. Documentation (`docs`)
**Purpose**: Documentation-only changes
**Scope**: Single documentation concern or update
**Examples**:
- `docs(api): update equipment endpoint examples for agricultural context`
- `docs(safety): add ISO 18497 compliance documentation`
- `docs(workflow): enhance TDD methodology examples`

**Requirements**:
- No code changes whatsoever
- Documentation must be complete and self-contained
- Professional tone and accuracy maintained

### 5. Testing (`test`)
**Purpose**: Test-only additions or improvements
**Scope**: Single testing concern enhancement
**Examples**:
- `test(equipment): add comprehensive tractor coordination scenarios`
- `test(integration): enhance multi-field operation validation`
- `test(performance): add sub-millisecond coordination timing tests`

**Requirements**:
- No production code changes
- Tests must follow TDD methodology if related to new features
- Agricultural context maintained in all test scenarios

### 6. Configuration (`config`)
**Purpose**: Configuration, build, or tooling changes
**Scope**: Single configuration aspect modification
**Examples**:
- `config(hooks): enhance TDD enforcement with commit validation`
- `config(ci): add agricultural safety standards validation pipeline`
- `config(deps): update FastAPI to support enhanced ISOBUS features`

**Requirements**:
- No functional code changes
- Configuration must be complete and tested
- Impact on development workflow documented

### 7. Performance (`perf`)
**Purpose**: Performance improvements without functional changes
**Scope**: Single performance optimization
**Examples**:
- `perf(coordination): optimize vector clock operations for embedded systems`
- `perf(api): reduce ISOBUS message serialization overhead`
- `perf(monitoring): improve sensor data processing throughput`

**Requirements**:
- Measurable performance improvement documented
- No functional behavior changes
- Agricultural equipment constraints considered

### 8. Security (`security`)
**Purpose**: Security-related improvements or fixes
**Scope**: Single security concern addressed
**Examples**:
- `security(api): add equipment authentication validation`
- `security(communication): enhance ISOBUS message encryption`
- `security(access): implement role-based tractor operation permissions`

**Requirements**:
- Security improvement must be complete
- No functional regressions
- Agricultural safety standards maintained

## Commit Message Format

### Standard Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Agricultural Robotics Examples
```
feat(equipment): implement automated field boundary detection
- Add LiDAR integration for precise boundary mapping
- Include safety override for manual operator intervention
- Support ISO 11783 position reporting standards

fix(coordination): resolve tractor collision avoidance timing
- Correct vector clock synchronization in emergency scenarios
- Ensure sub-100ms response time for collision detection
- Maintain ISO 18497 PLd safety integrity level

refactor(api): consolidate equipment status endpoints
- Extract common validation logic into shared utilities
- Improve ISOBUS message handling consistency
- Reduce endpoint complexity while maintaining functionality

docs(safety): add comprehensive emergency stop procedures
- Document ISO 18497 compliance requirements
- Include multi-tractor coordination emergency protocols
- Provide troubleshooting guide for safety system failures

test(integration): enhance multi-field operation validation
- Add realistic agricultural workflow scenarios
- Test equipment handoff between field boundaries
- Validate performance under various weather conditions

config(hooks): add commit separation enforcement
- Implement pre-commit validation for concern separation
- Ensure agricultural context in all commit messages
- Maintain professional development standards
```

## Enforcement Mechanisms

### Pre-commit Hook Validation
- Commit messages must follow prescribed format
- Each commit must address single concern category
- Agricultural context required in all commit messages
- Professional tone and technical accuracy enforced

### Cross-Session Persistence
- Requirements embedded in CLAUDE.md project configuration
- AGENTS.md documentation includes mandatory separation policy
- SESSION_SUMMARY.md preserves separation of concerns methodology
- Pre-commit hooks prevent non-compliant commits

### Quality Assurance
- Automated validation of commit message format
- Scope validation ensures single concern per commit
- Agricultural context verification in commit descriptions
- Integration with existing TDD enforcement framework

## Benefits for Agricultural Robotics

### Safety Critical Systems
- **Precise Change Tracking**: Essential for identifying root causes in safety incidents
- **Regulatory Compliance**: Supports ISO 18497 and ISO 11783 audit requirements
- **Rollback Capability**: Enables surgical fixes without affecting unrelated functionality

### Distributed Development
- **Code Review Efficiency**: Reviewers can focus on single concerns
- **Merge Conflict Reduction**: Smaller, focused commits reduce integration complexity
- **Knowledge Transfer**: Clear commit history serves as development documentation

### Quality Assurance
- **Automated Testing**: Enables targeted test execution based on change type
- **Continuous Integration**: Supports sophisticated CI/CD pipelines
- **Technical Debt Management**: Clear separation enables systematic refactoring

## Implementation Requirements

### For ALL AI Code Generation (Universal Agent Compliance)

**MANDATORY**: All AI development assistants generating commits for this platform MUST follow separation of concerns:

- **Claude Code** (Anthropic): Must separate feat/fix/refactor/docs/test/config commits
- **GitHub Copilot** (Microsoft/OpenAI): Must generate single-concern commit messages
- **ChatGPT Code Interpreter** (OpenAI): Must follow conventional commit format with separation
- **Gemini Code Assist** (Google): Must validate single logical concern per commit
- **Amazon CodeWhisperer** (AWS): Must adhere to commit separation methodology
- **Any Future AI Agent**: Must comply with mandatory separation of concerns framework

**AI-Specific Requirements**:
- **RED-GREEN-REFACTOR**: TDD commits must be properly separated by phase
- **Agricultural Context**: All commit messages must include domain-specific context
- **Professional Standards**: Commit quality reflects enterprise development practices
- **Investigation Pattern**: Complex changes should reference structured investigation when debugging or analyzing

**Rationale for Universal AI Compliance**: Safety-critical agricultural robotics requires traceable change management—commit separation enables precise rollback, targeted testing, and ISO compliance auditing regardless of code generation method.

### For Human Developers
- **Training Required**: All team members must understand separation methodology
- **Review Standards**: Code reviews must enforce separation requirements
- **Documentation**: Commit messages serve as living project documentation
- **Compliance**: Pre-commit hooks ensure consistent application
- **AI Oversight**: Developers using AI assistants must verify commit separation compliance

## Cross-Session Persistence

### Configuration Integration
- **CLAUDE.md**: Updated with mandatory commit separation requirements
- **AGENTS.md**: Enhanced with separation of concerns methodology
- **SESSION_SUMMARY.md**: Documents separation policy implementation
- **Pre-commit hooks**: Automated enforcement of separation standards

### Continuous Enforcement
- **New Sessions**: loadsession script reminds of separation requirements
- **Visual Warnings**: Critical separation enforcement displayed prominently
- **Automated Validation**: Pre-commit hooks prevent non-compliant commits
- **Documentation References**: Complete methodology guidance maintained

---

**Status**: MANDATORY and ENFORCED
**Effective**: Immediately for all AFS FastAPI development
**Scope**: All commits, all contributors, all development sessions
**Authority**: Agricultural robotics safety and quality requirements

This separation of concerns methodology ensures that the AFS FastAPI platform maintains the highest standards of code organization and change management, supporting the safety-critical nature of agricultural robotics development while enabling efficient collaboration and maintenance.