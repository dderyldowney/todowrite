# CLAUDE.md

This file defines **non-negotiable, permanent rules** for Claude and all agents working in this repository.
These mandates apply **at all times** with **zero exceptions**.

---

## Core Mandates (Must ALWAYS Be Followed)

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

- **Python**: <https://python.org> (official), <https://docs.python.org/3/library/typing.html> (typing), and <https://docs.python.org/3/library/asyncio.html> (async programming)
- **UV**: <https://docs.astral.sh/uv> (package management and environments)
- **Ruff**: <https://docs.astral.sh/ruff> (linting, formatting, security)
- **Bandit**: <https://bandit.readthedocs.io/en/latest/> (security scanning)
- **Semantic Commits**: <https://here-be-pythons.readthedocs.io/en/latest/git/semantic-commit-messages.html>
- **Conventional Commits**: <https://www.conventionalcommits.org/en/v1.0.0/#specification>
- **Pytest**: <https://docs.pytest.org/en/stable/> (testing framework)
- **TestPyPI/PyPI**: <https://docs.pypi.org/> (package publishing and distribution)
- **Git**: <https://git-scm.com/docs> (version control operations)
- **GitHub**: <https://docs.github.com/en> (platform-specific operations)
- **Python Packaging**: <https://packaging.python.org/en/latest/> (packaging standards and practices)
- **SQLite3**: <https://docs.python.org/3/library/sqlite3.html> and <https://sqlite.org/docs.html> (database operations)
- **PostgreSQL**: <https://www.postgresql.org/docs/current/> (database operations)
- **YAML**: <https://yaml.org/spec/1.2.2/> (data serialization format)
- **Hatchling**: <https://pypi.org/project/hatchling/> (build system - see Documentation links)
- **Twine**: <https://twine-bhrutledge.readthedocs.io/en/stable/> (PyPI publishing tool)
- **TDD Methodology**: <https://tddbuddy.com/references/tdd-cycle.html> and <https://www.ibm.com/think/topics/test-driven-development> (preferred references)
- **Ruby on Rails**: <https://guides.rubyonrails.org/> (official Rails guides for Active Record patterns)
- **Rails ActiveRecord API**: <https://api.rubyonrails.org/classes/ActiveRecord/Associations/ClassMethods.html> (ActiveRecord association methods and patterns)
- **Rails Association Basics**: <https://guides.rubyonrails.org/association_basics.html> (Rails has_many, belongs_to, collection methods)
- **NO ASSUMPTIONS**: Always verify syntax, semantics, and logic against authoritative sources
- **CODE GENERATION**: Must reference current official documentation, not memory or assumptions
- **TEST CREATION**: Must validate behavior against authoritative specifications

## 4. TRIPLE-CHECK before modifying - understand existing architecture FIRST

- **NEVER** modify architecture without fully understanding existing system
- **ALWAYS** cross-verify changes don't break existing relationships/patterns
- **RESEARCH thoroughly** before changing core data models, relationships, or imports
- **VERIFY** existing functionality isn't broken by your changes
- **THINK** about SQLAlchemy event systems, initialization, and object lifecycle
- **DOUBLE-CHECK** all imports, references, and architectural assumptions
- **TEST** both creation patterns AND database-loaded object patterns

## 5. NEVER fake code - write REAL implementations only

- **NEVER** use 'pass', '...', 'raise NotImplementedError', or placeholder code
- **NEVER** write fake implementations just to pass tests
- **ALWAYS** write actual, functional implementation code when writing code
- **NO TRICKS**: No clever hacks, workarounds, or test-cheating techniques
- **REAL BEHAVIOR**: Code must actually do what it's supposed to do
- **PROPER FUNCTIONALITY**: Implementation must solve the real problem, not just satisfy test assertions

## 6. NO GENERIC EXCEPTIONS - Use Specific Exception Types

- **NEVER** use generic `except Exception:` - MUST catch specific exception types
- **ALWAYS** identify and catch the specific exception types that can occur
- **MUST** handle ValueError, KeyError, AttributeError, TypeError, etc. specifically
- **ALWAYS** raise specific, meaningful exceptions instead of generic Exception
- **NEVER** use bare except clauses - must specify exception types
- **MUST** understand which exceptions each operation can throw and handle them explicitly
- **EXAMPLE**:
  - ✅ `except (ValueError, KeyError) as e:`
  - ❌ `except Exception as e:`

