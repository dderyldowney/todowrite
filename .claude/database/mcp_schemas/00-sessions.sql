-- MCP Sessions Database Schema
-- For Claude session persistence and tracking

-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_migrations (
    id SERIAL PRIMARY KEY,
    version VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    checksum VARCHAR(64)
);

-- Main sessions table (matches session manager expectations)
CREATE TABLE IF NOT EXISTS todowrite_sessions (
    id SERIAL PRIMARY KEY,
    session_id TEXT NOT NULL UNIQUE,
    title TEXT,
    description TEXT,
    status VARCHAR(20) DEFAULT 'active',

    -- Session metadata
    environment JSONB DEFAULT '{}',
    context JSONB DEFAULT '{}',

    -- Session state
    current_focus_id INTEGER,
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Session history
    actions JSONB DEFAULT '[]',
    conversations JSONB DEFAULT '[]',

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,

    CONSTRAINT todowrite_sessions_session_id_not_empty CHECK (length(trim(session_id)) > 0)
);

-- Session operations tracking
CREATE TABLE IF NOT EXISTS session_operations (
    id SERIAL PRIMARY KEY,
    session_id TEXT REFERENCES todowrite_sessions(session_id) ON DELETE CASCADE,
    operation_type VARCHAR(50) NOT NULL, -- save, load, restore, etc.
    status VARCHAR(20) DEFAULT 'completed', -- pending, completed, failed
    operation_details JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_todowrite_sessions_session_id ON todowrite_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_todowrite_sessions_status ON todowrite_sessions(status);
CREATE INDEX IF NOT EXISTS idx_todowrite_sessions_last_activity ON todowrite_sessions(last_activity);
CREATE INDEX IF NOT EXISTS idx_session_operations_session_id ON session_operations(session_id);
CREATE INDEX IF NOT EXISTS idx_session_operations_status ON session_operations(status);

-- Insert initial schema version
INSERT INTO schema_migrations (version, description, checksum)
VALUES
('1.0.0', 'Initial MCP Sessions database schema', 'initial')
ON CONFLICT (version) DO NOTHING;
