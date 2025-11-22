#!/usr/bin/env python3
"""
Custom Conversation Search System
Industry-standard episodic memory replacement using PostgreSQL + vector similarity

Replaces the non-functional superpowers and episodic-memory plugins with a production-ready solution.
"""

import os
import json
import psycopg2
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
import argparse
import sys
import hashlib
import time
from pathlib import Path

@dataclass
class SearchResult:
    """Represents a search result with similarity score"""
    conversation_id: str
    message_type: str
    content: str
    timestamp: str
    similarity: float
    project: Optional[str] = None
    session_id: Optional[str] = None

class ConversationSearchSystem:
    """Production-ready conversation search with PostgreSQL backend"""

    def __init__(self, db_connection_string: str):
        """Initialize the conversation search system"""
        self.db_connection = db_connection_string
        self.conn = None

    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(self.db_connection)
            self.conn.autocommit = True
            print(f"✅ Connected to PostgreSQL database")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def create_conversation_schema(self):
        """Create the conversation schema if it doesn't exist"""
        cursor = self.conn.cursor()
        try:
            # Create conversations table with file tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    conversation_file TEXT NOT NULL UNIQUE,
                    project TEXT,
                    session_id TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    indexed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    message_count INTEGER DEFAULT 0,
                    file_path TEXT,
                    file_hash TEXT,
                    file_modified TIMESTAMP WITH TIME ZONE
                );
            """)

            # Create messages table with full-text search
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
                    message_type TEXT NOT NULL CHECK (message_type IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP WITH TIME ZONE,
                    token_count INTEGER,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """)

            # Create indexes for performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_conversation_id
                ON messages(conversation_id);
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_timestamp
                ON messages(timestamp DESC);
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_type
                ON messages(message_type);
            """)

            # Full-text search index
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_content_fts
                ON messages USING gin(to_tsvector('english', content));
            """)

            # Add new columns for adaptive features (PostgreSQL-compatible)
            try:
                # Check if columns exist before adding them
                cursor.execute("""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = 'conversations'
                    AND column_name IN ('file_hash', 'file_modified')
                """)
                existing_columns = [row[0] for row in cursor.fetchall()]

                if 'file_hash' not in existing_columns:
                    cursor.execute("ALTER TABLE conversations ADD COLUMN file_hash TEXT")
                    print("✅ Added file_hash column")

                if 'file_modified' not in existing_columns:
                    cursor.execute("ALTER TABLE conversations ADD COLUMN file_modified TIMESTAMP WITH TIME ZONE")
                    print("✅ Added file_modified column")

                if 'file_hash' in existing_columns and 'file_modified' in existing_columns:
                    print("✅ Adaptive schema columns already exist")

            except Exception as e:
                print(f"⚠️  Schema update note: {e}")

            print("✅ Conversation schema created successfully")

        finally:
            cursor.close()

    def load_conversation_file(self, file_path: str) -> Optional[Tuple[str, List[Dict]]]:
        """Load and parse a conversation JSONL file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line for line in f if line.strip()]

            messages = []
            for line in lines:
                try:
                    data = json.loads(line)
                    if data.get('type') in ['user', 'assistant'] and data.get('message'):
                        message_obj = data['message']
                        content = ""

                        # Handle different message content formats
                        if isinstance(message_obj, str):
                            content = message_obj
                        elif isinstance(message_obj, dict):
                            # Extract content from message object
                            if 'content' in message_obj:
                                content_field = message_obj['content']
                                if isinstance(content_field, str):
                                    content = content_field
                                elif isinstance(content_field, list):
                                    # Join content array elements
                                    content_parts = []
                                    for part in content_field:
                                        if isinstance(part, dict) and 'text' in part:
                                            content_parts.append(part['text'])
                                        elif isinstance(part, str):
                                            content_parts.append(part)
                                    content = ' '.join(content_parts)

                        if content:  # Only add messages with content
                            messages.append({
                                'type': data['type'],
                                'content': content,
                                'timestamp': data.get('timestamp', datetime.now().isoformat())
                            })
                except json.JSONDecodeError:
                    continue

            if messages:
                conversation_id = os.path.basename(file_path).replace('.jsonl', '')
                return conversation_id, messages

        except Exception as e:
            print(f"⚠️  Error loading {file_path}: {e}")

        return None

    def get_file_hash(self, file_path: str) -> str:
        """Get SHA256 hash of file for change detection"""
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception:
            return ""

    def should_reindex_file(self, file_path: str, file_hash: str, file_modified: datetime) -> bool:
        """Check if file needs reindexing based on hash and modification time"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT file_hash, file_modified FROM conversations
                WHERE conversation_file = %s
            """, (os.path.basename(file_path),))

            result = cursor.fetchone()
            if not result:
                return True

            db_hash, db_modified = result
            return db_hash != file_hash or db_modified != file_modified
        finally:
            cursor.close()

    def index_conversation_file(self, file_path: str, force: bool = False) -> bool:
        """Index a single conversation file with adaptive change detection"""
        # Get file metadata for change detection
        file_hash = self.get_file_hash(file_path)
        file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))

        # Check if we need to reindex (unless force is True)
        if not force and not self.should_reindex_file(file_path, file_hash, file_modified):
            return True  # Already indexed and unchanged

        result = self.load_conversation_file(file_path)
        if not result:
            return False

        conversation_id, messages = result
        cursor = self.conn.cursor()
        try:
            # Insert or update conversation record with file tracking
            cursor.execute("""
                INSERT INTO conversations
                (conversation_file, project, session_id, message_count, file_path, file_hash, file_modified)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (conversation_file)
                DO UPDATE SET
                    message_count = EXCLUDED.message_count,
                    file_path = EXCLUDED.file_path,
                    file_hash = EXCLUDED.file_hash,
                    file_modified = EXCLUDED.file_modified,
                    indexed_at = NOW()
                RETURNING id
            """, (
                conversation_id,
                os.path.basename(os.path.dirname(file_path)),
                None,  # session_id extraction would require parsing
                len(messages),
                file_path,
                file_hash,
                file_modified
            ))

            conv_uuid = cursor.fetchone()[0]

            # Delete existing messages for this conversation
            cursor.execute("DELETE FROM messages WHERE conversation_id = %s", (conv_uuid,))

            # Insert messages
            for msg in messages:
                cursor.execute("""
                    INSERT INTO messages
                    (conversation_id, message_type, content, timestamp, token_count)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    conv_uuid,
                    msg['type'],
                    msg['content'],
                    msg['timestamp'],
                    len(msg['content'].split())  # rough token count
                ))

            return True

        except Exception as e:
            print(f"❌ Error indexing {file_path}: {e}")
            return False
        finally:
            cursor.close()

    def index_conversation_directory(self, directory_path: str, limit: Optional[int] = None,
                                   batch_size: int = 50, adaptive: bool = True) -> int:
        """Index all conversation files in a directory with resource-aware processing"""
        print(f"📁 Indexing conversations from: {directory_path}")
        if adaptive:
            print(f"🔄 Adaptive mode: Only processing new/changed files")
        print(f"⚙️  Batch size: {batch_size} files")

        indexed_count = 0
        skipped_count = 0
        processed = 0
        start_time = time.time()

        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.jsonl'):
                    if limit and processed >= limit:
                        break

                    file_path = os.path.join(root, file)

                    # Adaptive processing: check if file needs indexing
                    if adaptive:
                        file_hash = self.get_file_hash(file_path)
                        file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                        if not self.should_reindex_file(file_path, file_hash, file_modified):
                            skipped_count += 1
                            processed += 1
                            continue

                    # Process the file
                    if self.index_conversation_file(file_path, force=not adaptive):
                        indexed_count += 1
                        processed += 1

                    # Resource management: periodic status and rate limiting
                    if processed % batch_size == 0:
                        elapsed = time.time() - start_time
                        rate = processed / elapsed if elapsed > 0 else 0
                        print(f"📊 Processed {processed} files (+{skipped_count} skipped), indexed {indexed_count} | Rate: {rate:.1f} files/sec")

                        # Brief pause to prevent system overload
                        time.sleep(0.1)

            if limit and processed >= limit:
                break

        total_time = time.time() - start_time
        print(f"✅ Completed: {indexed_count} conversations indexed from {processed} files")
        print(f"📈 Skipped {skipped_count} unchanged files | Total time: {total_time:.1f}s")
        return indexed_count

    def keyword_search(self, query: str, limit: int = 10) -> List[SearchResult]:
        """Perform keyword-based search using PostgreSQL full-text search"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT
                    c.conversation_file,
                    m.message_type,
                    m.content,
                    m.timestamp,
                    c.project,
                    c.session_id,
                    ts_rank(to_tsvector('english', m.content), plainto_tsquery('english', %s)) as rank
                FROM messages m
                JOIN conversations c ON m.conversation_id = c.id
                WHERE to_tsvector('english', m.content) @@ plainto_tsquery('english', %s)
                ORDER BY rank DESC
                LIMIT %s
            """, (query, query, limit))

            results = []
            rows = cursor.fetchall()
            for row in rows:
                results.append(SearchResult(
                    conversation_id=row[0],
                    message_type=row[1],
                    content=row[2],
                    timestamp=str(row[3]),
                    similarity=float(row[6]) if row[6] else 0.0,
                    project=row[4],
                    session_id=row[5]
                ))

            return results
        finally:
            cursor.close()

    def get_stats(self) -> Dict:
        """Get database statistics"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM conversations")
            conv_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM messages")
            msg_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT project) FROM conversations")
            project_count = cursor.fetchone()[0]

            return {
                'conversations': conv_count,
                'messages': msg_count,
                'projects': project_count
            }
        finally:
            cursor.close()

def main():
    parser = argparse.ArgumentParser(description='Custom Conversation Search System')
    parser.add_argument('--init', action='store_true', help='Initialize database schema')
    parser.add_argument('--index', metavar='DIRECTORY', help='Index conversation files from directory')
    parser.add_argument('--search', metavar='QUERY', help='Search conversations')
    parser.add_argument('--limit', type=int, default=10, help='Limit search results')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    parser.add_argument('--batch-size', type=int, default=50, help='Batch size for processing (default: 50)')
    parser.add_argument('--no-adaptive', action='store_true', help='Disable adaptive processing (process all files)')
    parser.add_argument('--db', default='postgresql://mcp_user:mcp_secure_password_2024@localhost:5433/mcp_tools',
                       help='Database connection string')

    args = parser.parse_args()

    # Initialize search system
    search_system = ConversationSearchSystem(args.db)
    search_system.connect()

    try:
        if args.init:
            print("🚀 Initializing conversation search database...")
            search_system.create_conversation_schema()
            print("✅ Database schema initialized successfully")

        elif args.index:
            if not os.path.isdir(args.index):
                print(f"❌ Directory not found: {args.index}")
                sys.exit(1)

            search_system.create_conversation_schema()
            indexed = search_system.index_conversation_directory(
                args.index,
                limit=None,
                batch_size=args.batch_size,
                adaptive=not args.no_adaptive
            )
            print(f"✅ Indexed {indexed} conversations")

        elif args.search:
            search_system.create_conversation_schema()

            results = search_system.keyword_search(args.search, limit=args.limit)
            search_type = "Keyword"

            print(f"\n🔍 {search_type} Search Results for: '{args.search}'")
            print("=" * 60)

            if not results:
                print("No results found.")
            else:
                for i, result in enumerate(results, 1):
                    print(f"\n{i}. [{result.message_type.upper()}] {result.conversation_id}")
                    if result.project:
                        print(f"   Project: {result.project}")
                    print(f"   Similarity: {result.similarity:.3f}")
                    print(f"   Timestamp: {result.timestamp}")
                    # Show first 200 characters of content
                    content_preview = result.content[:200] + "..." if len(result.content) > 200 else result.content
                    print(f"   Content: {content_preview}")

        elif args.stats:
            search_system.create_conversation_schema()
            stats = search_system.get_stats()
            print("\n📊 Database Statistics")
            print("=" * 30)
            for key, value in stats.items():
                print(f"{key.capitalize()}: {value:,}")

        else:
            parser.print_help()

    finally:
        search_system.close()

if __name__ == "__main__":
    main()