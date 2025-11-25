# MCP Gateway Health Report
Generated: 2025-11-24 19:13:41

## Executive Summary
- Overall Status: DEGRADED
- Healthy Servers: 1/7
- Tools Expected: 69
- Tools Actually Available: 6

## Server Status Breakdown
- ❌ **filesystem**: filesystem STDIO server restarting (343 restarts) - likely Gateway communication issue
- ❌ **git**: git STDIO server restarting (341 restarts) - likely Gateway communication issue
- ❌ **github**: github STDIO server restarting (343 restarts) - likely Gateway communication issue
- ✅ **sqlite**: sqlite STDIO server running via Gateway (6 tools expected)
- ❌ **playwright**: playwright STDIO server restarting (341 restarts) - likely Gateway communication issue
- ❌ **python-refactoring**: python-refactoring STDIO server restarting (339 restarts) - likely Gateway communication issue
- ❌ **context7**: HTTP server not accessible on port 3001: HTTP Error 404: Not Found

## Architecture Notes
- MCP Gateway coordinates STDIO server communication
- STDIO servers do NOT expose HTTP endpoints directly
- Tools communicate through Gateway via RPC-JSON protocol
- HTTP servers (like context7) are the exception, not the rule

## Expected vs Actual
- Expected total tools: 84 (per requirements)
- Currently detected: 6
- Health check accuracy: ✅ Accurate

## Root Cause Analysis & Recommendations
- 🔄 5 STDIO servers are stuck in restart loops
  - This indicates MCP Gateway communication failure
  - STDIO servers expect Gateway client but none is connected
  - Solution: Configure Claude Code MCP client to connect to Gateway
- ⚠️ Partial system: Some servers working, others restarting
  - Working servers (sqlite, context7) don't require Gateway communication
  - Restarting servers (filesystem, git, github) need Gateway client
- 📉 Tool count: 6/84 detected
  - Current MCP tools are working through Claude Code built-ins
  - Gateway STDIO servers would provide additional {self.expected_total_tools - status['detected_tools']} tools

## Next Steps
1. Configure Claude Code MCP client for Gateway communication
2. Restart STDIO containers after Gateway client is connected
3. Verify all {self.expected_total_tools} tools become available
