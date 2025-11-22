-- Basic MCP Filesystem Service Database Schema
-- Minimal tables for filesystem operations tracking

-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_migrations (
    id SERIAL PRIMARY KEY,
    version VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    checksum VARCHAR(64)
);

-- File operations tracking
CREATE TABLE IF NOT EXISTS file_operations (
    id SERIAL PRIMARY KEY,
    operation_type VARCHAR(50) NOT NULL, -- read, write, list, delete
    file_path TEXT NOT NULL,
    session_id TEXT,
    status VARCHAR(20) DEFAULT 'completed', -- pending, completed, failed
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- File access cache for performance
CREATE TABLE IF NOT EXISTS file_cache (
    id SERIAL PRIMARY KEY,
    file_path TEXT UNIQUE NOT NULL,
    file_size BIGINT,
    file_hash VARCHAR(64),
    last_modified TIMESTAMP WITH TIME ZONE,
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_file_operations_session_id ON file_operations(session_id);
CREATE INDEX IF NOT EXISTS idx_file_operations_status ON file_operations(status);
CREATE INDEX IF NOT EXISTS idx_file_operations_created_at ON file_operations(created_at);
CREATE INDEX IF NOT EXISTS idx_file_cache_file_path ON file_cache(file_path);
CREATE INDEX IF NOT EXISTS idx_file_cache_last_accessed ON file_cache(last_accessed);

-- Insert initial schema version
INSERT INTO schema_migrations (version, description, checksum)
VALUES
('1.0.0', 'Initial MCP Fileservice database schema', 'initial')
ON CONFLICT (version) DO NOTHING;
