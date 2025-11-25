# MCP Usage Guide

## Overview

This document describes how to USE the GLOBAL MCP (Model Context Protocol) server infrastructure that provides system-wide AI development tools.

**🔴 CRITICAL**: These MCP servers are GLOBAL system infrastructure, NOT part of this specific todowrite project.

## Architecture Principle

**ALL MCP servers are GLOBAL system resources:**
- ✅ Used by ALL projects on this machine
- ✅ Stay running continuously
- ✅ Restart only when they break
- ✅ Never project-specific
- ✅ Both HTTP and STDIO servers are global infrastructure

## Installation Location

All MCP servers are installed globally at: `~/.mcp-servers/` (OUTSIDE any project repository)

## Installed Servers

### Docker MCP Gateway (7 servers)
- context7 - Up-to-date code documentation
- filesystem - Local filesystem access
- git - Git repository operations
- github-official - GitHub API integration
- mcp-python-refactoring - Python code refactoring
- playwright - Web automation
- sqlite - SQLite database operations

### Claude Code Integration (9 servers)
- cargo-mcp - Rust Cargo integration
- crates-mcp - Rust crate discovery
- rust-docs - Rust documentation from docs.rs
- chrome-devtools - Chrome DevTools Protocol
- kaggle-mcp - Kaggle datasets and competitions
- circleci-mcp-server - CircleCI CI/CD integration
- ai-pair-programmer - AI-powered pair programming
- agentic-control-framework - Task automation framework
- agentmode - Database queries (PostgreSQL)

## Configuration

### API Keys
All API keys are loaded from `~/.env`:
- CONTEXT7_API_KEY
- CIRCLECI_TOKEN
- OPENROUTER_API_KEY
- KAGGLE_API_TOKEN

### Database Access
- PostgreSQL: `postgresql://mcp_user:mcp_secure_password_2024@localhost:5433`
- System databases: mcp_episodic_memory, mcp_sessions, mcp_filesystem, mcp_main

## Usage

### For Claude Code
All GLOBAL MCP servers are automatically available in Claude Code sessions. No configuration needed.

### For Other Projects
All projects automatically have access to ALL GLOBAL MCP servers. No installation required.

**Usage Example:**
```bash
# Any project can immediately use MCP services
cd /path/to/any/project
# All MCP tools are available instantly
```

### Database Pattern (Industry Standard)
Each project creates its own database in the shared PostgreSQL engine:
```bash
docker exec mcp-postgres psql -U mcp_user -c "CREATE DATABASE your_project;"
```

## Documentation

Complete documentation available at:
- `~/.mcp-servers/FINAL_INSTALLATION_REPORT.md`
- `~/.mcp-servers/AVAILABLE_TOOLS.md`
- `~/.mcp-servers/CLAUDE_CODE_INTEGRATION.md`

## Status

- **Total Servers**: 16 GLOBAL MCP servers
- **Working**: 16/16 servers ✅ (all issues resolved)
- **System-wide**: Available to ALL projects
- **ENFORCED**: AI-Lint for code quality

## Maintenance Policy

- **ALL MCP servers**: Stay running as GLOBAL system resources
- **mcp-postgres container**: NEVER stops (shared by ALL projects on this machine)
- **Restart policy**: Only restart/troubleshoot when servers break
- **API keys**: Managed through environment variables
- **Updates**: Available through individual package managers
- **No project-specific maintenance**: All servers are shared infrastructure