#!/usr/bin/env python3
"""
Session State Manager for ToDoWrite PostgreSQL Backend
Automatically saves and restores session state when CLAUDE.md is loaded
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import psycopg2


class SessionManager:
    """Manages session state persistence and restoration"""

    def __init__(self):
        # Load configuration from environment variables
        self.db_config = {
            "host": os.environ.get("TODOWRITE_DB_HOST", "localhost"),
            "port": int(os.environ.get("TODOWRITE_DB_PORT", "5432")),
            "database": os.environ.get(
                "TODOWRITE_DATABASE_URL",
                "postgresql://todowrite_user:todowrite_secure_password_2024@localhost:5432/todowrite",
            ).split("/")[-1],  # Extract database name from URL
            "user": os.environ.get("TODOWRITE_DB_USER", "todowrite_user"),
            "password": os.environ.get("TODOWRITE_DB_PASSWORD", "todowrite_secure_password_2024"),
        }
        self.project_name = Path.cwd().name
        self.session_id = self._get_or_create_session_id()

    def _get_or_create_session_id(self) -> str:
        """Get or create session ID"""
        # Use existing session ID if available
        session_id = os.environ.get("TODOWRITE_SESSION_ID")

        if not session_id:
            # Create session ID following existing pattern
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_id = f"todowrite_session_{timestamp}_{os.getpid()}"
            os.environ["TODOWRITE_SESSION_ID"] = session_id

        return session_id

    def _check_port(self, port: int) -> bool:
        """Check if port is open and accessible"""
        try:
            import socket

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex(("localhost", port))
            sock.close()
            return result == 0
        except OSError:
            return False

    def save_session_state(self, context: dict[str, str | int | bool | None]) -> bool:
        """Save current session state to database"""
        try:
            conn = psycopg2.connect(**self.db_config)
            with conn.cursor() as cursor:
                session_data = {
                    "session_id": self.session_id,
                    "project": self.project_name,
                    "timestamp": datetime.now().isoformat(),
                    "context": context,
                    "claude_md_loaded": True,
                    "last_activity": datetime.now().isoformat(),
                }

                cursor.execute(
                    """
                    INSERT INTO sessions (
                        session_id, project_directory, environment_vars, context_summary, status
                    ) VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (session_id)
                    DO UPDATE SET
                        environment_vars = %s,
                        context_summary = %s,
                        session_end = NULL,
                        status = 'active'
                """,
                    (
                        self.session_id,
                        str(Path.cwd()),  # project_directory
                        json.dumps(
                            {"project": self.project_name, "environment": "claude_session"}
                        ),  # environment_vars
                        f"Session: {session_data.get('session_type', 'Development session')}",  # context_summary
                        "active",  # status
                        json.dumps(session_data),  # for UPDATE environment_vars
                        f"Session: {session_data.get('session_type', 'Development session')}",  # for UPDATE context_summary
                    ),
                )

                conn.commit()
                print(f"✅ Session state saved: {self.session_id}")
                return True

        except Exception as e:
            print(f"❌ Failed to save session state: {e}")
            return False
        finally:
            if "conn" in locals():
                conn.close()

    def load_latest_session_state(self) -> dict[str, str | int | bool | None] | None:
        """Load the most recent session state for this project"""
        try:
            conn = psycopg2.connect(**self.db_config)
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT environment_vars, context_summary, session_start, project_directory
                    FROM sessions
                    WHERE project_directory LIKE %s OR environment_vars::text LIKE %s
                    ORDER BY session_start DESC
                    LIMIT 1
                """,
                    (f"%{self.project_name}%", f'%"project": "{self.project_name}"%'),
                )

                result = cursor.fetchone()
                if result:
                    environment_vars, context_summary, session_start, project_directory = result
                    print(f"✅ Loaded session state from {session_start}")
                    print(f"📁 Project: {project_directory}")
                    print(f"📝 Context: {context_summary}")
                    # Handle both string and dict environment_vars
                    if isinstance(environment_vars, str):
                        return json.loads(environment_vars)
                    elif isinstance(environment_vars, dict):
                        return environment_vars
                    else:
                        print(f"⚠️  Unexpected environment_vars type: {type(environment_vars)}")
                        return None
                else:
                    print("No previous session state found")
                    return None

        except Exception as e:
            print(f"❌ Failed to load session state: {e}")
            return None
        finally:
            if "conn" in locals():
                conn.close()

    def get_session_summary(self) -> str:
        """Get a formatted summary of the latest session"""
        state = self.load_latest_session_state()
        if not state:
            return "No previous session state found."

        context = state.get("context", {})
        accomplishments = context.get("accomplishments", [])
        key_findings = context.get("key_findings", [])
        system_status = context.get("system_status", {})

        summary = f"""
🔄 **SESSION RESTORED** - {state.get("timestamp", "Unknown time")}

📋 **Previous Accomplishments:**
{chr(10).join(f"  • {acc}" for acc in accomplishments)}

🔍 **Key Findings:**
{chr(10).join(f"  • {finding}" for finding in key_findings)}

🗄️ **System Status:**
  • Container: {system_status.get("container", "Unknown")}
  • Database: {system_status.get("database", "Unknown")}
  • Tables: {system_status.get("tables", "Unknown")}
  • Port: {system_status.get("port", "Unknown")}

💾 **Session ID:** {self.session_id}
📁 **Project:** {self.project_name}

Ready to continue development with full context restored!
"""
        return f"""{summary}"""


def save_current_session(context: dict[str, str | int | bool | None]) -> bool:
    """Convenience function to save current session"""
    manager = SessionManager()
    return manager.save_session_state(context)


def load_session_summary() -> str:
    """Convenience function to get session summary"""
    manager = SessionManager()
    return manager.get_session_summary()


def main():
    """CLI interface for session management"""
    import argparse

    parser = argparse.ArgumentParser(description="Manage ToDoWrite session state")
    parser.add_argument("--save", action="store_true", help="Save current session state")
    parser.add_argument("--load", action="store_true", help="Load and display latest session")
    parser.add_argument("--summary", action="store_true", help="Get session summary")
    parser.add_argument("--context", help="JSON context to save")

    args = parser.parse_args()

    if args.save and args.context:
        context = json.loads(args.context)
        success = save_current_session(context)
        sys.exit(0 if success else 1)
    elif args.load:
        manager = SessionManager()
        state = manager.load_latest_session_state()
        if state:
            print(json.dumps(state, indent=2))
        sys.exit(0 if state else 1)
    elif args.summary:
        print(load_session_summary())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
