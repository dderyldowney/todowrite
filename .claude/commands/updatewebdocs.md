# updatewebdocs Command Specification

## Purpose

The `updatewebdocs` command automatically converts README.md to docs/index.html with proper formatting and git integration, ensuring web documentation stays synchronized with markdown source.

## Command Location

```
bin/updatewebdocs
```

## Usage

```bash
# Convert README.md to docs/index.html
./bin/updatewebdocs

# Show help information
./bin/updatewebdocs --help

# Test mode (for unit testing)
./bin/updatewebdocs --test-mode --root=/path/to/test
```

## Behavior

### Primary Function
1. **Validates README.md exists** in project root
2. **Converts markdown to HTML** using docs/convert_readme_to_index_html.py
3. **Creates docs/ directory** if it doesn't exist
4. **Generates docs/index.html** with professional styling
5. **Adds to git staging** automatically (if git repo detected)

### HTML Generation
- Uses CommonMark-compliant markdown parser with GFM extensions
- Preserves code blocks with syntax highlighting support
- Handles tables, footnotes, task lists, and strikethrough
- Applies professional agricultural robotics styling
- Maintains technical terminology (ISOBUS, ISO 11783, ISO 18497, etc.)

### Git Integration
- Automatically stages docs/index.html after generation
- Only runs in non-test mode
- Provides next-step guidance for committing changes

## Expected Output

```
📝 AFS FastAPI Web Documentation Generator
===========================================

🔄 Converting README.md to HTML...
✅ HTML generated successfully
   Output: docs/index.html

📋 Adding to git staging area...
✅ index.html added to git staging

💡 Next steps:
   1. Review generated HTML: docs/index.html
   2. Commit changes with README.md:
      git commit -m "docs(docs): Update documentation"

📋 Web Documentation Update Complete!
```

## Error Handling

### Missing README.md
```
❌ ERROR: README.md not found
   Expected location: README.md
```
Exit code: 1

### Missing Converter Script
```
❌ ERROR: Converter script not found
   Expected location: docs/convert_readme_to_index_html.py
```
Exit code: 1

### Conversion Failure
```
❌ ERROR: HTML conversion failed
```
Exit code: 1

## Agricultural Context

**Web Documentation Essential**: Professional HTML presentation critical for stakeholder communication in agricultural robotics platform. Automated conversion prevents documentation drift between README.md and web docs—essential for ISO compliance presentation.

**Stakeholder Access**: Equipment operators, safety engineers, and compliance auditors often access project documentation via web browsers rather than viewing raw markdown. Automated HTML generation ensures they see up-to-date information.

**Quality Assurance**: Preserves agricultural terminology (ISOBUS, vector clocks, multi-tractor coordination) and technical specifications (test counts, performance metrics, safety levels) in web-friendly format.

## Integration Points

### With README.md Updates
When README.md changes, `updatewebdocs` should be run to regenerate HTML:
```bash
# Edit README.md
vim README.md

# Regenerate HTML
./bin/updatewebdocs

# Commit both together
git add README.md docs/index.html
git commit -m "docs(docs): Update documentation"
```

### With Pre-commit Hooks (Future)
Future integration with pre-commit hooks will automatically detect README.md changes and run `updatewebdocs` to ensure HTML stays synchronized.

## Test Coverage

**Test Suite**: tests/unit/commands/test_updatewebdocs.py (11 tests)

**Test Categories**:
1. **Command Execution**: Existence, executability, help output
2. **HTML Generation**: Conversion accuracy, formatting, code blocks
3. **Git Integration**: Automatic staging, helpful messages
4. **Agricultural Context**: Terminology preservation, technical specs
5. **Error Handling**: Missing files, graceful failures

**Test Results**: All 11 tests passing in ~2 seconds

## Universal AI Agent Access

**CRITICAL**: ALL AI agents (Claude Code, GitHub Copilot, ChatGPT, Gemini Code Assist, Amazon CodeWhisperer) can use this command.

**Cross-Session Memory**: Command must be remembered across all sessions as part of documentation workflow automation.

## File Dependencies

- **Input**: README.md (project root)
- **Output**: docs/index.html (auto-created if missing)
- **Converter**: docs/convert_readme_to_index_html.py
- **Test Suite**: tests/unit/commands/test_updatewebdocs.py

## Related Commands

- **loadsession**: Loads complete session context including documentation requirements
- **savesession**: Saves session state with documentation changes
- **updatechangelog**: Generates CHANGELOG.md from git history
- **runtests**: Executes test suite including updatewebdocs tests

## Future Enhancements

1. **Pre-commit Hook Integration**: Automatic README.md change detection
2. **HTML Linting**: Validate generated HTML structure
3. **Link Checking**: Verify all links in documentation work
4. **Image Optimization**: Compress images for web delivery

## Complete Specification

**Created**: 2025-10-01
**Test-Driven**: YES (11 tests written FIRST, then implementation)
**Agricultural Context**: Web documentation for stakeholder communication
**Universal Access**: ALL AI agents can execute this command
