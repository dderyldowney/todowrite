# VS Code Extension Setup Guide

## 🚨 **IMPORTANT: CLAUDE.md MANUAL LOADING REQUIRED**

### **VS Code Extension Behavior:**
- ❌ **Does NOT** automatically load `CLAUDE.md` on startup
- ✅ **Requires** manual command: `load and apply CLAUDE.md`
- ✅ **Works correctly** once manually loaded

### **Required Steps for VS Code:**

1. **Open VS Code:**
   ```bash
   code .
   ```

2. **Manually Load CLAUDE.md:**
   ```
   load and apply CLAUDE.md
   ```

3. **Restore Previous Session (Automatic):**
   ```
   /session-load
   ```

4. **Verify System:**
   ```
   bash .claude/quick_check.sh
   ```

### **Session Management Commands:**
```
/session-load    # Load and display previous session state
/session-save    # Save current session state
```

These commands automatically work when CLAUDE.md is loaded and provide:
- ✅ Previous accomplishments restored
- ✅ Key findings and system status
- ✅ Continuity across sessions
- ✅ Complete context preservation

### **Expected Database Configuration:**
```python
db_config = {
    'host': 'localhost',
    'port': 5432,                    # PostgreSQL container
    'database': 'todowrite',         # ToDoWrite project database
    'user': 'todowrite_user',        # ToDoWrite user
    'password': 'todowrite_secure_password_2024'
}
```

### **Verification Test:**
```bash
docker exec todowrite-postgres psql -U todowrite_user -d todowrite -c "SELECT version();"
# Expected: PostgreSQL 16.10 on x86_64-pc-linux-musl...
```

### **System Status:**
- ✅ PostgreSQL Backend: FULLY OPERATIONAL
- ✅ Container: todowrite-postgres (running 24+ hours)
- ✅ Database: todowrite with project management tables
- ✅ VS Code Extension: Works with manual CLAUDE.md loading

### **Note:**
This behavior is different from terminal Claude Code, which automatically loads CLAUDE.md. The VS Code extension requires manual loading each time you start a new session or restart VS Code.
