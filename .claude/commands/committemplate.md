# Commit Message Template Command

## Command Name
committemplate

## Purpose
Provides proper commit message templates following mandatory separation of concerns methodology for the AFS FastAPI agricultural robotics platform.

## Description
This command generates commit message templates that comply with our automated validation hooks, ensuring single-concern commits with appropriate agricultural context.

## Template Format
```
type(scope): Description with agricultural context

Detailed explanation of changes focusing on:
- What was changed and why (single concern only)
- Technical implementation details
- Agricultural robotics context when applicable

Valid types: feat, fix, refactor, docs, test, config, perf, security
Required scope: equipment, coordination, api, monitoring, safety, etc.
Agricultural context: Required for feat, fix, refactor, perf, security types

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Template Examples

### Feature Implementation
```
feat(equipment): Add multi-tractor synchronization for field coordination

This commit implements distributed coordination allowing multiple tractors
to synchronize their operations during agricultural field cultivation.

Implementation Details:
- Vector clock synchronization for precise timing
- ISOBUS message protocol for equipment communication
- Safety override mechanisms for collision avoidance
- Performance optimization for embedded agricultural systems

Rationale:
Multi-tractor coordination essential for efficient large-scale farming
operations while maintaining safety standards for autonomous equipment.
```

### Bug Fix
```
fix(safety): Resolve emergency stop timing for tractor coordination

This commit corrects race condition in emergency stop propagation that
could delay safety responses during multi-tractor field operations.

Technical Changes:
- Reduced emergency stop latency from 150ms to 50ms
- Enhanced signal propagation across tractor fleet
- Added redundant safety validation for critical operations
- Improved ISO 18497 compliance for agricultural equipment safety

Rationale:
Emergency stop delays in agricultural equipment can cause equipment
damage or safety incidents requiring immediate response capability.
```

### Documentation
```
docs(workflow): Add tractor maintenance documentation for field operations

This commit establishes comprehensive maintenance procedures for
agricultural equipment used in multi-tractor coordination systems.

Documentation Updates:
- Daily equipment inspection procedures
- Preventive maintenance schedules aligned with farming seasons
- Safety checklist for autonomous field operations
- Troubleshooting guide for common agricultural equipment issues

Rationale:
Proper equipment maintenance essential for reliable agricultural
operations and compliance with ISO safety standards.
```

### Configuration
```
config(hooks): Enhance TDD enforcement for agricultural safety validation

This commit strengthens automated validation ensuring all agricultural
equipment code follows Test-First Development methodology.

Configuration Changes:
- Enhanced pre-commit hook validation
- Added agricultural context requirements
- Strengthened safety compliance checking
- Improved error messages for development guidance

Rationale:
Safety-critical agricultural systems require comprehensive testing
validation to prevent equipment failures during field operations.
```

## Validation Guidelines
All commit messages must pass these checks:
- **Format**: `type(scope): description` (max 72 characters for description)
- **Scope**: Must be from approved agricultural robotics scope list
- **Agricultural Context**: Required for safety-critical commit types
- **Single Concern**: Cannot address multiple concern types
- **Professional Standards**: Proper capitalization and grammar

## Common Validation Failures and Solutions

### Invalid Scope Error
```
❌ Invalid scope 'enforcement'. Must be one of: equipment, coordination, api...
✅ Solution: Use valid scope like 'hooks', 'workflow', or 'safety'
```

### Missing Agricultural Context
```
❌ Commit type 'feat' requires agricultural context in description
✅ Solution: Include terms like 'tractor', 'field', 'equipment', 'agricultural'
```

### Multiple Concerns Detected
```
❌ Commit description mentions other concern types: config
✅ Solution: Split into separate commits for each concern type
```

### Description Too Long
```
❌ Commit description too long (75 chars, max 72)
✅ Solution: Shorten subject line, use body for detailed explanation
```

## Agricultural Context Keywords
Include these terms for agricultural context validation:
- tractor, field, equipment, agricultural, farming
- coordination, fleet, safety, emergency, collision
- isobus, iso 11783, iso 18497, monitoring, sensor
- planting, harvesting, cultivation, precision, autonomous

## Integration with Workflow
- Use before creating any git commit
- Reference during commit separation violations
- Apply during error recovery from hook failures
- Essential for maintaining commit quality standards

## Related Commands
- `formatall`: Ensure code quality before committing
- `fixmodules`: Resolve import issues before validation
- Pre-commit hooks: Automated commit message validation

---

**Status**: Essential template for commit separation compliance
**Validation**: Required by automated commit separation hooks
**Context**: Mandatory agricultural context for safety-critical commits