# Autorun Skill

**Author:** HAL System
**Category:** System Initialization
**Tags:** startup, environment, mandatory, enforcement

## Description

Automatically executes the mandatory startup sequence when Claude loads this skill. Ensures all environment variables are configured, CLAUDE.md rules are enforced, HAL Agent System is initialized, and all mandatory startup procedures are executed.

## How It Works

This skill integrates directly with Claude's native Skill system to provide automatic session initialization without depending on hook execution chains.

### Features

- 🚀 **Automatic Environment Loading** - Sources all environment variables from .env
- 🔧 **Virtual Environment Activation** - Ensures proper Python path configuration
- ⚡ **HAL Agent System Initialization** - Activates enforcement and optimization systems
- 🗄️ **PostgreSQL Backend Verification** - Confirms database connectivity
- 📋 **Session State Management** - Loads and restores previous session context
- 🛡️ **Development Mandates Enforcement** - Applies all project rules and requirements

## Usage

```bash
/skill autorun
```

**Automatic Execution:** This skill is designed to run automatically when loaded by the Skill tool, providing seamless session initialization.

## Dependencies

- `.claude/startup.sh` - Mandatory startup sequence script
- `.claude/hooks/session_initialization.py` - Session management system
- PostgreSQL container `mcp-postgres` running on port 5433
- Virtual environment with required dependencies

## Integration Notes

Replaces the previous hook-based autorun system with Claude's native Skill integration for more reliable automatic execution.

## Files Modified

- Creates session markers and enforcement configurations
- Updates agent registry and workflow enforcement
- Activates comprehensive code quality systems

---

*This skill is part of the HAL Agent System's mandatory development workflow enforcement.*
