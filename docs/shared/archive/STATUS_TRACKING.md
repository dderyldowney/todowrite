# Status Tracking

**Version**: See VERSION file
**Status**: Production Ready
**Last Updated**: November 8, 2025

This document describes the status tracking functionality in ToDoWrite, which provides comprehensive status management for nodes with progress tracking, dates, and assignee information.

## Overview

The status tracking enhancement extends the ToDoWrite system with the following features:

- **Status Management**: Track node status with predefined states
- **Progress Tracking**: Monitor completion progress (0-100%)
- **Date Tracking**: Track started and completion dates
- **Assignee Management**: Assign nodes to specific users

## Status Values

Nodes can have the following status values:

| Status | Description | Use Case |
|--------|-------------|----------|
| `planned` | Node is planned but not yet started | Initial state for all nodes |
| `in_progress` | Node is actively being worked on | Work has commenced |
| `completed` | Node has been completed successfully | Work finished and accepted |
| `blocked` | Node is blocked by external dependencies | Cannot proceed until dependencies are resolved |
| `cancelled` | Node was cancelled and will not be completed | No longer needed or required |

## Status Tracking Fields

The following fields have been added to support status tracking:

### Root Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Current status of the node (one of the predefined values) |
| `progress` | integer | Progress percentage (0-100) |
| `started_date` | string | ISO 8601 timestamp when work started |
| `completion_date` | string | ISO 8601 timestamp when work completed |
| `assignee` | string | Person responsible for completing the node |

### Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `assignee` | string | Person responsible for completing the node (duplicate of root level for backward compatibility) |

## CLI Commands

For project development utilities, see [Project Utilities](PROJECT_UTILITIES.md).

### Status Update

Update the status and progress of a node:

```bash
todowrite update --id <NODE_ID> --status <STATUS> --progress <PROGRESS> [OPTIONS]
```

Options:
- `--status`: Set the status (planned, in_progress, completed, blocked, cancelled)
- `--progress`: Set progress percentage (0-100)
- `--assignee`: Set the assignee of the node

Examples:
```bash
# Mark a task as in progress with 50% progress
todowrite update --id TSK-123 --status in_progress --progress 50

# Mark a task as completed with full progress
todowrite update --id TSK-123 --status completed --progress 100

# Assign a task
todowrite update --id TSK-123 --assignee john.doe
```

### Node Details

Display detailed information for a node including status:

```bash
todowrite get --id <NODE_ID>
```

### Status Listing

List nodes with their current status:

```bash
# List all nodes
todowrite list

# List nodes by status (using search)
todowrite search "status:in_progress"
```

## Status Transitions

The system enforces the following status transition rules:

1. **completed** → Any status: Not allowed (completed nodes cannot be changed)
2. **planned** → `in_progress`, `blocked`, `cancelled`: Allowed
3. **in_progress** → `completed`, `blocked`, `cancelled`: Allowed
4. **blocked** → `in_progress`, `cancelled`: Allowed
5. **cancelled** → `in_progress`, `completed`: Allowed

Attempting to make an invalid transition will display a warning.

## Progress Tracking

Progress is tracked as a percentage from 0 to 100:

- **0%**: Node is planned or not started
- **1-99%**: Node is in progress with partial completion
- **100%**: Node is completed

When a node is marked as `completed`, the progress is automatically set to 100% if not already set.

## Date Tracking

Dates are stored in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ):

- **started_date**: Automatically set when status changes to `in_progress`
- **completion_date**: Automatically set when status changes to `completed`

## Backward Compatibility

The status tracking enhancement maintains full backward compatibility:

1. **Existing Nodes**: Nodes without status tracking fields work unchanged
2. **Default Values**: New status fields have sensible defaults:
   - `status`: "planned"
   - `progress`: None
   - `started_date`: None
   - `completion_date`: None
   - `assignee`: "" (empty string)
3. **Schema Validation**: Existing YAML files continue to validate against the updated schema
4. **CLI Compatibility**: Existing CLI commands work unchanged

## Database Schema Updates

The database schema has been extended with the following new columns:

