# mcp-filesystem-solution

You are Claude Code CLI.

I am pasting in prior research and a working diagnosis from another assistant (ChatGPT) about a Docker MCP Filesystem configuration issue. Use this as context and continue from it if I ask follow-up questions. You don’t need to re-discover this from scratch unless I explicitly ask you to.

──────────────────────────────── CONTEXT START ────────────────────────────────

## User’s Original Problem

I am having a problem configuring the docker mcp-filesystem MCP server. It keeps returning:

```
- Running mcp/filesystem with [run --rm -i --init --security-opt no-new-privileges --cpus 1 --memory 2Gb --pull never -l
docker-mcp=true -l docker-mcp-tool-type=mcp -l docker-mcp-name=filesystem -l docker-mcp-transport=stdio --network none] and command
[]
  > Can't start filesystem: failed to connect: calling "initialize": EOF
```

It expects a directory argument for `allowed_directories` which is being passed.
But the Docker MCP Gateway toolkit and CLI are not properly passing that information to the mcp-filesystem MCP server.

I want an authoritative, docs- and troubleshooting-verified solution.

──────────────────────────── CHATGPT REASONING + SOLUTION ─────────────────────

## Root Cause Summary

- The Docker MCP **Filesystem (Reference)** server does **not** use `allowed_directories`.
- The Docker MCP Gateway only reads configuration under:

```
filesystem:
  paths:
    - <absolute paths>
```

- If `filesystem.paths` is missing or empty, the filesystem server starts with *zero allowed roots*.
- Because of that, `mcp/filesystem` fails during initialization and returns:

```
Can't start filesystem: failed to connect: calling "initialize": EOF
```

- The key `allowed_directories` belongs to *other* filesystem MCP servers, including some Rust-based ones, and **is ignored by Docker's reference server**.

Thus, your gateway is launching the container without any allowed paths, causing the server to exit immediately during the `initialize` RPC.

────────────────────────────── PRACTICAL FIX (DOCKER) ─────────────────────────

## OPTION A — Using Docker Desktop UI

1. Open **Docker Desktop**.
2. Go to **MCP Toolkit → Catalog**.
3. Find **Filesystem (Reference)** and ensure it is enabled.
4. Open the **Configuration** tab.
5. Add allowed directories under `filesystem.paths`:

```
filesystem:
  paths:
    - /Users/<your-user>/Projects
    - /Users/<your-user>/GitHub
    - /absolute/path/to/any/location
```

6. Save.
7. Restart the Filesystem MCP server (Stop → Start or Restart).

This ensures the gateway passes the correct initialization arguments.

## OPTION B — Using Docker MCP CLI

Run:

```bash
cat << 'EOF' | docker mcp config write
filesystem:
  paths:
    - /absolute/path/to/your/project
    - /another/absolute/path
EOF
```

Verify:

```bash
docker mcp config read
```

You should see:

```
filesystem:
  paths:
    - /absolute/path/to/your/project
    - /another/absolute/path
```

Restart the server:

```bash
docker mcp server reset filesystem
docker mcp server enable filesystem
```

───────────────────────────── KEY TAKEAWAY FOR FUTURE ─────────────────────────

- Docker’s reference `mcp/filesystem` server only respects:

```
filesystem:
  paths:
    - <absolute paths>
```

- If `paths` is missing or empty, initialization fails with EOF.
- `allowed_directories` is **not** used by Docker’s reference image.

──────────────────────────────── CONTEXT END ───────────────────────────────────

Use this context as prior research. If I ask you to:
- verify my current `docker mcp config read` output
- generate updated YAML
- or help script the setup

continue from this understanding rather than re-deriving it.
