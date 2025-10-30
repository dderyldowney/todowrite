# ToDoWrite Improvement Summary

## CRITICAL: Load Token-Sage Agent First

**IMPORTANT:** Before implementing any recommendations below, you must load the token-sage agent. This should be the very first command executed in any session:

```bash
# Load token-sage agent immediately after reading this document
Task subagent_type=token-sage description="Initialize token-sage" prompt="Initialize and prepare for code analysis tasks"
```

**Why:** The token-sage agent provides optimized code analysis capabilities that are essential for implementing the improvements in this document efficiently and accurately.

This document contains prioritized improvements for the ToDoWrite codebase. Each improvement includes the exact steps needed to implement it, making it possible to work on these items even in a new session.

## Priority 1: [COMPLETED] Remove Active Items Limitation (HIGH)

**File:** `todowrite/app.py` (line 676)
**Current Issue:** The `get_active_items()` method artificially limits each layer to only one active item, preventing proper management of multiple parallel workstreams.

**Current Code:**
```python
def get_active_items(self, todos: dict[str, list[Node]]) -> dict[str, Node]:
    """Returns a dictionary of the active item in each layer."""
    active_items: dict[str, Node] = {}
    for layer, nodes in todos.items():
        for node in nodes:
            if node.status not in ["done", "rejected"]:
                active_items[layer] = node  # Only one active item per layer for now
                break
    return active_items
```

**Implementation Steps:**
1. Read the current `todowrite/app.py` file to understand the full context
2. Modify the `get_active_items()` method signature and implementation:
   - Change return type from `dict[str, Node]` to `dict[str, list[Node]]`
   - Remove the `break` statement that limits to one item per layer
   - Use `defaultdict(list)` to collect all active items
3. Update any code that calls this method to handle list instead of single Node
4. Test the changes to ensure functionality works correctly

**Expected New Code:**
```python
def get_active_items(self, todos: dict[str, list[Node]]) -> dict[str, list[Node]]:
    """Returns a dictionary of active items grouped by layer."""
    active_items: dict[str, list[Node]] = defaultdict(list)
    for layer, nodes in todos.items():
        for node in nodes:
            if node.status not in ["done", "rejected"]:
                active_items[layer].append(node)
    return dict(active_items)
```

**✅ COMPLETED - Implementation Results:**
- **Date Completed:** 2025-10-30
- **Changes Made:**
  - Modified method signature from `dict[str, Node]` to `dict[str, list[Node]]`
  - Added `defaultdict` import and usage
  - Removed artificial `break` limitation
  - Method now returns all active items per layer
- **Testing Results:**
  - ✅ All existing tests pass (9/9)
  - ✅ Manual testing confirms multiple active items work correctly
  - ✅ No breaking changes (method not currently called by other code)
- **Performance:** No impact on performance, same O(n) complexity
- **Backward Compatibility:** Breaking change for any direct callers, but no current callers identified

---

## Priority 2: Ensure Schema Package Inclusion (MEDIUM)

**File:** `todowrite/schema.py` and build configuration files
**Current Issue:** Schema file may not be properly bundled in package distribution, causing runtime errors.

**Implementation Steps:**
1. Read `todowrite/schema.py` to understand current schema loading mechanism
2. Check if `MANIFEST.in` exists and includes the schema file
3. Verify `pyproject.toml` includes necessary data files
4. Test schema accessibility after package installation
5. Add automated testing for schema availability

**Commands to Run:**
```bash
# Check current manifest and package configuration
cat MANIFEST.in
cat pyproject.toml | grep -A 10 -B 10 include

# Test schema loading in current environment
python -c "from todowrite import schema; print('Schema loaded successfully')"

# If needed, add schema to MANIFEST.in
echo "include todowrite/schema/*.json" >> MANIFEST.in
```

**Verification Steps:**
- Build package locally: `python -m build`
- Install in test environment: `pip install dist/todowrite-*.tar.gz`
- Verify schema loading: `python -c "from todowrite import schema"`

---

## Priority 3: Fix Link Inconsistency Detection (MEDIUM)

**File:** `todowrite/tools/tw_trace.py` (lines 104-126)
**Current Issue:** Complex logic for detecting bidirectional link inconsistencies may not handle all edge cases properly.

**Implementation Steps:**
1. Read `todowrite/tools/tw_trace.py` to understand current inconsistency detection
2. Extract the inconsistency detection logic into a separate method
3. Add automatic repair functionality for simple inconsistencies
4. Improve error reporting with specific node IDs and suggested fixes
5. Add comprehensive unit tests

**Current Problem Area:**
```python
# Around lines 104-126 - complex inconsistency detection logic
```

**Expected Improvements:**
- Separate method: `_detect_link_inconsistencies()`
- Auto-repair method: `_repair_simple_inconsistencies()`
- Better error messages with node IDs
- Unit tests for detection and repair logic

---

## Additional Improvements (LOWER PRIORITY)

### CLI Error Handling Enhancement
**File:** `todowrite/cli.py` (lines 82-87)
**Issue:** Incomplete prefix mapping for layers causes CLI commands to fail

**Implementation:**
1. Add comprehensive layer prefix mapping
2. Implement graceful fallback for missing prefixes
3. Add user-friendly error messages

### Code Duplication Removal
**File:** `todowrite/tools/tw_trace.py` (lines 331, 374-376)
**Issue:** Duplicated logic for determining if issues exist

**Implementation:**
1. Extract common logic into a helper method
2. Update all call sites to use the helper method

### Documentation and Clarity
**File:** `todowrite/cli.py` (line 152)
**Issue:** Temporary storage preference setting needs clarification

**Implementation:**
1. Clarify whether preference persists
2. Update documentation accordingly
3. Add user-facing documentation about preference behavior

---

## How to Use This Document

### To Implement the Highest Priority Recommendation:
1. Read this document to understand the context
2. Follow the implementation steps for "Priority 1: Remove Active Items Limitation"
3. Use the testing steps to verify the changes work correctly

### To Work on Any Recommendation:
1. Read the relevant section for full context
2. Follow the implementation steps exactly as written
3. Run the specified verification/testing commands
4. Update this document to mark items as completed

### After Implementation:
1. Mark completed items with `[COMPLETED]` prefix
2. Add any lessons learned or additional considerations
3. Update test coverage information
4. Consider adding new TODO comments to the codebase for future reference

---

## Implementation Checklist Template

For each improvement, track progress with this checklist:

- [ ] Read and understand current implementation
- [ ] Implement the required changes
- [ ] Update any dependent code
- [ ] Run existing tests to ensure no regressions
- [ ] Add new tests for the new functionality
- [ ] Test manually if applicable
- [ ] Update documentation
- [ ] Mark as completed in this document

---

*Last Updated: 2025-10-30*
*Generated by Claude Code analysis*
