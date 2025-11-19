ToDoWrite Overview
=================

ToDoWrite is a sophisticated hierarchical task management system designed for complex project planning and execution. Built with modern SQLAlchemy patterns, it provides both a standalone CLI and a Python module for programmatic use.

Architecture
------------

**12-Layer Hierarchy**

ToDoWrite uses a 12-layer hierarchical structure that maps to natural project planning:

.. code-block:: text

    Goal           → High-level project objectives
    ↓
    Concept        → Abstract ideas and requirements
    ↓
    Context        → Background information and constraints
    ↓
    Constraints    → Technical and business constraints
    ↓
    Requirements   → Specific functional requirements
    ↓
    AcceptanceCriteria → Definition of done criteria
    ↓
    InterfaceContract → API and interface contracts
    ↓
    Phase          → Project phases and milestones
    ↓
    Step           → Individual steps within phases
    ↓
    Task           → Specific tasks with owners and status
    ↓
    SubTask        → Breakdown of tasks into smaller units
    ↓
    Command        → Executable commands and scripts

**ToDoWrite Models Implementation**

* **Individual Tables**: Each layer has its own database table (e.g., ``goals``, ``tasks``, ``commands``)
* **Integer Primary Keys**: Auto-incrementing integer IDs (1, 2, 3, ...)
* **Proper Relationships**: Many-to-many associations through join tables
* **SQLAlchemy ORM**: Full SQLAlchemy integration with type hints
* **Schema Validation**: JSON schema validation for data integrity

Key Features
------------

* **Modern Database Design**: 33 tables total (12 model + 21 association tables)
* **Rich Relationships**: Complex many-to-many associations with proper foreign keys
* **CLI Interface**: Full command-line interface for all operations
* **Schema Validation**: Comprehensive JSON schema validation
* **Multiple Storage**: SQLite, PostgreSQL, and YAML file support
* **Type Safety**: Full Python 3.12+ type hints throughout
* **Extensible**: Plugin architecture for custom functionality
