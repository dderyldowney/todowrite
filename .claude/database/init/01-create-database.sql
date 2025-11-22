-- ToDoWrite PostgreSQL Database Initialization
-- This script creates the comprehensive schema for the ToDoWrite system
-- It represents the full 12-layer hierarchy: Goal → Concept → Context → Constraints → Requirements → AcceptanceCriteria → InterfaceContract → Phase → Step → Task → SubTask → Command

-- Create database if not exists (should already exist from docker-compose)
-- Extension initialization
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Enable case-insensitive text search
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Create custom types for ToDoWrite system
CREATE TYPE status_enum AS ENUM ('active', 'completed', 'paused', 'cancelled', 'archived');
CREATE TYPE priority_enum AS ENUM ('critical', 'high', 'medium', 'low');
CREATE TYPE layer_enum AS ENUM ('goal', 'concept', 'context', 'constraint', 'requirement', 'acceptance_criteria', 'interface_contract', 'phase', 'step', 'task', 'subtask', 'command');

-- Create schema version tracking
CREATE TABLE IF NOT EXISTS schema_migrations (
    id SERIAL PRIMARY KEY,
    version VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    checksum VARCHAR(64)
);

-- Core ToDoWrite Models Table (Unified structure for all layers)
CREATE TABLE IF NOT EXISTS todowrite_items (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() NOT NULL UNIQUE,
    layer layer_enum NOT NULL,
    parent_id INTEGER REFERENCES todowrite_items(id) ON DELETE CASCADE,

    -- Core fields
    title TEXT NOT NULL,
    description TEXT,
    status status_enum DEFAULT 'active',
    priority priority_enum DEFAULT 'medium',

    -- Hierarchical metadata
    level INTEGER NOT NULL, -- 1-12 depth in hierarchy
    path TEXT[], -- Materialized path for efficient queries
    sort_order INTEGER DEFAULT 0,

    -- Content fields
    content JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    tags TEXT[] DEFAULT '{}',

    -- Relationships
    dependencies INTEGER[] DEFAULT '{}', -- IDs of items this depends on
    children_count INTEGER DEFAULT 0,

    -- Session tracking
    session_id TEXT,
    conversation_history TEXT[],

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,

    -- Versioning and change tracking
    version INTEGER DEFAULT 1,
    changes JSONB DEFAULT '[]',

    -- Indexing and search
    search_vector tsvector,

    -- Constraints
    CONSTRAINT todowrite_items_title_not_empty CHECK (length(trim(title)) > 0),
    CONSTRAINT todowrite_items_level_valid CHECK (level >= 1 AND level <= 12),
    CONSTRAINT todowrite_items_status_valid CHECK (status IN ('active', 'completed', 'paused', 'cancelled', 'archived'))
);

-- Create indexes for optimal performance
CREATE INDEX IF NOT EXISTS idx_todowrite_items_layer ON todowrite_items(layer);
CREATE INDEX IF NOT EXISTS idx_todowrite_items_parent_id ON todowrite_items(parent_id);
CREATE INDEX IF NOT EXISTS idx_todowrite_items_level ON todowrite_items(level);
CREATE INDEX IF NOT EXISTS idx_todowrite_items_status ON todowrite_items(status);
CREATE INDEX IF NOT EXISTS idx_todowrite_items_priority ON todowrite_items(priority);
CREATE INDEX IF NOT EXISTS idx_todowrite_items_created_at ON todowrite_items(created_at);
CREATE INDEX IF NOT EXISTS idx_todowrite_items_updated_at ON todowrite_items(updated_at);
CREATE INDEX IF NOT EXISTS idx_todowrite_items_path ON todowrite_items USING GIN(path);
CREATE INDEX IF NOT EXISTS idx_todowrite_items_tags ON todowrite_items USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_todowrite_items_dependencies ON todowrite_items USING GIN(dependencies);
CREATE INDEX IF NOT EXISTS idx_todowrite_items_content ON todowrite_items USING GIN(content);
CREATE INDEX IF NOT EXISTS idx_todowrite_items_metadata ON todowrite_items USING GIN(metadata);
CREATE INDEX IF NOT EXISTS idx_todowrite_items_search ON todowrite_items USING GIN(search_vector);

