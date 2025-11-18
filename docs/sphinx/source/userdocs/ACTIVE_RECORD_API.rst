ActiveRecord API Guide
======================

ToDoWrite provides Rails-inspired ActiveRecord patterns for intuitive database operations. This guide covers the recommended ActiveRecord-style API for modern Python development.

.. contents::
   :local:
   :depth: 2

Getting Started
---------------

### Session Configuration

**Required** for all ActiveRecord methods:

.. code-block:: python

   from todowrite import ToDoWrite, Node

   # Initialize application
   app = ToDoWrite("sqlite:///project.db")
   app.init_database()

   # Configure Node class with database session
   Node.configure_session(app.get_session())

   print("✅ ActiveRecord API ready!")

Factory Methods
---------------

### Creating New Records

.. code-block:: python

   # Create new instance (not saved)
   goal = Node.new(
       layer="Goal",
       title="Launch Product",
       description="Successfully launch v1.0",
       owner="product-team",
       severity="high"
   )

   # Save to database
   goal = goal.save()

   # Create and save in one step
   goal = Node.new(
       layer="Goal",
       title="Launch Product",
       owner="product-team"
   ).save()

### Layer-Specific Factory Methods

.. code-block:: python

   # Create specific layer types
   goal = Node.create_goal("Launch Product", "product-team",
                          description="Successfully launch v1.0")
   phase = Node.create_phase("Development", "GOAL-001",
                           description="Build the product")
   task = Node.create_task("Implement API", "PH-001", owner="backend-team")
   command = Node.create_command("Run Tests", "TSK-001", command="pytest")

Finder Methods
--------------

### Basic Finders

.. code-block:: python

   # Find by ID (like Rails .find())
   goal = Node.find("GOAL-001")  # Returns Node or None

   # Find by attributes (like Rails .find_by())
   task = Node.find_by(title="Implement API")  # Returns Node or None
   tasks = Node.find_by(owner="backend-team")  # Returns list[Node]

   # Get all records (like Rails .all())
   all_goals = Node.all()
   all_tasks = Node.where(layer="Task")

### Query Methods

.. code-block:: python

   # Where clauses (like Rails .where())
   high_priority = Node.where(severity="high")
   in_progress = Node.where(status="in_progress")
   backend_tasks = Node.where(owner="backend-team", layer="Task")

   # Chain queries (like Rails)
   backend_high_priority = Node.where(owner="backend-team").where(severity="high")

Instance Methods
----------------

### Persistence Operations

.. code-block:: python

   # Find existing node
   task = Node.find("TSK-001")

   # Update and save
   task.update(title="Updated Task Title", progress=75)
   task.save()  # Explicit save after update()

   # Reload from database
   task.reload()

   # Delete record
   task.destroy()

### Business Logic Methods

.. code-block:: python

   # Workflow state management
   task = Node.find("TSK-001")

   # Start work
   task.start().save()  # Sets status to "in_progress"

   # Mark complete
   task.complete().save()  # Sets status to "completed", progress to 100

   # Block work
   task.block().save()  # Sets status to "blocked"

   # Cancel work
   task.cancel().save()  # Sets status to "cancelled"

   # Update progress manually
   task.update_progress(50)  # Sets progress field

Collection Methods (Rails has_many style)
----------------------------------------

### Hierarchical Relationships

.. code-block:: python

   # Get a goal
   goal = Node.find("GOAL-001")

   # Access related collections (like Rails has_many)
   phases = goal.phases()          # Get Phase collection
   requirements = goal.requirements()  # Get Requirement collection
   tasks = goal.tasks()           # Get Task collection
   commands = goal.commands()     # Get Command collection

### Collection Operations

.. code-block:: python

   # Collection methods (like Rails collections)
   phases = goal.phases()

   # Get all items
   all_phases = phases.all()

   # Get count
   count = phases.size()

   # Check existence
   has_phases = phases.exists()
   is_empty = phases.empty()

   # Build new (not saved)
   new_phase = phases.build(
       title="Development Phase",
       description="Build the product"
   )

   # Create and save
   created_phase = phases.create(
       title="Development Phase",
       description="Build the product"
   )

   # Query within collection
   planned_phases = phases.where(status="planned")

