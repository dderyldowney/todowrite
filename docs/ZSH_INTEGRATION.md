# ToDoWrite Shell Integration

This document explains how to set up shell integration for ToDoWrite's automatic database detection and loading.

## Quick Setup

## Available Integration Scripts

### Zsh Integration
Add to your `~/.zshrc`:
```bash
source /path/to/todowrite/todowrite_zshrc_integration.sh
```

### Bash Integration
Add to your `~/.bashrc`:
```bash
source /path/to/todowrite/todowrite_bash_integration.sh
```

### Installation Options

**Option 1: Clone and Source**
```bash
# For Zsh users
git clone https://github.com/dderyldowney/todowrite.git
echo 'source /path/to/todowrite/todowrite_zshrc_integration.sh' >> ~/.zshrc
source ~/.zshrc

# For Bash users
git clone https://github.com/dderyldowney/todowrite.git
echo 'source /path/to/todowrite/todowrite_bash_integration.sh' >> ~/.bashrc
source ~/.bashrc
```

**Option 2: Download and Source**
```bash
# For Zsh users
wget https://raw.githubusercontent.com/dderyldowney/todowrite/develop/todowrite_zshrc_integration.sh
echo 'source /path/to/todowrite/todowrite_zshrc_integration.sh' >> ~/.zshrc
source ~/.zshrc

# For Bash users
wget https://raw.githubusercontent.com/dderyldowney/todowrite/develop/todowrite_bash_integration.sh
echo 'source /path/to/todowrite/todowrite_bash_integration.sh' >> ~/.bashrc
source ~/.bashrc
```

**Option 3: Copy Integration Logic**
Copy the contents of the appropriate integration script into your shell rc file.

### Shell Reload
After setup, reload your shell:
```bash
# For Zsh
source ~/.zshrc

# For Bash
source ~/.bashrc
```

## Shell Differences

### Zsh Features
- Full directory change detection with `chpwd` hook
- Immediate loading when changing directories
- Real-time database switching

### Bash Features
- Uses `PROMPT_COMMAND` for directory change detection
- May have slight delay in detecting directory changes
- Limited to Bash 4.4+ for full functionality

Both shells provide the same core functionality:
- Automatic project root detection
- Proper database naming and location enforcement
- Warning system for naming violations
- Manual reload and status commands

## Troubleshooting
```

## Database Architecture

### Naming Convention
- **Development**: `~/dbs/{project}_{project}_development.db`
- **Production**: `~/dbs/{project}_{project}_production.db`
- **Testing**: `$PROJECT_ROOT/tmp/todowrite_todowrite_testing.db`

### Directory Structure
- **Project Root** (`$PROJECT_ROOT`): Monorepo root containing `lib_package`, `cli_package`, `web_package`
- **Package Root** (`$PACKAGE_ROOT`): Individual package directories

### Database Usage
- **Development Database**: For collaborative planning between developers (you + Claude)
- **Production Database**: For end users deploying ToDoWrite
- **Testing Database**: Exclusively for automated tests (tests must clean up)

## Features

### Automatic Detection
- Detects when you enter a project directory
- Identifies the correct project root automatically
- Loads the appropriate development database
- Works from any subdirectory within the monorepo

### Safety Features
- Warns about incorrect database file locations
- Prevents loading production databases in test/dev areas
- Provides clear guidance for creating correct databases
- No fallback behavior between database types

### Available Commands
```bash
reload_todowrite              # Manually reload project database
show_todowrite_status         # Show current database status
cleanup_todowrite_databases    # Find database naming violations
```

## Example Usage

```bash
# Navigate to a project
cd ~/Projects/myapp

# Shell automatically loads development database
🗂️  ToDoWrite DEV DB: myapp_myapp_development.db (collaborative project: myapp)

# Use todowrite commands
todowrite list
todowrite create -l goal --title "My Goal"

# Check status
show_todowrite_status
```

## Troubleshooting

### Database Not Found
```bash
# Create development database manually
TODOWRITE_DATABASE_URL=sqlite:///$HOME/dbs/myapp_myapp_development.db todowrite create -l goal --title "Setup"

# Or use reload function
reload_todowrite
```

### Incorrect Database Files
```bash
# Find violations
cleanup_todowrite_databases

# Manual fix
mv development_todowrite.db ~/dbs/todowrite_todowrite_development.db
```

### Test Database Issues
```bash
# Use testing database explicitly (for test scripts)
TODOWRITE_DATABASE_URL=sqlite:///path/to/project/tmp/todowrite_todowrite_testing.db

# For development work
reload_todowrite  # Never use testing database for general work
```

## Architecture Details

### Priority System
1. **Testing Database**: Explicit use only (never auto-loaded for general work)
2. **Development Database**: Auto-loaded for collaborative planning
3. **Production Database**: Auto-loaded only in production areas

### Monorepo Detection
The system searches up the directory tree for the characteristic package structure:
- `lib_package/` - Core library
- `cli_package/` - Command-line interface
- `web_package/` - Web frontend

When found, it uses that directory as the project root for database naming.

### Environment Variables
- `TODOWRITE_DATABASE_URL`: Current database connection string
- Auto-set based on detected project and environment

## Migration Notes

If you were using the old database naming:
- `development_todowrite.db` → `todowrite_todowrite_development.db`
- `todowrite.db` → `todowrite_todowrite_production.db`
- Move files from project directories to `~/dbs/`

The integration script will warn you about old naming patterns and provide migration guidance.
