from __future__ import annotations

import logging
from pathlib import Path

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

# Import ToDoWrite Models
from ..core.models import Base

# Import storage exceptions from updated storage module
from . import StorageConnectionError

logger = logging.getLogger(__name__)


class SQLiteBackend:
    """
    SQLite backend for ToDoWrite Models.

    Simplified implementation that works with the new ToDoWrite Models patterns.
    """

    def __init__(self, database_path: str | Path) -> None:
        """Initialize SQLite backend with database file path."""
        self.database_path = Path(database_path)
        self.database_url = f"sqlite:///{self.database_path}"
        self.engine: Engine | None = None
        self.Session: sessionmaker | None = None

        # Ensure parent directory exists
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> None:
        """Establish connection to SQLite database."""
        try:
            # Create engine optimized for SQLite
            self.engine = create_engine(
                self.database_url,
                echo=False,
                connect_args={
                    "check_same_thread": False,
                    "timeout": 30,
                },
                pool_pre_ping=True,
            )

            # Configure session factory
            self.Session = sessionmaker(
                bind=self.engine,
                expire_on_commit=False,
            )

            # Create tables using ToDoWrite Models
            Base.metadata.create_all(self.engine)

            logger.info(f"Connected to SQLite database: {self.database_path}")

        except Exception as e:
            raise StorageConnectionError(
                f"Failed to connect to SQLite: {e}"
            ) from e

    def disconnect(self) -> None:
        """Close SQLite connection."""
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self.Session = None
            logger.info("Disconnected from SQLite database")

    def get_session(self) -> Session:
        """Get a SQLAlchemy session."""
        if not self.Session:
            raise StorageConnectionError(
                "Not connected - call connect() first"
            )
        return self.Session()

    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            if not self.engine:
                return False
            with self.get_session() as session:
                session.execute(text("SELECT 1"))
                return True
        except Exception:
            return False
