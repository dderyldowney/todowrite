# Episodic Memory Database Locations & Recovery Guide

**CRITICAL: This file documents where all episodic memory databases are stored.
These are local-only files that MUST NEVER be committed to git, but MUST be preserved.**

---

## Project-Specific Episodic Memory Database (CURRENT PROJECT)

**Location**: `$(pwd)/.claude/episodic_memory.db`
**Purpose**: Contains ONLY ToDoWrite project conversations (isolated from other projects)
**Status**: ✅ ACTIVE - This is the current working database

### Files:
- `.claude/episodic_memory.db` - Main SQLite database
- `.claude/episodic_memory.db-shm` - SQLite shared memory file
- `.claude/episodic_memory.db-wal` - SQLite write-ahead log
- `.claude/episodic_memory_archive/` - Conversation files for this project

---

## Global Episodic Memory Database (ALL PROJECTS - CONTAMINATED)

**Location**: `$HOME/.config/superpowers/conversation-index/db.sqlite`
**Purpose**: Contains ALL conversations from ALL projects (including afs_fastapi contamination)
**Status**: ⚠️  LEGACY - Contains cross-project contamination, NOT used by this project

### Associated Files:
- `$HOME/.config/superpowers/conversation-archive/` - Global conversation archive
- `$HOME/.claude/projects/` - Claude's per-project conversation directories

---

## Recovery Instructions

### If Project Database is Lost or Corrupted:

1. **Check backup locations**:
   ```bash
   # Verify project database exists
   ls -la .claude/episodic_memory*

   # Check conversation archive
   ls -la .claude/episodic_memory_archive/
   ```

2. **Recreate from global database** (if needed):
   ```bash
   # Re-run migration script
   python dev_tools/migrate_episodic_memory.py --force

   # Or manually copy conversations
   cp -r "$HOME/.config/superpowers/conversation-archive/-Users-dderyldowney-Documents-GitHub-dderyldowney-ToDoWrite"/* .claude/episodic_memory_archive/

   # Re-index with correct database
   export EPISODIC_MEMORY_DB_PATH="$(pwd)/.claude/episodic_memory.db"
   node "$HOME/.claude/plugins/cache/episodic-memory/cli/episodic-memory.js" index --cleanup
   ```

3. **Verify isolation**:
   ```bash
   export EPISODIC_MEMORY_DB_PATH="$(pwd)/.claude/episodic_memory.db"
   node "$HOME/.claude/plugins/cache/episodic-memory/cli/episodic-memory.js" stats
   ```
   Should show only ToDoWrite project conversations, NO afs-fastapi.

---

## Environment Variable Requirements

**CRITICAL**: The project-specific database will ONLY be used when this environment variable is set:

```bash
export EPISODIC_MEMORY_DB_PATH="$(pwd)/.claude/episodic_memory.db"
```

**WITHOUT this variable**: Uses global contaminated database (BAD!)
**WITH this variable**: Uses clean project-specific database (GOOD!)

---

## Session Startup Requirements

All sessions MUST initialize episodic memory with project isolation:

```bash
# Set project-specific database FIRST
export EPISODIC_MEMORY_DB_PATH="$(pwd)/.claude/episodic_memory.db"

# Then initialize episodic memory
./dev_tools/ensure_episodic_memory.sh

# Or use project-specific commands
./dev_tools/project_episodic_memory.sh stats
```

---

## Backup Strategy

### Recommended Backup Locations:
1. **Project Database**: `.claude/episodic_memory.db`
2. **Conversation Archive**: `.claude/episodic_memory_archive/`
3. **Session Tracking**: `.claude/episodic_memory_ready.json`

### Backup Commands:
```bash
# Create backup archive
tar -czf episodic_memory_backup_$(date +%Y%m%d).tar.gz .claude/episodic_memory*

# Store in safe location (external drive, cloud storage, etc.)
```

---

## Migration History

- **2025-11-18**: Initial project isolation implementation
- **Migrated**: 1076+ ToDoWrite conversations from global database
- **Isolated**: afs_fastapi contamination removed
- **Status**: ✅ Project isolation working correctly

---

## Contact & Recovery

If episodic memory is lost:
1. Check this file for locations
2. Run migration script: `python dev_tools/migrate_episodic_memory.py --force`
3. Verify with: `./dev_tools/project_episodic_memory.sh stats`

**NEVER delete the global database** - it contains conversation history that may be needed for recovery.

---

*Last Updated: 2025-11-18*
*Project: ToDoWrite*
