# Post-Clear Enforcement Restoration

Restores full ToDoWrite enforcement systems after a `/clear` command.

## Usage

Run this command to restore all enforcement systems:

```bash
python .claude/restore_enforcement.py
```

## What It Does

1. **Session Initialization** - Reactivates session markers and agent registry
2. **Permanent Enforcement** - Activates all quality gates and compliance systems
3. **Episodic Memory** - Restores project-specific episodic memory database connection

## When to Use

Use this command if you notice any of the following after `/clear`:
- Missing enforcement messages
- No quality gate activations
- Episodic memory not responding
- Missing system status messages

## Manual Alternative

You can also run the components individually:

```bash
# Session initialization
python .claude/hooks/session_initialization.py

# Permanent enforcement
python .claude/autorun.py

# Episodic memory
python .claude/hooks/session_startup_episodic_memory.py
```

## Verification

After restoration, you should see:
- 🔒 Permanent enforcement activation message
- ✅ All quality gates marked as ENFORCED
- 🧠 Episodic memory ready confirmation
- 📋 Compliance system status

## Troubleshooting

If restoration fails:
1. Check that virtual environment is active
2. Verify `.claude/` directory exists and is writable
3. Ensure all required scripts are present
4. Run `./dev_tools/ensure_episodic_memory.sh` if needed
