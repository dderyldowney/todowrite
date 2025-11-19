ToDoWrite Models
===============

This section documents all the ToDoWrite Models - the core data models that form the 12-layer hierarchy.

Model Hierarchy
---------------

.. code-block:: text

    Goal
    ├── Concept
    ├── Context
    ├── Constraints
    ├── Requirements
    ├── AcceptanceCriteria
    ├── InterfaceContract
    ├── Phase
    │   └── Step
    │       └── Task
    │           └── SubTask
    └── Command

Label is a shared model for many-to-many relationships across all layers.

Core Models
-----------

Goal
----

.. autoclass:: todowrite.Goal
   :members:
   :undoc-members:
   :show-inheritance:

Concept
-------

.. autoclass:: todowrite.Concept
   :members:
   :undoc-members:
   :show-inheritance:

Context
-------

.. autoclass:: todowrite.Context
   :members:
   :undoc-members:
   :show-inheritance:

Constraints
-----------

.. autoclass:: todowrite.Constraints
   :members:
   :undoc-members:
   :show-inheritance:

Requirements
------------

.. autoclass:: todowrite.Requirements
   :members:
   :undoc-members:
   :show-inheritance:

AcceptanceCriteria
------------------

.. autoclass:: todowrite.AcceptanceCriteria
   :members:
   :undoc-members:
   :show-inheritance:

InterfaceContract
------------------

.. autoclass:: todowrite.InterfaceContract
   :members:
   :undoc-members:
   :show-inheritance:

Phase
-----

.. autoclass:: todowrite.Phase
   :members:
   :undoc-members:
   :show-inheritance:

Step
----

.. autoclass:: todowrite.Step
   :members:
   :undoc-members:
   :show-inheritance:

Task
----

.. autoclass:: todowrite.Task
   :members:
   :undoc-members:
   :show-inheritance:

SubTask
-------

.. autoclass:: todowrite.SubTask
   :members:
   :undoc-members:
   :show-inheritance:

Command
-------

.. autoclass:: todowrite.Command
   :members:
   :undoc-members:
   :show-inheritance:

Label
-----

.. autoclass:: todowrite.Label
   :members:
   :undoc-members:
   :show-inheritance:

Schema Information
-----------------

* **Total Tables**: 33 (12 model tables + 21 association tables)
* **Primary Keys**: Auto-incrementing integers (1, 2, 3, ...)
* **Foreign Keys**: Proper referential integrity
* **Database Support**: SQLite and PostgreSQL
* **Schema Files**: Available in ``lib_package/src/todowrite/core/schemas/``

For detailed SQL and JSON schemas, see :doc:`../devdocs/schema`.
