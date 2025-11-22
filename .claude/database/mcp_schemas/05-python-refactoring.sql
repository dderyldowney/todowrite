-- Basic MCP Python Refactoring Service Database Schema
-- Minimal tables for Python code analysis and refactoring operations tracking

-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_migrations (
    id SERIAL PRIMARY KEY,
    version VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    checksum VARCHAR(64)
);

-- Python projects tracking
CREATE TABLE IF NOT EXISTS python_projects (
    id SERIAL PRIMARY KEY,
    project_path TEXT UNIQUE NOT NULL,
    project_name VARCHAR(255),
    python_version VARCHAR(20),
    last_analyzed TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Code analysis results
CREATE TABLE IF NOT EXISTS code_analysis (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES python_projects(id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    analysis_type VARCHAR(50) NOT NULL, -- ast_analysis, complexity, imports, etc.
    session_id TEXT,
    status VARCHAR(20) DEFAULT 'completed', -- pending, completed, failed
    analysis_results JSONB DEFAULT '{}',
    metrics JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(project_id, file_path, analysis_type)
);

-- Refactoring operations tracking
CREATE TABLE IF NOT EXISTS refactoring_operations (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES python_projects(id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    refactoring_type VARCHAR(50) NOT NULL, -- extract_function, rename_variable, etc.
    session_id TEXT,
    status VARCHAR(20) DEFAULT 'pending', -- pending, completed, failed
    original_code TEXT,
    refactored_code TEXT,
    diff_summary TEXT,
    auto_applied BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Python imports tracking
CREATE TABLE IF NOT EXISTS python_imports (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES python_projects(id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    import_statement TEXT NOT NULL,
    import_type VARCHAR(20), -- import, from_import
    module_name TEXT NOT NULL,
    alias TEXT,
    is_unused BOOLEAN DEFAULT false,
    first_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_python_projects_project_path ON python_projects(project_path);
CREATE INDEX IF NOT EXISTS idx_code_analysis_project_id ON code_analysis(project_id);
CREATE INDEX IF NOT EXISTS idx_code_analysis_file_path ON code_analysis(file_path);
CREATE INDEX IF NOT EXISTS idx_code_analysis_session_id ON code_analysis(session_id);
CREATE INDEX IF NOT EXISTS idx_refactoring_operations_project_id ON refactoring_operations(project_id);
CREATE INDEX IF NOT EXISTS idx_refactoring_operations_session_id ON refactoring_operations(session_id);
CREATE INDEX IF NOT EXISTS idx_refactoring_operations_status ON refactoring_operations(status);
CREATE INDEX IF NOT EXISTS idx_python_imports_project_id ON python_imports(project_id);
CREATE INDEX IF NOT EXISTS idx_python_imports_module_name ON python_imports(module_name);

-- Insert initial schema version
INSERT INTO schema_migrations (version, description, checksum)
VALUES
('1.0.0', 'Initial MCP Python Refactoring database schema', 'initial')
ON CONFLICT (version) DO NOTHING;
