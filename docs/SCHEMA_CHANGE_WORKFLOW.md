# ToDoWrite Schema Change Workflow

## Overview

This document establishes the standard workflow for making schema changes in the ToDoWrite project. **All schema changes must be made against the new package-integrated schema location** to ensure consistency and proper distribution.

## Primary Schema Location

### ✅ **Current Schema Location (PRIMARY)**
```bash
todowrite/schemas/todowrite.schema.json
```

### ❌ **Deprecated Schema Location (LEGACY)**
```bash
configs/schemas/todowrite.schema.json
```

## Schema Change Workflow

### Step 1: Edit the Package Schema
All schema modifications must be made to the package schema:
```bash
# Edit the primary schema file
vim todowrite/schemas/todowrite.schema.json
```

### Step 2: Update Schema Export
The schema is automatically exported through the package. No manual export needed.

### Step 3: Test Package Import
Verify the schema can be imported correctly:
```python
# Test in Python
import todowrite
schema = todowrite.TODOWRITE_SCHEMA
print(f"Schema loaded: {len(schema)} properties")
```

### Step 4: Run Validation Tests
```bash
# Test CLI validation
todowrite validate

# Test if needed
python -c "
import todowrite
from jsonschema import validate
test_node = {
    'id': 'TEST-001',
    'layer': 'Goal',
    'title': 'Test',
    'description': 'Test node',
    'links': {'parents': [], 'children': []}
}
validate(instance=test_node, schema=todowrite.TODOWRITE_SCHEMA)
print('Validation successful!')
"
```

## Development Tools

### Schema Generation
The `extract_schema.py` tool now generates to the package location:
```bash
# Generate schema from documentation
python todowrite/tools/extract_schema.py
# Output: todowrite/schemas/todowrite.schema.json
```

### Schema Validation
The `tw_validate.py` tool now uses package schema by default:
```bash
# Validate using package schema
python todowrite/tools/tw_validate.py

# Legacy location fallback (automatic if package not available)
python todowrite/tools/tw_validate.py --schema configs/schemas/todowrite.schema.json
```

## Automated Checks

### Pre-commit Hook
Add this check to `.pre-commit-config.yaml`:
```yaml
- repo: local
  hooks:
    - id: schema-check
      name: Ensure schema changes are in package location
      entry: todowrite utils check-schema
      language: system
      pass_filenames: true
      always_run: true
```

### CI/CD Pipeline
Add to GitHub Actions or similar CI:
```yaml
- name: Validate Schema Location
  run: |
    # Check that primary schema exists and is not empty
    if [ ! -f "todowrite/schemas/todowrite.schema.json" ]; then
      echo "ERROR: Primary schema file not found!"
      exit 1
    fi
    # Check deprecated schema doesn't have new changes
    todowrite utils check-deprecated
```

## Change Tracking

### Version Control Pattern
```bash
# When making schema changes, commit with message format:
git commit -m "feat(schema): Add new validation property

- Add 'severity' field to metadata section
- Update validation rules for Command layer
- Ensure backward compatibility

🤖 Generated with [Claude Code](https://claude.com/claude-code)"
```

### Change Log Entry
```markdown
## [0.1.7.0] - 2025-10-29

### Added
- New validation property: metadata.severity (enum: low, med, high)
- Enhanced command layer validation
- Improved error messages for validation failures
```

## Migration Guide Updates

When making schema changes, update relevant documentation:
- `SCHEMA_MIGRATION_GUIDE.md` - Add migration notes
- `DEPRECATED.md` - Update deprecation timeline if needed
- Any API documentation that references schema changes

## Common Pitfalls to Avoid

### ❌ **Don't Edit Deprecated Location**
```bash
# WRONG - Do not edit:
vim configs/schemas/todowrite.schema.json
```

### ✅ **Do Edit Package Location**
```bash
# CORRECT - Edit package schema:
vim todowrite/schemas/todowrite.schema.json
```

### ❌ **Don't Update Old References**
- Tools should not reference deprecated schema location
- Documentation should point to new import method

### ✅ **Use Package Import**
```python
# CORRECT - Use package import:
import todowrite
schema = todowrite.TODOWRITE_SCHEMA
```

## Testing Checklist

Before committing schema changes:
- [ ] Can schema be imported via `todowrite.TODOWRITE_SCHEMA`?
- [ ] Does `todowrite validate` work correctly?
- [ ] Are existing YAML files still valid?
- [ ] Does the CLI work with new schema?
- [ ] Are validation tests passing?

## Emergency Procedures

### If Schema Breaks
1. **Immediate Fix**: Edit `todowrite/schemas/todowrite.schema.json`
2. **Test**: Import and validate with `todowrite.TODOWRITE_SCHEMA`
3. **Document**: Add fix notes to change log
4. **Communicate**: Notify team of breaking changes

### Rollback Procedure
1. **Revert to previous package schema**:
   ```bash
   git checkout HEAD~1 -- todowrite/schemas/todowrite.schema.json
   ```
2. **Test**: Ensure old functionality works
3. **Document**: Note rollback in change log

---

**Remember**: All schema changes must go through the package schema location. The deprecated location is for legacy compatibility only and should not be modified for new features.
