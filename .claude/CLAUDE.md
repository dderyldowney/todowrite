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

## 3. Authoritative sources have final say - MUST be consulted
- **Python**: https://python.org (official) and https://docs.python.org/3/library/typing.html (typing)
- **UV**: https://docs.astral.sh/uv (package management and environments)
- **Ruff**: https://docs.astral.sh/ruff (linting, formatting, security)
- **Bandit**: https://bandit.readthedocs.io/en/latest/ (security scanning)
- **Semantic Commits**: https://here-be-pythons.readthedocs.io/en/latest/git/semantic-commit-messages.html
- **Conventional Commits**: https://www.conventionalcommits.org/en/v1.0.0/#specification
- **Pytest**: https://docs.pytest.org/en/stable/ (testing framework)
- **TestPyPI/PyPI**: https://docs.pypi.org/ (package publishing and distribution)
- **Git**: https://git-scm.com/docs (version control operations)
- **GitHub**: https://docs.github.com/en (platform-specific operations)
- **Python Packaging**: https://packaging.python.org/en/latest/ (packaging standards and practices)
- **SQLite**: https://sqlite.org/docs.html (database operations)
- **PostgreSQL**: https://www.postgresql.org/docs/ (database operations)
- **TDD Methodology**: https://tddbuddy.com/references/tdd-cycle.html and https://www.ibm.com/think/topics/test-driven-development (preferred references)
- **NO ASSUMPTIONS**: Always verify syntax, semantics, and logic against authoritative sources
- **CODE GENERATION**: Must reference current official documentation, not memory or assumptions
- **TEST CREATION**: Must validate behavior against authoritative specifications

## 4. Test-Driven Development only (Red → Green → Refactor)
- Strict Red → Green → Refactor workflow:
  1. Write a failing test (**Red**).
  2. Implement the **minimal** code needed to pass (**Green**).
  3. Clean up with tests still passing (**Refactor**).

## 5. No code without tests FIRST
- All production code must originate from a failing test.
- No feature work or fixes happen without the test created first.

## 6. Tests must be broken down by component and subsystem
- Tests must be organized by:
  - High-level **components**
  - Lower-level **component subsystems**

## 7. Agents MUST use the token-optimization system
- Prefer local tools (`grep`, `rg`, `sed`, `awk`, `jq`, `greptool`) over long LLM reasoning.
- Reuse existing context.
- Produce small, efficient, incremental changes.

## 8. Use local command-line tools
- Prefer CLI utilities for all inspection and transformation tasks.

## 9. Simplicity over complexity
- Favor concise, direct, expressive solutions.

## 10. Code must read like natural language
- Use conversational naming.
- Clear logic and helpful docstrings.

## 11. FULL TYPE HINTING & TYPE ANNOTATIONS REQUIRED
- All code must include complete type hints:
  - Typed `self`
  - Typed parameters
  - Typed returns
  - Typed attributes
  - No implicit `Any`

## 12. Agents MUST read `AGENT_STARTUP.md` before beginning any development work
- Contains essential tooling configuration and startup checklist
- Defines UV, Ruff, Bandit, and build system requirements
- Specifies correct workflows and prohibited direct tool usage

# 13. Working Directory Boundary

- **Root Directory**: `./` refers to `/Users/dderyldowney/Documents/GitHub/dderyldowney/todowrite`
- **ALL operations must be confined within this directory structure**
- **NO operations outside the project root directory**

# 14. Monorepo Structure

```
$project_root/
├── BUILD_SYSTEM.md
├── docs/ToDoWrite.md
├── tests/
├── lib_package/
├── cli_package/
└── web_package/   # planning only
```

# 15. Tooling & Environment Rules

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
