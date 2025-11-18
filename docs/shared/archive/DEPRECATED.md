# Deprecated Features and Paths

This document tracks deprecated features and file paths in the ToDoWrite project.

## Deprecated Schema Location

### File Path
- **Deprecated**: `configs/schemas/todowrite.schema.json`
- **Recommended**: `todowrite/schemas/todowrite.schema.json`

### Migration Status
- ✅ **Package Integration**: Schema is now part of the package distribution
- ✅ **Backward Compatibility**: Old location still works with fallback
- ✅ **Documentation Updated**: All references updated to new location
- ⏳ **Deprecation Warning**: Will be fully deprecated in future version

### Why the Change?
1. **Package Distribution**: Schema should be included with package installation
2. **External Access**: Easy import for external projects: `todowrite.TODOWRITE_SCHEMA`
3. **Version Consistency**: Schema version stays in sync with package version
4. **Maintainability**: Single source of truth for schema definition

### For External Projects

#### Before (Old Way)
```python
# External projects managing their own schema files
import json
from pathlib import Path

# Manual schema file management
schema_path = Path("configs/schemas/todowrite.schema.json")
with open(schema_path) as f:
    schema = json.load(f)
```

#### After (New Way)
```python
# Import schema directly from package
import todowrite

schema = todowrite.TODOWRITE_SCHEMA

# Or direct import
from todowrite.schema import TODOWRITE_SCHEMA
```

## Migration Timeline

### Phase 1: Current (✅ Complete)
- [x] Schema moved to package directory
- [x] Package configuration updated
- [x] Backward compatibility maintained
- [x] Documentation created

### Phase 2: Short Term (🔄 In Progress)
- [ ] Update all internal tools to use package schema
- [ ] Add deprecation warning to old schema location
- [ ] Update CI/CD to use package schema

### Phase 3: Future (⏳ Planned)
- [ ] Remove dependency on old schema location
- [ ] Remove backward compatibility fallback
- [ ] Update all documentation references

## How to Update Your Project

### For Project Maintainers
1. **Update Imports**: Change to use `todowrite.TODOWRITE_SCHEMA`
2. **Remove Schema File**: Delete `configs/schemas/todowrite.schema.json`
3. **Update Documentation**: Update any internal documentation

### For External Users
1. **No Action Required**: Your current setup will continue to work
2. **Recommended**: Update to use package import for cleaner code
3. **Benefit**: Schema updates automatically with package upgrades

## Detection and Warnings

### Runtime Warnings
When using the old schema location, you may see:
```bash
# CLI usage with fallback
todowrite validate
# Note: Using legacy schema location, consider updating to package schema
```

### Import Warnings
Future versions may include deprecation warnings for the old path.

## Impact Assessment

### Low Impact
- ✅ **Backward Compatibility**: Existing code continues to work
- ✅ **CLI Tools**: Work with both old and new locations
- ✅ **External Projects**: No breaking changes

### Benefits
- 🎯 **Package Consistency**: Schema is now part of the distribution
- 🚀 **Easy Access**: Simple import for external projects
- 🔒 **Version Management**: Schema version stays with package version
- 📦 **Distribution**: Schema available with package installation

## Questions or Issues

If you have questions about this deprecation or need help migrating, please:
1. Check the [SCHEMA_MIGRATION_GUIDE.md](./SCHEMA_MIGRATION_GUIDE.md)
2. Review the [SCHEMA_USAGE.md](./SCHEMA_USAGE.md)
3. Open an issue in the project repository

---

*This document is part of the ongoing improvement of the ToDoWrite package to better serve external projects while maintaining backward compatibility.*
