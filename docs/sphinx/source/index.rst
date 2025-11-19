ToDoWrite Documentation
=====================

Welcome to the comprehensive documentation for ToDoWrite, a hierarchical task management system built with ToDoWrite Models.

**ToDoWrite** provides a sophisticated 12-layer hierarchical task management system for complex project planning and execution.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   userdocs/overview
   userdocs/quickstart
   userdocs/todowrite_models_api
   library/todowrite
   library/models
   library/core_modules
   devdocs/contributing
   devdocs/schema

Features
--------

* **12-Layer Hierarchy**: Goal → Concept → Context → Constraints → Requirements → AcceptanceCriteria → InterfaceContract → Phase → Step → Task → SubTask → Command
* **Modern SQLAlchemy Patterns**: Modern SQLAlchemy ORM implementation with proper relationships
* **Multiple Storage Backends**: SQLite, PostgreSQL, and YAML file support
* **CLI Interface**: Full command-line interface for task management
* **Schema Validation**: JSON schema validation and database integrity checks
* **Rich Relationships**: Many-to-many associations through join tables

Getting Started
---------------

To start using ToDoWrite:

.. code-block:: python

   from todowrite import Goal, Task, initialize_database

   # Initialize database
   initialize_database("sqlite:///myproject.db")

   # Create a goal
   goal = Goal(
       title="Launch Product",
       description="Successfully launch the new product",
       owner="product-team",
       severity="high"
   )

   # Save to database
   session.add(goal)
   session.commit()

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
