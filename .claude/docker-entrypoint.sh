#!/bin/bash
# Docker entrypoint for Standalone Episodic Memory System

set -e

# Function to wait for database
wait_for_db() {
    echo "⏳ Waiting for PostgreSQL database..."
    until python -c "
import psycopg2
import os
try:
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    conn.close()
    print('✅ Database is ready')
except Exception as e:
    print(f'❌ Database not ready: {e}')
    exit(1)
" 2>/dev/null; do
        echo "⏳ Database unavailable - sleeping 2 seconds"
        sleep 2
    done
}

# Function to initialize database schema
init_database() {
    echo "🚀 Initializing database schema..."
    python -c "
from episodic_memory import EpisodicMemory
try:
    em = EpisodicMemory()
    em.close()
    print('✅ Database schema initialized')
except Exception as e:
    print(f'❌ Schema initialization failed: {e}')
    exit(1)
"
}

# Function to run initial indexing if needed
initial_index() {
    if [ "$AUTO_INDEX" = "true" ] && [ -d "$CONVERSATIONS_DIR" ]; then
        echo "📁 Running initial indexing..."
        python -m episodic_memory.cli --index --batch-size "${BATCH_SIZE:-25}"
    fi
}

# Main execution
main() {
    echo "🚀 Starting Standalone Episodic Memory System..."
    echo "📊 Version: 1.0.0"
    echo "🔧 Environment: Production"

    # Show configuration
    echo "⚙️  Configuration:"
    echo "   Database: ${DATABASE_URL}"
    echo "   Conversations: ${CONVERSATIONS_DIR:-/data/conversations}"
    echo "   Batch Size: ${BATCH_SIZE:-25}"
    echo "   Adaptive Indexing: ${ADAPTIVE_INDEXING:-true}"

    # Wait for database if DATABASE_URL is set
    if [ -n "$DATABASE_URL" ]; then
        wait_for_db
        init_database
        initial_index
    fi

    # Execute the command
    echo "🎯 Executing: $@"
    exec "$@"
}

# Run main function with all arguments
main "$@"
