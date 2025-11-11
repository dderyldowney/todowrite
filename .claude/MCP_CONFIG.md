# ToDoWrite Project - MCP Episodic Memory Configuration

## Permanent MCP Configuration for This Project

This project is configured with permanent access to the episodic memory MCP system for **every session**.

### Available MCP Tools

1. **Search Conversations**: `mcp__plugin_episodic-memory_episodic-memory__search`
   - Semantic and text search across all conversations
   - Built-in pagination (offset/limit) to prevent heap issues
   - Date filtering capabilities

2. **Read Conversations**: `mcp__plugin_episodic-memory_episodic-memory__read`
   - Read specific conversation excerpts with pagination
   - Use `startLine` and `endLine` parameters for chunked access

3. **Remembering Conversations Skill**: `Skill(episodic-memory:remembering-conversations)`
   - **ALWAYS USE THIS SKILL** before starting any work
   - Provides perfect recall of past conversations and decisions
   - Prevents reinventing solutions and repeating mistakes

### CLI Tools Available

- **episodic-memory**: `~/.claude/plugins/cache/episodic-memory/cli/episodic-memory`
  - Commands: `search`, `index`, `show`, `stats`
- **search-conversations**: `~/.claude/plugins/cache/episodic-memory/cli/search-conversations`
  - Semantic + text search with filtering
- **index-conversations**: `~/.claude/plugins/cache/episodic-memory/cli/index-conversations`
  - Manage conversation indexing

### Usage Protocols (MANDATORY)

#### 1. Before Any Task
```bash
# ALWAYS use this skill first
Skill(episodic-memory:remembering-conversations)
```

#### 2. For Searching Past Conversations
```bash
# Use Task tool with search-conversations subagent
Task tool:
  description: "Search past conversations for [topic]"
  prompt: "Search for [specific query]. Focus on [what you need]."
  subagent_type: "search-conversations"
```

#### 3. For Reading Conversation Data
```bash
# ALWAYS use pagination parameters
mcp__plugin_episodic-memory_episodic-memory__read
  path: "path/to/conversation.jsonl"
  startLine: 100
  endLine: 200
```

### Pagination Safety Rules

1. **NEVER load entire conversation files** - always use offset/limit
2. **Maximum 50 results per search** - use `limit` parameter
3. **Use line-based pagination** for large conversations
4. **Prefer agent dispatch** over direct MCP tool access

### Environment Variables (Auto-set)

- `EPISODIC_MEMORY_PAGINATION_ENABLED=true`
- `EPISODIC_MEMORY_MAX_RESULTS=50`
- `EPISODIC_MEMORY_USE_OFFSET_LIMIT=true`

### Project Permissions

All MCP tools are permanently authorized in `.claude/settings.local.json`:
- MCP search and read tools
- Task tool for agent dispatch
- All CLI episodic memory tools
- Essential bash commands for setup

### Search-Covered Projects

- **todowrite**: Current project - hierarchical task management
- Plus 600+ other conversations across multiple projects

### Deployment Tools Configuration (MCP Indexed)

**Build System (MANDATORY):**
- hatchling ONLY (NEVER setuptools)
- Command: `uv run hatchling build` (PREFERRED & RECOMMENDED)

**Package Publishing (MANDATORY):**
- twine ONLY for PyPI/TestPyPI
- ALWAYS TestPyPI first, then production PyPI
- Commands:
  - `uv run twine upload --repository testpypi dist/*` (TestPyPI FIRST)
  - `uv run twine upload dist/*` (Production PyPI SECOND)

**GitHub Releases (MANDATORY):**
- GitHub CLI ONLY (NEVER web interface)
- Releases are for the entire codebase, not dist/* files
- Command: `gh release create v0.4.1 --title "Release v0.4.1" --notes "Release notes"`

**Documentation Reference:**
- See `docs/development/DEPLOYMENT_TOOLS.md` for complete deployment procedures

### Memory Efficiency

This configuration prevents heap issues by:
- Using agent dispatch (saves 50-100x context)
- Built-in pagination limits
- Chunked conversation reading
- Semantic search with result limits

---

**This configuration is permanent and applies to EVERY session in this project.**
