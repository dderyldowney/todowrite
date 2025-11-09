# Development Tools

This directory contains development utilities and tools that are not part of the main ToDoWrite packages but are used during development.

## Structure

```
dev_tools/
├── README.md                    # This file
├── token_optimization/          # Token optimization tools
│   ├── __init__.py
│   ├── always_token_sage.py
│   ├── auto_agent.py
│   ├── token_optimized_agent.py
│   ├── CLAUDE_WORKFLOW.py
│   └── *.md                     # Documentation files
└── agent_controls/              # Agent control and management tools
    ├── __init__.py
    ├── hal_agent_loop.py
    ├── hal_token_savvy_agent.py
    ├── always_token_sage.py
    ├── auto_agent.py
    ├── CLAUDE_WORKFLOW.py
    ├── claude_auto_setup.sh
    └── *.md                     # Documentation files
```

## Running Tools

### Method 1: Using the Shell Wrapper

```bash
# List available tools
./run_token_tools.sh list

# Run a token optimization tool
./run_token_tools.sh token_optimized_agent [args]

# Run an agent control tool
./run_token_tools.sh hal_agent_loop [args]

# Get help
./run_token_tools.sh help
```

### Method 2: Using the Python Wrapper

```bash
# List available tools
python3 dev_tools_runner.py list

# Run a token optimization tool
python3 dev_tools_runner.py token_optimized_agent [args]

# Run an agent control tool
python3 dev_tools_runner.py hal_agent_loop [args]
```

### Method 3: Direct Python Import

```python
import sys
sys.path.insert(0, 'dev_tools')

# Import and run token optimization tools
from token_optimization import token_optimized_agent
result = token_optimized_agent.main()

# Import and run agent control tools
from agent_controls import hal_token_savvy_agent
result = hal_token_savvy_agent.filter_repo_for_llm()
```

## Token Optimization Tools

### `always_token_sage.py`
Always uses token-sage optimization for maximum token efficiency when processing large codebases.

### `auto_agent.py`
Automatic token-optimized agent pipeline that combines token-sage and HAL agents.

### `token_optimized_agent.py`
Advanced token optimization with filtering and caching capabilities.

## Agent Control Tools

### `hal_agent_loop.py`
HAL (Hierarchical Agent Logic) agent loop for autonomous agent management.

### `hal_token_savvy_agent.py`
HAL agent with token-aware processing and optimization.

## Backward Compatibility

The project root includes wrapper scripts that maintain backward compatibility with the original tool locations:

- `run_token_tools.sh` - Shell script wrapper
- `dev_tools_runner.py` - Python script wrapper

These allow you to use the tools just as you did before the reorganization.

## Notes

- These tools are **development-only** and not included in the distributed packages
- All tools maintain their original functionality after the reorganization
- The `dev_tools` directory is not part of the main package structure
- Import paths have been updated to work with the new structure
