-- Migration 001: Fix Data Types and Constraints
-- This migration fixes improper data types and adds proper constraints

-- Fix progress fields (should be INTEGER with 0-100 constraint)
DO $$
BEGIN
    -- Goals table
    ALTER TABLE goals DROP CONSTRAINT IF EXISTS goals_progress_check;
    ALTER TABLE goals ADD CONSTRAINT goals_progress_check CHECK (progress >= 0 AND progress <= 100);

    -- Phases table
    ALTER TABLE phases DROP CONSTRAINT IF EXISTS phases_progress_check;
    ALTER TABLE phases ADD CONSTRAINT phases_progress_check CHECK (progress >= 0 AND progress <= 100);

    -- Steps table
    ALTER TABLE steps DROP CONSTRAINT IF EXISTS steps_progress_check;
    ALTER TABLE steps ADD CONSTRAINT steps_progress_check CHECK (progress >= 0 AND progress <= 100);

    -- Tasks table
    ALTER TABLE tasks DROP CONSTRAINT IF EXISTS tasks_progress_check;
    ALTER TABLE tasks ADD CONSTRAINT tasks_progress_check CHECK (progress >= 0 AND progress <= 100);

    -- Sub-tasks table
    ALTER TABLE sub_tasks DROP CONSTRAINT IF EXISTS sub_tasks_progress_check;
    ALTER TABLE sub_tasks ADD CONSTRAINT sub_tasks_progress_check CHECK (progress >= 0 AND progress <= 100);
END $$;

-- Create ENUM types for status, severity, and work_type
CREATE TYPE status_enum AS ENUM ('planned', 'pending', 'active', 'in_progress', 'completed', 'on_hold', 'cancelled');
CREATE TYPE severity_enum AS ENUM ('low', 'medium', 'high', 'critical');
CREATE TYPE work_type_enum AS ENUM ('frontend', 'backend', 'full-stack', 'devops', 'database', 'security', 'testing', 'documentation', 'architecture', 'payment', 'ui_ux', 'design', 'research', 'analysis', 'planning', 'deployment', 'maintenance');

-- Convert status columns to ENUMs (handle existing values)
ALTER TABLE goals ALTER COLUMN status TYPE status_enum USING CASE WHEN status = 'active' THEN 'active'::status_enum WHEN status = 'planned' THEN 'planned'::status_enum ELSE 'planned'::status_enum END;
ALTER TABLE phases ALTER COLUMN status TYPE status_enum USING status::status_enum;
ALTER TABLE steps ALTER COLUMN status TYPE status_enum USING status::status_enum;
ALTER TABLE tasks ALTER COLUMN status TYPE status_enum USING status::status_enum;
ALTER TABLE sub_tasks ALTER COLUMN status TYPE status_enum USING status::status_enum;
ALTER TABLE acceptance_criteria ALTER COLUMN status TYPE status_enum USING status::status_enum;
ALTER TABLE commands ALTER COLUMN status TYPE status_enum USING CASE WHEN status = 'pending' THEN 'pending'::status_enum WHEN status = 'planned' THEN 'planned'::status_enum ELSE 'pending'::status_enum END;
ALTER TABLE concepts ALTER COLUMN status TYPE status_enum USING status::status_enum;
ALTER TABLE constraints ALTER COLUMN status TYPE status_enum USING status::status_enum;
ALTER TABLE contexts ALTER COLUMN status TYPE status_enum USING status::status_enum;
ALTER TABLE interface_contracts ALTER COLUMN status TYPE status_enum USING status::status_enum;
ALTER TABLE requirements ALTER COLUMN status TYPE status_enum USING status::status_enum;

-- Convert severity columns to ENUMs
ALTER TABLE goals ALTER COLUMN severity TYPE severity_enum USING severity::severity_enum;
ALTER TABLE phases ALTER COLUMN severity TYPE severity_enum USING severity::severity_enum;
ALTER TABLE steps ALTER COLUMN severity TYPE severity_enum USING severity::severity_enum;
ALTER TABLE tasks ALTER COLUMN severity TYPE severity_enum USING severity::severity_enum;
ALTER TABLE sub_tasks ALTER COLUMN severity TYPE severity_enum USING severity::severity_enum;
ALTER TABLE acceptance_criteria ALTER COLUMN severity TYPE severity_enum USING severity::severity_enum;
ALTER TABLE commands ALTER COLUMN severity TYPE severity_enum USING severity::severity_enum;
ALTER TABLE concepts ALTER COLUMN severity TYPE severity_enum USING severity::severity_enum;
ALTER TABLE constraints ALTER COLUMN severity TYPE severity_enum USING severity::severity_enum;
ALTER TABLE contexts ALTER COLUMN severity TYPE severity_enum USING severity::severity_enum;
ALTER TABLE interface_contracts ALTER COLUMN severity TYPE severity_enum USING severity::severity_enum;
ALTER TABLE requirements ALTER COLUMN severity TYPE severity_enum USING severity::severity_enum;

