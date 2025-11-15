# CLAUDE.md

This file defines **non-negotiable, permanent rules** for Claude and all agents working in this repository.
These mandates apply **at all times** with **zero exceptions**.

---

# Core Mandates (Must ALWAYS Be Followed)

## 1. No mocking allowed, ever
- No mocks, stubs, fakes, or any test double.
- Tests must use real implementations or real in-memory components shared with production.

## 2. Agents MUST read and load documentation files IN ORDER on startup and across '/clear'
- **FIRST**: Read `.claude/CLAUDE.md` (this file)
- **SECOND**: Read `docs/ToDoWrite.md` to understand project structure
- **THIRD**: Read `BUILD_SYSTEM.md` to understand build requirements
- **NO EXCEPTIONS**: This applies to ALL agents at ALL times
- **NO BYPASSING**: Documentation loading is a prerequisite for ALL other work
- **AFTER '/clear'**: Immediately re-load all three files IN ORDER before any other work
- **AFTER '/quit'**: Re-load all three files IN ORDER in new session before any other work

## 3. Test-Driven Development only (Red → Green → Refactor)
- Strict Red → Green → Refactor workflow:
  1. Write a failing test (**Red**).
  2. Implement the **minimal** code needed to pass (**Green**).
  3. Clean up with tests still passing (**Refactor**).

## 4. No code without tests FIRST
- All production code must originate from a failing test.
- No feature work or fixes happen without the test created first.

## 5. Tests must be broken down by component and subsystem
- Tests must be organized by:
  - High-level **components**
  - Lower-level **component subsystems**

## 6. Agents MUST use the token-optimization system
- Prefer local tools (`grep`, `rg`, `sed`, `awk`, `jq`, `greptool`) over long LLM reasoning.
- Reuse existing context.
- Produce small, efficient, incremental changes.

## 7. Use local command-line tools
- Prefer CLI utilities for all inspection and transformation tasks.

## 8. Simplicity over complexity
- Favor concise, direct, expressive solutions.

## 9. Code must read like natural language
- Use conversational naming.
- Clear logic and helpful docstrings.

## 10. FULL TYPE HINTING & TYPE ANNOTATIONS REQUIRED
- All code must include complete type hints:
  - Typed `self`
  - Typed parameters
  - Typed returns
  - Typed attributes
  - No implicit `Any`

## 11. Agents MUST read `AGENT_STARTUP.md` before beginning any development work
- Contains essential tooling configuration and startup checklist
- Defines UV, Ruff, Bandit, and build system requirements
- Specifies correct workflows and prohibited direct tool usage

# 11. Working Directory Boundary

- **Root Directory**: `./` refers to `/Users/dderyldowney/Documents/GitHub/dderyldowney/todowrite`
- **ALL operations must be confined within this directory structure**
- **NO operations outside the project root directory**

# 12. Monorepo Structure

```
$project_root/
├── BUILD_SYSTEM.md
├── docs/ToDoWrite.md
├── tests/
├── lib_package/
├── cli_package/
└── web_package/   # planning only
```

# 13. Tooling & Environment Rules

- `uv` for environments
- `ruff` for formatting, linting, basic security
- **NO mypy**
- `bandit` for security scanning
- `hatchling` for builds
- `twine` for PyPI uploads

# Standard Workflow
1. **MANDATORY**: Load documentation files IN ORDER (CLAUDE.md → ToDoWrite.md → BUILD_SYSTEM.md)
   - **On session start**: Load before any other work
   - **After '/clear'**: Immediately reload before any other work
   - **After '/quit'**: Load in new session before any other work
2. Clarify request & verify understanding from loaded docs
3. Search using CLI tools
4. Red test
5. Green minimal code with full typing
6. Refactor
7. Commit (never using --no-verify without permission)

# Emergency Documentation Verification
**If agent appears to have lost context after '/clear' or '/quit':**
1. IMMEDIATELY command: "Re-read CLAUDE.md, ToDoWrite.md, and BUILD_SYSTEM.md IN ORDER"
2. Verify compliance by asking: "Confirm you have loaded all three documentation files"
3. Do not proceed with any work until compliance is confirmed

# Conflict Resolution
- Identify the violated rule
- Propose an alternative
- Execute only once aligned
