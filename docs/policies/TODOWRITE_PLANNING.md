# ToDoWrite Planning Policy

## 🚨 NON-NEGOTIABLE REQUIREMENTS

### Mandatory Planning Hierarchy

**ALL DEVELOPMENT WORK** MUST start with ToDoWrite planning:
- **NO CODE IMPLEMENTATION** without goal/concept/task breakdown
- **ZERO EXCEPTIONS** for "quick fixes" or "simple changes"
- **ALL AGENTS** (Chat, CLI, VSCode) MUST enforce this requirement

### Single Source of Truth Planning

For ToDoWrite planning:
- **NO code is written** until Goal → Phase → Step → Task → Sub-Task tree exists
- **This planning hierarchy is mandatory**
- **All work must be traceable** to a specific planning element

### Pre-Work Verification

```bash
# Verify active goals exist:
docker exec mcp-postgres psql -U mcp_user -d todowrite -c "SELECT COUNT(*) FROM goals WHERE status = 'active';"

# Check session context:
python .claude/session_manager.py --summary

# Verify TDD compliance (MUST PASS before any coding):
pytest tests/ -v  # Should show existing tests, fail new ones
```

## Planning Hierarchy

### 1. Goals (Strategic Level)
- **Purpose**: High-level objectives and desired outcomes
- **Format**: Clear, measurable, achievable objectives
- **Validation**: Must align with project vision and user needs
- **Database**: Stored in `goals` table

```python
# Example Goal Structure
goal = Goal(
    title="Implement User Authentication System",
    description="Add secure user authentication with OAuth2 providers",
    acceptance_criteria=[
        "Users can register with email/password",
        "Users can login with Google OAuth",
        "Password reset functionality works",
        "Session management implemented"
    ]
)
```

### 2. Concepts (Design Level)
- **Purpose**: High-level approach and design philosophy
- **Format**: Design decisions, architectural choices
- **Validation**: Must be feasible and technically sound
- **Database**: Stored in `concepts` table

```python
# Example Concept Structure
concept = Concept(
    title="JWT-based Session Management",
    description="Use JSON Web Tokens for stateless authentication",
    technical_approach="Token-based authentication with refresh tokens"
)
```

### 3. Context (Environment Level)
- **Purpose**: Current state, constraints, and environment
- **Format**: Current system state, existing components
- **Validation**: Must accurately reflect current reality
- **Database**: Stored in `context` table

```python
# Example Context Structure
context = Context(
    title="Current Authentication State",
    description="System currently has no authentication mechanism",
    existing_components=["User model (basic)", "Database schema"]
)
```

### 4. Constraints (Limitations Level)
- **Purpose**: Technical and business constraints
- **Format**: Resource limitations, technical constraints
- **Validation**: Must be realistic and documented
- **Database**: Stored in `constraints` table

```python
# Example Constraints Structure
constraints = Constraints(
    title="Development Constraints",
    technical_constraints=["Must use PostgreSQL", "Python 3.12+ required"],
    business_constraints=["Must be GDPR compliant", "No third-party auth services"]
)
```

### 5. Requirements (Specification Level)
- **Purpose**: Detailed functional and non-functional requirements
- **Format**: Specific, testable requirements
- **Validation**: Must be measurable and verifiable
- **Database**: Stored in `requirements` table

```python
# Example Requirements Structure
requirements = Requirements(
    title="Authentication Requirements",
    functional_requirements=[
        "User registration with email verification",
        "Login with email/password",
        "Social login (Google, GitHub)",
        "Password reset with email"
    ],
    non_functional_requirements=[
        "Response time < 500ms",
        "99.9% uptime",
        "Secure password hashing"
    ]
)
```

### 6. Phases (Timeline Level)
- **Purpose**: Major development phases or milestones
- **Format**: Time-based development stages
- **Validation**: Must be logical and achievable
- **Database**: Stored in `phases` table

```python
# Example Phases Structure
phase = Phase(
    title="Phase 1: Core Authentication",
    description="Implement basic email/password authentication",
    estimated_duration="2 weeks",
    dependencies=[]
)
```

### 7. Steps (Task Level)
- **Purpose**: Specific implementation steps
- **Format**: Concrete, actionable steps
- **Validation**: Must be specific and achievable
- **Database**: Stored in `steps` table