-- Full-text search index
CREATE INDEX IF NOT EXISTS idx_todowrite_items_fulltext ON todowrite_items USING GIN(to_tsvector('english', title || ' ' || COALESCE(description, '')));

-- Session tracking table for cross-session continuity
CREATE TABLE IF NOT EXISTS todowrite_sessions (
    id SERIAL PRIMARY KEY,
    session_id TEXT NOT NULL UNIQUE,
    title TEXT,
    description TEXT,
    status status_enum DEFAULT 'active',

    -- Session metadata
    environment JSONB DEFAULT '{}',
    context JSONB DEFAULT '{}',

    -- Session state
    current_focus_id INTEGER REFERENCES todowrite_items(id),
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

CREATE INDEX IF NOT EXISTS idx_todowrite_sessions_session_id ON todowrite_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_todowrite_sessions_status ON todowrite_sessions(status);
CREATE INDEX IF NOT EXISTS idx_todowrite_sessions_last_activity ON todowrite_sessions(last_activity);

-- Relationship tracking table (many-to-many relationships)
CREATE TABLE IF NOT EXISTS todowrite_relationships (
    id SERIAL PRIMARY KEY,
    source_id INTEGER NOT NULL REFERENCES todowrite_items(id) ON DELETE CASCADE,
    target_id INTEGER NOT NULL REFERENCES todowrite_items(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    UNIQUE(source_id, target_id, relationship_type)
);

CREATE INDEX IF NOT EXISTS idx_todowrite_relationships_source_id ON todowrite_relationships(source_id);
CREATE INDEX IF NOT EXISTS idx_todowrite_relationships_target_id ON todowrite_relationships(target_id);
CREATE INDEX IF NOT EXISTS idx_todowrite_relationships_type ON todowrite_relationships(relationship_type);

-- Workflow state tracking
CREATE TABLE IF NOT EXISTS todowrite_workflows (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    definition JSONB NOT NULL,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_todowrite_workflows_active ON todowrite_workflows(active);
CREATE INDEX IF NOT EXISTS idx_todowrite_workflows_name ON todowrite_workflows(name);

-- Insert initial schema version
INSERT INTO schema_migrations (version, description, checksum)
VALUES
('1.0.0', 'Initial ToDoWrite database schema with 12-layer hierarchy', 'initial')
ON CONFLICT (version) DO NOTHING;

-- Create default data if needed
-- This will be populated by the initialization scripts

-- Create function for updating search_vector
CREATE OR REPLACE FUNCTION update_search_vector() RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := to_tsvector('english',
        COALESCE(NEW.title, '') || ' ' ||
        COALESCE(NEW.description, '') || ' ' ||
        COALESCE(array_to_string(NEW.tags, ' '), '')
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for automatic search_vector updates
CREATE TRIGGER update_todowrite_items_search_vector
    BEFORE INSERT OR UPDATE ON todowrite_items
    FOR EACH ROW EXECUTE FUNCTION update_search_vector();

-- Create function for updating path
CREATE OR REPLACE FUNCTION update_path() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.parent_id IS NULL THEN
        NEW.path := ARRAY[NEW.layer, NEW.id::TEXT];
        NEW.level := 1;
    ELSE
        SELECT path || ARRAY[NEW.layer, NEW.id::TEXT], level + 1
        INTO NEW.path, NEW.level
        FROM todowrite_items
        WHERE id = NEW.parent_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for automatic path updates
CREATE TRIGGER update_todowrite_items_path
    BEFORE INSERT OR UPDATE ON todowrite_items
    FOR EACH ROW EXECUTE FUNCTION update_path();

-- Function to get full hierarchy
CREATE OR REPLACE FUNCTION get_item_hierarchy(item_id INTEGER)
RETURNS TABLE(id INTEGER, layer layer_enum, title TEXT, level INTEGER, path TEXT[]) AS $$
BEGIN
    RETURN QUERY
    WITH RECURSIVE item_tree AS (
        SELECT i.id, i.layer, i.title, i.level, i.path
        FROM todowrite_items i
        WHERE i.id = item_id

        UNION ALL

        SELECT i.id, i.layer, i.title, i.level, i.path
        FROM todowrite_items i
        INNER JOIN item_tree it ON i.parent_id = it.id
    )
    SELECT * FROM item_tree ORDER BY level, sort_order;
END;
$$ LANGUAGE plpgsql;
