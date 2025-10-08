# Update CHANGELOG.md Command

## Command Name
updatechangelog

## Purpose
Regenerates and formats CHANGELOG.md to include all changes up to and including the current commit, ensuring comprehensive version history for the AFS FastAPI agricultural robotics platform.

## Description
This command maintains complete change tracking essential for safety-critical agricultural robotics development where regulatory compliance (ISO 18497, ISO 11783), debugging, and safety audits require detailed version history.

## Implementation Process

### 1. Pre-Commit CHANGELOG Update
```bash
# Extract recent commits since last changelog update
git log --pretty=format:"%h|%s|%an|%ad" --date=short --reverse --since="last changelog update"

# Categorize commits by type (feat, fix, docs, config, etc.)
# feat -> Added section
# fix -> Fixed section
# refactor, perf -> Changed section
# docs -> Documentation section
# config -> Configuration section
# security -> Security section

# Update [Unreleased] section with new entries
# Include agricultural context for safety-critical changes
# Apply Keep a Changelog formatting standards
```

### 2. Formatting Standards Applied
```markdown
## [Unreleased]

### Added
- New agricultural robotics features with safety context
- Multi-tractor coordination capabilities
- Test coverage for field operations

### Changed
- Enhanced tractor coordination algorithms
- Performance improvements for embedded systems
- Updated documentation for equipment interfaces

### Fixed
- Resolved safety-critical issues in equipment coordination
- Corrected timing issues in multi-tractor synchronization
- Fixed agricultural sensor integration problems

### Security
- Enhanced authentication for agricultural equipment
- Improved ISOBUS communication protocols
- Strengthened safety validation systems
```

### 3. Agricultural Context Requirements
For safety-critical commits, include:
- **Equipment impact**: How changes affect tractor operations
- **Safety compliance**: ISO 18497 and ISO 11783 considerations
- **Multi-tractor coordination**: Impact on fleet synchronization
- **Field operations**: Effects on agricultural productivity

## When to Use

### MANDATORY Before Every Commit
1. **Before staging files**: Update CHANGELOG.md first
2. **After code changes**: Include all recent modifications
3. **Before git commit**: Ensure changelog reflects current state
4. **Cross-session persistence**: Maintain complete version history

### Integration with Git Workflow
```bash
# Standard workflow with changelog update:
1. Make code changes
2. Run updatechangelog command
3. Review updated CHANGELOG.md
4. Add CHANGELOG.md to git: git add CHANGELOG.md
5. Commit with updated changelog: git commit -m "type(scope): description"
```

## Expected Output Structure

### Keep a Changelog Format
- **[Unreleased]** section for current changes
- **Semantic versioning** for release organization
- **Change categories**: Added, Changed, Fixed, Security, etc.
- **Agricultural context** in safety-critical entries
- **Professional tone** matching project standards

### Agricultural Context Examples
```markdown
### Added
- Multi-tractor synchronization capability for coordinated field cultivation
- Safety override systems compliant with ISO 18497 agricultural standards
- ISOBUS communication interface for John Deere and Case IH equipment

### Fixed
- Resolved emergency stop propagation delays affecting fleet safety
- Corrected GPS coordinate drift during autonomous field operations
- Fixed sensor data corruption in dusty agricultural environments
```

## Cross-Session Enforcement

### CLAUDE.md Integration
- CHANGELOG.md update mandatory before commits
- Format-first application to changelog entries
- Agricultural context requirements embedded
- Cross-session persistence through configuration

### Pre-Commit Hook Integration
```yaml
# Future enhancement: Pre-commit hook validation
- id: changelog-updated
  name: CHANGELOG.md Updated
  entry: python .claude/hooks/changelog_validation.py
  language: system
  pass_filenames: false
  always_run: true
```

## Quality Standards

### Format Compliance
- **Keep a Changelog** standard formatting
- **Semantic Versioning** for release organization
- **Professional tone** matching documentation standards
- **Agricultural context** for safety-critical changes

### Content Requirements
- **Complete change tracking** from git commit history
- **Proper categorization** by change type and impact
- **Safety compliance notes** for equipment-related changes
- **Performance metrics** for optimization changes

### Validation Criteria
- **Chronological accuracy** matching git timeline
- **Change completeness** ensuring no commits missing
- **Format consistency** across all entries
- **Agricultural relevance** maintained throughout

## Error Prevention

### Common Issues Addressed
- **Missing changelog updates**: Automated detection of uncommitted changes
- **Format inconsistencies**: Standardized Keep a Changelog structure
- **Agricultural context omission**: Required for safety-critical commits
- **Version mismatch**: Ensure changelog reflects actual commit state

### Quality Assurance Integration
- **Pre-commit validation**: Ensure changelog updated before commits
- **Format checking**: Verify Keep a Changelog compliance
- **Content validation**: Confirm agricultural context included
- **Cross-reference commits**: Match changelog to git history

## Implementation Benefits

### Regulatory Compliance
- **Complete audit trail** for agricultural equipment certification
- **Change traceability** supporting ISO compliance reviews
- **Version history** enabling regulatory validation
- **Safety documentation** for equipment approval processes

### Development Efficiency
- **Change awareness** across development teams
- **Impact assessment** for multi-tractor coordination
- **Debugging support** through detailed change history
- **Release planning** with comprehensive change overview

### Safety Assurance
- **Critical change tracking** for agricultural equipment safety
- **Emergency debugging** through precise change identification
- **Compliance verification** for regulatory requirements
- **Quality maintenance** through systematic documentation

## Related Commands
- `formatall`: Ensure changelog formatting meets quality standards
- `committemplate`: Proper commit messages supporting changelog generation
- `fixmodules`: Resolve import issues before changelog updates

---

**Status**: Essential for regulatory compliance and change tracking
**Frequency**: MANDATORY before every git commit
**Integration**: Required component of agricultural robotics development workflow
**Purpose**: Complete version history for safety-critical agricultural systems

This command ensures that CHANGELOG.md provides the comprehensive change tracking essential for agricultural robotics development where regulatory compliance, debugging, and safety audits depend on detailed version history.