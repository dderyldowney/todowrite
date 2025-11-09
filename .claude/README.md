# Claude Code Configuration Directory

This directory contains Claude Code's session configuration and initialization scripts for the ToDoWrite project.

## File Structure

```
.claude/
├── README.md                    # This file
├── settings.local.json          # Claude Code permissions and settings
├── system_instructions.md       # System-level instructions for Claude
├── session_startup.py           # Main session initialization script
├── init_script.py              # Python initialization wrapper
└── session_init.sh              # Shell session initialization script
```

## Session Initialization System

The session initialization system ensures that token optimization and agent control processes are automatically loaded at the beginning of every Claude Code session.

### How It Works

1. **Automatic Loading**: The system is automatically triggered when:
   - Starting a new Claude Code session
   - Using the `/clear` command in the CLI
   - Opening new conversations

2. **Initialization Process**:
   - Sets up token optimization environment
   - Initializes HAL agents and token-sage
   - Configures project-specific Python paths
   - Sets environment variables for efficiency

3. **Permissions**: The `settings.local.json` file includes permissions to run:
   - `./.claude/session_init.sh` - Shell initialization script
   - `python3 .claude/session_startup.py` - Direct Python execution
   - Read access to all `.claude/` files

### Files Description

#### `session_startup.py`
- **Purpose**: Main Python script that initializes all token optimization and agent control processes
- **Functionality**:
  - Sets up Python paths for dev_tools
  - Initializes token-sage and HAL agents
  - Configures environment variables
  - Displays session information summary
- **Execution**: Automatically imported and executed at session start

#### `session_init.sh`
- **Purpose**: Shell script wrapper for session initialization
- **Functionality**:
  - Sets environment variables for the shell session
  - Executes Python session startup
  - Provides fallback if Python script fails
- **Usage**: Executed automatically by Claude Code CLI

#### `init_script.py`
- **Purpose**: Python wrapper that ensures session startup runs correctly
- **Functionality**: Safe execution with error handling
- **Usage**: Alternative execution method for session initialization

## Configuration

### Environment Variables Set Automatically

- `CLAUDE_TOKEN_OPTIMIZATION=enabled` - Enables token optimization
- `CLAUDE_DEFAULT_AGENT=token-sage` - Sets default agent
- `CLAUDE_HAL_AGENTS=enabled` - Enables HAL agents
- `TODOWRITE_PROJECT_ROOT` - Sets project root directory
- `PYTHONPATH` - Updated to include dev_tools and project packages

### Python Path Configuration

The system automatically adds these paths to `PYTHONPATH`:
- `dev_tools/` - For token optimization and agent control tools
- `lib_package/src/` - For core ToDoWrite library
- `cli_package/src/` - For ToDoWrite CLI

## Troubleshooting

### Session Initialization Not Running

If you don't see the session initialization message, check:

1. **Permissions**: Ensure `settings.local.json` includes the necessary permissions
2. **File Permissions**: Verify scripts are executable:
   ```bash
   chmod +x .claude/session_init.sh
   ```
3. **Python Path**: Check that the session startup script can be imported:
   ```bash
   python3 .claude/session_startup.py
   ```

### Token Optimization Tools Not Available

If token optimization tools are not working:

1. **Check dev_tools Directory**:
   ```bash
   ls -la dev_tools/
   ```

2. **Verify Python Imports**:
   ```bash
   python3 -c "
   import sys
   sys.path.insert(0, 'dev_tools')
   from token_optimization import token_optimized_agent
   print('✅ Token optimization tools accessible')
   "
   ```

3. **Run Tools Manually**:
   ```bash
   ./run_token_tools.sh list
   ```

## Customization

### Adding Custom Initialization

To add custom session initialization steps:

1. **Edit `session_startup.py`**:
   ```python
   def custom_setup():
       print("🔧 Custom initialization...")
       # Add your custom code here

   def main():
       # ... existing code ...
       custom_setup()
       return True
   ```

2. **Update Permissions** (if needed):
   Add any new commands to `settings.local.json`

### Modifying Environment Variables

To change default environment variables:

1. **Edit `session_startup.py`**:
   ```python
   os.environ["YOUR_CUSTOM_VAR"] = "value"
   ```

2. **Edit `session_init.sh`**:
   ```bash
   export YOUR_CUSTOM_VAR="value"
   ```

## Security Notes

- The `.claude/` directory permissions in `settings.local.json` are carefully scoped
- Only necessary read and execute permissions are granted
- Session initialization scripts run with the same permissions as Claude Code
- No sensitive credentials are stored in initialization scripts

## Development

### Testing Session Initialization

To test the session initialization without waiting for a new Claude Code session:

```bash
# Test Python startup
python3 .claude/session_startup.py

# Test shell startup
./.claude/session_init.sh

# Test with simulated Claude Code environment
CLAUDE_TOKEN_OPTIMIZATION=enabled python3 .claude/session_startup.py
```

### Debugging

To debug session initialization issues:

1. **Enable Verbose Logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Check Environment Variables**:
   ```bash
   env | grep CLAUDE_
   ```

3. **Verify Python Path**:
   ```bash
   echo $PYTHONPATH
   python3 -c "import sys; print(sys.path)"
   ```

---

For more information about Claude Code configuration, see the official Claude Code documentation.