-- Convert work_type columns to ENUMs
ALTER TABLE goals ALTER COLUMN work_type TYPE work_type_enum USING work_type::work_type_enum;
ALTER TABLE phases ALTER COLUMN work_type TYPE work_type_enum USING work_type::work_type_enum;
ALTER TABLE steps ALTER COLUMN work_type TYPE work_type_enum USING work_type::work_type_enum;
ALTER TABLE tasks ALTER COLUMN work_type TYPE work_type_enum USING work_type::work_type_enum;
ALTER TABLE sub_tasks ALTER COLUMN work_type TYPE work_type_enum USING work_type::work_type_enum;
ALTER TABLE commands ALTER COLUMN work_type TYPE work_type_enum USING CASE WHEN work_type = 'database' THEN 'database'::work_type_enum WHEN work_type = 'devops' THEN 'devops'::work_type_enum ELSE 'database'::work_type_enum END;
ALTER TABLE concepts ALTER COLUMN work_type TYPE work_type_enum USING work_type::work_type_enum;
ALTER TABLE constraints ALTER COLUMN work_type TYPE work_type_enum USING work_type::work_type_enum;
ALTER TABLE contexts ALTER COLUMN work_type TYPE work_type_enum USING work_type::work_type_enum;
ALTER TABLE interface_contracts ALTER COLUMN work_type TYPE work_type_enum USING work_type::work_type_enum;
ALTER TABLE requirements ALTER COLUMN work_type TYPE work_type_enum USING work_type::work_type_enum;

-- Fix timestamp columns - convert from VARCHAR to TIMESTAMP WITH TIME ZONE
-- Note: This will only work if existing data is in valid ISO format
DO $$
BEGIN
    -- Goals table timestamps
    ALTER TABLE goals ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE goals ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE USING updated_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE goals ALTER COLUMN started_date TYPE TIMESTAMP WITH TIME ZONE USING started_date::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE goals ALTER COLUMN completion_date TYPE TIMESTAMP WITH TIME ZONE USING completion_date::TIMESTAMP WITH TIME ZONE;

    -- Phases table timestamps
    ALTER TABLE phases ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE phases ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE USING updated_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE phases ALTER COLUMN started_date TYPE TIMESTAMP WITH TIME ZONE USING started_date::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE phases ALTER COLUMN completion_date TYPE TIMESTAMP WITH TIME ZONE USING completion_date::TIMESTAMP WITH TIME ZONE;

    -- Steps table timestamps
    ALTER TABLE steps ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE steps ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE USING updated_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE steps ALTER COLUMN started_date TYPE TIMESTAMP WITH TIME ZONE USING started_date::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE steps ALTER COLUMN completion_date TYPE TIMESTAMP WITH TIME ZONE USING completion_date::TIMESTAMP WITH TIME ZONE;

    -- Tasks table timestamps
    ALTER TABLE tasks ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE tasks ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE USING updated_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE tasks ALTER COLUMN started_date TYPE TIMESTAMP WITH TIME ZONE USING started_date::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE tasks ALTER COLUMN completion_date TYPE TIMESTAMP WITH TIME ZONE USING completion_date::TIMESTAMP WITH TIME ZONE;

    -- Sub-tasks table timestamps
    ALTER TABLE sub_tasks ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE sub_tasks ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE USING updated_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE sub_tasks ALTER COLUMN started_date TYPE TIMESTAMP WITH TIME ZONE USING started_date::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE sub_tasks ALTER COLUMN completion_date TYPE TIMESTAMP WITH TIME ZONE USING completion_date::TIMESTAMP WITH TIME ZONE;

    -- Acceptance Criteria table timestamps
    ALTER TABLE acceptance_criteria ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE acceptance_criteria ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE USING updated_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE acceptance_criteria ALTER COLUMN started_date TYPE TIMESTAMP WITH TIME ZONE USING started_date::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE acceptance_criteria ALTER COLUMN completion_date TYPE TIMESTAMP WITH TIME ZONE USING completion_date::TIMESTAMP WITH TIME ZONE;

    -- Commands table timestamps
    ALTER TABLE commands ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE commands ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE USING updated_at::TIMESTAMP WITH TIME ZONE;

    -- Concepts table timestamps
    ALTER TABLE concepts ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE concepts ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE USING updated_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE concepts ALTER COLUMN started_date TYPE TIMESTAMP WITH TIME ZONE USING started_date::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE concepts ALTER COLUMN completion_date TYPE TIMESTAMP WITH TIME ZONE USING completion_date::TIMESTAMP WITH TIME ZONE;

    -- Constraints table timestamps
    ALTER TABLE constraints ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE constraints ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE USING updated_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE constraints ALTER COLUMN started_date TYPE TIMESTAMP WITH TIME ZONE USING started_date::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE constraints ALTER COLUMN completion_date TYPE TIMESTAMP WITH TIME ZONE USING completion_date::TIMESTAMP WITH TIME ZONE;

    -- Contexts table timestamps
    ALTER TABLE contexts ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE contexts ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE USING updated_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE contexts ALTER COLUMN started_date TYPE TIMESTAMP WITH TIME ZONE USING started_date::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE contexts ALTER COLUMN completion_date TYPE TIMESTAMP WITH TIME ZONE USING completion_date::TIMESTAMP WITH TIME ZONE;

    -- Interface Contracts table timestamps
    ALTER TABLE interface_contracts ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE interface_contracts ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE USING updated_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE interface_contracts ALTER COLUMN started_date TYPE TIMESTAMP WITH TIME ZONE USING started_date::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE interface_contracts ALTER COLUMN completion_date TYPE TIMESTAMP WITH TIME ZONE USING completion_date::TIMESTAMP WITH TIME ZONE;

    -- Requirements table timestamps
    ALTER TABLE requirements ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE requirements ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE USING updated_at::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE requirements ALTER COLUMN started_date TYPE TIMESTAMP WITH TIME ZONE USING started_date::TIMESTAMP WITH TIME ZONE;
    ALTER TABLE requirements ALTER COLUMN completion_date TYPE TIMESTAMP WITH TIME ZONE USING completion_date::TIMESTAMP WITH TIME ZONE;
