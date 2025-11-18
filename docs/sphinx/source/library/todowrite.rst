todowrite library package
=======================

**Modern API Only** - The old Node-based API has been completely removed.

.. automodule:: todowrite
   :members:
   :show-inheritance:
   :undoc-members:

Models
------------------------

The todowrite package provides ToDoWrite Models for hierarchical task management:

**Core Models (12 Layers)**:

.. autoclass:: todowrite.Goal
   :members:
   :show-inheritance:
   :undoc-members:

.. autoclass:: todowrite.Concept
   :members:
   :show-inheritance:
   :undoc-members:

.. autoclass:: todowrite.Context
   :members:
   :show-inheritance:
   :undoc-members:

.. autoclass:: todowrite.Constraints
   :members:
   :show-inheritance:
   :undoc-members:

.. autoclass:: todowrite.Requirements
   :members:
   :show-inheritance:
   :undoc-members:

.. autoclass:: todowrite.AcceptanceCriteria
   :members:
   :show-inheritance:
   :undoc-members:

.. autoclass:: todowrite.InterfaceContract
   :members:
   :show-inheritance:
   :undoc-members:

.. autoclass:: todowrite.Phase
   :members:
   :show-inheritance:
   :undoc-members:

.. autoclass:: todowrite.Step
   :members:
   :show-inheritance:
   :undoc-members:

.. autoclass:: todowrite.Task
   :members:
   :show-inheritance:
   :undoc-members:

.. autoclass:: todowrite.SubTask
   :members:
   :show-inheritance:
   :undoc-members:

.. autoclass:: todowrite.Command
   :members:
   :show-inheritance:
   :undoc-members:

.. autoclass:: todowrite.Label
   :members:
   :show-inheritance:
   :undoc-members:

**Database Utilities**:

.. autoclass:: sqlalchemy.engine.Engine
   :members:
   :show-inheritance:
   :undoc-members:

.. autoclass:: sqlalchemy.orm.sessionmaker
   :members:
   :show-inheritance:
   :undoc-members:

Subpackages
-----------

.. toctree::
   :maxdepth: 4

   todowrite.core

Core Database Components
------------------------

.. automodule:: todowrite.core
   :members:
   :show-inheritance:
   :undoc-members:

SQLAlchemy Base
~~~~~~~~~~~~~~

.. autoclass:: todowrite.core.types.Base
   :members:
   :show-inheritance:
   :undoc-members:

Version Information
-------------------

.. automodule:: todowrite.version
   :members:
   :show-inheritance:
   :undoc-members:

Usage Examples
--------------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from todowrite import Goal, Task, Label, create_engine, sessionmaker

   # Initialize database session (Development)
   engine = create_engine("sqlite:////$HOME/dbs/todowrite_development.db")
   Session = sessionmaker(bind=engine)
   session = Session()

   # Create a goal
   goal = Goal(
       title="Launch Product",
       description="Successfully launch v1.0",
       owner="product-team",
       severity="high"
   )
   session.add(goal)
   session.commit()

   print(f"Created goal with ID: {goal.id}")  # Integer: 1, 2, 3...

   # Create and associate labels
   label = Label(name="product")
   session.add(label)
   session.commit()

   goal.labels.append(label)
   session.commit()

   # Query records
   all_goals = session.query(Goal).all()
   high_priority = session.query(Goal).filter(Goal.severity == "high").all()

Associations
~~~~~~~~~~~~

.. code-block:: python

   # Many-to-many relationships
   task = Task(title="Build API", owner="backend-team")
   session.add(task)
   session.commit()

   database_label = Label(name="database")
   session.add(database_label)
   session.commit()

   # Associate (Rails-style)
   task.labels.append(database_label)
   session.commit()

   # Access associations
   print(f"Task labels: {[l.name for l in task.labels]}")
   print(f"Label tasks: {[t.title for t in database_label.tasks]}")

Hierarchical Relationships
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Create goal with phases
   goal = Goal(title="Complete Project", owner="manager")
   phase = Phase(title="Development", owner="tech-lead")
   session.add_all([goal, phase])
   session.commit()

   # Associate
   goal.phases.append(phase)
   session.commit()

   # Create task under phase
   task = Task(title="Build Backend", owner="backend-team")
   session.add(task)
   session.commit()

   phase.tasks.append(task)
   session.commit()

Data Schema
~~~~~~~~~~~

For complete database schema documentation, see :doc:`../userdocs/ToDoWrite_Data_Schema`.

Key Features:

* **Integer Primary Keys**: Auto-incrementing integers (1, 2, 3, 4, 5...)
* **Timestamp Fields**: ``created_at`` and ``updated_at`` fields on all models
* **Proper Foreign Keys**: Enforced referential integrity
* **Many-to-Many Associations**: Standard join tables
* **Type Safety**: Full SQLAlchemy model definitions

Migration Information
~~~~~~~~~~~~~~~~~~~~

**⚠️  BREAKING CHANGE**: The old Node-based API has been completely removed.

Old API (removed):

.. code-block:: python

   # ❌ NO LONGER EXISTS
   from todowrite import Node, create_node
   node = create_node(database, node_data)

New ToDoWrite Models API:

.. code-block:: python

   # ✅ USE THIS INSTEAD
   from todowrite import Task, create_engine, sessionmaker

   engine = create_engine("sqlite:////$HOME/dbs/todowrite_development.db")
   Session = sessionmaker(bind=engine)
   session = Session()

   task = Task(title="My Task", owner="team")
   session.add(task)
   session.commit()