## 7. ALWAYS test actual implementation - REAL testing only

- **ALWAYS** test the actual implementation, not fake/test doubles
- **REAL INTERACTIONS**: Tests must exercise real functionality
- **NO MOCKING**: This rule reinforces Rule #1 - no mocking of any kind
- **INTEGRATION FOCUS**: Test how components actually work together
- **VERIFIABLE BEHAVIOR**: Tests must verify real, observable behavior
- **END-TO-END VALIDATION**: Prefer testing complete workflows over isolated pieces

## 8. Test-Driven Development only (Red → Green → Refactor)

- Strict Red → Green → Refactor workflow:
  1. Write a failing test (**Red**).
  2. Implement the **minimal** code needed to pass (**Green**).
  3. Clean up with tests still passing (**Refactor**).

## 9. No code without tests FIRST

- All production code must originate from a failing test.
- No feature work or fixes happen without the test created first.

## 10. Tests must be broken down by component and subsystem - SoC REQUIRED

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
-- **DIRECTORY STRUCTURE EXAMPLES** (not exhaustive):

  ```text
  tests/
  ├── lib/                          # todowrite package tests
  │   ├── models/                   # Data model tests
  │   ├── api/                      # API interface tests
  │   ├── database/                 # Database layer tests
  │   └── schema/                   # Schema validation tests
  ├── cli/                          # todowrite_cli package tests
  ├── web/                          # todowrite_web package tests
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

- **MONOREPO PACKAGE MAPPING**:
  - `lib/` → `todowrite` package tests
  - `cli/` → `todowrite_cli` package tests
  - `web/` → `todowrite_web` package tests

## 11. MINIMIZE DATABASE CALLS - Optimize for performance

- **NEVER** make redundant database calls that could be combined
- **ALWAYS** batch operations when possible to minimize round trips
- **THINK** about database efficiency: one query vs multiple queries
- **CACHE** results when appropriate to avoid repeated calls
- **LAZY LOAD** only when needed, eager load when you know you'll need the data
- **ANALYZE** query performance and optimize N+1 problems
- **CONSIDER** using joins instead of multiple separate queries
- **PROFILE** database operations to identify bottlenecks
- Prefer local tools (`grep`, `rg`, `sed`, `awk`, `jq`, `greptool`) over long LLM reasoning.
- Reuse existing context.
- Produce small, efficient, incremental changes.

## 12. Agents MUST use HAL Agent AND Token Optimization Systems (ZERO EXCEPTIONS)

**MANDATORY REQUIREMENT**: ALL agents MUST use BOTH the HAL Agent System AND the Token Optimization System for EVERY task. NO EXCEPTIONS.

### 12.1 HAL Agent System - MUST USE (Zero API Tokens for Local Processing)

**Purpose**: Local preprocessing and filtering before AI interactions (0 API tokens)

**Location**: `dev_tools/agent_controls/hal_token_savvy_agent.py`

**Mandatory Usage Patterns**:

```bash
# Basic HAL Agent Usage (ALWAYS use this first)
python dev_tools/agent_controls/hal_token_savvy_agent.py \
  --provider openai \
  --model $OPENAI_MODEL \
  --goal "find database model files" \
  --roots lib_package/ \
  --include "*.py" \
  --chars 1000 \
  --max-files 50

# HAL Agent for Code Analysis
python dev_tools/agent_controls/hal_token_savvy_agent.py \
  --provider openai \
  --model $OPENAI_MODEL \
  --goal "analyze authentication patterns" \
  --pattern "class.*Auth" \
  --roots lib_package/ cli_package/ \
  --include "*.py" \
  --chars 1500

# HAL Agent for Error Investigation
python dev_tools/agent_controls/hal_token_savvy_agent.py \
  --provider openai \
  --model $OPENAI_MODEL \
  --goal "find test failures" \
  --pattern "def test.*" \
  --roots tests/ \
  --include "*.py" \
  --chars 2000 \
  --context 5
