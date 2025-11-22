# Load and display session state

Retrieves and displays the most recent session state for the current project from the PostgreSQL database.

## Usage

```
/session-load
```

## What it does

1. Queries todowrite_sessions table for latest project session
2. Retrieves previous session context and accomplishments
3. Displays formatted summary of previous work
4. Shows system status and key findings
5. Restores continuity for continued development

## Output

Displays a comprehensive summary including:

### 🔄 **SESSION RESTORED**
- Timestamp of previous session
- Session ID reference

### 📋 **Previous Accomplishments**
- List of completed tasks and achievements
- Progress milestones reached

### 🔍 **Key Findings**
- Important discoveries and insights
- Technical solutions implemented
- Documentation created

### 🗄️ **System Status**
- PostgreSQL container status
- Database connectivity information
- Table and record counts
- Current system configuration

### 💾 **Session Information**
- Current session ID
- Project name
- Ready state for continued work

## Requirements

- PostgreSQL container running (mcp-postgres)
- Virtual environment activated
- Previous session data exists in database
- Proper database connectivity established

## Notes

- If no previous session found, indicates first-time setup
- Sessions are project-specific (todowrite project only)
- Most recent session for the project is loaded
