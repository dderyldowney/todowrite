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
- **Python**: https://python.org (official), https://docs.python.org/3/library/typing.html (typing), and https://docs.python.org/3/library/asyncio.html (async programming)
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
- **SQLite3**: https://docs.python.org/3/library/sqlite3.html and https://sqlite.org/docs.html (database operations)
- **PostgreSQL**: https://www.postgresql.org/docs/current/ (database operations)
- **YAML**: https://yaml.org/spec/1.2.2/ (data serialization format)
- **Hatchling**: https://pypi.org/project/hatchling/ (build system - see Documentation links)
- **Twine**: https://twine-bhrutledge.readthedocs.io/en/stable/ (PyPI publishing tool)
- **TDD Methodology**: https://tddbuddy.com/references/tdd-cycle.html and https://www.ibm.com/think/topics/test-driven-development (preferred references)
- **NO ASSUMPTIONS**: Always verify syntax, semantics, and logic against authoritative sources
- **CODE GENERATION**: Must reference current official documentation, not memory or assumptions
- **TEST CREATION**: Must validate behavior against authoritative specifications

## 4. NEVER fake code - write REAL implementations only
- **NEVER** use 'pass', '...', 'raise NotImplementedError', or placeholder code
- **NEVER** write fake implementations just to pass tests
- **ALWAYS** write actual, functional implementation code when writing code
- **NO TRICKS**: No clever hacks, workarounds, or test-cheating techniques
- **REAL BEHAVIOR**: Code must actually do what it's supposed to do
- **PROPER FUNCTIONALITY**: Implementation must solve the real problem, not just satisfy test assertions

## 5. ALWAYS test actual implementation - REAL testing only
- **ALWAYS** test the actual implementation, not fake/test doubles
- **REAL INTERACTIONS**: Tests must exercise real functionality
- **NO MOCKING**: This rule reinforces Rule #1 - no mocking of any kind
- **INTEGRATION FOCUS**: Test how components actually work together
- **VERIFIABLE BEHAVIOR**: Tests must verify real, observable behavior
- **END-TO-END VALIDATION**: Prefer testing complete workflows over isolated pieces

## 6. Test-Driven Development only (Red → Green → Refactor)
- Strict Red → Green → Refactor workflow:
  1. Write a failing test (**Red**).
  2. Implement the **minimal** code needed to pass (**Green**).
  3. Clean up with tests still passing (**Refactor**).

## 7. No code without tests FIRST
- All production code must originate from a failing test.
- No feature work or fixes happen without the test created first.

## 8. Tests must be broken down by component and subsystem - SoC REQUIRED
- **SEPARATION OF CONCERNS**: SoC in both code AND tests is preferred
- **COMPONENT ORGANIZATION**: Tests must be organized by high-level components
- **SUBSYSTEM BREAKDOWN**: Each component's tests must be divided into subsystem tests
- **NO MONOLITHIC FILES**: Never attempt to put all tests into a single file
- **LOGICAL GROUPING**: Group related functionality tests together
- **CLEAR BOUNDARIES**: Each test file should have a single, clear responsibility
- **COMPONENT-FIRST**: Structure tests to mirror the component architecture
- **SUBSYSTEM-SPECIFIC**: Create focused test files for each subsystem within components
- **MAINTAINABILITY**: Smaller, focused test files are easier to maintain and understand
- **SCALABILITY**: Component-based test structure scales better as projects grow
- **NAVIGABILITY**: Developers can quickly find tests for specific functionality
- **DIRECTORY STRUCTURE EXAMPLES** (not exhaustive):
  ```
  tests/
  ├── lib/                          # Core library tests
  │   ├── models/                   # Data model tests
  │   ├── api/                      # API interface tests
  │   ├── database/                 # Database layer tests
  │   └── schema/                   # Schema validation tests
  ├── cli/                          # Command-line interface tests
  ├── web/                          # Web application tests
  │   ├── models/                   # Web data models
  │   ├── frontend/
  │   │   └── api/                  # Frontend API tests
  │   └── backend/
  │       └── api/                  # Backend API tests
  ├── features/                     # Feature-based tests
  │   ├── feature1/                 # Specific feature tests
  │   └── scenarios/
  │       └── scenario1/            # Test scenario groupings
  ├── unittests/                    # Unit test collections
  └── shared/                       # Shared test utilities and fixtures
  ```

