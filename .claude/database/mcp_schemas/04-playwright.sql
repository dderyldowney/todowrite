-- Basic MCP Playwright Service Database Schema
-- Minimal tables for web automation operations tracking

-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_migrations (
    id SERIAL PRIMARY KEY,
    version VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    checksum VARCHAR(64)
);

-- Browser sessions tracking
CREATE TABLE IF NOT EXISTS browser_sessions (
    id SERIAL PRIMARY KEY,
    session_id TEXT UNIQUE NOT NULL,
    browser_type VARCHAR(50), -- chromium, firefox, webkit
    headless BOOLEAN DEFAULT true,
    viewport_width INTEGER DEFAULT 1280,
    viewport_height INTEGER DEFAULT 720,
    status VARCHAR(20) DEFAULT 'active', -- active, closed, crashed
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    closed_at TIMESTAMP WITH TIME ZONE
);

-- Page operations tracking
CREATE TABLE IF NOT EXISTS page_operations (
    id SERIAL PRIMARY KEY,
    session_id TEXT REFERENCES browser_sessions(session_id) ON DELETE CASCADE,
    page_url TEXT NOT NULL,
    operation_type VARCHAR(50) NOT NULL, -- navigate, click, type, screenshot, wait, etc.
    selector TEXT,
    value TEXT,
    status VARCHAR(20) DEFAULT 'completed', -- pending, completed, failed
    screenshot_path TEXT,
    error_message TEXT,
    execution_time_ms INTEGER,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Screenshot storage tracking
CREATE TABLE IF NOT EXISTS screenshots (
    id SERIAL PRIMARY KEY,
    operation_id INTEGER REFERENCES page_operations(id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    file_size INTEGER,
    screenshot_type VARCHAR(20), -- full_page, element, viewport
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_browser_sessions_session_id ON browser_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_browser_sessions_status ON browser_sessions(status);
CREATE INDEX IF NOT EXISTS idx_page_operations_session_id ON page_operations(session_id);
CREATE INDEX IF NOT EXISTS idx_page_operations_page_url ON page_operations(page_url);
CREATE Index IF NOT EXISTS idx_page_operations_status ON page_operations(status);
CREATE INDEX IF NOT EXISTS idx_page_operations_created_at ON page_operations(created_at);
CREATE INDEX IF NOT EXISTS idx_screenshots_operation_id ON screenshots(operation_id);

-- Insert initial schema version
INSERT INTO schema_migrations (version, description, checksum)
VALUES
('1.0.0', 'Initial MCP Playwright database schema', 'initial')
ON CONFLICT (version) DO NOTHING;
