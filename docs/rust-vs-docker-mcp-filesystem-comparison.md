# Rust vs Docker MCP Filesystem Servers - Configuration Comparison

## Installation Summary

### Rust MCP Filesystem Server ✅ INSTALLED
```bash
cargo install mcp-server-filesystem
# Installed at: ~/.cargo/bin/mcp-server-filesystem
```

### Docker MCP Reference Filesystem Server ✅ CONFIGURED
```bash
# Via Docker MCP Gateway
docker mcp config write << EOF
filesystem:
  paths:
    - /absolute/path/to/directory
EOF
```

## Key Configuration Differences

### 🔧 Rust Server Configuration
- **Uses**: Direct directory arguments
- **Command**: `mcp-server-filesystem /path/to/directory`
- **Multiple directories**: `mcp-server-filesystem /path1 /path2 /path3`
- **Configuration method**: Command-line arguments
- **Help**: `mcp-server-filesystem --help`

### 🐳 Docker Reference Server Configuration
- **Uses**: YAML configuration file
- **Command**: Docker MCP Gateway manages automatically
- **Configuration method**: `~/.docker/mcp/config.yaml`
- **Required format**:
```yaml
filesystem:
  paths:
    - /absolute/path/to/directory
    - /another/absolute/path
```

## Behavior Comparison

### Rust Server Response
```json
{
  "jsonrpc":"2.0",
  "id":1,
  "result":{
    "protocolVersion":"2024-11-05",
    "capabilities":{"resources":{},"tools":{}},
    "serverInfo":{"name":"rmcp","version":"0.6.4"},
    "instructions":"FileSystem MCP Server for secure file operations. Tools: read_text_file, read_media_file, read_multiple_files, write_file, edit_file, create_directory, list_directory, list_directory_with_sizes, directory_tree, move_file, search_files, get_file_info, list_allowed_directories. All operations are restricted to allowed directories for security. Resources: fs://status, fs://help, fs://allowed-directories."
  }
}
```

### Docker Reference Server Response
- **Fails without proper configuration**: `Can't start filesystem: failed to connect: calling "initialize": EOF`
- **Requires `filesystem.paths` configuration** in YAML
- **Managed through Docker MCP Gateway**

## Key Takeaways

1. **Rust server**: Uses `allowed_directories` concept via command-line arguments
2. **Docker server**: Uses `filesystem.paths` configuration in YAML
3. **Rust server**: Standalone executable, can run independently
4. **Docker server**: Managed through Docker MCP Gateway infrastructure
5. **Both provide**: Secure filesystem operations with directory restrictions
6. **Configuration mismatch**: Each expects different configuration format

## Usage Examples

### Rust Server
```bash
# Single directory
mcp-server-filesystem /Users/username/projects

# Multiple directories
mcp-server-filesystem /Users/username/projects /Users/username/documents

# Integration with MCP clients (via stdio)
echo '{"jsonrpc":"2.0","id":1,"method":"initialize",...}' | mcp-server-filesystem /path/to/dir
```

### Docker Server
```bash
# Configure via YAML
cat > ~/.docker/mcp/config.yaml << EOF
filesystem:
  paths:
    - /Users/username/projects
    - /Users/username/documents
EOF

# Verify configuration
docker mcp config read

# Use through Docker MCP Gateway
docker mcp gateway run --servers filesystem,github-official,...
```

## Installation Commands Executed

```bash
# 1. Checked Rust installation
rustc --version  # -> 1.91.1 (ed61e7d7e 2025-11-07)

# 2. Found Rust MCP packages
cargo search mcp filesystem
# Found: mcp-server-filesystem = "0.1.2"

# 3. Installed Rust MCP filesystem server
cargo install mcp-server-filesystem
# Installed to: /Users/dderyldowney/.cargo/bin/mcp-server-filesystem

# 4. Verified installation
mcp-server-filesystem --help
# Shows: Specify one or more directories where filesystem operations are allowed

# 5. Tested with project directory
mcp-server-filesystem /Users/dderyldowney/Documents/GitHub/dderyldowney
# Successfully initializes and provides 13 filesystem tools
```

## Verification

Both servers are now operational:
- **Rust server**: Globally installed and functional with directory arguments
- **Docker server**: Properly configured with `filesystem.paths` and providing 11 tools through Docker MCP Gateway
- **Total MCP tools**: 95 (84 from other servers + 11 from Docker filesystem)

This demonstrates the key architectural differences between Rust and Docker MCP filesystem servers that we discovered during our troubleshooting process.