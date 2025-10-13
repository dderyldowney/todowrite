# ToDoWrite: Minimal Agent Rules (paste into your agent config/prompt)

AGENT_OBJECTIVE: >
  Plan and execute Strategic Goals by recursively decomposing work into single-concern
  commands, enforcing Separation of Concerns (SoC) at every level, until atomic executables.

HIERARCHY:
  - Goal: contains Phases
  - Phase: contains Steps
  - Step: contains Tasks
  - Task: contains SubTasks
  - SubTask: maps 1:1 to an executable Command

SEPARATION_OF_CONCERNS (SoC):
  - Every Phase/Step/Task/SubTask MUST address exactly one concern.
  - If any item spans multiple concerns, split it into multiple sibling items at the same level.
  - No item may include actions that belong to a different item/concern.
  - Validation MUST reject mixed-concern items (“git pre-commit” style block).

GRANULARITY:
  - Unlimited children allowed at each level to achieve proper granularity.
  - Decompose until each SubTask is an atomic Command with no further internal concerns.

TRACEABILITY:
  - Maintain parent→child links and child→parent references for all items.
  - Each item MUST list dependencies using only sibling or ancestor IDs; circular deps are invalid.

SCHEMA (required fields for ALL levels):
  - id: unique string
  - parent_id: string|null
  - level: one of [Goal, Phase, Step, Task, SubTask]
  - title: short, single-concern name
  - description: brief, single-concern intent
  - single_concern: boolean MUST be true after validation
  - dependencies: list[id]
  - status: one of [planned, in_progress, blocked, done, rejected]
  - validation_log: list[string] (reasons produced by validators)

EXECUTION_RULES:
  - Only SubTask items may be executed.
  - Each SubTask MUST compile to exactly one Command (string or structured call).
  - Command MUST be self-sufficient given declared dependencies and parent context.

VALIDATION_PIPELINE (run on every write/update):
  - V1: Require hierarchy order: Goal>Phase>Step>Task>SubTask; reject skips/misplacements.
  - V2: SoC check: title+description MUST express one concern; if multiple verbs/concerns, split.
  - V3: Granularity check: Steps MUST only contain Tasks serving the Step’s concern; Tasks MUST only contain SubTasks serving the Task’s concern.
  - V4: Dependency check: no cycles; deps reference existing items; no cross-concern leakage.
  - V5: SubTask atomicity: 1 SubTask → 1 Command; no composite/multi-action commands.
  - V6: Status rules: parents cannot be done unless all children are done; blocked bubbles upward.

PLANNING_ALGORITHM (deterministic outline):
  - P1: For each Goal, enumerate Phases (each Phase = one concern).
  - P2: For each Phase, enumerate Steps (each Step = one concern of that Phase).
  - P3: For each Step, enumerate Tasks (each Task = one concern of that Step).
  - P4: For each Task, enumerate SubTasks as atomic Commands.
  - P5: Apply VALIDATION_PIPELINE; if any check fails, split/reshape and re-validate.

PERSISTENCE:
  - Always save items using SCHEMA after validation.
  - Rewrites MUST preserve ids; changed fields append to validation_log with reason and timestamp.

DONE_CRITERIA:
  - A parent item becomes done only when:
      * all children are done,
      * SoC and dependency integrity remain satisfied,
      * no validation errors remain.

OUTPUT_CONTRACTS:
  - Plan outputs MUST render as the strict hierarchy with SCHEMA fields populated.
  - Execution outputs MUST list executed SubTask ids, their Commands, status transitions, and any artifacts/notes.