```

**HAL Agent Options**:
- `--provider {openai,anthropic}`: AI provider (OpenAI always preferred)
- `--model`: Model name (uses $OPENAI_MODEL environment variable)
- `--goal`: Analysis goal (required)
- `--pattern`: Regex pattern for focused search
- `--roots`: Directories to search
- `--include`: File glob patterns
- `--chars`: Max snippet size (default 1000)
- `--max-files`: Maximum files to process
- `--context`: Context lines around matches

**OpenAI Environment Variables**:
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_BASE_URL`: Custom API endpoint (required for non-OpenAI endpoints)
- `OPENAI_MODEL`: Model to use (e.g., gpt-4o-mini, glm-4.6)
- `OPENAI_TIMEOUT`: Request timeout in seconds (optional, uses OpenAI default if not set; typically 600 seconds)

### 12.2 Token Optimization System - MUST USE (90% Token Savings)

**Purpose**: Optimized AI interactions with minimal token usage

**Location**: `dev_tools/token_optimization/always_token_sage.py`

**Mandatory Usage Patterns**:

```bash
# Token-Sage Analysis (ALWAYS use after HAL preprocessing)
python dev_tools/token_optimization/always_token_sage.py "analyze database relationships"

# Token-Sage for Feature Investigation
python dev_tools/token_optimization/always_token_sage.py "implement user authentication flow"

# Token-Sage for Debugging
python dev_tools/token_optimization/always_token_sage.py "fix failing test in storage layer"

# Advanced Token Optimization with Caching
python dev_tools/token_optimization/token_optimized_agent.py "database models" "class.*Model"
```

### 12.3 Mandatory Workflow for ALL Agents

**EVERY task MUST follow this exact sequence**:

1. **HAL Preprocessing First** (0 API tokens):
   ```bash
   python dev_tools/agent_controls/hal_token_savvy_agent.py --provider openai --model gpt-4o --goal "YOUR TASK HERE"
   ```

2. **Token-Sage Analysis Second** (optimized tokens):
   ```bash
   python dev_tools/token_optimization/always_token_sage.py "YOUR ANALYSIS TASK"
   ```

3. **Direct Tool Usage Only When HAL/Token-Sage Cannot Handle**:
   - Use `sed`, `awk`, `grep/greptool`, `jq` for text processing
   - Use `cat`, `head`, `tail`, `ls` for file operations
   - Use `patch` for code changes
   - Use `find` and `xargs` for file searching

**FORBIDDEN**: Direct AI model usage without HAL preprocessing and token optimization

### 12.4 Token Savings Verification

**Expected Results**:
- **HAL Preprocessing**: 0 API tokens (local processing only)
- **Token-Sage Analysis**: Up to 90% token reduction vs standard analysis
- **Combined Workflow**: Maximum efficiency with minimal API usage

**Verification Commands**:
```bash
# Test HAL Agent works
python dev_tools/agent_controls/hal_token_savvy_agent.py --help

# Test Token Optimization works
python dev_tools/token_optimization/always_token_sage.py "test query"

# Verify dependencies are installed
python -c "import openai; print('✅ HAL dependencies ready')"

# Verify OpenAI API configuration is set (OpenAI always preferred over Anthropic)
python -c "import os; print('✅ OpenAI API key ready' if os.getenv('OPENAI_API_KEY') else '❌ OPENAI_API_KEY not set')"
python -c "import os; print('✅ OpenAI base URL set' if os.getenv('OPENAI_BASE_URL') else '❌ OPENAI_BASE_URL not set')"
python -c "import os; print('✅ OpenAI model set' if os.getenv('OPENAI_MODEL') else '❌ OPENAI_MODEL not set')"
python -c "import os; print('✅ OpenAI timeout set' if os.getenv('OPENAI_TIMEOUT') else 'ℹ️ OPENAI_TIMEOUT not set (using default)')"
```

### 12.5 Enforcement and Compliance

**ABSOLUTE REQUIREMENTS**:
- **NO EXCEPTIONS**: This applies to ALL agents at ALL times
- **NO BYPASSING**: HAL preprocessing is required before any AI interaction
- **MANDATORY DEPENDENCIES**: `openai>=1.12.0` always installed (OpenAI always preferred over Anthropic)
- **ZERO ALTERNATIVES**: No other tools or workflows are permitted
- **CONTINUOUS USAGE**: Must be used for every single task, no matter how small

**VIOLATION CONSEQUENCES**: Any agent not using HAL Agent + Token Optimization System is in violation of CLAUDE.md mandates and must be corrected immediately.

