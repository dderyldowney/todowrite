-- ToDoWrite Database Schema - Generated from Models
-- This is the single source of truth for database schema
-- Field names follow standard ORM conventions: created_at, updated_at, started_on, ended_on
-- All IDs are INTEGER with proper constraints
-- All timestamps use TIMESTAMP WITH TIME ZONE for UTC storage
-- Association tables use standard practice without timestamps

-- Commands

CREATE TABLE IF NOT EXISTS commands (
	id SERIAL NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_on TIMESTAMP WITHOUT TIME ZONE,
	ended_on TIMESTAMP WITHOUT TIME ZONE,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	acceptance_criteria_id INTEGER,
	cmd TEXT,
	cmd_params TEXT,
	runtime_env TEXT,
	output TEXT,
	artifacts TEXT,
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (id)
)



-- Concepts

CREATE TABLE IF NOT EXISTS concepts (
	id SERIAL NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_on TIMESTAMP WITHOUT TIME ZONE,
	ended_on TIMESTAMP WITHOUT TIME ZONE,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (id)
)



-- Constraints

CREATE TABLE IF NOT EXISTS constraints (
	id SERIAL NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_on TIMESTAMP WITHOUT TIME ZONE,
	ended_on TIMESTAMP WITHOUT TIME ZONE,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (id)
)



-- Contexts

CREATE TABLE IF NOT EXISTS contexts (
	id SERIAL NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_on TIMESTAMP WITHOUT TIME ZONE,
	ended_on TIMESTAMP WITHOUT TIME ZONE,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (id)
)



-- Goals

CREATE TABLE IF NOT EXISTS goals (
	id SERIAL NOT NULL,
	title VARCHAR(255) NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER NOT NULL,
	started_on TIMESTAMP WITHOUT TIME ZONE,
	ended_on TIMESTAMP WITHOUT TIME ZONE,
	owner VARCHAR(255),
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR(255),
	extra_data TEXT,
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (id)
)



-- Labels

CREATE TABLE IF NOT EXISTS labels (
	id SERIAL NOT NULL,
	name VARCHAR NOT NULL,
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (name)
)



-- Phases

CREATE TABLE IF NOT EXISTS phases (
	id SERIAL NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_on TIMESTAMP WITHOUT TIME ZONE,
	ended_on TIMESTAMP WITHOUT TIME ZONE,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (id)
)



-- Requirements

CREATE TABLE IF NOT EXISTS requirements (
	id SERIAL NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_on TIMESTAMP WITHOUT TIME ZONE,
	ended_on TIMESTAMP WITHOUT TIME ZONE,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (id)
)



-- Steps

CREATE TABLE IF NOT EXISTS steps (
	id SERIAL NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_on TIMESTAMP WITHOUT TIME ZONE,
	ended_on TIMESTAMP WITHOUT TIME ZONE,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (id)
)



-- Tasks

CREATE TABLE IF NOT EXISTS tasks (
	id SERIAL NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_on TIMESTAMP WITHOUT TIME ZONE,
	ended_on TIMESTAMP WITHOUT TIME ZONE,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (id)
)



-- Association Tables

CREATE TABLE IF NOT EXISTS acceptance_criteria (
	id SERIAL NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_on TIMESTAMP WITHOUT TIME ZONE,
	ended_on TIMESTAMP WITHOUT TIME ZONE,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (id)
)




CREATE TABLE IF NOT EXISTS acceptance_criteria_interface_contracts (
	acceptance_criterion_id INTEGER,
	interface_contract_id INTEGER,
	FOREIGN KEY(acceptance_criterion_id) REFERENCES acceptance_criteria (id),
	FOREIGN KEY(interface_contract_id) REFERENCES interface_contracts (id)
)




