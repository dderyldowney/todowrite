# iso11783ref Command

## Purpose

Provides quick access to authoritative ISO 11783 ISOBUS technical specification documentation. This command ensures ALL AI agents (Claude, GPT, Gemini, Copilot, CodeWhisperer) reference official specifications when working with ISOBUS-related features, implementation, or analysis.

## Command Sequence

```
# View all ISO 11783 reference materials
ls -lh docs/iso*.{pdf,zip,svg}

# Extract ISO 11783 reference paths for documentation
echo "ISO 11783 Reference Materials:"
echo "- PDF: docs/iso11783-11-online_data_base.pdf"
echo "- CSV: docs/isoExport_csv.zip"
echo "- SVG: docs/isobus-osi-model-layer-iso-11783.svg"
```

## Expected Output

The command will display:

1. **File Listing**: Size and location of all ISO 11783 reference materials
2. **Reference Paths**: Clickable file paths for quick access
3. **Material Types**: PDF specifications, CSV data export, SVG architecture diagram

Example output:
```
-rw-r--r-- 1 user staff 2.1M Sep 30 20:15 docs/iso11783-11-online_data_base.pdf
-rw-r--r-- 1 user staff 450K Sep 30 20:15 docs/isoExport_csv.zip
-rw-r--r-- 1 user staff  85K Sep 30 20:15 docs/isobus-osi-model-layer-iso-11783.svg

ISO 11783 Reference Materials:
- PDF: docs/iso11783-11-online_data_base.pdf
- CSV: docs/isoExport_csv.zip
- SVG: docs/isobus-osi-model-layer-iso-11783.svg
```

## Usage Context

### When to Execute

- **Before ISOBUS Implementation**: Reference specifications before coding ISOBUS features
- **During Technical Analysis**: Verify compliance with official ISO 11783 standards
- **Educational Explanations**: Cite authoritative sources in ISOBUS discussions
- **Compliance Validation**: Check implementation against official specifications

### Prerequisites

- ISO 11783 reference materials must exist in docs/ directory
- Files committed to version control (commit: 944995f)

## Reference Material Descriptions

### ISO 11783-11 Online Database (PDF)
- **File**: [docs/iso11783-11-online_data_base.pdf](docs/iso11783-11-online_data_base.pdf)
- **Content**: Complete ISO 11783-11 technical specifications
- **Use Cases**:
  - Protocol implementation requirements
  - Message structure definitions
  - Compliance requirements
  - Tractor-implement communication standards

### ISOBUS Data Export (CSV)
- **File**: [docs/isoExport_csv.zip](docs/isoExport_csv.zip)
- **Content**: Machine-readable ISO 11783 database export
- **Use Cases**:
  - Automated validation tools
  - Code generation from specifications
  - Message ID lookups
  - Parameter group definitions

### ISOBUS OSI Model (SVG)
- **File**: [docs/isobus-osi-model-layer-iso-11783.svg](docs/isobus-osi-model-layer-iso-11783.svg)
- **Content**: Seven-layer communication stack visualization
- **Use Cases**:
  - Architecture understanding
  - Protocol layer relationships
  - Educational documentation
  - System design reference

## Mandatory Usage Policy

**ALL AI agents MUST**:
- Reference these materials when discussing ISOBUS implementation
- Cite specific sections for implementation decisions
- Verify compliance against official specifications
- Include references in educational explanations
- Align code generation with specification requirements

## Integration with Development Workflow

### ISOBUS Development Sequence

1. Execute `iso11783ref` command to review available materials
2. Reference appropriate specification documents
3. Implement features aligned with ISO 11783 standards
4. Validate against official specifications
5. Document compliance in commit messages

### Quality Assurance

- Ensures authoritative reference usage across all AI agents
- Maintains ISO 11783 compliance consistency
- Supports educational framework with official specifications
- Enables verifiable compliance validation

## Cross-Session Persistence

**Universal Agent Access**: This command and its reference materials MUST be:
- **Remembered** by ALL AI agents (Claude, GPT, Gemini, Copilot, CodeWhisperer)
- **Referenced** in every ISOBUS-related discussion or implementation
- **Accessible** across all development sessions
- **Enforced** through SESSION_SUMMARY.md and CLAUDE.md policies

## Command Rationale

**Standards Compliance**: Agricultural robotics demands precise compliance with international standards. ISO 11783 specifications ensure interoperability between tractors and implements from different manufacturers. By making authoritative reference materials easily accessible and mandating their use, we ensure professional-grade ISOBUS implementation that meets industry requirements.

## Version Control

This command specification is version-controlled as part of the .claude/commands/ framework, ensuring consistent team-wide access to ISO 11783 reference materials and maintaining professional agricultural equipment standards.

---

**Command Type**: Technical Reference Access
**Priority**: Mandatory for all ISOBUS work
**Dependencies**: ISO 11783 reference materials in docs/ directory
**Output**: Quick access to authoritative ISOBUS specifications
