# Startup Sequence Policy

> **Manual startup is required for each session since Claude Code CLI does not have automatic startup capabilities.**

## Mandatory Manual Startup Sequence

**Before starting any work, manually run:**
```bash
./.claude/startup.sh
```

### Startup Sequence Components

This manual startup sequence executes:
- ✅ Load all environment variables from .env.dev
- ✅ Activate virtual environment and set PYTHONPATH
- ✅ Load and enforce CLAUDE.md rules
- ✅ Initialize HAL Agent System (token-savvy preprocessing)
- ✅ Activate Token Optimization System (always_token_sage)
- ✅ Initialize MCP Systems (81 tools across 7 servers)
- ✅ Verify MCP server health and connectivity
- ✅ Verify PostgreSQL backend connectivity
- ✅ Load session state from database
- ✅ Enforce TDD compliance and all development mandates
- ✅ Enforce MCP-First workflow

**DO NOT START ANY WORK until startup sequence completes successfully!**

## Prerequisites

- PostgreSQL container `todowrite-postgres` must be running
- All environment variables in `.env.dev` must be set
- Virtual environment must be available
- MCP servers should be running (system-wide resources)

## Verification Commands

```bash
# Quick health check
bash .claude/quick_check.sh

# Verify MCP servers
python .claude/mcp_server_health_check.py

# Check session state
python .claude/session_manager.py --summary
```

## Troubleshooting

If startup fails:
1. Check PostgreSQL container: `docker ps | grep todowrite-postgres`
2. Verify environment variables: `source .env.dev`
3. Check MCP servers: `docker mcp server ls`
4. Consult enforcement logs in startup output
