-- ToDoWrite Database CASCADE DELETE Constraints
-- ==========================================
--
-- This SQL script adds CASCADE DELETE constraints to the ToDoWrite database
-- to ensure automatic cleanup of child entities when parent entities are deleted.
--
-- Usage:
--   psql -U your_user -d your_todowrite_database -f cascade_constraints.sql
--
-- Effect:
--   When Goal(id).delete() is called, all associated phases, steps, tasks,
--   sub-tasks, and relationships are automatically deleted, preventing orphaned data.
--
-- Compatible with:
--   - PostgreSQL 12+
--   - ToDoWrite library users with todowrite database only

-- Add CASCADE DELETE to hierarchy constraints for proper cleanup
-- This ensures that when Goal(id).delete() is called, all associated entities are automatically deleted

-- Goals -> Junction Tables (CASCADE on delete from goals)
ALTER TABLE goals_phases DROP CONSTRAINT IF EXISTS goals_phases_goal_id_fkey;
ALTER TABLE goals_phases ADD CONSTRAINT goals_phases_goal_id_fkey
    FOREIGN KEY (goal_id) REFERENCES goals(id) ON DELETE CASCADE;

ALTER TABLE goals_concepts DROP CONSTRAINT IF EXISTS goals_concepts_goal_id_fkey;
ALTER TABLE goals_concepts ADD CONSTRAINT goals_concepts_goal_id_fkey
    FOREIGN KEY (goal_id) REFERENCES goals(id) ON DELETE CASCADE;

ALTER TABLE goals_contexts DROP CONSTRAINT IF EXISTS goals_contexts_goal_id_fkey;
ALTER TABLE goals_contexts ADD CONSTRAINT goals_contexts_goal_id_fkey
    FOREIGN KEY (goal_id) REFERENCES goals(id) ON DELETE CASCADE;

ALTER TABLE goals_tasks DROP CONSTRAINT IF EXISTS goals_tasks_goal_id_fkey;
ALTER TABLE goals_tasks ADD CONSTRAINT goals_tasks_goal_id_fkey
    FOREIGN KEY (goal_id) REFERENCES goals(id) ON DELETE CASCADE;

ALTER TABLE constraints_goals DROP CONSTRAINT IF EXISTS constraints_goals_goal_id_fkey;
ALTER TABLE constraints_goals ADD CONSTRAINT constraints_goals_goal_id_fkey
    FOREIGN KEY (goal_id) REFERENCES goals(id) ON DELETE CASCADE;

-- Phases -> Junction Tables (CASCADE on delete from phases)
ALTER TABLE goals_phases DROP CONSTRAINT IF EXISTS goals_phases_phase_id_fkey;
ALTER TABLE goals_phases ADD CONSTRAINT goals_phases_phase_id_fkey
    FOREIGN KEY (phase_id) REFERENCES phases(id) ON DELETE CASCADE;

ALTER TABLE phases_steps DROP CONSTRAINT IF EXISTS phases_steps_phase_id_fkey;
ALTER TABLE phases_steps ADD CONSTRAINT phases_steps_phase_id_fkey
    FOREIGN KEY (phase_id) REFERENCES phases(id) ON DELETE CASCADE;

ALTER TABLE interface_contracts_phases DROP CONSTRAINT IF EXISTS interface_contracts_phases_phase_id_fkey;
ALTER TABLE interface_contracts_phases ADD CONSTRAINT interface_contracts_phases_phase_id_fkey
    FOREIGN KEY (phase_id) REFERENCES phases(id) ON DELETE CASCADE;

-- Steps -> Junction Tables (CASCADE on delete from steps)
ALTER TABLE phases_steps DROP CONSTRAINT IF EXISTS phases_steps_step_id_fkey;
ALTER TABLE phases_steps ADD CONSTRAINT phases_steps_step_id_fkey
    FOREIGN KEY (step_id) REFERENCES steps(id) ON DELETE CASCADE;

