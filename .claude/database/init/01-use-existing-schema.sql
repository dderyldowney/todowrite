-- Use existing ToDoWrite schema from lib_package
-- This script verifies that the existing schema is properly initialized
-- and sets up the todowrite database for use with the existing Models API

-- Check if we're connecting to the right database
SELECT current_database() AS current_db;

-- Verify that the todowrite schema exists (should be created by existing ToDoWrite Models)
-- The existing models use standard table names: goals, concepts, contexts, etc.

-- Enable extensions that existing ToDoWrite models might need
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create a session tracking table that doesn't conflict with existing models
CREATE TABLE IF NOT EXISTS todowrite_sessions (
    id SERIAL PRIMARY KEY,
    session_id TEXT NOT NULL UNIQUE,
    title TEXT,
    description TEXT,
    environment JSONB DEFAULT '{}',
    context JSONB DEFAULT '{}',
    current_focus_layer TEXT,
    current_focus_id INTEGER,
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    actions JSONB DEFAULT '[]',
    conversations JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,

    CONSTRAINT todowrite_sessions_session_id_not_empty CHECK (length(trim(session_id)) > 0)
);

-- Create indexes for session table
CREATE INDEX IF NOT EXISTS idx_todowrite_sessions_session_id ON todowrite_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_todowrite_sessions_last_activity ON todowrite_sessions(last_activity);

-- Create cross-session planning table
CREATE TABLE IF NOT EXISTS todowrite_planning_sessions (
    id SERIAL PRIMARY KEY,
    session_id TEXT NOT NULL,
    planning_type TEXT NOT NULL, -- 'strategic', 'tactical', 'implementation'
    focus_area TEXT,
    context_summary TEXT,
    decisions JSONB DEFAULT '[]',
    action_items JSONB DEFAULT '[]',
    next_steps JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_todowrite_planning_sessions_session_id ON todowrite_planning_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_todowrite_planning_sessions_type ON todowrite_planning_sessions(planning_type);

-- Create migration tracking for this setup
CREATE TABLE IF NOT EXISTS todowrite_migration_log (
    id SERIAL PRIMARY KEY,
    version VARCHAR(20) NOT NULL,
    description TEXT,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    checksum VARCHAR(64)
);

-- Insert migration record
INSERT INTO todowrite_migration_log (version, description, checksum)
VALUES ('1.0.0', 'PostgreSQL backend setup for existing ToDoWrite Models API', 'existing_schema_setup')
ON CONFLICT (version) DO NOTHING;

-- Verify we can see the existing ToDoWrite tables (if they exist)
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name LIKE '%goal%' OR table_name LIKE '%concept%' OR table_name LIKE '%context%'
ORDER BY table_name;