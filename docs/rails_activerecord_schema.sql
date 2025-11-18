CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE goals (
	id INTEGER NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_date VARCHAR,
	completion_date VARCHAR,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at VARCHAR NOT NULL,
	updated_at VARCHAR NOT NULL,
	PRIMARY KEY (id)
);
CREATE TABLE concepts (
	id INTEGER NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_date VARCHAR,
	completion_date VARCHAR,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at VARCHAR NOT NULL,
	updated_at VARCHAR NOT NULL,
	PRIMARY KEY (id)
);
CREATE TABLE contexts (
	id INTEGER NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_date VARCHAR,
	completion_date VARCHAR,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at VARCHAR NOT NULL,
	updated_at VARCHAR NOT NULL,
	PRIMARY KEY (id)
);
CREATE TABLE constraints (
	id INTEGER NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_date VARCHAR,
	completion_date VARCHAR,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at VARCHAR NOT NULL,
	updated_at VARCHAR NOT NULL,
	PRIMARY KEY (id)
);
CREATE TABLE requirements (
	id INTEGER NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_date VARCHAR,
	completion_date VARCHAR,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at VARCHAR NOT NULL,
	updated_at VARCHAR NOT NULL,
	PRIMARY KEY (id)
);
CREATE TABLE acceptance_criteria (
	id INTEGER NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_date VARCHAR,
	completion_date VARCHAR,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at VARCHAR NOT NULL,
	updated_at VARCHAR NOT NULL,
	PRIMARY KEY (id)
);
CREATE TABLE interface_contracts (
	id INTEGER NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_date VARCHAR,
	completion_date VARCHAR,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at VARCHAR NOT NULL,
	updated_at VARCHAR NOT NULL,
	PRIMARY KEY (id)
);
CREATE TABLE phases (
	id INTEGER NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_date VARCHAR,
	completion_date VARCHAR,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at VARCHAR NOT NULL,
	updated_at VARCHAR NOT NULL,
	PRIMARY KEY (id)
);
CREATE TABLE steps (
	id INTEGER NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_date VARCHAR,
	completion_date VARCHAR,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at VARCHAR NOT NULL,
	updated_at VARCHAR NOT NULL,
	PRIMARY KEY (id)
);
CREATE TABLE tasks (
	id INTEGER NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_date VARCHAR,
	completion_date VARCHAR,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at VARCHAR NOT NULL,
	updated_at VARCHAR NOT NULL,
	PRIMARY KEY (id)
);
CREATE TABLE sub_tasks (
	id INTEGER NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_date VARCHAR,
	completion_date VARCHAR,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	extra_data TEXT,
	created_at VARCHAR NOT NULL,
	updated_at VARCHAR NOT NULL,
	PRIMARY KEY (id)
);
CREATE TABLE labels (
	id INTEGER NOT NULL,
	name VARCHAR NOT NULL,
	created_at VARCHAR NOT NULL,
	updated_at VARCHAR NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (name)
);
CREATE TABLE nodes (
	id BIGINT NOT NULL,
	layer VARCHAR NOT NULL,
	title VARCHAR NOT NULL,
	description TEXT,
	status VARCHAR NOT NULL,
	progress INTEGER,
	started_date VARCHAR,
	completion_date VARCHAR,
	owner VARCHAR,
	severity VARCHAR,
	work_type VARCHAR,
	assignee VARCHAR,
	PRIMARY KEY (id)
);
CREATE TABLE labels_nodes (
	node_id BIGINT NOT NULL,
	label_id BIGINT NOT NULL,
	PRIMARY KEY (node_id, label_id),
	FOREIGN KEY(node_id) REFERENCES nodes (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
);
CREATE TABLE goals_labels (
	goal_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(goal_id) REFERENCES goals (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
);
CREATE TABLE concepts_labels (
	concept_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(concept_id) REFERENCES concepts (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
);
CREATE TABLE contexts_labels (
	context_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(context_id) REFERENCES contexts (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
);
CREATE TABLE constraints_labels (
	constraint_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(constraint_id) REFERENCES constraints (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
);
CREATE TABLE requirements_labels (
	requirement_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(requirement_id) REFERENCES requirements (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
);
CREATE TABLE acceptance_criteria_labels (
	acceptance_criterion_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(acceptance_criterion_id) REFERENCES acceptance_criteria (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
);
CREATE TABLE interface_contracts_labels (
	interface_contract_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(interface_contract_id) REFERENCES interface_contracts (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
);
CREATE TABLE phases_labels (
	phase_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(phase_id) REFERENCES phases (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
);
CREATE TABLE steps_labels (
	step_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(step_id) REFERENCES steps (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
);
CREATE TABLE tasks_labels (
	task_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(task_id) REFERENCES tasks (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
);
CREATE TABLE sub_tasks_labels (
	sub_task_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY(sub_task_id) REFERENCES sub_tasks (id),
	FOREIGN KEY(label_id) REFERENCES labels (id)
);
CREATE TABLE constraints_goals (
	goal_id VARCHAR NOT NULL,
	constraint_id VARCHAR NOT NULL,
	PRIMARY KEY (goal_id, constraint_id),
	FOREIGN KEY(goal_id) REFERENCES nodes (id),
	FOREIGN KEY(constraint_id) REFERENCES nodes (id)
);
CREATE TABLE constraints_requirements (
	constraint_id VARCHAR NOT NULL,
	requirement_id VARCHAR NOT NULL,
	PRIMARY KEY (constraint_id, requirement_id),
	FOREIGN KEY(constraint_id) REFERENCES nodes (id),
	FOREIGN KEY(requirement_id) REFERENCES nodes (id)
);
CREATE TABLE requirements_acceptance_criteria (
	requirement_id VARCHAR NOT NULL,
	acceptance_criterion_id VARCHAR NOT NULL,
	PRIMARY KEY (requirement_id, acceptance_criterion_id),
	FOREIGN KEY(requirement_id) REFERENCES nodes (id),
	FOREIGN KEY(acceptance_criterion_id) REFERENCES nodes (id)
);
CREATE TABLE acceptance_criteria_interface_contracts (
	acceptance_criterion_id VARCHAR NOT NULL,
	interface_contract_id VARCHAR NOT NULL,
	PRIMARY KEY (acceptance_criterion_id, interface_contract_id),
	FOREIGN KEY(acceptance_criterion_id) REFERENCES nodes (id),
	FOREIGN KEY(interface_contract_id) REFERENCES nodes (id)
);
CREATE TABLE interface_contracts_phases (
	interface_contract_id VARCHAR NOT NULL,
	phase_id VARCHAR NOT NULL,
	PRIMARY KEY (interface_contract_id, phase_id),
	FOREIGN KEY(interface_contract_id) REFERENCES nodes (id),
	FOREIGN KEY(phase_id) REFERENCES nodes (id)
);
CREATE TABLE phases_steps (
	phase_id VARCHAR NOT NULL,
	step_id VARCHAR NOT NULL,
	PRIMARY KEY (phase_id, step_id),
	FOREIGN KEY(phase_id) REFERENCES nodes (id),
	FOREIGN KEY(step_id) REFERENCES nodes (id)
);
CREATE TABLE steps_tasks (
	step_id VARCHAR NOT NULL,
	task_id VARCHAR NOT NULL,
	PRIMARY KEY (step_id, task_id),
	FOREIGN KEY(step_id) REFERENCES nodes (id),
	FOREIGN KEY(task_id) REFERENCES nodes (id)
);
CREATE TABLE tasks_sub_tasks (
	task_id VARCHAR NOT NULL,
	sub_task_id VARCHAR NOT NULL,
	PRIMARY KEY (task_id, sub_task_id),
	FOREIGN KEY(task_id) REFERENCES nodes (id),
	FOREIGN KEY(sub_task_id) REFERENCES nodes (id)
);
CREATE TABLE sub_tasks_commands (
	sub_task_id VARCHAR NOT NULL,
	command_id VARCHAR NOT NULL,
	PRIMARY KEY (sub_task_id, command_id),
	FOREIGN KEY(sub_task_id) REFERENCES nodes (id),
	FOREIGN KEY(command_id) REFERENCES nodes (id)
);
CREATE TABLE links (
	parent_id VARCHAR NOT NULL,
	child_id VARCHAR NOT NULL,
	PRIMARY KEY (parent_id, child_id),
	FOREIGN KEY(parent_id) REFERENCES nodes (id),
	FOREIGN KEY(child_id) REFERENCES nodes (id)
);
CREATE TABLE commands (
	id INTEGER NOT NULL,
	node_id INTEGER NOT NULL,
	ac_ref VARCHAR NOT NULL,
	run_data TEXT,
	artifacts TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY(node_id) REFERENCES nodes (id)
);
CREATE TABLE development_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT,
            tasks_worked_on TEXT,
            commits_made INTEGER DEFAULT 0,
            description TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
CREATE TABLE session_tasks (
            session_id INTEGER NOT NULL,
            task_id INTEGER NOT NULL,
            time_spent_minutes INTEGER DEFAULT 0,
            notes TEXT,
            FOREIGN KEY (session_id) REFERENCES development_sessions(id),
            PRIMARY KEY (session_id, task_id)
        );
