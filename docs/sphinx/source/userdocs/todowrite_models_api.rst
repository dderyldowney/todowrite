ToDoWrite Models API Reference
===============================

This section provides a comprehensive reference for ToDoWrite Models implementation.

Core Imports
------------

.. code-block:: python

   from todowrite import (
       # ToDoWrite Models (12 layers)
       Goal, Concept, Context, Constraints,
       Requirements, AcceptanceCriteria, InterfaceContract,
       Phase, Step, Task, SubTask, Command,
       Label,

       # Database utilities
       Base, create_engine, sessionmaker,

       # Schema validation
       initialize_database, validate_model_data,
   )

Database Operations
-------------------

**Initialize Database**

.. code-block:: python

   from todowrite.core.schema_validator import initialize_database

   # Initialize with SQLite
   initialize_database("sqlite:///project.db")

   # Initialize with PostgreSQL
   initialize_database("postgresql://user:pass@localhost/project")

**Create Session**

.. code-block:: python

   from sqlalchemy import create_engine
   from sqlalchemy.orm import sessionmaker

   engine = create_engine("sqlite:///project.db")
   Session = sessionmaker(bind=engine)
   session = Session()

Models
------

All models follow ToDoWrite Models patterns with integer primary keys.

**Goal Model**

.. autoclass:: todowrite.Goal
   :members:
   :undoc-members:

**Task Model**

.. autoclass:: todowrite.Task
   :members:
   :undoc-members:

**Command Model**

.. autoclass:: todowrite.Command
   :members:
   :undoc-members:

**Label Model**

.. autoclass:: todowrite.Label
   :members:
   :undoc-members:

Relationships
------------

**Many-to-Many Associations**

All models support many-to-many relationships through join tables:

.. code-block:: python

   # Create a goal
   goal = Goal(title="Launch Product", owner="team")
   session.add(goal)

   # Create tasks
   task1 = Task(title="Design UI", owner="designer")
   task2 = Task(title="Write tests", owner="developer")
   session.add(task1)
   session.add(task2)

   # Associate tasks with goal
   goal.tasks.append(task1)
   goal.tasks.append(task2)

   # Create and associate labels
   urgent_label = Label(name="urgent")
   design_label = Label(name="design")
   session.add(urgent_label)
   session.add(design_label)

   task1.labels.extend([urgent_label, design_label])
   task2.labels.append(urgent_label)

   session.commit()

**Query Patterns**

.. code-block:: python

   # Get all goals
   goals = session.query(Goal).all()

   # Get tasks for a specific goal
   goal_tasks = session.query(Task).filter(Task.goals.contains(goal)).all()

   # Get tasks with specific labels
   from sqlalchemy.orm import joinedload
   urgent_tasks = session.query(Task).options(
       joinedload(Task.labels)
   ).filter(Task.labels.any(Label.name == "urgent")).all()

Schema Validation
-----------------

**Validate Model Data**

.. code-block:: python

   from todowrite.core.schema_validator import validate_model_data

   # Validate a task dictionary
   task_data = {
       "title": "New Task",
       "description": "Task description",
       "owner": "team",
       "severity": "high"
   }

   is_valid, errors = validate_model_data(Task, task_data)
   if not is_valid:
       print("Validation errors:", errors)

Complete Model List
------------------

The 12 ToDoWrite Models are:

1. **Goal** - High-level project objectives
2. **Concept** - Abstract ideas and requirements
3. **Context** - Background information and constraints
4. **Constraints** - Technical and business constraints
5. **Requirements** - Specific functional requirements
6. **AcceptanceCriteria** - Definition of done criteria
7. **InterfaceContract** - API and interface contracts
8. **Phase** - Project phases and milestones
9. **Step** - Individual steps within phases
10. **Task** - Specific tasks with owners and status
11. **SubTask** - Breakdown of tasks into smaller units
12. **Command** - Executable commands and scripts

Plus the **Label** model for many-to-many tagging.

For detailed model documentation, see :doc:`../library/models`.
