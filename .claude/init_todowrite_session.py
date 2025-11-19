#!/usr/bin/env python3
"""
ToDoWrite Session Initialization Script

This script automatically initializes the ToDoWrite system for every session,
including after '/clear' commands and emergency recoveries. It ensures the
database is loaded and ready for development tracking.

Author: Claude Code Assistant
Version: 2025.1.0
"""

import sys
from datetime import datetime
from pathlib import Path

# Add project paths for imports
project_root = Path.cwd()
sys.path.insert(0, str(project_root / "lib_package" / "src"))
sys.path.insert(0, str(project_root / "cli_package" / "src"))

try:
    import todowrite as ToDoWrite
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from todowrite.core.models import Base, Goal, Label, Task

except ImportError as e:
    print(f"❌ Failed to import todowrite modules: {e}")
    sys.exit(1)

# Global session variables
_session_initialized = False
_db_session = None
_db_path = None


def get_database_path() -> Path:
    """Get the path to the ToDoWrite database."""
    global _db_path

    if _db_path is None:
        # Use correct development database in ~/dbs/
        _db_path = Path.home() / "dbs" / "todowrite_development.db"

    return _db_path


def get_session_database_path() -> Path:
    """Get the path to the ToDoWrite session tracking database."""
    return Path.home() / "dbs" / "todowrite_sessions.db"


def initialize_ToDoWrite_session() -> bool:
    """
    Initialize ToDoWrite session for development tracking.

    Returns:
        True if initialization successful, False otherwise
    """
    global _session_initialized, _db_session

    if _session_initialized:
        return True

    try:
        print("🔧 Initializing ToDoWrite session for development tracking...")

        # Setup development database with proper directory handling
        db_path = get_database_path()
        db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize ToDoWrite Models database
        engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(engine)

        # Create session for development database
        Session = sessionmaker(bind=engine)
        _db_session = Session()

        # Initialize session tracking database
        session_db_path = get_session_database_path()
        session_db_path.parent.mkdir(parents=True, exist_ok=True)

        from datetime import datetime

        from sqlalchemy import Column, Integer, String, Text
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

        session_engine = create_engine(f"sqlite:///{session_db_path}")
        SessionBase.metadata.create_all(session_engine)
        session_session = sessionmaker(bind=session_engine)()

        # Create session record
        session_record = DevelopmentSession(
            session_id=datetime.now().strftime("%Y%m%d_%H%M%S"),
            start_time=datetime.now().isoformat(),
            activities_completed=0,
            notes="ToDoWrite Models Session Initialized",
        )
        session_session.add(session_record)
        session_session.commit()
        session_session.close()
        session_engine.dispose()

        # Verify ToDoWrite functionality
        test_goal = Goal(title="Test Goal", owner="session-init")
        _db_session.add(test_goal)
        _db_session.commit()

        print("✅ ToDoWrite session initialized successfully!")
        print(f"   Development Database: {db_path}")
        print(f"   Session Database: {session_db_path}")
        print("   API: Working correctly")

        _session_initialized = True
        return True

    except (FileNotFoundError, PermissionError) as e:
        print(f"❌ Cannot initialize ToDoWrite session - file system error: {e}")
        return False
    except ImportError as e:
        print(f"❌ Cannot initialize ToDoWrite session - missing dependencies: {e}")
        return False
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
        "database_path": str(get_database_path()),
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

        # Test database connection
        total_nodes = len(Node.all())

        # Test queries
        goals_count = len(Node.where(layer="Goal"))
        tasks_count = len(Node.where(layer="SubTask"))

        # Check for our production goal
        prod_goals = Node.find_by(title="Deploy ToDoWrite as Standard Development Tracking System")

        return {
            "status": "healthy",
            "database_path": str(get_database_path()),
            "total_nodes": total_nodes,
            "goals": goals_count,
            "tasks": tasks_count,
            "production_goal_found": len(prod_goals) > 0,
            "session_active": _session_initialized,
        }


    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "database_path": str(get_database_path()) if _db_path else "unknown",
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
        print(f"   Database: {health['database_path']}")
        print(f"   Total nodes: {health.get('total_nodes', 0)}")
        print(f"   Goals: {health.get('goals', 0)}")
        print(f"   Tasks: {health.get('tasks', 0)}")

        if health.get("production_goal_found"):
            print("   ✅ Production goal active")

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
