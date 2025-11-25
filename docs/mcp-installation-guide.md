# MCP Installation Guide

## Overview

This document describes the MCP (Model Context Protocol) server installation that provides system-wide AI development tools.

## Installation Location

All MCP servers are installed globally at: `~/.mcp-servers/`

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
All servers are automatically available in Claude Code sessions.

### For Other Projects
```bash
cd /path/to/project
# Add servers as needed
claude mcp add cargo-mcp ~/.mcp-servers/cargo-mcp/target/release/cargo-mcp
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

- **Total Servers**: 16 MCP servers
- **Working**: 15/16 servers (agentmode has asyncio compatibility issues)
- **System-wide**: Available to all projects
- **ENFORCED**: AI-Lint for code quality

## Maintenance

- All MCP servers stay running as system resources
- mcp-postgres container never stops (shared system resource)
- API keys managed through environment variables
- Updates available through individual package managers