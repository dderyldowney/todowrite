#!/usr/bin/env python3
"""
Seamless Episodic Memory Replacement
Industry-standard PostgreSQL-based episodic memory system

Drop-in replacement for the old episodic-memory plugin with enhanced performance and reliability.
"""

import argparse
import json
import os
from typing import Any

# Import our conversation search system
from conversation_search import ConversationSearchSystem


class EpisodicMemory:
    """Seamless episodic memory replacement with PostgreSQL backend"""

    def __init__(self, db_path: str | None = None):
        """Initialize episodic memory with PostgreSQL backend"""
        # Use environment variable or default
        if db_path:
            self.db_connection = db_path
        else:
            self.db_connection = os.getenv(
                "EPISODIC_MEMORY_DB_PATH",
                "postgresql://mcp_user:mcp_secure_password_2024@localhost:5433/mcp_tools",
            )

        self.search_system = ConversationSearchSystem(self.db_connection)
        self.search_system.connect()
        self.search_system.create_conversation_schema()

    def close(self):
        """Close database connection"""
        self.search_system.close()

    def index_conversations(
        self, conversations_dir: str = None, force: bool = False
    ) -> dict[str, Any]:
        """Index conversation files (equivalent to original plugin's indexing)"""
        if not conversations_dir:
            conversations_dir = os.path.expanduser("~/.claude/projects")

        if not os.path.exists(conversations_dir):
            return {
                "success": False,
                "error": f"Conversations directory not found: {conversations_dir}",
                "indexed": 0,
                "total": 0,
            }

        try:
            # Use adaptive indexing by default
            indexed = self.search_system.index_conversation_directory(
                conversations_dir,
                adaptive=not force,
                batch_size=25,  # Conservative for day-to-day usage
            )

            # Get stats
            stats = self.search_system.get_stats()

            return {
                "success": True,
                "indexed": indexed,
                "total_conversations": stats["conversations"],
                "total_messages": stats["messages"],
                "projects": stats["projects"],
            }
        except Exception as e:
            return {"success": False, "error": str(e), "indexed": 0, "total": 0}

    def search_conversations(
        self, query: str, limit: int = 10, message_type: str = None
    ) -> list[dict[str, Any]]:
        """Search conversations (equivalent to original plugin's search)"""
        try:
            results = self.search_system.keyword_search(query, limit=limit)

            # Convert to format compatible with original episodic memory
            formatted_results = []
            for result in results:
                formatted_result = {
                    "conversation_id": result.conversation_id,
                    "message_type": result.message_type,
                    "content": result.content,
                    "timestamp": result.timestamp,
                    "similarity_score": result.similarity,
                    "project": result.project,
                    "session_id": result.session_id,
                }

                # Filter by message type if specified
                if message_type and message_type.lower() != result.message_type.lower():
                    continue

                formatted_results.append(formatted_result)

            return formatted_results
        except Exception as e:
            return [{"error": str(e)}]

    def get_stats(self) -> dict[str, Any]:
        """Get episodic memory statistics"""
        try:
            stats = self.search_system.get_stats()
            return {
                "conversations": stats["conversations"],
                "messages": stats["messages"],
                "projects": stats["projects"],
                "database": "PostgreSQL",
                "backend": "industry-standard",
            }
        except Exception as e:
            return {"error": str(e)}

    def cleanup_old_sessions(self, days: int = 30) -> dict[str, Any]:
        """Cleanup old sessions (placeholder for future implementation)"""
        return {
            "success": True,
            "message": "Cleanup not implemented yet - conversations are preserved indefinitely",
            "deleted": 0,
        }


def main():
    """CLI interface mimicking original episodic-memory plugin"""
    parser = argparse.ArgumentParser(description="Episodic Memory - PostgreSQL Conversation Search")
    parser.add_argument("--index", action="store_true", help="Index conversations")
    parser.add_argument("--search", metavar="QUERY", help="Search conversations")
    parser.add_argument("--limit", type=int, default=10, help="Limit search results")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    parser.add_argument("--cleanup", action="store_true", help="Cleanup old sessions")
    parser.add_argument("--force", action="store_true", help="Force full reindexing")
    parser.add_argument("--db", help="Database connection string")
    parser.add_argument("--type", choices=["user", "assistant"], help="Filter by message type")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format")

    args = parser.parse_args()

    # Initialize episodic memory
    episodic = EpisodicMemory(args.db)

    try:
        if args.index:
            print("🔍 Indexing conversations...")
            result = episodic.index_conversations(force=args.force)

            if args.format == "json":
                print(json.dumps(result, indent=2))
            else:
                if result["success"]:
                    print(f"✅ Successfully indexed {result['indexed']} conversations")
                    print(
                        f"📊 Total: {result['total_conversations']} conversations, {result['total_messages']} messages"
                    )
                    print(f"🏗️  Projects: {result['projects']}")
                else:
                    print(f"❌ Indexing failed: {result['error']}")

        elif args.search:
            print(f"🔍 Searching for: '{args.search}'")
            results = episodic.search_conversations(
                args.search, limit=args.limit, message_type=args.type
            )

            if args.format == "json":
                print(json.dumps(results, indent=2))
            else:
                if not results:
                    print("No results found.")
                else:
                    print(f"Found {len(results)} results:")
                    for i, result in enumerate(results, 1):
                        print(
                            f"\n{i}. [{result['message_type'].upper()}] {result['conversation_id']}"
                        )
                        if result.get("project"):
                            print(f"   Project: {result['project']}")
                        print(f"   Score: {result.get('similarity_score', 0):.3f}")
                        print(f"   Time: {result['timestamp']}")

                        # Truncate content for display
                        content = result["content"]
                        if len(content) > 200:
                            content = content[:200] + "..."
                        print(f"   Content: {content}")

        elif args.stats:
            stats = episodic.get_stats()

            if args.format == "json":
                print(json.dumps(stats, indent=2))
            else:
                if "error" in stats:
                    print(f"❌ Error getting stats: {stats['error']}")
                else:
                    print("📊 Episodic Memory Statistics")
                    print("=" * 30)
                    for key, value in stats.items():
                        if isinstance(value, int):
                            print(f"{key.replace('_', ' ').title()}: {value:,}")
                        else:
                            print(f"{key.replace('_', ' ').title()}: {value}")

        elif args.cleanup:
            print("🧹 Cleaning up old sessions...")
            result = episodic.cleanup_old_sessions()

            if args.format == "json":
                print(json.dumps(result, indent=2))
            else:
                if result["success"]:
                    print(f"✅ {result['message']}")
                else:
                    print(f"❌ Cleanup failed: {result.get('error', 'Unknown error')}")

        else:
            # Default action: show help
            parser.print_help()
            print("\n🚀 Enhanced Features:")
            print("  • PostgreSQL backend for production reliability")
            print("  • Adaptive indexing for fast incremental updates")
            print("  • Full-text search with similarity scoring")
            print("  • Resource-aware processing")
            print("  • Industry-standard SQL with proper indexing")

    except KeyboardInterrupt:
        print("\n⏹️  Operation interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        episodic.close()


if __name__ == "__main__":
    main()
