"""Core module for ToDoWrite Models API."""

import logging

logger = logging.getLogger(__name__)

# This module is intentionally minimal - all functionality
# has been moved to the individual models and storage modules
# Use the ToDoWrite Models API directly:

# from todowrite import Goal, Task, create_engine, sessionmaker
#
# engine = create_engine("sqlite:///development.db")
# Session = sessionmaker(bind=engine)
# session = Session()
#
# goal = Goal(title="My Goal", owner="team")
# session.add(goal)
# session.commit()
