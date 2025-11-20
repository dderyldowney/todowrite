#!/usr/bin/env python3
"""
ToDoWrite Session Initialization Script

This script automatically initializes the ToDoWrite system for every session,
including after '/clear' commands and emergency recoveries. It ensures the
database is loaded and ready for development tracking.

Author: Claude Code Assistant
Version: 2025.1.0
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add project paths for imports
project_root = Path.cwd()
sys.path.insert(0, str(project_root / "lib_package" / "src"))
sys.path.insert(0, str(project_root / "cli_package" / "src"))

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from todowrite.core.models import Base, Goal

except ImportError as e:
    print(f"❌ Failed to import todowrite modules: {e}")
    sys.exit(1)

# Global session variables
_session_initialized = False
_db_session = None
_database_url = None


def get_database_url() -> str:
    """Get the PostgreSQL database URL from environment."""
    global _database_url

    if _database_url is None:
        # Load PostgreSQL environment from .claude/postgresql_env.sh
        postgresql_env_file = project_root / ".claude" / "postgresql_env.sh"
        if postgresql_env_file.exists():
            # Read and source the environment file
            with open(postgresql_env_file) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("export TODOWRITE_DATABASE_URL="):
                        _database_url = line.split("=", 1)[1].strip('"')
                        break

        # Fallback to environment variable if file not found
        if _database_url is None:
            # pragma: allowlist secret
            _database_url = os.getenv(
                "TODOWRITE_DATABASE_URL",
                "postgresql://todowrite:todowrite_dev_password@localhost:5432/todowrite",
            )

    return _database_url


def get_session_database_url() -> str:
    """Get the PostgreSQL database URL for session tracking."""
    return get_database_url()


def initialize_ToDoWrite_session() -> bool:
    """
    Initialize ToDoWrite session for development tracking using PostgreSQL.

    Returns:
        True if initialization successful, False otherwise
    """
    global _session_initialized, _db_session

    if _session_initialized:
        return True

    try:
        print("🔧 Initializing ToDoWrite session for development tracking...")

        # Get PostgreSQL database URL
        database_url = get_database_url()
        print(f"   Using PostgreSQL database: {database_url}")

        # Initialize ToDoWrite Models database
        engine = create_engine(database_url)
        Base.metadata.create_all(engine)

        # Create session for development database
        Session = sessionmaker(bind=engine)
        _db_session = Session()

        # Initialize session tracking table in PostgreSQL
        from datetime import datetime

        from sqlalchemy import Integer, String, Text
        from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

        class SessionBase(DeclarativeBase):
            pass

        class DevelopmentSession(SessionBase):
            __tablename__ = "development_sessions"

            id: Mapped[int] = mapped_column(Integer, primary_key=True)
            session_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
            start_time: Mapped[str] = mapped_column(String, nullable=False)
            activities_completed: Mapped[int] = mapped_column(Integer, default=0)
            notes: Mapped[str | None] = mapped_column(Text)
            created_at: Mapped[str] = mapped_column(
                String, default=lambda: datetime.now().isoformat(), nullable=False
            )

        # Create session tracking table
        SessionBase.metadata.create_all(engine)

        # Create session record
        session_record = DevelopmentSession(
            session_id=datetime.now().strftime("%Y%m%d_%H%M%S"),
            start_time=datetime.now().isoformat(),
            activities_completed=0,
            notes="ToDoWrite Models Session Initialized",
        )
        _db_session.add(session_record)
        _db_session.commit()

        # Verify ToDoWrite functionality
        test_goal = Goal(title="Test Goal", owner="session-init")
        _db_session.add(test_goal)
        _db_session.commit()

        print("✅ ToDoWrite session initialized successfully!")
        print(f"   PostgreSQL Database: {database_url}")
        print("   API: Working correctly")

        _session_initialized = True
        return True

    except Exception as e:
        print(f"❌ Failed to initialize ToDoWrite session: {e}")
        return False


def get_ToDoWrite_session():
    """Get the current ToDoWrite database session."""
    if not _session_initialized:
        initialize_ToDoWrite_session()
    return _db_session


def create_session_marker() -> None:
    """Create a marker file indicating successful session initialization."""
    marker_data = {
        "session_init_time": datetime.now().isoformat(),
        "database_url": get_database_url(),
        "session_type": "todowrite_development_tracking",
        "version": "2025.1.0",
    }

    claude_dir = project_root / ".claude"
    marker_file = claude_dir / "ToDoWrite_session_active.json"

    try:
        import json

        # Ensure .claude directory exists before creating the marker
        claude_dir.mkdir(exist_ok=True)

        with open(marker_file, "w") as f:
            json.dump(marker_data, f, indent=2)
        print(f"✅ Session marker created: {marker_file}")

    except FileNotFoundError as e:
        print(f"❌ Cannot create session marker - directory not found: {e}")
        raise
    except PermissionError as e:
        print(f"❌ Cannot create session marker - permission denied: {e}")
        raise
    except OSError as e:
        print(f"❌ Cannot create session marker - OS error: {e}")
        raise


def verify_session_health() -> dict:
    """
    Verify the health of the current ToDoWrite session.

    Returns:
        Dictionary with health status information
    """
    try:
        if not _session_initialized:
            return {"status": "not_initialized", "message": "Session not initialized"}

        # Test database connection by checking goals count
        from todowrite.core.models import Goal

        goals_count = _db_session.query(Goal).count()

        return {
            "status": "healthy",
            "database_url": get_database_url(),
            "goals": goals_count,
            "session_active": _session_initialized,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "database_url": get_database_url() if _database_url else "unknown",
        }


def main():
    """Main initialization function."""
    print("🚀 ToDoWrite Session Initialization")
    print("=" * 50)

    success = initialize_ToDoWrite_session()

    if success:
        create_session_marker()

        health = verify_session_health()
        print("\n📊 Session Health Status:")
        print(f"   Status: {health['status']}")
        print(f"   Database: {health['database_url']}")
        print(f"   Goals: {health.get('goals', 0)}")

        print("\n✅ ToDoWrite system ready for development tracking!")
        print("   All development work should now be tracked using ToDoWrite.")
        print("   Use the ToDoWrite API for task management.")

        return 0
    else:
        print("\n❌ Failed to initialize ToDoWrite system")
        print("   Development tracking will not be available")
        return 1


if __name__ == "__main__":
    sys.exit(main())
