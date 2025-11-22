-- Initial Data and Seed Data for ToDoWrite Database
-- This script sets up the foundational data for the ToDoWrite system

-- Insert initial session
INSERT INTO todowrite_sessions (session_id, title, description, environment)
VALUES (
    'initial_setup',
    'ToDoWrite Initial Setup',
    'Initial session to set up ToDoWrite PostgreSQL backend',
    '{"version": "1.0.0", "stage": "initialization"}'
) ON CONFLICT (session_id) DO NOTHING;

-- Insert default workflows
INSERT INTO todowrite_workflows (name, description, definition, active)
VALUES
('todo_workflow', 'Standard Todo Workflow',
 '{"steps": ["create", "plan", "execute", "review", "complete"]}', true),
('planning_workflow', 'Strategic Planning Workflow',
 '{"steps": ["analyze", "design", "validate", "implement", "test"]}', true)
ON CONFLICT DO NOTHING;

-- Create root goal for this project if it doesn't exist
-- This represents the main project goal that all other items will branch from
INSERT INTO todowrite_items (layer, title, description, priority, session_id, level)
SELECT 'goal', 'Enhance ToDoWrite Planning Capabilities',
       'Comprehensive development of the ToDoWrite system with PostgreSQL backend, MCP integration, and persistent cross-session data management',
       'critical', 'initial_setup', 1
WHERE NOT EXISTS (
    SELECT 1 FROM todowrite_items WHERE layer = 'goal' AND title = 'Enhance ToDoWrite Planning Capabilities'
);

-- Get the ID of the root goal for creating initial concepts
DO $$
DECLARE
    root_goal_id INTEGER;
BEGIN
    SELECT id INTO root_goal_id FROM todowrite_items WHERE layer = 'goal' AND title = 'Enhance ToDoWrite Planning Capabilities';

    IF root_goal_id IS NOT NULL THEN
        -- Create initial concept: PostgreSQL Backend Development
        INSERT INTO todowrite_items (parent_id, layer, title, description, priority, session_id)
        VALUES (root_goal_id, 'concept', 'PostgreSQL Backend Development',
                'Develop robust PostgreSQL database backend for ToDoWrite with full 12-layer hierarchy support',
                'critical', 'initial_setup');

        -- Create initial concept: MCP Integration
        INSERT INTO todowrite_items (parent_id, layer, title, description, priority, session_id)
        VALUES (root_goal_id, 'concept', 'MCP Integration & Global Availability',
                'Integrate comprehensive MCP servers globally with auto-loading and session management',
                'high', 'initial_setup');

        -- Create initial concept: Cross-Session Persistence
        INSERT INTO todowrite_items (parent_id, layer, title, description, priority, session_id)
        VALUES (root_goal_id, 'concept', 'Cross-Session Data Persistence',
                'Implement robust cross-session data persistence with session continuity and state management',
                'critical', 'initial_setup');

        -- Create initial concept: Token Optimization
        INSERT INTO todowrite_items (parent_id, layer, title, description, priority, session_id)
        VALUES (root_goal_id, 'concept', 'Advanced Token Optimization',
                'Implement sophisticated token optimization algorithms beyond KV-cache for 90%+ reduction',
                'medium', 'initial_setup');
    END IF;
END $$;

-- Insert default project configuration
INSERT INTO todowrite_items (layer, title, description, content, metadata, session_id, level)
SELECT 'interface_contract', 'ToDoWrite Project Configuration',
       'Core configuration for the ToDoWrite development project',
       '{
           "project": {
               "name": "ToDoWrite",
               "version": "1.0.0",
               "description": "Comprehensive task management system with PostgreSQL backend"
           },
           "database": {
               "type": "postgresql",
               "host": "localhost",
               "port": 5433,
               "database": "todowrite",
               "container": "todowrite-postgres"
           },
           "mcp_servers": {
               "global": ["context7", "docker", "github-official", "git", "filesystem", "postgres", "SQLite", "hugging-face", "playwright"],
               "total_tools": "91+"
           },
           "token_optimization": {
               "algorithms": ["semantic_deduplication", "context_compression", "progressive_windowing", "adaptive_selection"],
               "reduction_capability": "99.98%"
           }
       }',
       '{
           "type": "project_config",
           "enforced": true,
           "session_required": true,
           "version": "1.0"
       }',
       'initial_setup', 1
WHERE NOT EXISTS (
    SELECT 1 FROM todowrite_items WHERE layer = 'interface_contract' AND title = 'ToDoWrite Project Configuration'
);