ALTER TABLE steps_tasks DROP CONSTRAINT IF EXISTS steps_tasks_step_id_fkey;
ALTER TABLE steps_tasks ADD CONSTRAINT steps_tasks_step_id_fkey
    FOREIGN KEY (step_id) REFERENCES steps(id) ON DELETE CASCADE;

-- Tasks -> Junction Tables (CASCADE on delete from tasks)
ALTER TABLE steps_tasks DROP CONSTRAINT IF EXISTS steps_tasks_task_id_fkey;
ALTER TABLE steps_tasks ADD CONSTRAINT steps_tasks_task_id_fkey
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE;

ALTER TABLE tasks_sub_tasks DROP CONSTRAINT IF EXISTS tasks_sub_tasks_task_id_fkey;
ALTER TABLE tasks_sub_tasks ADD CONSTRAINT tasks_sub_tasks_task_id_fkey
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE;

-- Sub-Tasks -> Junction Tables (CASCADE on delete from sub_tasks)
ALTER TABLE tasks_sub_tasks DROP CONSTRAINT IF EXISTS tasks_sub_tasks_sub_task_id_fkey;
ALTER TABLE tasks_sub_tasks ADD CONSTRAINT tasks_sub_tasks_sub_task_id_fkey
    FOREIGN KEY (sub_task_id) REFERENCES sub_tasks(id) ON DELETE CASCADE;

ALTER TABLE sub_tasks_commands DROP CONSTRAINT IF EXISTS sub_tasks_commands_sub_task_id_fkey;
ALTER TABLE sub_tasks_commands ADD CONSTRAINT sub_tasks_commands_sub_task_id_fkey
    FOREIGN KEY (sub_task_id) REFERENCES sub_tasks(id) ON DELETE CASCADE;

-- Requirements -> Junction Tables (CASCADE on delete from requirements)
ALTER TABLE requirements_concepts DROP CONSTRAINT IF EXISTS requirements_concepts_requirement_id_fkey;
ALTER TABLE requirements_concepts ADD CONSTRAINT requirements_concepts_requirement_id_fkey
    FOREIGN KEY (requirement_id) REFERENCES requirements(id) ON DELETE CASCADE;

ALTER TABLE requirements_acceptance_criteria DROP CONSTRAINT IF EXISTS requirements_acceptance_criteria_requirement_id_fkey;
ALTER TABLE requirements_acceptance_criteria ADD CONSTRAINT requirements_acceptance_criteria_requirement_id_fkey
    FOREIGN KEY (requirement_id) REFERENCES requirements(id) ON DELETE CASCADE;

-- Acceptance Criteria -> Junction Tables (CASCADE on delete from acceptance_criteria)
ALTER TABLE requirements_acceptance_criteria DROP CONSTRAINT IF EXISTS requirements_acceptance_criteria_acceptance_criterion_id_fkey;
ALTER TABLE requirements_acceptance_criteria ADD CONSTRAINT requirements_acceptance_criteria_acceptance_criterion_id_fkey
    FOREIGN KEY (acceptance_criterion_id) REFERENCES acceptance_criteria(id) ON DELETE CASCADE;

ALTER TABLE acceptance_criteria_interface_contracts DROP CONSTRAINT IF EXISTS acceptance_criteria_interface_cont_acceptance_criterion_id_fkey;
ALTER TABLE acceptance_criteria_interface_contracts ADD CONSTRAINT acceptance_criteria_interface_cont_acceptance_criterion_id_fkey
    FOREIGN KEY (acceptance_criterion_id) REFERENCES acceptance_criteria(id) ON DELETE CASCADE;

-- Commands -> Junction Tables (CASCADE on delete from commands)
ALTER TABLE sub_tasks_commands DROP CONSTRAINT IF EXISTS sub_tasks_commands_command_id_fkey;
ALTER TABLE sub_tasks_commands ADD CONSTRAINT sub_tasks_commands_command_id_fkey
    FOREIGN KEY (command_id) REFERENCES commands(id) ON DELETE CASCADE;