- `progress`: INTEGER (NULLABLE)
- `started_date`: TEXT (NULLABLE)
- `completion_date`: TEXT (NULLABLE)
- `assignee`: TEXT (NULLABLE)

## JSON Schema Updates

The JSON schema has been updated to include:

- Status field with enum validation
- Progress field with range validation (0-100)
- Date fields with format validation
- Assignee field in both root and metadata levels

## Migration Considerations

1. **Database Migration**: Existing databases will be automatically updated when the application starts
2. **YAML Files**: Existing YAML files remain valid and will be auto-imported
3. **Validation**: New validation rules apply only to nodes created after the enhancement

## Best Practices

1. **Status Consistency**: Use the appropriate status value for the current state
2. **Progress Updates**: Regularly update progress for `in_progress` nodes
3. **Date Accuracy**: Set started dates when work begins and completion dates when work finishes
4. **Assignee Clarity**: Always assign nodes to specific individuals when work begins
5. **Status Transitions**: Follow the allowed transition rules to maintain data integrity

## Troubleshooting

### Common Issues

1. **Validation Errors**: Ensure status values match the predefined enum
2. **Date Format**: Use ISO 8601 format for date fields
3. **Progress Range**: Keep progress values between 0 and 100
4. **Status Transitions**: Check transition rules before changing status

### Debug Mode

Enable debug logging for detailed status tracking information:

```bash
export LOG_LEVEL=debug
python -m todowrite status show <NODE_ID>
```

## Examples

### Example 1: Task Lifecycle

```bash
# Create a task (automatically has planned status)
python -m todowrite create --id TSK-IMPLEMENT-FEATURE --layer Task --title "Implement Feature X"

# Start work on the task
python -m todowrite status update TSK-IMPLEMENT-FEATURE --status in_progress --assignee developer1 --progress 25

# Update progress as work continues
python -m todowrite status update TSK-IMPLEMENT-FEATURE --progress 50

# Complete the task
python -m todowrite status update TSK-IMPLEMENT-FEATURE --status completed --progress 100 --completion-date "2025-01-20T18:00:00Z"
```

### Example 2: Project Tracking

```bash
# Create multiple tasks for a project
python -m todowrite create --id TSK-DESIGN --layer Task --title "System Design"
python -m todowrite create --id TSK-DEVELOP --layer Task --title "Core Development"
python -m todowrite create --id TSK-TEST --layer Task --title "Testing"

# Start the design phase
python -m todowrite status update TSK-DESIGN --status in_progress --assignee architect

# Design is complete
python -m todowrite status update TSK-DESIGN --status completed --progress 100

# Start development
python -m todowrite status update TSK-DEVELOP --status in_progress --assignee developer1 --progress 30

# Generate project status report
python -m todowrite status report --layer Task --format table
```

## API Integration

The status tracking enhancement is fully integrated with the ToDoWrite API:

- All existing API endpoints work with the new status fields
- New fields are included in GET responses
- POST/PUT requests can include status tracking fields
- Validation is enforced at the API level

## Additional Documentation

- **[← Documentation Index](README.md)** - Complete documentation overview
- **[Installation Guide](installation.md)** - Get ToDoWrite installed
- **[Integration Guide](INTEGRATION_GUIDE.md)** - Real-world usage examples
- **[Project Utilities](PROJECT_UTILITIES.md)** - Available utilities and helpers
- **[Main Project Documentation](../README.md)** - Project overview and features
- **[CLI Reference](../cli_package/README.md)** - Command-line interface reference

## Testing

Comprehensive tests have been added to verify:

1. **Status Validation**: Only allowed status values are accepted
2. **Transition Rules**: Status transitions follow the defined rules
3. **Backward Compatibility**: Existing nodes continue to work
4. **CLI Commands**: All status-related CLI commands function correctly
5. **Database Integration**: Status tracking fields persist correctly
6. **JSON Schema**: Schema validation works with new fields

---

**Current Version**: See VERSION file
**Python Support**: 3.12+
**Test Status**: 157/157 tests passing ✅
**License**: MIT
