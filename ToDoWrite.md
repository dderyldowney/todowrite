# Create the ToDoWrite.md file with the requested markdown content
content = """# ToDoWrite: Minimal Agent Rules

## Agent Objective
Plan and execute Strategic Goals by **recursively decomposing** work into **single-concern** commands, enforcing **Separation of Concerns (SoC)** at every level, until **atomic** executables.

## Hierarchy
- **Goal** → contains **Phases**
- **Phase** → contains **Steps**
- **Step** → contains **Tasks**
- **Task** → contains **SubTasks**
- **SubTask** → maps **1:1** to an executable **Command**

## Separation of Concerns (SoC)
- Every **Phase/Step/Task/SubTask** addresses **exactly one concern**.
- If an item spans multiple concerns, **split** it into multiple siblings at the same level.
- No item may include actions that belong to a different concern.
- Validation **blocks mixed concerns** (think: `git pre-commit` style).

## Granularity
- **Unlimited children** allowed at each level to achieve proper granularity.
- Decompose until each **SubTask** is an **atomic Command** with no internal sub-concerns.

## Traceability
- Maintain **parent→child** and **child→parent** links for all items.
- **Dependencies** reference only **existing** sibling/ancestor IDs; **no cycles**.

## Schema (all levels)
- `id`: unique string  
- `parent_id`: string or null  
- `level`: one of `[Goal, Phase, Step, Task, SubTask]`  
- `title`: short, single-concern name  
- `description`: brief, single-concern intent  
- `single_concern`: boolean (MUST be `true` after validation)  
- `dependencies`: list of `id`  
- `status`: one of `[planned, in_progress, blocked, done, rejected]`  
- `validation_log`: list of strings (reasons from validators)

## Execution Rules
- Only **SubTasks** may be **executed**.  
- Each SubTask compiles to **exactly one Command** (string or structured call).  
- A Command must be **self-sufficient** given declared dependencies + parent context.

## Validation Pipeline (run on every write/update)
1. **Hierarchy order**: enforce `Goal > Phase > Step > Task > SubTask`; reject skips/misplacements.  
2. **SoC check**: `title + description` express one concern; if multiple verbs/concerns → **split**.  
3. **Granularity check**:  
   - Steps contain **only Tasks** that serve the Step’s concern.  
   - Tasks contain **only SubTasks** that serve the Task’s concern.  
4. **Dependency check**: no cycles; all deps exist; no cross-concern leakage.  
5. **SubTask atomicity**: **1 SubTask → 1 Command**; no composite/multi-action commands.  
6. **Status rules**: parents can’t be `done` unless **all children** are `done`; `blocked` bubbles upward.

## Planning Algorithm (deterministic)
1. For each **Goal**, enumerate **Phases** (each = one concern).  
2. For each **Phase**, enumerate **Steps** (each = one concern of that Phase).  
3. For each **Step**, enumerate **Tasks** (each = one concern of that Step).  
4. For each **Task**, enumerate **SubTasks** as **atomic Commands**.  
5. Run the **Validation Pipeline**; on any failure, **split/reshape** and re-validate.

## Persistence
- Save items using the **Schema** **after** validation.  
- Preserve `id`s on rewrites; append reasons + timestamp to `validation_log`.

## Done Criteria
A parent item becomes `done` only when:
- **All children** are `done`.  
- **SoC** and **dependency integrity** remain satisfied.  
- **No validation errors** remain.

## Output Contracts
- **Plan outputs**: render the strict hierarchy with all **Schema** fields populated.  
- **Execution outputs**: list executed **SubTask ids**, their **Commands**, **status transitions**, and any **artifacts/notes**.
"""
path = "/mnt/data/ToDoWrite.md"
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
path
"""

