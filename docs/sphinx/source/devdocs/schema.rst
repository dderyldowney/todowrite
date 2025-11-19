Database Schema
===============

This section provides detailed information about the ToDoWrite Models database schema.

Schema Overview
---------------

The ToDoWrite Models implementation uses:

* **33 Total Tables**: 12 model tables + 21 association tables
* **Integer Primary Keys**: Auto-incrementing IDs (1, 2, 3, ...)
* **Proper Foreign Keys**: Referential integrity across all relationships
* **Database Support**: SQLite and PostgreSQL

Schema Files
------------

The complete database schema is available in the following files:

SQL Schema
~~~~~~~~~

The SQL schema file contains complete table definitions for SQLite:

* ``lib_package/src/todowrite/core/schemas/todowrite_models_schema.sql``

.. literalinclude:: ../../../../lib_package/src/todowrite/core/schemas/todowrite_models_schema.sql
   :language: sql
   :lines: 1-50

JSON Schema
~~~~~~~~~~

The JSON schema provides detailed model definitions for validation:

* ``lib_package/src/todowrite/core/schemas/todowrite_models.schema.json``

.. literalinclude:: ../../../../lib_package/src/todowrite/core/schemas/todowrite_models.schema.json
   :language: json
   :lines: 1-30

Model Tables
------------

Each of the 12 ToDoWrite Models has its own table:

1. **goals** - Project objectives
2. **concepts** - Abstract ideas
3. **contexts** - Background information
4. **constraints** - Technical/business constraints
5. **requirements** - Functional requirements
6. **acceptance_criteria** - Definition of done criteria
7. **interface_contracts** - API contracts
8. **phases** - Project phases
9. **steps** - Individual steps
10. **tasks** - Specific tasks
11. **sub_tasks** - Task breakdowns
12. **commands** - Executable commands
13. **labels** - Tagging system

Association Tables
------------------

Many-to-many relationships are handled through join tables following the pattern:

.. code-block:: sql

   -- Example: goals and tasks relationship
   CREATE TABLE goals_tasks (
       goal_id INTEGER NOT NULL,
       task_id INTEGER NOT NULL,
       FOREIGN KEY (goal_id) REFERENCES goals(id),
       FOREIGN KEY (task_id) REFERENCES tasks(id),
       PRIMARY KEY (goal_id, task_id)
   );

Common association tables include:

* ``goals_tasks`` - Goals ↔ Tasks
* ``tasks_labels`` - Tasks ↔ Labels
* ``commands_labels`` - Commands ↔ Labels
* ``phases_steps`` - Phases ↔ Steps
* ``steps_tasks`` - Steps ↔ Tasks
* ``tasks_sub_tasks`` - Tasks ↔ SubTasks

And many more to support the complete hierarchy.

Foreign Key Constraints
------------------------

All association tables maintain referential integrity:

* **Parent-Child**: Direct hierarchy relationships
* **Many-to-Many**: Cross-layer associations
* **Cascading**: Proper cascade rules for data consistency

Schema Validation
------------------

The schema is validated using:

1. **JSON Schema**: Data structure validation
2. **SQLAlchemy ORM**: Model definition validation
3. **Database Constraints**: Referential integrity checks

For programmatic schema validation, see :doc:`../userdocs/todowrite_models_api`.
