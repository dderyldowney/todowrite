-- Episodic Memory Service Database Schema
-- Stores conversation history and search data for episodic memory functionality

-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_migrations (
    id SERIAL PRIMARY KEY,
    version VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    checksum VARCHAR(64)
);

-- Conversations tracking (equivalent to session-based directories)
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    project_path TEXT NOT NULL,
    git_branch VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    message_count INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    -- Search indexing
    search_vector tsvector,
    CONSTRAINT conversations_session_id_not_empty CHECK (length(TRIM(session_id)) > 0)
);

-- Messages (equivalent to JSONL file contents)
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    uuid VARCHAR(255) UNIQUE NOT NULL,
    parent_uuid VARCHAR(255),
    is_sidechain BOOLEAN DEFAULT false,
    user_type VARCHAR(50), -- external, internal
    cwd TEXT,
    session_id VARCHAR(255) NOT NULL,
    version VARCHAR(50),
    git_branch VARCHAR(100),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    message_type VARCHAR(50), -- user, assistant, system
    content JSONB NOT NULL, -- Full message content including role, text, etc.
    metadata JSONB DEFAULT '{}', -- Additional fields like usage, model, stop_reason
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT messages_uuid_not_empty CHECK (length(TRIM(uuid)) > 0)
);

-- Message summaries for faster search
CREATE TABLE IF NOT EXISTS message_summaries (
    id SERIAL PRIMARY KEY,
    message_id INTEGER NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
    summary TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Queue operations (from JSONL files)
CREATE TABLE IF NOT EXISTS queue_operations (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    session_id VARCHAR(255) NOT NULL,
    operation VARCHAR(50), -- enqueue, dequeue
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    content JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Search indexes
CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_conversations_project_path ON conversations(project_path);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at);
CREATE INDEX IF NOT EXISTS idx_conversations_search_vector ON conversations USING GIN(search_vector);

CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_session_id ON messages(session_id);
CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
CREATE INDEX IF NOT EXISTS idx_messages_message_type ON messages(message_type);
CREATE INDEX IF NOT EXISTS idx_messages_uuid ON messages(uuid);
CREATE INDEX IF NOT EXISTS idx_messages_parent_uuid ON messages(parent_uuid);
CREATE INDEX IF NOT EXISTS idx_messages_content ON messages USING GIN(content);

CREATE INDEX IF NOT EXISTS idx_message_summaries_message_id ON message_summaries(message_id);
CREATE INDEX IF NOT EXISTS idx_message_summaries_summary ON message_summaries USING GIN(to_tsvector('english', summary));

CREATE INDEX IF NOT EXISTS idx_queue_operations_session_id ON queue_operations(session_id);
CREATE INDEX IF NOT EXISTS idx_queue_operations_timestamp ON queue_operations(timestamp);

-- Trigger to update conversation stats and search vectors
CREATE OR REPLACE FUNCTION update_conversation_stats()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE conversations
        SET message_count = message_count + 1,
            updated_at = NEW.timestamp
        WHERE id = NEW.conversation_id;
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        UPDATE conversations
        SET updated_at = NEW.timestamp
        WHERE id = NEW.conversation_id;
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
DROP TRIGGER IF EXISTS trigger_update_conversation_stats ON messages;
CREATE TRIGGER trigger_update_conversation_stats
    AFTER INSERT OR UPDATE ON messages
    FOR EACH ROW
    EXECUTE FUNCTION update_conversation_stats();

-- Function to update search vectors
CREATE OR REPLACE FUNCTION update_conversation_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE conversations
    SET search_vector = to_tsvector('english',
        COALESCE(session_id, '') || ' ' ||
        COALESCE(project_path, '') || ' ' ||
        COALESCE(git_branch, '')
    )
    WHERE id = NEW.id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create search vector trigger
DROP TRIGGER IF EXISTS trigger_update_conversation_search_vector ON conversations;
CREATE TRIGGER trigger_update_conversation_search_vector
    AFTER INSERT OR UPDATE ON conversations
    FOR EACH ROW
    EXECUTE FUNCTION update_conversation_search_vector();

-- Insert initial schema version
INSERT INTO schema_migrations (version, description, checksum)
VALUES
('1.0.0', 'Initial MCP Episodic Memory database schema', 'initial')
ON CONFLICT (version) DO NOTHING;