# ToDoWrite AI CLI Startup Guide

To ensure all CLAUDE.md rules are properly loaded and enforced when starting the AI CLI, use the following startup methods:

## Recommended Startup Method

**FORGET ABOUT MANUAL VENV ACTIVATION!** The script does it automatically.

Use the provided startup script instead of directly calling `claude .` or `uv run claude .`:

```bash
# From the ToDoWrite project root directory:
./start-ai-cli.sh .

# NO NEED to run: source .venv/bin/activate  (script does this automatically!)
```

## Alternative: Manual Startup

If you prefer to start manually, follow these steps in order:

```bash
# 1. Activate virtual environment (MANDATORY)
source .venv/bin/activate

# 2. Set required environment variables (MANDATORY)
export TODOWRITE_DATABASE_URL="sqlite:///$HOME/dbs/todowrite_development.db"
export PYTHONPATH="$PWD/lib_package/src:$PWD/cli_package/src"
export EPISODIC_MEMORY_DB_PATH="$(pwd)/.claude/episodic_memory.db"

# 3. Run CLAUDE.md rule enforcement (MANDATORY)
python .claude/startup_enforcement.py

# 4. Initialize episodic memory (MANDATORY)
./dev_tools/ensure_episodic_memory.sh

# 5. Initialize ToDoWrite Models API (MANDATORY)
python .claude/auto_init_todowrite_models.py

# 6. Start AI CLI
claude .
```

## What the Startup Script Does

The startup script (`./start-ai-cli.sh`) automatically enforces all CLAUDE.md rules:

1. **Directory Verification**: Ensures you're in the ToDoWrite project root
2. **🔄 AUTOMATIC Virtual Environment**:
   - Creates `.venv` if it doesn't exist (runs `uv sync`)
   - **ALWAYS activates virtual environment automatically**
   - **NO manual `source .venv/bin/activate` needed EVER!**
3. **Environment Variables**: Sets all required variables:
   - `TODOWRITE_DATABASE_URL`: Points to `$HOME/dbs/todowrite_development.db`
   - `PYTHONPATH`: Includes lib and cli package sources
   - `EPISODIC_MEMORY_DB_PATH`: Project-specific episodic memory
4. **Database Verification**: Checks that the development database exists
5. **Rule Enforcement**: Runs `.claude/startup_enforcement.py` to verify all CLAUDE.md rules
6. **Episodic Memory**: Initializes episodic memory system (MCP)
7. **HAL Agent Dependencies**: Installs and verifies HAL Agent system
8. **ToDoWrite Models API**: Initializes the Rails ActiveRecord API
9. **HAL Agent System**: Verifies local preprocessing (0 API tokens)
10. **Token Optimization**: Verifies 90% token savings system
11. **MCP Systems**: Verifies Model Context Protocol plugins
12. **Anthropic Configuration**: Checks API keys for HAL Agent
13. **Claude Code Start**: Launches the AI CLI with ALL systems enforced

## Verification Checklist

Before starting any work, the system verifies:

- ✅ Virtual environment is active
- ✅ Database URL is correctly configured
- ✅ Database contains required planning structure
- ✅ All CLAUDE.md mandates are satisfied
- ✅ Episodic memory is initialized
- ✅ ToDoWrite Models API is ready
- ✅ No absolute hardcoded paths are used

## Troubleshooting

### If startup enforcement fails:
```
❌ CLAUDE.md RULE VIOLATIONS DETECTED
```
- Follow the specific fix instructions provided
- Most common issues: missing venv activation or incorrect database location

### If database not found:
```
⚠️ Development database not found at $HOME/dbs/todowrite_development.db
```
- Run: `python .claude/auto_init_todowrite_models.py`

### If episodic memory fails:
```
⚠️ Episodic memory initialization script not found
```
- Ensure `.claude/episodic_memory` directory exists
- Check that EPISODIC_MEMORY_DB_PATH is set correctly

## Why This Startup Method is Required

The AI CLI enforcement system cannot work reliably if:
- Virtual environment isn't active (missing dependencies)
- Database URL is incorrect (wrong database location)
- CLAUDE.md rules aren't loaded (bypassable mandates)
- Episodic memory isn't initialized (no conversation memory)
- HAL Agent System isn't ready (no local preprocessing)
- Token Optimization isn't active (wasted API tokens)
- MCP Systems aren't connected (no plugin support)
- Anthropic API isn't configured (HAL Agent can't function)
- ToDoWrite Models API isn't ready (cannot track work)

The startup script ensures **ALL** these prerequisites are met before allowing any AI work to proceed, and enforces the same verification across `/clear` commands.

## Quick Start Commands

```bash
# Make script executable (one-time setup)
chmod +x start-ai-cli.sh

# 🎯 THE ONLY COMMAND YOU NEED TO REMEMBER:
./start-ai-cli.sh .

# That's it! NO manual venv activation needed - EVER!

# Start AI CLI with specific file
./start-ai-cli.sh path/to/file.py

# Start AI CLI with directory
./start-ai-cli.sh src/
```

## For Users Who Forget to Activate Venv (That's You!)

**Stop worrying about virtual environment activation!** The startup script handles it automatically:

- ❌ **OLD WAY (forgetful)**: Remember to run `source .venv/bin/activate` first
- ✅ **NEW WAY (foolproof)**: Just run `./start-ai-cli.sh .` - script handles everything

The script will:
1. Check if `.venv` exists, create it with `uv sync` if needed
2. **Automatically activate the virtual environment**
3. Verify activation worked
4. Continue with all other setup steps

**You can literally forget about virtual environment activation forever.** The script won't let you proceed without it being active.

This ensures every AI session starts with all CLAUDE.md rules properly loaded and enforced, with zero chance of forgetting the virtual environment.