## 13. Use local command-line tools - ALWAYS preferred over internal CLI tools

- **ALWAYS** choose the simplest solution that works
- **NO OVER-ENGINEERING**: Avoid unnecessary complexity, abstraction, or indirection
- **DIRECT SOLUTIONS**: Favor straightforward, explicit, clear approaches
- **MINIMAL DEPENDENCIES**: Use only what's necessary to solve the problem
- **READABILITY FIRST**: If complexity is unavoidable, prioritize readability over cleverness

## 14. Simplicity over complexity - ALWAYS prefer

- **ALWAYS** write code that reads like human conversation
- **APPLIES TO**: Both production code AND test code - no exceptions
- **FULL TYPING REQUIRED**: All generated code must include complete type hints
- **NATURAL CONSTRUCTS**: Use clear, readable code patterns and flow
- **CONVERSATIONAL NAMING**: Use names that tell a story (user_authenticates, not auth)
- **NATURAL FLOW**: Code should read like sentences, not puzzles
- **CONTEXTUAL FUNCTIONALITY**: Code should follow natural business logic flow
- **SELF-DOCUMENTING**: Code should explain itself without excessive comments
- **CLEAR LOGIC**: Each line should have an obvious purpose
- **HELPFUL DOCSTRINGS**: Write documentation that speaks to humans
- **READABLE TESTS**: Test names and content should describe behavior in plain language
- **NO TECHNICAL JARGON**: Avoid overly technical descriptions unless absolutely necessary
- **AGENT RESPONSIBILITY**: AI-generated code must be production-ready with full typing

## 15. Code AND Tests must read like natural language - ALWAYS write naturally

- **ALWAYS** write code that reads like human conversation
- **APPLIES TO**: Both production code AND test code - no exceptions
- **FULL TYPING REQUIRED**: All generated code must include complete type hints
- **NATURAL CONSTRUCTS**: Use clear, readable code patterns and flow
- **CONVERSATIONAL NAMING**: Use names that tell a story (user_authenticates, not auth)
- **NATURAL FLOW**: Code should read like sentences, not puzzles
- **CONTEXTUAL FUNCTIONALITY**: Code should follow natural business logic flow
- **SELF-DOCUMENTING**: Code should explain itself without excessive comments
- **CLEAR LOGIC**: Each line should have an obvious purpose
- **HELPFUL DOCSTRINGS**: Write documentation that speaks to humans
- **READABLE TESTS**: Test names and content should describe behavior in plain language
- **NO TECHNICAL JARGON**: Avoid overly technical descriptions unless absolutely necessary
- **AGENT RESPONSIBILITY**: AI-generated code must be production-ready with full typing

## 16. IMPORT ORGANIZATION STANDARDS

**MANDATORY**: All imports must follow strict alphabetical organization per PEP 8 standards

### Required Import Structure

1. **Standard Library Imports** (alphabetically sorted):
   ```python
   import json
   import logging
   from collections.abc import Iterator
   from pathlib import Path
   from typing import Any
   ```

2. **Third-Party Imports** (alphabetically sorted):
   ```python
   import jsonschema
   import pytest
   from sqlalchemy import Engine
   ```

3. **Local/Application Imports** (alphabetically sorted):
   ```python
   from ..storage import (
       NodeCreationError,
       NodeNotFoundError,
       StorageBackend,
   )
   from .types import Node
   ```

### Import Rules

- **ALWAYS SORT ALPHABETICALLY**: Each import group must be alphabetically sorted
- **USE RUFF FORMAT**: Run `./dev_tools/build.sh format` to automatically sort imports
- **NO IMPORT STAR**: `from module import *` is forbidden
- **PLACE TYPE_CHECKING IMPORTS**: Runtime imports should NOT be in TYPE_CHECKING blocks
- **SEPARATE GROUPS**: Use blank lines between import groups
- **CONSISTENT STYLE**: Follow the exact pattern shown above

### Import Validation

- **Before committing**: Run `./dev_tools/build.sh lint` to verify import organization
- **Automatic fixing**: Use `./dev_tools/build.sh format` to fix import order
- **Manual verification**: Ensure imports are readable and properly grouped

## 17. COMMIT MESSAGE STANDARDS

**MANDATORY**: All commits MUST follow strict Conventional Commits format with no exceptions

