# PostgreSQL Architecture Policy

## 🚨 POSTGRESQL BACKEND SYSTEM

### Single Source of Truth Mandate

**FUNDAMENTAL RULE: PostgreSQL databases are the ONLY authoritative data source**

### 🚫 Forbidden Storage Methods

**NEVER ALLOWED for persistent data:**
- ❌ SQLite (except explicitly marked test files)
- ❌ JSON session storage
- ❌ YAML primary storage
- ❌ Local file data persistence

### 🔴 Required Data Storage

**ALL persistent data MUST use:**
- All session state → `mcp_sessions`
- All ToDoWrite data → `todowrite`
- All conversation history → `mcp_episodic_memory`

If persistent data is encountered outside PostgreSQL → **STOP**.

#### Container Information
- **Container**: `mcp-postgres` (port 5433, auto-restart)
- **IMPORTANT CLARIFICATION**: `mcp-postgres` is the Docker **container name** for the PostgreSQL database engine, NOT an MCP server
- **Purpose**: This container hosts multiple databases that serve MCP servers and the application

### Database Architecture

#### Authoritative Databases
1. **`todowrite`** - Project management (43 tables, 12-layer hierarchy) - **AUTHORITATIVE**
2. **`mcp_episodic_memory`** - Conversation storage (6,686+ conversations) - **AUTHORITATIVE**
3. **`mcp_sessions`** - Session management and persistence - **AUTHORITATIVE**
4. **`mcp_filesystem`** - MCP filesystem tool data - **AUTHORITATIVE**
5. **`mcp_main`** - General MCP server data - **AUTHORITATIVE**

### Database Connection Mandate

#### PostgreSQL-ONLY Requirement
```python
# REQUIRED - Connect to PostgreSQL ONLY
DATABASE_URL = "postgresql://mcp_user:mcp_secure_password_2024@localhost:5433/todowrite"

# FORBIDDEN - NEVER use these:
# sqlite:///path/to/todowrite.db  # ❌ FORBIDDEN
# yaml file storage               # ❌ FORBIDDEN
# local JSON files               # ❌ FORBIDDEN
```

#### CLI Usage Requirements
```bash
# CORRECT - PostgreSQL ONLY
PYTHONPATH="lib_package/src:cli_package/src" python -m todowrite_cli --storage-preference postgresql_only

# FORBIDDEN - NEVER use:
# python -m todowrite_cli --storage-preference sqlite_only  # ❌ FORBIDDEN
# python -m todowrite_cli --storage-preference yaml_only   # ❌ FORBIDDEN
```

### 🚨 TABLE PROTECTION MANDATE

#### Production Data Protection
```bash
# FORBIDDEN - NEVER delete production tables:
# DROP TABLE commands on production data
# TRUNCATE TABLE on production tables
# DELETE FROM production_tables without specific business reason
# Database schema modifications outside of migration scripts

# ALLOWED - Testing and development tables (naming convention: test_, temp_, dev_):
DROP TABLE test_user_data;           # OK - clearly marked as test
TRUNCATE temp_processing_queue;      # OK - clearly marked as temporary
DROP TABLE dev_feature_experiment;   # OK - clearly marked as development
DROP DATABASE dev_test_database;      # OK - clearly marked as development
```

### Database Investigation Protocol

#### Before Any Database Operations
1. **Verify table exists**: Check database structure before modifications
2. **Check for data**: Verify existing data before making changes
3. **Use investigation commands**: Follow DATABASE_INVESTIGATION_PROTOCOL.md
4. **Never assume missing**: Always verify actual state

### Verification Commands

```bash
# Verify ToDoWrite is using PostgreSQL (MUST PASS):
docker exec mcp-postgres psql -U mcp_user -d todowrite -c "SELECT COUNT(*) FROM goals;"

# Verify no SQLite files are being used:
find . -name "*.db" -o -name "*.sqlite" 2>/dev/null | grep -v ".venv" && echo "❌ FORBIDDEN SQLITE FILES FOUND" || echo "✅ No forbidden SQLite files"

# Verify database accessibility:
docker exec mcp-postgres psql -U mcp_user -d mcp_sessions -c "SELECT COUNT(*) FROM sessions LIMIT 1;"
docker exec mcp-postgres psql -U mcp_user -d mcp_episodic_memory -c "SELECT COUNT(*) FROM conversations LIMIT 1;"
```

### Database Usage Patterns

#### Session Storage (mcp_sessions)
- **Purpose**: Cross-session persistence, conversation state, work continuity
- **Authority**: SINGLE source of truth for ALL session data
- **File-based session storage**: FORBIDDEN
- **Cache only**: JSON files may be used as cache, never primary storage

#### Project Management (todowrite)
- **Purpose**: ToDoWrite system data
- **Structure**: 43 tables in 12-layer hierarchy
- **All operations**: MUST use PostgreSQL exclusively
- **Models API**: ONLY use existing lib_package Models API

#### Conversation History (mcp_episodic_memory)
- **Purpose**: Store conversation history across sessions
- **Authority**: NEVER use file cache as primary storage
- **Size**: 6,686+ conversations (as of documentation)
- **Tables created**: Automatically on first use

### MCP Server Databases

#### Database Assignment
- **MCP servers MUST store data** in designated PostgreSQL databases
- **No file-based persistence** for MCP server data
- **Cross-server communication**: Via PostgreSQL databases
- **System-wide resources**: Databases serve all projects on the machine

### PostgreSQL Configuration

#### Connection Details
```bash
# Connection parameters for all applications:
Host: localhost
Port: 5433
Username: mcp_user
Password: mcp_secure_password_2024
Database: varies (see list above)
```

#### Container Management
- **Auto-restart**: Container configured to restart automatically
- **Data persistence**: Docker volumes ensure data persistence across container restarts
- **Backup strategy**: Regular backups recommended for all databases
- **Monitoring**: Use health check scripts to verify database availability

### Compliance Requirements

Before submitting any work that interacts with databases:

1. ✅ All operations use PostgreSQL connections only
2. ✅ No SQLite files created or used
3. ✅ No YAML/JSON primary storage
4. ✅ Production tables protected from DROP/TRUNCATE
5. ✅ Investigation protocol followed before changes
6. ✅ Verification commands pass
7. ✅ Database accessibility confirmed
8. ✅ Cross-session continuity maintained
9. ✅ MCP server data stored in correct databases
10. ✅ File-based storage limited to cache only

### PostgreSQL vs Alternative Storage

#### PostgreSQL Advantages
- **ACID compliance**: Ensures data integrity
- **Concurrent access**: Multiple users/sessions
- **Complex queries**: Powerful SQL capabilities
- **Scalability**: Handles large datasets efficiently
- **Transactions**: Atomic operations across multiple tables
- **Indexing**: Optimized query performance
- **Backup/Recovery**: Mature backup tools and procedures

#### Alternative Storage Limitations
- **SQLite**: Not suitable for concurrent access across sessions
- **JSON files**: No transaction support, limited query capabilities
- **YAML files**: Manual parsing, no integrity guarantees
- **File-based**: No ACID properties, prone to corruption
