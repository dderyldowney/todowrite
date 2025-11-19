#!/usr/bin/env python3
"""
Migrate episodic memory conversations from global database to project-specific database

This script extracts only the current project's conversations from the global episodic memory
database and imports them into the project-specific database, maintaining project isolation.
"""

import os
import sys
import shutil
from pathlib import Path
import sqlite3
import argparse
from typing import List, Dict, Any

def get_project_conversation_paths(project_root: Path) -> List[str]:
    """Get all possible conversation directory paths for the current project"""
    project_root = project_root.resolve()

    # Generate possible encoded paths that Claude might use
    paths = []

    # Current working directory approach
    cwd_encoded = str(project_root).lstrip('/').replace('/', '-')
    paths.append(f"-Users-{cwd_encoded}")

    # Alternative encoding approaches
    if "Users" in cwd_encoded:
        # Handle double Users case: -Users-Users-dderyldowney...
        paths.append(f"-{cwd_encoded}")

    # Also check common variations
    home = Path.home()
    if str(project_root).startswith(str(home)):
        relative = str(project_root).replace(str(home), "~").lstrip('~').lstrip('/')
        relative_encoded = relative.replace('/', '-')
        paths.append(f"-Users-{relative_encoded}")

    # Remove duplicates
    return list(set(paths))

def find_global_conversations(project_conversation_paths: List[str]) -> List[str]:
    """Find conversation files in global episodic memory archive"""
    global_archive = Path.home() / ".config" / "superpowers" / "conversation-archive"

    if not global_archive.exists():
        print(f"❌ Global episodic memory archive not found: {global_archive}")
        return []

    conversations = []

    # Look for project directories in global archive
    for project_path in project_conversation_paths:
        project_dir = global_archive / project_path
        if project_dir.exists():
            jsonl_files = list(project_dir.glob("*.jsonl"))
            conversations.extend([str(f) for f in jsonl_files])
            print(f"📁 Found {len(jsonl_files)} conversations in {project_path}")

    return conversations

def extract_project_conversations_from_global_db(project_paths: List[str], project_db_path: Path) -> List[Dict[str, Any]]:
    """Extract project-specific conversations from global episodic memory database"""
    global_db_path = Path.home() / ".config" / "superpowers" / "conversation-index" / "db.sqlite"

    if not global_db_path.exists():
        print(f"❌ Global episodic memory database not found: {global_db_path}")
        return []

    print(f"📖 Reading global episodic memory database: {global_db_path}")

    try:
        conn = sqlite3.connect(global_db_path)
        cursor = conn.cursor()

        # First, let's check the schema
        cursor.execute("PRAGMA table_info(exchanges)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        print(f"📋 Database columns: {column_names}")

        # Query for exchanges that match our project paths (adjust column names as needed)
        if 'content' in column_names:
            query = f"""
            SELECT DISTINCT id, project, timestamp, content, role, metadata
            FROM exchanges
            WHERE project IN ({placeholders})
            ORDER BY timestamp ASC
            """
        else:
            # Fallback to basic columns
            query = f"""
            SELECT DISTINCT id, project, timestamp
            FROM exchanges
            WHERE project IN ({placeholders})
            ORDER BY timestamp ASC
            """

        cursor.execute(query, project_paths)
        rows = cursor.fetchall()

        conversations = []
        for row in rows:
            conversations.append({
                'id': row[0],
                'project': row[1],
                'timestamp': row[2],
                'content': row[3],
                'role': row[4],
                'metadata': row[5]
            })

        conn.close()
        print(f"📊 Found {len(conversations)} project-specific exchanges in global database")
        return conversations

    except Exception as e:
        print(f"❌ Error reading global database: {e}")
        return []

def create_project_database(project_db_path: Path) -> bool:
    """Create project-specific episodic memory database"""
    try:
        # Ensure directory exists
        project_db_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy conversation files to project archive
        project_archive = project_db_path.parent / "episodic_memory_archive"
        project_archive.mkdir(exist_ok=True)

        # Find and copy project conversations
        project_conversation_paths = get_project_conversation_paths(project_db_path.parent.parent)
        conversations = find_global_conversations(project_conversation_paths)

        copied_count = 0
        for conv_file in conversations:
            src = Path(conv_file)
            dst = project_archive / src.name

            if not dst.exists():
                shutil.copy2(src, dst)
                copied_count += 1

        print(f"📋 Copied {copied_count} conversation files to project archive")

        # Run episodic memory index on project archive
        import subprocess
        episodic_cli = Path.home() / ".claude" / "plugins" / "cache" / "episodic-memory" / "cli" / "episodic-memory.js"

        if episodic_cli.exists():
            # Set environment variable for project database
            env = os.environ.copy()
            env['EPISODIC_MEMORY_DB_PATH'] = str(project_db_path)

            print("🔧 Indexing project conversations...")
            result = subprocess.run(
                ["node", str(episodic_cli), "index", "--cleanup", "--concurrency", "2"],
                env=env,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                print("✅ Successfully indexed project conversations")
                return True
            else:
                print(f"❌ Error indexing conversations: {result.stderr}")
                return False
        else:
            print(f"❌ Episodic memory CLI not found: {episodic_cli}")
            return False

    except Exception as e:
        print(f"❌ Error creating project database: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Migrate episodic memory to project-specific database")
    parser.add_argument("--project-root", type=str, help="Project root directory (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be migrated without doing it")
    parser.add_argument("--force", action="store_true", help="Overwrite existing project database")

    args = parser.parse_args()

    if args.project_root:
        project_root = Path(args.project_root)
    else:
        project_root = Path.cwd()

    print(f"🏠 Project Root: {project_root}")

    # Set up project database path
    project_db_path = project_root / ".claude" / "episodic_memory.db"

    if project_db_path.exists() and not args.force:
        print(f"⚠️  Project database already exists: {project_db_path}")
        print("   Use --force to overwrite or --dry-run to check what would be migrated")
        return

    # Get project conversation paths
    project_conversation_paths = get_project_conversation_paths(project_root)
    print(f"🔍 Looking for project conversation paths: {project_conversation_paths}")

    if args.dry_run:
        # Just show what would be migrated
        conversations = find_global_conversations(project_conversation_paths)
        db_conversations = extract_project_conversations_from_global_db(project_conversation_paths, project_db_path)

        print(f"\n📊 DRY RUN RESULTS:")
        print(f"   Found {len(conversations)} conversation files")
        print(f"   Found {len(db_conversations)} database exchanges")
        print(f"   Project database would be: {project_db_path}")
        return

    # Check if we have anything to migrate
    conversations = find_global_conversations(project_conversation_paths)
    db_conversations = extract_project_conversations_from_global_db(project_conversation_paths, project_db_path)

    if not conversations and not db_conversations:
        print("ℹ️  No project conversations found in global episodic memory")
        print("   This is normal for new projects or projects without episodic memory")
        return

    # Create project database
    print(f"\n🚀 Starting migration to project database: {project_db_path}")

    if create_project_database(project_db_path):
        print(f"✅ Migration completed successfully!")
        print(f"   Project database: {project_db_path}")
        print(f"   Run './dev_tools/project_episodic_memory.sh stats' to verify")
    else:
        print(f"❌ Migration failed")
        sys.exit(1)

if __name__ == "__main__":
    main()