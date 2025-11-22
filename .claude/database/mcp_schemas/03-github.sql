-- Basic MCP GitHub Service Database Schema
-- Minimal tables for GitHub API operations tracking

-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_migrations (
    id SERIAL PRIMARY KEY,
    version VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    checksum VARCHAR(64)
);

-- GitHub repositories tracking
CREATE TABLE IF NOT EXISTS github_repositories (
    id SERIAL PRIMARY KEY,
    repo_full_name TEXT UNIQUE NOT NULL, -- owner/repo
    repo_id INTEGER UNIQUE, -- GitHub repository ID
    owner TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    is_private BOOLEAN DEFAULT false,
    default_branch TEXT DEFAULT 'main',
    clone_url TEXT,
    api_url TEXT,
    last_fetched TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- GitHub API operations tracking
CREATE TABLE IF NOT EXISTS github_operations (
    id SERIAL PRIMARY KEY,
    repo_id INTEGER REFERENCES github_repositories(id) ON DELETE SET NULL,
    operation_type VARCHAR(50) NOT NULL, -- get_repo, list_issues, create_issue, get_commits, etc.
    session_id TEXT,
    status VARCHAR(20) DEFAULT 'completed', -- pending, completed, failed
    api_endpoint TEXT,
    request_details JSONB DEFAULT '{}',
    response_summary JSONB DEFAULT '{}',
    rate_limit_remaining INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- GitHub issues tracking
CREATE TABLE IF NOT EXISTS github_issues (
    id SERIAL PRIMARY KEY,
    repo_id INTEGER REFERENCES github_repositories(id) ON DELETE CASCADE,
    issue_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    state VARCHAR(20), -- open, closed
    author TEXT,
    created_at_github TIMESTAMP WITH TIME ZONE,
    updated_at_github TIMESTAMP WITH TIME ZONE,
    last_fetched TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    UNIQUE(repo_id, issue_number)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_github_repositories_full_name ON github_repositories(repo_full_name);
CREATE INDEX IF NOT EXISTS idx_github_repositories_owner ON github_repositories(owner);
CREATE INDEX IF NOT EXISTS idx_github_operations_repo_id ON github_operations(repo_id);
CREATE INDEX IF NOT EXISTS idx_github_operations_session_id ON github_operations(session_id);
CREATE INDEX IF NOT EXISTS idx_github_operations_status ON github_operations(status);
CREATE INDEX IF NOT EXISTS idx_github_issues_repo_id ON github_issues(repo_id);
CREATE INDEX IF NOT EXISTS idx_github_issues_state ON github_issues(state);

-- Insert initial schema version
INSERT INTO schema_migrations (version, description, checksum)
VALUES
('1.0.0', 'Initial MCP GitHub database schema', 'initial')
ON CONFLICT (version) DO NOTHING;
