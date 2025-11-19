# Project-Scoped Episodic Memory Configuration

## Problem Solved

The default episodic memory configuration indexes conversations from **ALL projects** into a single global database, causing cross-project contamination:

- **762 conversations** from ToDoWrite project
- **188 conversations** from afs_fastapi project
- **9 conversations** from other projects

This means search results from one project could contain irrelevant context from completely different projects.

## Solution: Project-Scoped Episodic Memory

Each project now has its own isolated episodic memory database:

### Database Location
```
<todowrite_root>/.claude/episodic_memory.db
```

### Isolation Benefits
- ✅ **Pure Context**: Search results only contain conversations from current project
- ✅ **No Cross-Contamination**: afs_fastapi conversations cannot poison ToDoWrite results
- ✅ **Relevant Memory**: All search results are guaranteed to be project-specific
- ✅ **Privacy**: Each project's conversation history remains isolated

## Implementation

### 1. Project-Specific Database Path
The `EPISODIC_MEMORY_DB_PATH` environment variable overrides the default global database location:

```bash
export EPISODIC_MEMORY_DB_PATH="$(pwd)/.claude/episodic_memory.db"
```

### 2. Project Management Script
Use `./dev_tools/project_episodic_memory.sh` for project-specific operations:

```bash
# Setup project-scoped episodic memory
./dev_tools/project_episodic_memory.sh setup

# Index only current project conversations
./dev_tools/project_episodic_memory.sh index

# Search only current project conversations
./dev_tools/project_episodic_memory.sh search "database issues"

# Show current project statistics
./dev_tools/project_episodic_memory.sh stats
```

### 3. Automatic Project Isolation
The project includes session startup hooks that automatically set `EPISODIC_MEMORY_DB_PATH` to the project-specific location, ensuring all episodic memory operations are isolated by default.

## Usage Examples

### Global vs Project-Scoped Comparison

**Before (Global Database):**
```bash
$ episodic-memory stats
Total Conversations: 927
Top Projects:
   762 - -Users-dderyldowney-Documents-GitHub-dderyldowney-ToDoWrite
   188 - -Users-dderyldowney-Documents-GitHub-dderyldowney-afs-fastapi
```

**After (Project-Scoped):**
```bash
$ ./dev_tools/project_episodic_memory.sh stats
Total Conversations: 42  # Only ToDoWrite conversations
Unique Projects: 1      # Only current project
```

### Search Isolation
```bash
# Project-scoped search - only finds ToDoWrite conversations
./dev_tools/project_episodic_memory.sh search "authentication"

# Global search - finds results from ALL projects
episodic-memory search "authentication"  # Mixed results from multiple projects
```

## Verification

### 1. Check Project Isolation
```bash
# Should show only current project conversations
./dev_tools/project_episodic_memory.sh stats

# Should show different results than global
node ~/.claude/plugins/cache/episodic-memory/cli/episodic-memory.js stats
```

### 2. Test Search Purity
```bash
# Search for project-specific terms
./dev_tools/project_episodic_memory.sh search "ToDoWrite"

# Results should only contain current project context
```

## Multi-Project Setup

Each project should set up its own episodic memory isolation:

### afs_fastapi Project
```bash
cd ~/Documents/GitHub/dderyldowney/afs_fastapi
# Copy project_episodic_memory.sh script
# Run ./dev_tools/project_episodic_memory.sh setup
```

### Other Projects
Repeat the same setup process for each project that wants isolated episodic memory.

## Technical Details

### Environment Variable Override
The episodic memory system respects `EPISODIC_MEMORY_DB_PATH` as defined in `$HOME/.claude/plugins/cache/episodic-memory/dist/paths.js`:

```javascript
export function getDbPath() {
    // Allow test override with direct DB path
    if (process.env.EPISODIC_MEMORY_DB_PATH || process.env.TEST_DB_PATH) {
        return process.env.EPISODIC_MEMORY_DB_PATH || process.env.TEST_DB_PATH;
    }
    return path.join(getIndexDir(), 'db.sqlite');
}
```

### Database Schema Support
The episodic memory database schema already supports project-level organization with a `project` field in the exchanges table, enabling proper isolation when using separate databases per project.

## Security Benefits

1. **Context Isolation**: Prevents accidental information leakage between projects
2. **Relevant Results**: All search results are guaranteed to be from current project context
3. **Privacy Control**: Each project maintains its own private conversation history
4. **Compliance**: Better control over data access and retention per project

## Migration from Global

Use the provided migration script to import existing project conversations from the global episodic memory database:

```bash
# Check what conversations are available for migration (dry run)
python dev_tools/migrate_episodic_memory.py --dry-run

# Perform the actual migration
python dev_tools/migrate_episodic_memory.py

# Verify migration completed
./dev_tools/project_episodic_memory.sh stats
```

### Migration Example
**Before Migration:**
- Global database: 927 conversations (mixed from multiple projects)
- Project database: 0 conversations

**After Migration:**
- Successfully migrated 864 ToDoWrite conversations
- Project database: 864+ ToDoWrite conversations only
- Complete isolation achieved

### Migration Script Features
- ✅ **Automatic Detection**: Finds all project conversation paths
- ✅ **Safe Copy**: Copies conversations without affecting global database
- ✅ **Project Isolation**: Only imports conversations from current project
- ✅ **Indexing**: Automatically indexes migrated conversations
- ✅ **Verification**: Provides detailed migration reports

## File Structure

```
todowrite/
├── .claude/
│   ├── episodic_memory.db              # Project-specific database
│   ├── episodic_memory_archive/        # Project conversation archive
│   └── hooks/
│       └── session_startup_project_episodic_memory.py
├── dev_tools/
│   └── project_episodic_memory.sh      # Project management script
└── docs/
    └── EPISODIC_MEMORY_PROJECT_ISOLATION.md
```

This configuration ensures complete episodic memory isolation between projects while maintaining full functionality within each project's context.
