Save the current session state to the PostgreSQL database for persistence across Claude sessions, capturing current context and accomplishments.

The command will:
1. Capture current session context and accomplishments
2. Save to todowrite_sessions table in PostgreSQL
3. Associate session with current project (todowrite)
4. Generate unique session ID with timestamp
5. Provide confirmation of successful save

You'll see:
- Confirmation of successful save operation
- Session ID that was created/saved
- Timestamp of the save operation
- Success/failure status message