## 9. Agents MUST use the token-optimization system
- Prefer local tools (`grep`, `rg`, `sed`, `awk`, `jq`, `greptool`) over long LLM reasoning.
- Reuse existing context.
- Produce small, efficient, incremental changes.

## 10. Use local command-line tools - ALWAYS preferred over internal CLI tools
- **ALWAYS PREFER**: Local command-line tools over internal CLI tools
- **NO LIMITATIONS**: Not limited to the examples given - use appropriate tools
- **Primary Examples**: `sed`, `awk`, `grep/greptool`, `jq`, `patch`, `cat`, `head`, `gperf`, `ls`, `rm`
- **TEXT PROCESSING**: Use `sed`, `awk`, `grep` for text manipulation and searching
- **JSON PROCESSING**: Use `jq` for JSON parsing, filtering, and transformation
- **FILE OPERATIONS**: Use `cat`, `head`, `tail`, `ls`, `rm` for file inspection and management
- **PATCH MANAGEMENT**: Use `patch` for applying and managing code changes
- **PERFORMANCE**: Use `gperf` for perfect hash functions when needed
- **PIPELINES**: Combine tools with pipes (`|`) for powerful multi-step operations
- **SHELL SCRIPTING**: Prefer shell commands over Python scripts for simple operations
- **DIRECT EXECUTION**: Use subprocess/system calls to execute local tools directly
- **EFFICIENCY**: Local tools are typically faster and more resource-efficient than internal implementations
- **RELIABILITY**: Well-tested system tools are more reliable than custom implementations
- **STANDARDS**: Use POSIX-compliant tools for maximum portability

## 11. Simplicity over complexity - ALWAYS prefer
- **ALWAYS** choose the simplest solution that works
- **NO OVER-ENGINEERING**: Avoid unnecessary complexity, abstraction, or indirection
- **DIRECT SOLUTIONS**: Favor straightforward, explicit, clear approaches
- **MINIMAL DEPENDENCIES**: Use only what's necessary to solve the problem
- **READABILITY FIRST**: If complexity is unavoidable, prioritize readability over cleverness

## 12. Code must read like natural language - ALWAYS write naturally
- **ALWAYS** write code that reads like human conversation
- **CONVERSATIONAL NAMING**: Use names that tell a story (user_authenticates, not auth)
- **NATURAL FLOW**: Code should read like sentences, not puzzles
- **SELF-DOCUMENTING**: Code should explain itself without excessive comments
- **CLEAR LOGIC**: Each line should have an obvious purpose
- **HELPFUL DOCSTRINGS**: Write documentation that speaks to humans
- **TESTS TOO**: Tests must also read like natural language, not technical specifications

## 13. FULL TYPE HINTING & TYPE ANNOTATIONS REQUIRED
- All code must include complete type hints:
  - Typed `self`
  - Typed parameters
  - Typed returns
  - Typed attributes
  - No implicit `Any`

## 14. Agents MUST read `AGENT_STARTUP.md` before beginning any development work
- Contains essential tooling configuration and startup checklist
- Defines UV, Ruff, Bandit, and build system requirements
- Specifies correct workflows and prohibited direct tool usage

# 15. Working Directory Boundary

- **Root Directory**: `./` refers to the current project's root directory
- **Project Context**: Each project has its own root directory boundary
  - Example: For `afs_fastapi` project: `~/Documentation/GitHub/dderyldowney/afs_fastapi/`
  - Example: For this `todowrite` project: `~/Documentation/GitHub/dderyldowney/todowrite/`
- **Boundary Rule**: ALL operations must be confined within the current project's directory structure
- **NO CROSS-PROJECT**: Never operate outside the current project's root directory
- **RESPECT BOUNDARIES**: Honor each project's working directory boundary independently

# 16. Monorepo Structure

```
$project_root/
├── BUILD_SYSTEM.md
├── docs/ToDoWrite.md
├── tests/
├── lib_package/
├── cli_package/
└── web_package/   # planning only
```

# 17. Tooling & Environment Rules

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
