-- Basic MCP Git Service Database Schema
-- Minimal tables for Git operations tracking

-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_migrations (
    id SERIAL PRIMARY KEY,
    version VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    checksum VARCHAR(64)
);

-- Git repositories tracking
CREATE TABLE IF NOT EXISTS git_repositories (
    id SERIAL PRIMARY KEY,
    repo_path TEXT UNIQUE NOT NULL,
    repo_url TEXT,
    branch TEXT DEFAULT 'main',
    is_bare BOOLEAN DEFAULT false,
    last_commit_hash VARCHAR(40),
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Git operations tracking
CREATE TABLE IF NOT EXISTS git_operations (
    id SERIAL PRIMARY KEY,
    repo_id INTEGER REFERENCES git_repositories(id) ON DELETE CASCADE,
    operation_type VARCHAR(50) NOT NULL, -- clone, pull, push, commit, checkout, status
    session_id TEXT,
    status VARCHAR(20) DEFAULT 'completed', -- pending, completed, failed
    details JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Git branches tracking
CREATE TABLE IF NOT EXISTS git_branches (
    id SERIAL PRIMARY KEY,
    repo_id INTEGER REFERENCES git_repositories(id) ON DELETE CASCADE,
    branch_name VARCHAR(255) NOT NULL,
    commit_hash VARCHAR(40),
    is_active BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(repo_id, branch_name)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_git_repositories_repo_path ON git_repositories(repo_path);
CREATE INDEX IF NOT EXISTS idx_git_operations_repo_id ON git_operations(repo_id);
CREATE INDEX IF NOT EXISTS idx_git_operations_session_id ON git_operations(session_id);
CREATE INDEX IF NOT EXISTS idx_git_operations_status ON git_operations(status);
CREATE INDEX IF NOT EXISTS idx_git_branches_repo_id ON git_branches(repo_id);

-- Insert initial schema version
INSERT INTO schema_migrations (version, description, checksum)
VALUES
('1.0.0', 'Initial MCP Git database schema', 'initial')
ON CONFLICT (version) DO NOTHING;
