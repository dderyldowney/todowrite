-- ToDoWrite PostgreSQL Initialization Script
-- This script sets up the ToDoWrite database with proper permissions and extensions

-- Create additional users if needed
-- CREATE USER todowrite_readonly WITH PASSWORD 'readonly_password';

-- Grant permissions
GRANT CONNECT ON DATABASE todowrite TO todowrite;
GRANT USAGE ON SCHEMA public TO todowrite;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO todowrite;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO todowrite;

-- Enable extensions if needed
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create indexes for better performance (will be created by SQLAlchemy migrations)
-- This file can be extended with additional setup as needed

-- Set default database settings for ToDoWrite
ALTER DATABASE todowrite SET timezone TO 'UTC';
ALTER DATABASE todowrite SET log_statement TO 'all';
