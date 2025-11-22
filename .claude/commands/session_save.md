# Save current session state

Automatically saves the current session state to the PostgreSQL database for persistence across Claude sessions.

## Usage

```
/session-save
```

## What it does

1. Captures current session context and accomplishments
2. Saves to todowrite_sessions table in PostgreSQL
3. Associates session with current project (todowrite)
4. Generates unique session ID with timestamp
5. Provides confirmation of successful save

## Output

Returns a confirmation message showing:
- Session ID that was saved
- Timestamp of save operation
- Success/failure status

## Requirements

- PostgreSQL container running (mcp-postgres)
- Virtual environment activated
- Proper database connectivity established
