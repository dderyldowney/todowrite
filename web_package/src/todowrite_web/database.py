"""
Database configuration and session management for ToDoWrite web application.
"""

from sqlalchemy.orm import Session
from todowrite_web.main import SessionLocal

def get_db() -> Session:
    """
    Dependency function to get a database session.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()