### Required Commit Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Valid Commit Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code change that neither fixes bug nor adds feature
- **perf**: Performance improvement
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes affecting build system or dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

### Valid Commit Scopes

**Project-specific scopes:**
- **lib** - Core todowrite library
- **cli** - Command-line interface
- **web** - Web interface
- **tests** - Test suite and testing infrastructure
- **docs** - Documentation
- **build** - Build system and packaging
- **config** - Configuration files and settings
- **ci** - Continuous integration and deployment
- **deps** - Dependencies and requirements

**Layer-specific scopes (ToDoWrite hierarchy):**
- **goal**, **concept**, **context**, **constraints**
- **req**, **ac**, **iface**
- **phase**, **step**, **task**, **subtask**, **cmd**
- **schema**, **lint**, **trace**, **api**, **validation**, **tools**

### Requirements (Updated for Industry Standards)

- **Subject line MAXIMUM 100 characters** - Following Google/Angular practices
- **Subject MUST start with capital letter**
- **Scope is OPTIONAL** - Project-specific scopes encouraged but not required
- **Description MUST be in present tense** - "add" not "added"
- **Description MUST be in imperative mood** - "Fix bug" not "Fixes bug"
- **Minimum subject length**: 5 characters (reduced from 10)

### Examples of Correct Format

```bash
feat(lib): add hierarchical task relationships
fix(cli): resolve authentication timeout
test(web): add comprehensive user interface coverage
docs(readme): update installation instructions
refactor(api): simplify database connection logic
build(schema): generate updated todowrite.schema.json
chore(config): update import organization standards
```

### Extended Commit Message Format with Body

For more detailed commits, use this exact pattern:

```
chore(config): <Short description goes here>

Full description goes here for as long as needed.
```

### Examples of INCORRECT Format

```bash
❌ "Add new feature"                    # Missing type and scope
❌ "feat: add feature"                 # Missing scope
❌ "feat(lib): Add new feature"        # Subject starts with capital but too long
❌ "feat(lib): this is a really long description that exceeds the 72 character limit"
❌ "docs(cli): Fixed the documentation" # Past tense, not imperative
```

### Validation

- **Before committing**: Hooks will validate format automatically
- **Failed commits**: Fix the message to meet ALL requirements
- **No exceptions**: Format is mandatory, not optional

## 18. FULL TYPE HINTING & TYPE ANNOTATIONS REQUIRED

**MANDATORY**: All code MUST include complete type hints following Python 3.12+ standards

### Required Type Annotations

- **Typed `self`**: All method parameters must include type hints for `self`
- **Typed parameters**: All function/method parameters must have explicit type hints
- **Typed returns**: All functions/methods must have explicit return type annotations
- **Typed attributes**: All class attributes must have type hints
- **NO IMPLICIT `Any`**: Never rely on implicit `Any` types
- **STRICT PROHIBITION ON `Any`**: `Any` type is NOT allowed unless ABSOLUTELY NECESSARY! Types MUST be resolved to concrete types or proper unions/interfaces

### Python 3.12+ Features Required

- **Modern typing syntax**: Use Python 3.12+ typing features and syntax
- **Union types**: Use `|` syntax for union types (e.g., `str | int` instead of `Union[str, int]`)
- **Generic types**: Use proper generic type syntax
- **Type guards**: Implement proper type guards where needed
- **Protocol types**: Use `Protocol` for structural typing where appropriate

### Strict Requirements

- **Complete coverage**: Every public function/method must be fully typed
- **Private methods**: Private methods should also be typed for clarity
- **Lambda functions**: Use proper type annotations for lambda functions where possible
- **Complex types**: Use `typing` module for complex types (Dict, List, Optional, etc.)
- **Forward references**: Use proper forward references for circular imports
- **ABSOLUTELY NO `Any` TYPES**: `Any` is FORBIDDEN unless absolutely unavoidable - types MUST be resolved to concrete types or proper unions/protocols

### Enforcement

- **Static analysis**: Code must pass ruff type checking
- **IDE compatibility**: Type hints must work with modern IDE type checking
- **Runtime type checking**: Consider runtime type checking for critical paths
- **Documentation**: Type hints serve as documentation - make them meaningful

### Examples

