-- ToDoWrite Database Schema with Proper Data Types
-- All timestamps use TIMESTAMP WITH TIME ZONE (UTC)
-- All status/severity/work_type use proper ENUM types
-- All progress fields are INTEGER with 0-100 constraints

-- Create ENUM types
CREATE TYPE status_enum AS ENUM ('planned', 'pending', 'active', 'in_progress', 'completed', 'on_hold', 'cancelled');
CREATE TYPE severity_enum AS ENUM ('low', 'medium', 'high', 'critical');
CREATE TYPE work_type_enum AS ENUM ('frontend', 'backend', 'full-stack', 'devops', 'database', 'security', 'testing', 'documentation', 'architecture', 'payment', 'ui_ux', 'design', 'research', 'analysis', 'planning', 'deployment', 'maintenance');

-- Core Model Tables
CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    status status_enum NOT NULL DEFAULT 'planned',
    progress INTEGER CHECK (progress >= 0 AND progress <= 100) DEFAULT 0,
    started_date TIMESTAMP WITH TIME ZONE,
    completion_date TIMESTAMP WITH TIME ZONE,
    owner VARCHAR,
    severity severity_enum,
    work_type work_type_enum,
    assignee VARCHAR,
    extra_data TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE phases (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    status status_enum NOT NULL DEFAULT 'planned',
    progress INTEGER CHECK (progress >= 0 AND progress <= 100) DEFAULT 0,
    started_date TIMESTAMP WITH TIME ZONE,
    completion_date TIMESTAMP WITH TIME ZONE,
    owner VARCHAR,
    severity severity_enum,
    work_type work_type_enum,
    assignee VARCHAR,
    extra_data TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE steps (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    status status_enum NOT NULL DEFAULT 'planned',
    progress INTEGER CHECK (progress >= 0 AND progress <= 100) DEFAULT 0,
    started_date TIMESTAMP WITH TIME ZONE,
    completion_date TIMESTAMP WITH TIME ZONE,
    owner VARCHAR,
    severity severity_enum,
    work_type work_type_enum,
    assignee VARCHAR,
    extra_data TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    status status_enum NOT NULL DEFAULT 'planned',
    progress INTEGER CHECK (progress >= 0 AND progress <= 100) DEFAULT 0,
    started_date TIMESTAMP WITH TIME ZONE,
    completion_date TIMESTAMP WITH TIME ZONE,
    owner VARCHAR,
    severity severity_enum,
    work_type work_type_enum,
    assignee VARCHAR,
    extra_data TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sub_tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    status status_enum NOT NULL DEFAULT 'planned',
    progress INTEGER CHECK (progress >= 0 AND progress <= 100) DEFAULT 0,
    started_date TIMESTAMP WITH TIME ZONE,
    completion_date TIMESTAMP WITH TIME ZONE,
    owner VARCHAR,
    severity severity_enum,
    work_type work_type_enum,
    assignee VARCHAR,
    extra_data TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE commands (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    status status_enum NOT NULL DEFAULT 'pending',
    progress INTEGER CHECK (progress >= 0 AND progress <= 100) DEFAULT 0,
    started_date TIMESTAMP WITH TIME ZONE,
    completion_date TIMESTAMP WITH TIME ZONE,
    owner VARCHAR,
    severity severity_enum,
    work_type work_type_enum,
    assignee VARCHAR,
    acceptance_criteria_id INTEGER,
    cmd TEXT,
    cmd_params TEXT,
    runtime_env TEXT,
    output TEXT,
    artifacts TEXT,
    extra_data TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE concepts (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    status status_enum NOT NULL DEFAULT 'planned',
    progress INTEGER CHECK (progress >= 0 AND progress <= 100) DEFAULT 0,
    started_date TIMESTAMP WITH TIME ZONE,
    completion_date TIMESTAMP WITH TIME ZONE,
    owner VARCHAR,
    severity severity_enum,
    work_type work_type_enum,
    assignee VARCHAR,
    extra_data TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE constraints (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    status status_enum NOT NULL DEFAULT 'planned',
    progress INTEGER CHECK (progress >= 0 AND progress <= 100) DEFAULT 0,
    started_date TIMESTAMP WITH TIME ZONE,
    completion_date TIMESTAMP WITH TIME ZONE,
    owner VARCHAR,
    severity severity_enum,
    work_type work_type_enum,
    assignee VARCHAR,
    extra_data TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contexts (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    status status_enum NOT NULL DEFAULT 'planned',
    progress INTEGER CHECK (progress >= 0 AND progress <= 100) DEFAULT 0,
    started_date TIMESTAMP WITH TIME ZONE,
    completion_date TIMESTAMP WITH TIME ZONE,
    owner VARCHAR,
    severity severity_enum,
    work_type work_type_enum,
    assignee VARCHAR,
    extra_data TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE interface_contracts (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    status status_enum NOT NULL DEFAULT 'planned',
    progress INTEGER CHECK (progress >= 0 AND progress <= 100) DEFAULT 0,
    started_date TIMESTAMP WITH TIME ZONE,
    completion_date TIMESTAMP WITH TIME ZONE,
    owner VARCHAR,
    severity severity_enum,
    work_type work_type_enum,
    assignee VARCHAR,
    extra_data TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE labels (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE requirements (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    status status_enum NOT NULL DEFAULT 'planned',
    progress INTEGER CHECK (progress >= 0 AND progress <= 100) DEFAULT 0,
    started_date TIMESTAMP WITH TIME ZONE,
    completion_date TIMESTAMP WITH TIME ZONE,
    owner VARCHAR,
    severity severity_enum,
    work_type work_type_enum,
    assignee VARCHAR,
    extra_data TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE acceptance_criteria (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    status status_enum NOT NULL DEFAULT 'planned',
    progress INTEGER CHECK (progress >= 0 AND progress <= 100) DEFAULT 0,
    started_date TIMESTAMP WITH TIME ZONE,
    completion_date TIMESTAMP WITH TIME ZONE,
    owner VARCHAR,
    severity severity_enum,
    work_type work_type_enum,
    assignee VARCHAR,
    extra_data TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Association Tables with proper INTEGER foreign keys and CASCADE DELETE
CREATE TABLE goals_phases (
    goal_id INTEGER NOT NULL REFERENCES goals(id) ON DELETE CASCADE,
    phase_id INTEGER NOT NULL REFERENCES phases(id) ON DELETE CASCADE,
    PRIMARY KEY (goal_id, phase_id)
);

CREATE TABLE phases_steps (
    phase_id INTEGER NOT NULL REFERENCES phases(id) ON DELETE CASCADE,
    step_id INTEGER NOT NULL REFERENCES steps(id) ON DELETE CASCADE,
    PRIMARY KEY (phase_id, step_id)
);

CREATE TABLE steps_tasks (
    step_id INTEGER NOT NULL REFERENCES steps(id) ON DELETE CASCADE,
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    PRIMARY KEY (step_id, task_id)
);

CREATE TABLE tasks_sub_tasks (
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    sub_task_id INTEGER NOT NULL REFERENCES sub_tasks(id) ON DELETE CASCADE,
    PRIMARY KEY (task_id, sub_task_id)
);

CREATE TABLE sub_tasks_commands (
    sub_task_id INTEGER NOT NULL REFERENCES sub_tasks(id) ON DELETE CASCADE,
    command_id INTEGER NOT NULL REFERENCES commands(id) ON DELETE CASCADE,
    PRIMARY KEY (sub_task_id, command_id)
);

CREATE TABLE goals_tasks (
    goal_id INTEGER NOT NULL REFERENCES goals(id) ON DELETE CASCADE,
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    PRIMARY KEY (goal_id, task_id)
);

CREATE TABLE constraints_goals (
    constraint_id INTEGER NOT NULL REFERENCES constraints(id) ON DELETE CASCADE,
    goal_id INTEGER NOT NULL REFERENCES goals(id) ON DELETE CASCADE,
    PRIMARY KEY (constraint_id, goal_id)
);

CREATE TABLE constraints_requirements (
    constraint_id INTEGER NOT NULL REFERENCES constraints(id) ON DELETE CASCADE,
    requirement_id INTEGER NOT NULL REFERENCES requirements(id) ON DELETE CASCADE,
    PRIMARY KEY (constraint_id, requirement_id)
);

CREATE TABLE concepts_contexts (
    concept_id INTEGER NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    context_id INTEGER NOT NULL REFERENCES contexts(id) ON DELETE CASCADE,
    PRIMARY KEY (concept_id, context_id)
);

CREATE TABLE concepts_goals (
    concept_id INTEGER NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    goal_id INTEGER NOT NULL REFERENCES goals(id) ON DELETE CASCADE,
    PRIMARY KEY (concept_id, goal_id)
);

CREATE TABLE contexts_goals (
    context_id INTEGER NOT NULL REFERENCES contexts(id) ON DELETE CASCADE,
    goal_id INTEGER NOT NULL REFERENCES goals(id) ON DELETE CASCADE,
    PRIMARY KEY (context_id, goal_id)
);

CREATE TABLE contexts_requirements (
    context_id INTEGER NOT NULL REFERENCES contexts(id) ON DELETE CASCADE,
    requirement_id INTEGER NOT NULL REFERENCES requirements(id) ON DELETE CASCADE,
    PRIMARY KEY (context_id, requirement_id)
);

CREATE TABLE requirements_acceptance_criteria (
    requirement_id INTEGER NOT NULL REFERENCES requirements(id) ON DELETE CASCADE,
    acceptance_criteria_id INTEGER NOT NULL REFERENCES acceptance_criteria(id) ON DELETE CASCADE,
    PRIMARY KEY (requirement_id, acceptance_criteria_id)
);

CREATE TABLE requirements_concepts (
    requirement_id INTEGER NOT NULL REFERENCES requirements(id) ON DELETE CASCADE,
    concept_id INTEGER NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    PRIMARY KEY (requirement_id, concept_id)
);

CREATE TABLE acceptance_criteria_interface_contracts (
    acceptance_criteria_id INTEGER NOT NULL REFERENCES acceptance_criteria(id) ON DELETE CASCADE,
    interface_contract_id INTEGER NOT NULL REFERENCES interface_contracts(id) ON DELETE CASCADE,
    PRIMARY KEY (acceptance_criteria_id, interface_contract_id)
);

CREATE TABLE interface_contracts_phases (
    interface_contract_id INTEGER NOT NULL REFERENCES interface_contracts(id) ON DELETE CASCADE,
    phase_id INTEGER NOT NULL REFERENCES phases(id) ON DELETE CASCADE,
    PRIMARY KEY (interface_contract_id, phase_id)
);

-- Label association tables
CREATE TABLE goals_labels (
    goal_id INTEGER NOT NULL REFERENCES goals(id) ON DELETE CASCADE,
    label_id INTEGER NOT NULL REFERENCES labels(id) ON DELETE CASCADE,
    PRIMARY KEY (goal_id, label_id)
);

CREATE TABLE phases_labels (
    phase_id INTEGER NOT NULL REFERENCES phases(id) ON DELETE CASCADE,
    label_id INTEGER NOT NULL REFERENCES labels(id) ON DELETE CASCADE,
    PRIMARY KEY (phase_id, label_id)
);

CREATE TABLE steps_labels (
    step_id INTEGER NOT NULL REFERENCES steps(id) ON DELETE CASCADE,
    label_id INTEGER NOT NULL REFERENCES labels(id) ON DELETE CASCADE,
    PRIMARY KEY (step_id, label_id)
);

CREATE TABLE tasks_labels (
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    label_id INTEGER NOT NULL REFERENCES labels(id) ON DELETE CASCADE,
    PRIMARY KEY (task_id, label_id)
);

CREATE TABLE sub_tasks_labels (
    sub_task_id INTEGER NOT NULL REFERENCES sub_tasks(id) ON DELETE CASCADE,
    label_id INTEGER NOT NULL REFERENCES labels(id) ON DELETE CASCADE,
    PRIMARY KEY (sub_task_id, label_id)
);

CREATE TABLE commands_labels (
    command_id INTEGER NOT NULL REFERENCES commands(id) ON DELETE CASCADE,
    label_id INTEGER NOT NULL REFERENCES labels(id) ON DELETE CASCADE,
    PRIMARY KEY (command_id, label_id)
);

CREATE TABLE concepts_labels (
    concept_id INTEGER NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    label_id INTEGER NOT NULL REFERENCES labels(id) ON DELETE CASCADE,
    PRIMARY KEY (concept_id, label_id)
);

CREATE TABLE constraints_labels (
    constraint_id INTEGER NOT NULL REFERENCES constraints(id) ON DELETE CASCADE,
    label_id INTEGER NOT NULL REFERENCES labels(id) ON DELETE CASCADE,
    PRIMARY KEY (constraint_id, label_id)
);

CREATE TABLE contexts_labels (
    context_id INTEGER NOT NULL REFERENCES contexts(id) ON DELETE CASCADE,
    label_id INTEGER NOT NULL REFERENCES labels(id) ON DELETE CASCADE,
    PRIMARY KEY (context_id, label_id)
);

CREATE TABLE interface_contracts_labels (
    interface_contract_id INTEGER NOT NULL REFERENCES interface_contracts(id) ON DELETE CASCADE,
    label_id INTEGER NOT NULL REFERENCES labels(id) ON DELETE CASCADE,
    PRIMARY KEY (interface_contract_id, label_id)
);

CREATE TABLE requirements_labels (
    requirement_id INTEGER NOT NULL REFERENCES requirements(id) ON DELETE CASCADE,
    label_id INTEGER NOT NULL REFERENCES labels(id) ON DELETE CASCADE,
    PRIMARY KEY (requirement_id, label_id)
);

CREATE TABLE acceptance_criteria_labels (
    acceptance_criteria_id INTEGER NOT NULL REFERENCES acceptance_criteria(id) ON DELETE CASCADE,
    label_id INTEGER NOT NULL REFERENCES labels(id) ON DELETE CASCADE,
    PRIMARY KEY (acceptance_criteria_id, label_id)
);

-- Add foreign key constraint for commands to acceptance_criteria
ALTER TABLE commands ADD CONSTRAINT commands_acceptance_criteria_id_fkey
    FOREIGN KEY (acceptance_criteria_id) REFERENCES acceptance_criteria(id) ON DELETE SET NULL;

-- Create indexes for better performance
CREATE INDEX idx_goals_status ON goals(status);
CREATE INDEX idx_goals_progress ON goals(progress);
CREATE INDEX idx_goals_created_at ON goals(created_at);

CREATE INDEX idx_phases_status ON phases(status);
CREATE INDEX idx_phases_progress ON phases(progress);

CREATE INDEX idx_steps_status ON steps(status);
CREATE INDEX idx_steps_progress ON steps(progress);

CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_progress ON tasks(progress);

CREATE INDEX idx_sub_tasks_status ON sub_tasks(status);
CREATE INDEX idx_sub_tasks_progress ON sub_tasks(progress);

CREATE INDEX idx_commands_status ON commands(status);
CREATE INDEX idx_commands_work_type ON commands(work_type);

CREATE INDEX idx_labels_name ON labels(name);

CREATE INDEX idx_goals_phases_goal_id ON goals_phases(goal_id);
CREATE INDEX idx_goals_phases_phase_id ON goals_phases(phase_id);

CREATE INDEX idx_phases_steps_phase_id ON phases_steps(phase_id);
CREATE INDEX idx_phases_steps_step_id ON phases_steps(step_id);

CREATE INDEX idx_steps_tasks_step_id ON steps_tasks(step_id);
CREATE INDEX idx_steps_tasks_task_id ON steps_tasks(task_id);

CREATE INDEX idx_tasks_sub_tasks_task_id ON tasks_sub_tasks(task_id);
CREATE INDEX idx_tasks_sub_tasks_sub_task_id ON tasks_sub_tasks(sub_task_id);

CREATE INDEX idx_sub_tasks_commands_sub_task_id ON sub_tasks_commands(sub_task_id);
CREATE INDEX idx_sub_tasks_commands_command_id ON sub_tasks_commands(command_id);

-- Create trigger to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply the trigger to all tables with updated_at
CREATE TRIGGER update_goals_updated_at BEFORE UPDATE ON goals FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_phases_updated_at BEFORE UPDATE ON phases FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_steps_updated_at BEFORE UPDATE ON steps FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sub_tasks_updated_at BEFORE UPDATE ON sub_tasks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_commands_updated_at BEFORE UPDATE ON commands FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_concepts_updated_at BEFORE UPDATE ON concepts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_constraints_updated_at BEFORE UPDATE ON constraints FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_contexts_updated_at BEFORE UPDATE ON contexts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_interface_contracts_updated_at BEFORE UPDATE ON interface_contracts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_requirements_updated_at BEFORE UPDATE ON requirements FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_acceptance_criteria_updated_at BEFORE UPDATE ON acceptance_criteria FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_labels_updated_at BEFORE UPDATE ON labels FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