```python
# Example Steps Structure
step = Step(
    title="Create User Model",
    description="Extend existing User model with authentication fields",
    implementation_details=[
        "Add password_hash field",
        "Add email_verified field",
        "Add last_login timestamp"
    ]
)
```

### 8. Tasks (Implementation Level)
- **Purpose**: Individual development tasks
- **Format:** Specific, assignable work items
- **Validation**: Must follow TDD principles
- **Database**: Stored in `tasks` table

### 9. Sub-Tasks (Detail Level)
- **Purpose**: Granular sub-components of tasks
- **Format**: Fine-grained implementation details
- **Validation**: Must be atomic and testable
- **Database**: Stored in `subtasks` table

## Planning Workflow

### 1. Discovery Phase
- **Identify Goal**: Understand what needs to be accomplished
- **Analyze Context**: Assess current state and constraints
- **Define Requirements**: Specify what success looks like

### 2. Design Phase
- **Develop Concept**: High-level approach and architecture
- **Identify Constraints**: Document limitations and boundaries
- **Plan Phases**: Break into major development stages

### 3. Implementation Planning
- **Create Steps**: Detailed implementation steps
- **Define Tasks**: Specific, assignable work items
- **Break Down Sub-Tasks**: Granular implementation details

### 4. Validation Phase
- **Review Planning**: Ensure completeness and correctness
- **Verify Dependencies**: Check for missing relationships
- **Validate Feasibility**: Confirm plan is achievable

## Database Integration

### Planning Tables Structure
```sql
-- Core planning hierarchy
goals (id, title, description, status, acceptance_criteria)
concepts (id, title, description, goal_id, technical_approach)
context (id, title, description, current_state, components)
constraints (id, title, description, goal_id, constraints_type)
requirements (id, title, description, goal_id, requirement_type)
phases (id, title, description, goal_id, estimated_duration, dependencies)
steps (id, title, description, phase_id, implementation_details)
tasks (id, title, description, step_id, status, assignee)
subtasks (id, title, description, task_id, status, implementation_notes)
```

### Planning Operations
```bash
# View planning hierarchy
python -m todowrite_cli planning show --goal-id <goal_id>

# Create new planning element
python -m todowrite_cli planning create --type task --title "Implement User Model"

# Update planning status
python -m todowrite_cli planning update --task-id <task_id> --status "in_progress"

# Validate planning completeness
python -m todowrite_cli planning validate --goal-id <goal_id>
```

## Compliance Requirements

### Mandatory Planning Validation
Before any code implementation:

1. ✅ Goal exists and is approved
2. ✅ Concept is defined and technically sound
3. ✅ Context is understood and documented
4. ✅ Constraints are identified and documented
5. ✅ Requirements are specific and measurable
6. ✅ Phases are logical and achievable
7. ✅ Steps are detailed and actionable
8. ✅ Tasks are specific and assignable
9. ✅ Sub-tasks are granular and testable

### Anti-Patterns (Forbidden)

- **Code-first approach**: Writing code without planning hierarchy
- **"Quick fix" exception**: Bypassing planning for "simple" changes
- **Incomplete planning**: Missing levels in the hierarchy
- **Vague requirements**: Non-specific, unmeasurable requirements
- **Unconnected elements**: Tasks not linked to higher-level goals

## Planning Tools Integration

### Models API Usage
```python
from todowrite.core.models import (
    Goal, Concept, Context, Constraints, Requirements,
    AcceptanceCriteria, InterfaceContract, Phase, Step,
    Task, SubTask, Command, Label
)

# Create planning hierarchy
goal = Goal(title="My Goal", description="Goal description")
concept = Concept(title="My Concept", description="Concept description")
# ... continue with hierarchy
```

### CLI Integration
```bash
# Planning commands
todowrite goal create "Implement Feature X"
todowrite concept create "Microservices Architecture" --goal-id 1
todowrite task create "Create user service" --step-id 5

# Planning visualization
todowrite planning tree --goal-id 1
todowrite planning gantt --phase-id 3
todowrite planning burndown --task-id 10
```

### Enforcement
- **CLAUDE.md enforcement**: Requires planning hierarchy before code
- **Startup verification**: Validates active goals exist
- **TDD integration**: Tests trace back to planning requirements
- **Database authority**: All planning stored in PostgreSQL