```python
# ✅ CORRECT: Complete type hints
class NodeManager:
    def __init__(self: Self, database_url: str) -> None:
        self.database_url: str = database_url
        self.nodes: dict[str, Node] = {}

    def create_node(
        self: Self,
        node_data: dict[str, Any],
        layer: NodeLayer
    ) -> Node:
        """Create a new node with proper type hints."""
        return Node.from_dict(node_data, layer)

# ❌ WRONG: Missing type hints
class NodeManager:
    def __init__(self, database_url):
        self.database_url = database_url
        self.nodes = {}

    def create_node(self, node_data, layer):
        return Node.from_dict(node_data, layer)

# ❌ EXTREMELY WRONG: Using Any types
class BadNodeManager:
    def __init__(self: Self, database_url: Any) -> Any:  # FORBIDDEN Any types!
        self.database_url: Any = database_url  # FORBIDDEN!
        self.nodes: dict[str, Any] = {}  # FORBIDDEN Any usage!

    def create_node(self: Self, node_data: Any, layer: Any) -> Any:  # ALL FORBIDDEN!
        """NEVER use Any unless absolutely unavoidable!"""
        return Node.from_dict(node_data, layer)
```

**ABSOLUTE REQUIREMENT**: `Any` types are FORBIDDEN unless absolutely unavoidable. Always resolve to concrete types, proper unions, or Protocol interfaces. Type ambiguity is unacceptable - resolve your types!

**NO EXCEPTIONS**: All production code must follow these typing requirements without exception.

## 17. Agents MUST read `docs/ToDoWrite.md` before beginning any development work

## 18. Agents MUST respect Working Directory Boundaries

- **Root Directory**: `./` refers to the current project's root directory
- **Project Context**: Each project has its own root directory boundary
  - Example: For `afs_fastapi` project: `~/Documentation/GitHub/dderyldowney/afs_fastapi/`
  - Example: For this `todowrite` project: `~/Documentation/GitHub/dderyldowney/todowrite/`
- **Boundary Rule**: ALL operations must be confined within the current project's directory structure
- **NO CROSS-PROJECT**: Never operate outside the current project's root directory
- **RESPECT BOUNDARIES**: Honor each project's working directory boundary independently

## Agent Startup Checklist & Quick Commands

**CRITICAL: VENV ACTIVATION REQUIRED**

Every session MUST start with virtual environment activation. This is non-negotiable:

```bash
# ALWAYS start each session by activating the virtual environment
source .venv/bin/activate

# Verify activation
which python      # Should point to .venv/bin/python
uv --version      # Should show UV version
```

**Why this is critical**:
- Ensures all dependencies are available
- Maintains consistent tool versions
- Prevents system Python conflicts
- Guarantees reproducible environments

### MANDATORY Startup Checklist

All agents MUST complete this checklist before beginning any work:

- [ ] **Environment**: UV workspace is active and venv is loaded (`source .venv/bin/activate`)
- [ ] **Verification**: Confirm .venv is active with `which python` and `uv --version`
- [ ] **Code Quality**: Ruff configured for formatting, linting, and security (S mode)
- [ ] **Security**: Bandit available for deep security scans
- [ ] **Build System**: Using `./dev_tools/build.sh` commands (not direct tools)
- [ ] **Testing**: pytest configured with `--ignore=tests/web/`
- [ ] **No Mocking**: STRICT no-mocking policy understood and followed
- [ ] **HAL Agent System**: Ready and functional (`python dev_tools/agent_controls/hal_token_savvy_agent.py --help`)
- [ ] **Token Optimization**: Active and verified (`python dev_tools/token_optimization/always_token_sage.py "test"`)
- [ ] **HAL Dependencies**: `openai` package installed and importable
- [ ] **OpenAI Configuration**: `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, and optionally `OPENAI_TIMEOUT` environment variables set

### Preferred Tool Invocation

Use the build script `./dev_tools/build.sh` for day-to-day tasks. Use `uv run <tool>` only when the build script does not expose the required action.

```bash
# Preferred high-level workflow
./dev_tools/build.sh install    # Install/update dependencies
./dev_tools/build.sh format     # Format code (ruff)
./dev_tools/build.sh lint       # Lint code (ruff)
./dev_tools/build.sh test       # Run tests (pytest)
./dev_tools/build.sh audit      # Security scan (bandit + ruff S-mode)
./dev_tools/build.sh validate   # Validate build system
./dev_tools/build.sh dev        # Full dev workflow (install+format+lint+test)

