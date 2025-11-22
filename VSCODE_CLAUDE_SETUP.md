# VSCode Claude Code Integration Setup

This guide explains how to set up automatic CLAUDE.md loading and token optimization in VSCode.

## **Current Limitations**

The VSCode Claude Code extension (currently in beta) does **not** automatically load CLAUDE.md files like the CLI version does. However, we can work around this with VSCode tasks and settings.

## **Setup Instructions**

### **1. Automatic Token Optimization (✅ Complete)**

The following VSCode configuration has been added:

**Terminal Environment Variables:**
- `CLAUDE_MAX_TOKENS=40000`
- `HAL_PREPROCESSING_MANDATORY=true`
- `CLI_TOOLS_MANDATORY=true`
- `PYTHONPATH=lib_package/src:cli_package/src`

**Auto-Run Tasks:**
- Apply token optimization when folder opens
- Restore session state automatically
- Verify optimization status

### **2. Manual CLAUDE.md Application**

Since VSCode extension doesn't auto-load CLAUDE.md, use one of these methods:

#### **Method A: VSCode Tasks (Recommended)**
1. Open Command Palette: `Cmd/Ctrl + Shift + P`
2. Type: `Tasks: Run Task`
3. Select: `Claude: Apply CLAUDE.md Configuration`
4. Select: `Claude: Restore Session State`

#### **Method B: Integrated Terminal (Full CLI Support)**
```bash
# In VSCode integrated terminal:
source .claude/optimization_env.sh
# This gives you full CLI functionality with CLAUDE.md processing
```

#### **Method C: Launch Configuration**
1. Open Command Palette: `Cmd/Ctrl + Shift + P`
2. Type: `Debug: Open Launch.json`
3. Select: `Claude: Load CLAUDE.md Environment`
4. Press F5 to run

### **3. WebSearch Permissions**

**To enable WebSearch in VSCode Claude Code extension:**

#### **Option 1: VSCode Extension Settings**
1. VSCode → Settings → Extensions → Claude Code
2. Look for "WebSearch" or "Internet Access" permissions
3. Enable if available

#### **Option 2: Claude Account Settings**
1. Go to https://claude.com/account
2. Enable web search capabilities
3. Re-authenticate VSCode extension

#### **Option 3: Use CLI with WebSearch**
```bash
# In VSCode integrated terminal:
claude --web-search "your query here"
```

## **What Works Automatically**

✅ **Token Optimization**: 40000 tokens, HAL preprocessing, CLI tools enforced
✅ **Environment Setup**: PYTHONPATH, virtual environment activation
✅ **Package Detection**: Adaptive limits for lib/cli/web packages
✅ **Session Tasks**: VSCode tasks for manual CLAUDE.md loading

## **What Requires Manual Action**

⚠️ **CLAUDE.md Loading**: Must run tasks or use CLI terminal
⚠️ **WebSearch**: Extension permissions need to be configured
⚠️ **Session Restoration**: Manual via VSCode tasks

## **Best Practice Workflow**

1. **Open ToDoWrite in VSCode** → Terminal environment auto-configured
2. **Run VSCode Task** → `Claude: Apply CLAUDE.md Configuration`
3. **Run VSCode Task** → `Claude: Restore Session State`
4. **Use Claude in VSCode** → Full token optimization active
5. **For WebSearch** → Use CLI terminal or enable extension permissions

## **Files Added**

- `.vscode/tasks.json` - Auto-run tasks for CLAUDE.md loading
- `.vscode/settings.json` - Environment variables and optimization settings
- `.vscode/launch.json` - Debug configuration for session loading
- `.claude/optimization_env.sh` - Environment loader (already exists)
- `.claude/auto_optimization_hook.sh` - Shell integration (already exists)

## **Alternative: Use CLI in VSCode**

For the most seamless experience:
1. Use VSCode integrated terminal
2. Run: `claude` (CLI version)
3. Gets full CLAUDE.md processing + web search + all optimizations

This approach gives you 100% of the functionality while still using VSCode as your editor.