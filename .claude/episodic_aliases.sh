#!/bin/bash
# Episodic Memory Aliases for Quick Access
# Add to your .bashrc or .zshrc for convenience

# Set up environment
export TODOWRITE_ROOT="/Users/dderyldowney/Documents/GitHub/dderyldowney/todowrite"
export PYTHONPATH="$TODOWRITE_ROOT/lib_package/src:$TODOWRITE_ROOT/cli_package/src"

# Episodic memory shortcuts
alias em-search="source $TODOWRITE_ROOT/.venv/bin/activate && python $TODOWRITE_ROOT/.claude/episodic_memory.py --search"
alias em-stats="source $TODOWRITE_ROOT/.venv/bin/activate && python $TODOWRITE_ROOT/.claude/episodic_memory.py --stats"
alias em-index="source $TODOWRITE_ROOT/.venv/bin/activate && python $TODOWRITE_ROOT/.claude/episodic_memory.py --index"
alias em-help="source $TODOWRITE_ROOT/.venv/bin/activate && python $TODOWRITE_ROOT/.claude/episodic_memory.py --help"

# Quick search examples
alias em-postgres="em-search 'PostgreSQL'"
alias em-database="em-search 'database'"
alias em-api="em-search 'API'"
alias em-todowrite="em-search 'ToDoWrite'"