END $$;

-- Add NOT NULL constraints where appropriate
ALTER TABLE goals ALTER COLUMN title SET NOT NULL;
ALTER TABLE goals ALTER COLUMN status SET NOT NULL;
ALTER TABLE phases ALTER COLUMN title SET NOT NULL;
ALTER TABLE phases ALTER COLUMN status SET NOT NULL;
ALTER TABLE steps ALTER COLUMN title SET NOT NULL;
ALTER TABLE steps ALTER COLUMN status SET NOT NULL;
ALTER TABLE tasks ALTER COLUMN title SET NOT NULL;
ALTER TABLE tasks ALTER COLUMN status SET NOT NULL;
ALTER TABLE sub_tasks ALTER COLUMN title SET NOT NULL;
ALTER TABLE sub_tasks ALTER COLUMN status SET NOT NULL;
ALTER TABLE acceptance_criteria ALTER COLUMN title SET NOT NULL;
ALTER TABLE acceptance_criteria ALTER COLUMN status SET NOT NULL;
ALTER TABLE commands ALTER COLUMN title SET NOT NULL;
ALTER TABLE commands ALTER COLUMN status SET NOT NULL;
ALTER TABLE concepts ALTER COLUMN title SET NOT NULL;
ALTER TABLE concepts ALTER COLUMN status SET NOT NULL;
ALTER TABLE constraints ALTER COLUMN title SET NOT NULL;
ALTER TABLE constraints ALTER COLUMN status SET NOT NULL;
ALTER TABLE contexts ALTER COLUMN title SET NOT NULL;
ALTER TABLE contexts ALTER COLUMN status SET NOT NULL;
ALTER TABLE interface_contracts ALTER COLUMN title SET NOT NULL;
ALTER TABLE interface_contracts ALTER COLUMN status SET NOT NULL;
ALTER TABLE requirements ALTER COLUMN title SET NOT NULL;
ALTER TABLE requirements ALTER COLUMN status SET NOT NULL;

-- Add default status values
ALTER TABLE goals ALTER COLUMN status SET DEFAULT 'planned';
ALTER TABLE phases ALTER COLUMN status SET DEFAULT 'planned';
ALTER TABLE steps ALTER COLUMN status SET DEFAULT 'planned';
ALTER TABLE tasks ALTER COLUMN status SET DEFAULT 'planned';
ALTER TABLE sub_tasks ALTER COLUMN status SET DEFAULT 'planned';
ALTER TABLE acceptance_criteria ALTER COLUMN status SET DEFAULT 'planned';
ALTER TABLE commands ALTER COLUMN status SET DEFAULT 'pending';
ALTER TABLE concepts ALTER COLUMN status SET DEFAULT 'planned';
ALTER TABLE constraints ALTER COLUMN status SET DEFAULT 'planned';
ALTER TABLE contexts ALTER COLUMN status SET DEFAULT 'planned';
ALTER TABLE interface_contracts ALTER COLUMN status SET DEFAULT 'planned';
ALTER TABLE requirements ALTER COLUMN status SET DEFAULT 'planned';

-- Add default progress values
ALTER TABLE goals ALTER COLUMN progress SET DEFAULT 0;
ALTER TABLE phases ALTER COLUMN progress SET DEFAULT 0;
ALTER TABLE steps ALTER COLUMN progress SET DEFAULT 0;
ALTER TABLE tasks ALTER COLUMN progress SET DEFAULT 0;
ALTER TABLE sub_tasks ALTER COLUMN progress SET DEFAULT 0;