CREATE TABLE IF NOT EXISTS acceptance_criteria_labels (
	acceptance_criterion_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(acceptance_criterion_id) REFERENCES acceptance_criteria (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
)




CREATE TABLE IF NOT EXISTS commands_labels (
	command_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(command_id) REFERENCES commands (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
)




CREATE TABLE IF NOT EXISTS concepts_contexts (
	concept_id INTEGER,
	context_id INTEGER,
	FOREIGN KEY(concept_id) REFERENCES concepts (id),
	FOREIGN KEY(context_id) REFERENCES contexts (id)
)




CREATE TABLE IF NOT EXISTS concepts_labels (
	concept_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(concept_id) REFERENCES concepts (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
)




CREATE TABLE IF NOT EXISTS constraints_goals (
	constraint_id INTEGER,
	goal_id INTEGER,
	FOREIGN KEY(constraint_id) REFERENCES constraints (id),
	FOREIGN KEY(goal_id) REFERENCES goals (id)
)




CREATE TABLE IF NOT EXISTS constraints_labels (
	constraint_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(constraint_id) REFERENCES constraints (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
)




CREATE TABLE IF NOT EXISTS constraints_requirements (
	constraint_id INTEGER,
	requirement_id INTEGER,
	FOREIGN KEY(constraint_id) REFERENCES constraints (id),
	FOREIGN KEY(requirement_id) REFERENCES requirements (id)
)




CREATE TABLE IF NOT EXISTS contexts_labels (
	context_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(context_id) REFERENCES contexts (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
)




CREATE TABLE IF NOT EXISTS goals_concepts (
	goal_id INTEGER,
	concept_id INTEGER,
	FOREIGN KEY(goal_id) REFERENCES goals (id),
	FOREIGN KEY(concept_id) REFERENCES concepts (id)
)




CREATE TABLE IF NOT EXISTS goals_contexts (
	goal_id INTEGER,
	context_id INTEGER,
	FOREIGN KEY(goal_id) REFERENCES goals (id),
	FOREIGN KEY(context_id) REFERENCES contexts (id)
)




CREATE TABLE IF NOT EXISTS goals_labels (
	goal_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(goal_id) REFERENCES goals (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
)




CREATE TABLE IF NOT EXISTS goals_phases (
	goal_id INTEGER,
	phase_id INTEGER,
	FOREIGN KEY(goal_id) REFERENCES goals (id),
	FOREIGN KEY(phase_id) REFERENCES phases (id)
)




CREATE TABLE IF NOT EXISTS goals_tasks (
	goal_id INTEGER,
	task_id INTEGER,
	FOREIGN KEY(goal_id) REFERENCES goals (id),
	FOREIGN KEY(task_id) REFERENCES tasks (id)
)




CREATE TABLE IF NOT EXISTS interface_contracts (
	id SERIAL NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_on TIMESTAMP WITHOUT TIME ZONE,
	ended_on TIMESTAMP WITHOUT TIME ZONE,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (id)
)




CREATE TABLE IF NOT EXISTS interface_contracts_labels (
	interface_contract_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(interface_contract_id) REFERENCES interface_contracts (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
)




CREATE TABLE IF NOT EXISTS interface_contracts_phases (
	interface_contract_id INTEGER,
	phase_id INTEGER,
	FOREIGN KEY(interface_contract_id) REFERENCES interface_contracts (id),
	FOREIGN KEY(phase_id) REFERENCES phases (id)
)




CREATE TABLE IF NOT EXISTS phases_labels (
	phase_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(phase_id) REFERENCES phases (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
)




CREATE TABLE IF NOT EXISTS phases_steps (
	phase_id INTEGER,
	step_id INTEGER,
	FOREIGN KEY(phase_id) REFERENCES phases (id),
	FOREIGN KEY(step_id) REFERENCES steps (id)
)




CREATE TABLE IF NOT EXISTS requirements_acceptance_criteria (
	requirement_id INTEGER,
	acceptance_criterion_id INTEGER,
	FOREIGN KEY(requirement_id) REFERENCES requirements (id),
	FOREIGN KEY(acceptance_criterion_id) REFERENCES acceptance_criteria (id)
)




CREATE TABLE IF NOT EXISTS requirements_concepts (
	requirement_id INTEGER,
	concept_id INTEGER,
	FOREIGN KEY(requirement_id) REFERENCES requirements (id),
	FOREIGN KEY(concept_id) REFERENCES concepts (id)
)




CREATE TABLE IF NOT EXISTS requirements_contexts (
	requirement_id INTEGER,
	context_id INTEGER,
	FOREIGN KEY(requirement_id) REFERENCES requirements (id),
	FOREIGN KEY(context_id) REFERENCES contexts (id)
)




CREATE TABLE IF NOT EXISTS requirements_labels (
	requirement_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(requirement_id) REFERENCES requirements (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
)




CREATE TABLE IF NOT EXISTS steps_labels (
	step_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(step_id) REFERENCES steps (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
)




CREATE TABLE IF NOT EXISTS steps_tasks (
	step_id INTEGER,
	task_id INTEGER,
	FOREIGN KEY(step_id) REFERENCES steps (id),
	FOREIGN KEY(task_id) REFERENCES tasks (id)
)




CREATE TABLE IF NOT EXISTS sub_tasks (
	id SERIAL NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_on TIMESTAMP WITHOUT TIME ZONE,
	ended_on TIMESTAMP WITHOUT TIME ZONE,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (id)
)




CREATE TABLE IF NOT EXISTS sub_tasks_commands (
	sub_task_id INTEGER,
	command_id INTEGER,
	FOREIGN KEY(sub_task_id) REFERENCES sub_tasks (id),
	FOREIGN KEY(command_id) REFERENCES commands (id)
)




CREATE TABLE IF NOT EXISTS sub_tasks_labels (
	sub_task_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(sub_task_id) REFERENCES sub_tasks (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
)




CREATE TABLE IF NOT EXISTS tasks_labels (
	task_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(task_id) REFERENCES tasks (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
)




CREATE TABLE IF NOT EXISTS tasks_sub_tasks (
	task_id INTEGER,
	sub_task_id INTEGER,
	FOREIGN KEY(task_id) REFERENCES tasks (id),
	FOREIGN KEY(sub_task_id) REFERENCES sub_tasks (id)
)



-- Indexes for Performance

-- Triggers for Automatic updated_at

-- Create trigger function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to all tables with updated_at

CREATE TRIGGER update_commands_updated_at BEFORE UPDATE ON commands FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_concepts_updated_at BEFORE UPDATE ON concepts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_constraints_updated_at BEFORE UPDATE ON constraints FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_contexts_updated_at BEFORE UPDATE ON contexts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_goals_updated_at BEFORE UPDATE ON goals FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_labels_updated_at BEFORE UPDATE ON labels FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_phases_updated_at BEFORE UPDATE ON phases FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_requirements_updated_at BEFORE UPDATE ON requirements FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_steps_updated_at BEFORE UPDATE ON steps FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