# Quality gate examples
./dev_tools/build.sh quality-gate --coverage-threshold 80
./dev_tools/build.sh quality-gate --strict
```

### Direct UV Examples (Only When Necessary)

```bash
uv run ruff format lib_package/ cli_package/
uv run ruff check lib_package/ cli_package/
uv run bandit -r lib_package/ cli_package/
uv run pytest tests/ --ignore=tests/web/
uv run pytest tests/ --cov=lib_package/src --cov=cli_package/src --ignore=tests/web/
```

### Essential File Locations

**Configuration Files**:
- **`pyproject.toml`**: UV workspace, Ruff, Bandit configuration
- **`VERSION`**: Central version management
- **`.claude/CLAUDE.md`**: Project rules and mandates

**Build System Files**:
- **`dev_tools/build.sh`**: PRIMARY build interface (use this!)
- **`lib_package/src/todowrite/build_system.py`**: Library API for applications
- **`dev_tools/build_system.py`**: Development tool API

**Package Structure**:
```text
todowrite/
├── lib_package/     # Core library (todowrite) - PRODUCTION READY
├── cli_package/     # CLI interface (todowrite_cli) - PRODUCTION READY
├── web_package/     # Web application - PLANNING STAGE (excluded from tools)
└── tests/           # Test suites (NO MOCKING ALLOWED)
```

### Agent Workflows

**Before Starting Work**:
1. Verify UV environment: `uv sync --group dev` and `uv tree`
2. Run validation: `./dev_tools/build.sh validate`
3. Check code quality: `./dev_tools/build.sh lint` and `./dev_tools/build.sh format`

**During Development**:
1. Use build scripts ONLY (never direct tool calls)
2. Security scanning: `./dev_tools/build.sh audit`

**Before Committing**:
1. Run complete workflow: `./dev_tools/build.sh dev`
2. Quality gate validation: `./dev_tools/build.sh quality-gate --strict`

### Quick Start (Copyable)

```bash
# 0. CRITICAL: Always start with venv activation
source .venv/bin/activate

# 1. Setup environment
./dev_tools/build.sh install

# 2. Validate everything works
./dev_tools/build.sh validate

# 3. Run complete development workflow
./dev_tools/build.sh dev

# 4. Check quality gates
./dev_tools/build.sh quality-gate
```

**Notes**:
- `web_package` is intentionally excluded from automated tests and formatting; build scripts handle exclusions automatically.
- These items are operational details to be followed by agents; the authoritative policies (TDD, no-mocking, type hints, etc.) remain in the main CLAUDE mandates above.

## 18. Standard Workflow

1. **MANDATORY**: Load documentation files IN ORDER (CLAUDE.md → ToDoWrite.md → BUILD_SYSTEM.md)
   - **On session start**: Load before any other work
   - **After '/clear'**: Immediately reload before any other work
   - **After '/quit'**: Load in new session before any other work
2. **MANDATORY**: Complete Startup Checklist including HAL Agent + Token Optimization verification
3. **MANDATORY**: Use HAL Agent System for ALL tasks (Rule #12.1)
   ```bash
   python dev_tools/agent_controls/hal_token_savvy_agent.py --provider openai --model gpt-4o --goal "YOUR TASK"
   ```
4. **MANDATORY**: Use Token Optimization System for ALL AI analysis (Rule #12.2)
   ```bash
   python dev_tools/token_optimization/always_token_sage.py "YOUR ANALYSIS"
   ```
5. Clarify request & verify understanding from loaded docs
6. Search using HAL Agent preprocessing + local CLI tools only
7. Red test (using real implementations only)
8. Green minimal code with full typing
9. Refactor
10. Commit (never using --no-verify without permission)

**FORBIDDEN**: Any work without HAL Agent preprocessing and Token Optimization usage

## Emergency Documentation Verification

**If agent appears to have lost context after '/clear' or '/quit':**

1. IMMEDIATELY command: "Re-read CLAUDE.md, ToDoWrite.md, and BUILD_SYSTEM.md IN ORDER"
2. Verify compliance by asking: "Confirm you have loaded all three documentation files"
3. Do not proceed with any work until compliance is confirmed

## Conflict Resolution

- Identify the violated rule
- Propose an alternative
- Execute only once aligned
