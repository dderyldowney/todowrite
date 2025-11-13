# CLAUDE.md

This file defines **non-negotiable, permanent rules** for Claude and all agents working in this repository.  
These mandates apply **at all times** with **zero exceptions**.

---

# Core Mandates (Must ALWAYS Be Followed)

## 1. No mocking allowed, ever
- No mocks, stubs, fakes, or any test double.
- Tests must use real implementations or real in-memory components shared with production.

## 2. Test-Driven Development only (Red → Green → Refactor)
- Strict Red → Green → Refactor workflow:
  1. Write a failing test (**Red**).
  2. Implement the **minimal** code needed to pass (**Green**).
  3. Clean up with tests still passing (**Refactor**).

## 3. No code without tests FIRST
- All production code must originate from a failing test.
- No feature work or fixes happen without the test created first.

## 4. Tests must be broken down by component and subsystem
- Tests must be organized by:
  - High-level **components**
  - Lower-level **component subsystems**

## 5. Agents MUST use the token-optimization system
- Prefer local tools (`grep`, `rg`, `sed`, `awk`, `jq`, `greptool`) over long LLM reasoning.
- Reuse existing context.
- Produce small, efficient, incremental changes.

## 6. Use local command-line tools
- Prefer CLI utilities for all inspection and transformation tasks.

## 7. Simplicity over complexity
- Favor concise, direct, expressive solutions.

## 8. Code must read like natural language
- Use conversational naming.
- Clear logic and helpful docstrings.

## 9. FULL TYPE HINTING & TYPE ANNOTATIONS REQUIRED
- All code must include complete type hints:
  - Typed `self`
  - Typed parameters
  - Typed returns
  - Typed attributes
  - No implicit `Any`

## 10. Agents MUST read and load `docs/ToDoWrite.md`

# 11. Monorepo Structure

```
$project_root/
├── BUILD_SYSTEM.md
├── docs/ToDoWrite.md
├── tests/
├── lib_package/
├── cli_package/
└── web_package/   # planning only
```

# 12. Tooling & Environment Rules

- `uv` for environments
- `ruff` for formatting, linting, basic security
- **NO mypy**
- `bandit` for security scanning
- `hatchling` for builds
- `twine` for PyPI uploads

# Standard Workflow
1. Clarify request & load ToDoWrite
2. Search using CLI tools
3. Red test
4. Green minimal code with full typing
5. Refactor
6. Commit (never using --no-verify without permission)

# Conflict Resolution
- Identify the violated rule
- Propose an alternative
- Execute only once aligned