-- Create initial maintenance phase for database operations
INSERT INTO todowrite_items (layer, title, description, content, metadata, session_id, level)
SELECT 'phase', 'Database Operations & Maintenance',
       'Ongoing database operations, backups, monitoring, and maintenance tasks',
       '{
           "operations": [
               "daily_backup",
               "health_check",
               "performance_monitoring",
               "connection_pool_management",
               "query_optimization"
           ],
           "schedule": {
               "backup": "daily",
               "health_check": "hourly",
               "optimization": "weekly"
           }
       }',
       '{
           "type": "maintenance",
           "critical": true,
           "automation": true
       }',
       'initial_setup', 1
WHERE NOT EXISTS (
    SELECT 1 FROM todowrite_items WHERE layer = 'phase' AND title = 'Database Operations & Maintenance'
);

-- Create initial requirements for data integrity
INSERT INTO todowrite_items (layer, title, description, content, metadata, session_id, level)
SELECT 'requirement', 'Data Integrity & Consistency',
       'Strict requirements for data integrity across all ToDoWrite operations and cross-session continuity',
       '{
           "requirements": [
               "All changes must be stored in PostgreSQL",
               "Cross-session data continuity required",
               "Atomic operations for complex hierarchies",
               "Referential integrity enforcement",
               "Session state persistence",
               "Rollback capability",
               "Audit logging for all operations"
           ],
           "constraints": [
               "No direct file-based data storage",
               "Database-first approach mandatory",
               "Session validation required",
               "Change tracking enforced"
           ]
       }',
       '{
           "type": "data_integrity",
           "mandatory": true,
           "validation": "strict",
           "enforcement": "session_hook"
       }',
       'initial_setup', 1
WHERE NOT EXISTS (
    SELECT 1 FROM todowrite_items WHERE layer = 'requirement' AND title = 'Data Integrity & Consistency'
);

-- Create acceptance criteria for database integration
INSERT INTO todowrite_items (layer, title, description, content, metadata, session_id, level)
SELECT 'acceptance_criteria', 'PostgreSQL Integration Acceptance',
       'Acceptance criteria for PostgreSQL backend integration and mandatory usage enforcement',
       '{
           "criteria": [
               {
                   "id": "db_001",
                   "description": "todowrite-postgres container runs perpetually",
                   "test": "docker ps | grep todowrite-postgres"
               },
               {
                   "id": "db_002",
                   "description": "All 12-layer tables created and accessible",
                   "test": "SELECT COUNT(DISTINCT layer) FROM todowrite_items = 12"
               },
               {
                   "id": "db_003",
                   "description": "Cross-session data persistence functional",
                   "test": "Data persists across /clear and session restarts"
               },
               {
                   "id": "db_004",
                   "description": "Session hooks enforce database usage",
                   "test": "Session startup hooks validate database connectivity"
               },
               {
                   "id": "db_005",
                   "description": "All development work stored in database",
                   "test": "Every action creates database record"
               }
           ]
       }',
       '{
           "type": "acceptance",
           "testable": true,
           "mandatory": true,
           "verification": "automated"
       }',
       'initial_setup', 1
WHERE NOT EXISTS (
    SELECT 1 FROM todowrite_items WHERE layer = 'acceptance_criteria' AND title = 'PostgreSQL Integration Acceptance'
);

-- Create initial tasks for immediate implementation
INSERT INTO todowrite_items (layer, title, description, content, metadata, session_id, level)
SELECT 'task', 'Initialize todowrite-postgres Container',
       'Start and configure the todowrite-postgres Docker container with persistent data',
       '{
           "steps": [
               "Create docker-compose configuration",
               "Initialize database schema",
               "Verify connectivity",
               "Set up health checks",
               "Configure automatic restart"
           ]
       }',
       '{
           "type": "infrastructure",
           "priority": "critical",
           "dependencies": ["docker", "postgres"]
       }',
       'initial_setup', 1
WHERE NOT EXISTS (
    SELECT 1 FROM todowrite_items WHERE layer = 'task' AND title = 'Initialize todowrite-postgres Container'
);

-- Insert schema version tracking
INSERT INTO schema_migrations (version, description, checksum)
VALUES ('1.0.1', 'Initial ToDoWrite data and seed data', 'seed_data_initial')
ON CONFLICT (version) DO NOTHING;

-- Grant permissions
-- These will be adjusted based on the actual database user created in Docker