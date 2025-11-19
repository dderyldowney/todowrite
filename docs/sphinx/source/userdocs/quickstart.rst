Quick Start Guide
=================

This guide will get you up and running with ToDoWrite in minutes.

Installation
------------

Install ToDoWrite using pip:

.. code-block:: bash

   pip install todowrite

Or install from source:

.. code-block:: bash

   git clone https://github.com/dderyldowney/todowrite.git
   cd todowrite
   pip install -e .

Basic Usage
-----------

**Python API**

.. code-block:: python

   from todowrite import Goal, Task, Command, Label, create_engine, sessionmaker
   from todowrite.core.schema_validator import initialize_database

   # Initialize database
   initialize_database("sqlite:///myproject.db")

   # Create database session
   engine = create_engine("sqlite:///myproject.db")
   Session = sessionmaker(bind=engine)
   session = Session()

   # Create a goal
   goal = Goal(
       title="Launch Product",
       description="Successfully launch the new product",
       owner="product-team",
       severity="high"
   )
   session.add(goal)
   session.commit()

   # Create tasks for the goal
   task = Task(
       title="Design UI mockups",
       description="Create user interface mockups for the product",
       owner="design-team",
       severity="medium",
       work_type="implementation"
   )
   session.add(task)
   session.commit()

   # Add labels
   label = Label(name="urgent")
   session.add(label)
   session.commit()

   # Associate label with task
   task.labels.append(label)
   session.commit()

**CLI Interface**

Initialize a new project:

.. code-block:: bash

   todowrite init

Create items:

.. code-block:: bash

   # Create a goal
   todowrite create Goal "Launch Product" \
       --description "Successfully launch the new product" \
       --owner "product-team" \
       --severity "high"

   # Create a task
   todowrite create Task "Design UI mockups" \
       --description "Create user interface mockups" \
       --owner "design-team" \
       --severity "medium"

List items:

.. code-block:: bash

   # List all goals
   todowrite list --layer Goal

   # List all tasks
   todowrite list --layer Task

   # List everything
   todowrite list

Get status:

.. code-block:: bash

   todowrite status
   todowrite db-status

Database Schema
---------------

ToDoWrite automatically creates the proper database schema with 33 tables:

* **12 Model Tables**: ``goals``, ``tasks``, ``commands``, etc.
* **21 Association Tables**: ``goals_tasks``, ``tasks_labels``, etc.
* **Proper Foreign Keys**: All relationships maintain referential integrity

The schema is available in:

* :doc:`../devdocs/schema` - Complete SQL and JSON schemas
* ``lib_package/src/todowrite/core/schemas/`` - Machine-readable schema files

Next Steps
----------

* :doc:`todowrite_models_api` - Complete API reference
* :doc:`../library/models` - Model documentation
* :doc:`../devdocs/contributing` - Contributing guide