Advanced Patterns
-----------------

### Method Chaining

.. code-block:: python

   # Chain multiple operations
   completed_task = Node.new(
       layer="Task",
       title="Quick Task",
       owner="dev"
   ).save().complete().save()

   # Chain queries
   backend_tasks = Node.where(layer="Task").where(owner="backend-team")
   high_priority_backend = backend_tasks.where(severity="high")

### Complex Queries

.. code-block:: python

   # Find with relationships
   goal_with_tasks = Node.find_with_children("GOAL-001", include_tasks=True)

   # Complex filtering
   critical_tasks = Node.where(
       layer="Task",
       severity="critical",
       status="in_progress"
   )

   # Business logic queries
   blocked_high_priority = Node.where(
       status="blocked",
       severity__in=["high", "critical"]
   )

Error Handling
--------------

### ActiveRecord-Style Errors

.. code-block:: python

   # Find operations return None (like Rails)
   node = Node.find("NONEXISTENT")
   if node is None:
       print("Node not found")

   # Session configuration errors
   try:
       Node.find("GOAL-001")  # Without configure_session()
   except RuntimeError as e:
       print(f"Session error: {e}")

   # Validation errors (if implemented)
   try:
       node = Node.new(layer="InvalidLayer").save()
   except Exception as e:
       print(f"Validation error: {e}")

Complete Example
----------------

Here's a complete workflow using the ActiveRecord API:

.. code-block:: python

   from todowrite import ToDoWrite, Node

   # Initialize application
   app = ToDoWrite("sqlite:///project.db")
   app.init_database()
   Node.configure_session(app.get_session())

   # Create a project goal
   goal = Node.create_goal(
       "Launch New Feature",
       "product-team",
       description="Successfully launch the new user dashboard",
       severity="high"
   )

   # Create phases
   design_phase = goal.phases().create(
       title="Design Phase",
       description="Create wireframes and mockups",
       owner="design-team"
   )

   dev_phase = goal.phases().create(
       title="Development Phase",
       description="Implement the feature",
       owner="backend-team"
   )

   # Create tasks for development phase
   api_task = dev_phase.tasks().create(
       title="Build API endpoints",
       owner="backend-team",
       severity="high"
   )

   ui_task = dev_phase.tasks().create(
       title="Create user interface",
       owner="frontend-team",
       severity="medium"
   )

   # Start working on tasks
   api_task.start().save()
   ui_task.start().save()

   # Update progress
   api_task.update_progress(75)

   # Complete a task
   ui_task.complete().save()

   # Check progress
   all_tasks = dev_phase.tasks().all()
   completed = dev_phase.tasks().where(status="completed")
   in_progress = dev_phase.tasks().where(status="in_progress")

   print(f"Goal: {goal.title}")
   print(f"Development Phase: {dev_phase.title}")
   print(f"Total tasks: {len(all_tasks)}")
   print(f"Completed: {len(completed)}")
   print(f"In Progress: {len(in_progress)}")

Migration from Traditional API
------------------------------

If you're currently using the traditional dictionary-based API, here's how to migrate:

**Traditional:**

.. code-block:: python

   # Old way
   app = ToDoWrite("sqlite:///project.db")
   app.init_database()

   node_data = {
       "id": "GOAL-001",
       "layer": "Goal",
       "title": "My Goal",
       "metadata": {"owner": "dev"}
   }
   goal = app.create_node(node_data)

**ActiveRecord:**

.. code-block:: python

   # New way
   app = ToDoWrite("sqlite:///project.db")
   app.init_database()
   Node.configure_session(app.get_session())

   goal = Node.create_goal("My Goal", "dev")

The ActiveRecord API provides:

* **Better type safety** - No more dictionary construction
* **Method chaining** - More expressive code
* **Business logic methods** - Built-in workflow management
* **Collection operations** - Rails-style relationship handling
* **Cleaner syntax** - More readable and maintainable code
