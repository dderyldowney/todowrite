SQLAlchemy ORM API Guide
========================

ToDoWrite provides SQLAlchemy ORM interfaces for hierarchical task management with proper foreign key relationships and referential integrity. This is the **ONLY supported API** - the old Node-based API has been completely removed.

.. contents::
   :local:
   :depth: 2

Getting Started
---------------

### Database Session Configuration

**Required** for all SQLAlchemy operations:

.. code-block:: python

   from todowrite import (
       Goal, Concept, Context, Constraints,
       Requirements, AcceptanceCriteria, InterfaceContract,
       Phase, Step, Task, SubTask, Command, Label,
       create_engine, sessionmaker
   )

   # Development database
   engine = create_engine("sqlite:///project.db")
   Session = sessionmaker(bind=engine)
   session = Session()

   print("✅ SQLAlchemy ORM API ready!")

**Database Naming Conventions:**

- **Development**: ``sqlite:///project.db`` (Development work)
- **Production**: ``postgresql://user:pass@localhost/projectdb`` (Production)
- **Development**: ``$HOME/dbs/todowrite_development.db`` (All development work)
- **Testing**: ``tests/todowrite_testing.db`` (Test suite only)
- **Sessions**: ``$HOME/dbs/todowrite_sessions.db`` (Session tracking)

### Supported Models

ToDoWrite provides models for each of the 12 hierarchical layers:

.. code-block:: python

   from todowrite import (
       Goal, Concept, Context, Constraints, Requirements,
       AcceptanceCriteria, InterfaceContract, Phase, Step,
       Task, SubTask, Command, Label,
       create_engine, sessionmaker
   )

   # All models follow standard patterns
   # Integer primary keys (1, 2, 3, 4, 5...)
   # Timestamp fields (created_at, updated_at)
   # Proper associations and foreign keys

Creating Records
----------------

### Basic Record Creation

.. code-block:: python

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

   # Create a task
   task = Task(
       title="Build authentication system",
       description="Implement user login and registration",
       owner="backend-team",
       severity="medium"
   )
   session.add(task)
   session.commit()

   print(f"Created task with ID: {task.id}")  # Integer: 1, 2, 3...

### Create with Labels

.. code-block:: python

   # Create labels
   backend_label = Label(name="backend")
   auth_label = Label(name="authentication")
   session.add_all([backend_label, auth_label])
   session.commit()

   # Create task with labels
   auth_task = Task(
       title="Implement OAuth2",
       description="Add OAuth2 authentication",
       owner="backend-team",
       severity="high"
   )
   session.add(auth_task)
   session.commit()

   # Associate labels (SQLAlchemy ORM pattern)
   auth_task.labels.append(backend_label)
   auth_task.labels.append(auth_label)
   session.commit()

Querying Records
----------------

### Basic Queries

.. code-block:: python

   # Get all goals (SQLAlchemy ORM pattern)
   all_goals = session.query(Goal).all()

   # Find by primary key (SQLAlchemy ORM pattern)
   goal = session.query(Goal).filter(Goal.id == 1).first()

   # Find by attributes (SQLAlchemy ORM pattern)
   task = session.query(Task).filter(Task.title == "Build authentication").first()
   backend_tasks = session.query(Task).filter(Task.owner == "backend-team").all()

### Filtered Queries

.. code-block:: python

   # Filter with where clauses (SQLAlchemy ORM pattern)
   high_priority = session.query(Goal).filter(Goal.severity == "high").all()
   in_progress = session.query(Task).filter(Task.status == "in_progress").all()

   # Multiple conditions
   backend_high_priority = session.query(Task).filter(
       Task.owner == "backend-team",
       Task.severity == "high"
   ).all()

   # Complex queries
   critical_in_progress = session.query(Task).filter(
       Task.severity == "critical",
       Task.status == "in_progress"
   ).all()

### Ordering and Limiting

.. code-block:: python

   # Order by creation date
   recent_goals = session.query(Goal).order_by(Goal.created_at.desc()).all()

   # Limit results
   top_5_tasks = session.query(Task).order_by(Task.severity).limit(5).all()

Updating Records
----------------

### Simple Updates

.. code-block:: python

   # Find existing record
   task = session.query(Task).filter(Task.id == 1).first()

   # Update attributes
   task.title = "Updated Task Title"
   task.progress = 75
   task.status = "in_progress"

   # Save changes
   session.commit()

### Batch Updates

.. code-block:: python

   # Update multiple records
   session.query(Task).filter(Task.owner == "backend-team").update(
       {"status": "in_progress"},
       synchronize_session=False
   )
   session.commit()

Deleting Records
----------------

### Single Record Deletion

.. code-block:: python

   # Find and delete
   task = session.query(Task).filter(Task.id == 1).first()
   if task:
       session.delete(task)
       session.commit()

### Batch Deletion

.. code-block:: python

   # Delete multiple records
   session.query(Task).filter(Task.status == "completed").delete(
       synchronize_session=False
   )
   session.commit()

Associations and Relationships
-------------------------------

### Many-to-Many Relationships

.. code-block:: python

   # Create labels
   database_label = Label(name="database")
   api_label = Label(name="api")
   session.add_all([database_label, api_label])
   session.commit()

   # Create task
   api_task = Task(
       title="Build REST API",
       description="Create RESTful endpoints",
       owner="backend-team"
   )
   session.add(api_task)
   session.commit()

   # Associate labels (SQLAlchemy ORM pattern)
   api_task.labels.append(database_label)
   api_task.labels.append(api_label)
   session.commit()

   # Access associated labels
   print(f"Task labels: {[label.name for label in api_task.labels]}")

   # Access tasks with specific label
   api_tasks = session.query(Task).join(Task.labels).filter(Label.name == "api").all()
   print(f"API tasks: {[task.title for task in api_tasks]}")

### Hierarchical Relationships

.. code-block:: python

   # Create goal
   project_goal = Goal(
       title="Launch Project",
       description="Complete the project launch",
       owner="project-manager"
   )
   session.add(project_goal)
   session.commit()

   # Create phase
   dev_phase = Phase(
       title="Development",
       description="Build the application",
       owner="tech-lead"
   )
   session.add(dev_phase)
   session.commit()

   # Associate phase with goal
   project_goal.phases.append(dev_phase)
   session.commit()

   # Create task under phase
   backend_task = Task(
       title="Build backend",
       description="Implement server-side logic",
       owner="backend-team"
   )
   session.add(backend_task)
   session.commit()

   # Associate task with phase
   dev_phase.tasks.append(backend_task)
   session.commit()

Business Logic Methods
-----------------------

### Status Management

.. code-block:: python

   # Find task
   task = session.query(Task).filter(Task.id == 1).first()

   # Start work
   task.status = "in_progress"
   task.started_date = datetime.now().isoformat()
   session.commit()

   # Update progress
   task.progress = 50
   session.commit()

   # Complete work
   task.status = "completed"
   task.progress = 100
   task.completion_date = datetime.now().isoformat()
   session.commit()

   # Block work
   task.status = "blocked"
   session.commit()

### Progress Tracking

.. code-block:: python

   # Get progress statistics
   total_tasks = session.query(Task).count()
   completed_tasks = session.query(Task).filter(Task.status == "completed").count()
   in_progress_tasks = session.query(Task).filter(Task.status == "in_progress").count()

   completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

   print(f"Total tasks: {total_tasks}")
   print(f"Completed: {completed_tasks} ({completion_rate:.1f}%)")
   print(f"In Progress: {in_progress_tasks}")

Advanced Patterns
-----------------

### Complex Queries

.. code-block:: python

   # Tasks with specific labels
   labeled_tasks = session.query(Task).join(Task.labels).filter(
       Label.name.in_(["backend", "api"])
   ).distinct().all()

   # Goals with progress
   goals_with_progress = session.query(Goal).filter(
       Goal.progress > 0
   ).all()

   # High priority uncompleted tasks
   urgent_tasks = session.query(Task).filter(
       Task.severity.in_(["high", "critical"]),
       Task.status != "completed"
   ).order_by(Task.severity.desc()).all()

### Aggregation and Analytics

.. code-block:: python

   from sqlalchemy import func, and_

   # Task count by owner
   task_counts = session.query(
       Task.owner,
       func.count(Task.id).label('task_count')
   ).group_by(Task.owner).all()

   # Progress by severity
   progress_by_severity = session.query(
       Task.severity,
       func.avg(Task.progress).label('avg_progress')
   ).group_by(Task.severity).all()

   # Goals with most tasks
   goals_with_task_counts = session.query(
       Goal,
       func.count(Task.id).label('task_count')
   ).join(Goal.tasks).group_by(Goal.id).order_by(
       func.count(Task.id).desc()
   ).all()

### Transaction Management

.. code-block:: python

   from sqlalchemy.orm import sessionmaker

   # Create session with transaction support
   Session = sessionmaker(bind=engine)
   session = Session()

   try:
       # Create multiple related records
       goal = Goal(title="Complex Project", owner="team")
       session.add(goal)
       session.flush()  # Get the ID without committing

       phase = Phase(title="Planning", owner="team")
       session.add(phase)
       session.flush()

       # Associate
       goal.phases.append(phase)
       session.commit()

   except Exception as e:
       # Rollback on error
       session.rollback()
       print(f"Transaction failed: {e}")
   finally:
       session.close()

Error Handling
--------------

### Handling Missing Records

.. code-block:: python

   # Find operations return None (SQLAlchemy ORM pattern)
   task = session.query(Task).filter(Task.id == 99999).first()
   if task is None:
       print("Task not found")

   # Safe operations
   def get_task_safely(task_id):
       task = session.query(Task).filter(Task.id == task_id).first()
       if task:
           return task
       else:
           print(f"Task {task_id} not found")
           return None

### Database Errors

.. code-block:: python

   from sqlalchemy.exc import IntegrityError, OperationalError

   try:
       # Try to create duplicate label (should fail)
       duplicate_label = Label(name="existing_label")
       session.add(duplicate_label)
       session.commit()
   except IntegrityError as e:
       session.rollback()
       print(f"Integrity error (duplicate): {e}")
   except OperationalError as e:
       session.rollback()
       print(f"Database operation error: {e}")

Complete Example
----------------

Here's a complete workflow using the actual SQLAlchemy ORM API:

.. code-block:: python

   from todowrite import (
       Goal, Phase, Task, Label, create_engine, sessionmaker
   )
   from datetime import datetime

   # Initialize database session
   engine = create_engine("sqlite:///development_todowrite.db")
   Session = sessionmaker(bind=engine)
   session = Session()

   # Create a project goal
   project_goal = Goal(
       title="Launch User Dashboard",
       description="Successfully launch the new user dashboard with analytics",
       owner="product-team",
       severity="high"
   )
   session.add(project_goal)
   session.commit()

   # Create labels
   ui_label = Label(name="ui")
   backend_label = Label(name="backend")
   analytics_label = Label(name="analytics")
   session.add_all([ui_label, backend_label, analytics_label])
   session.commit()

   # Create development phases
   design_phase = Phase(
       title="Design Phase",
       description="Create wireframes, mockups, and user flows",
       owner="design-team",
       severity="medium"
   )
   session.add(design_phase)
   session.commit()

   dev_phase = Phase(
       title="Development Phase",
       description="Implement frontend and backend components",
       owner="tech-lead",
       severity="high"
   )
   session.add(dev_phase)
   session.commit()

   # Associate phases with goal
   project_goal.phases.extend([design_phase, dev_phase])
   session.commit()

   # Create tasks for development phase
   ui_task = Task(
       title="Build responsive UI components",
       description="Create React components for dashboard layout",
       owner="frontend-team",
       severity="high"
   )
   session.add(ui_task)
   ui_task.labels.extend([ui_label])
   session.commit()

   api_task = Task(
       title="Implement REST API endpoints",
       description="Create backend API for dashboard data",
       owner="backend-team",
       severity="high"
   )
   session.add(api_task)
   api_task.labels.extend([backend_label])
   session.commit()

   analytics_task = Task(
       title="Integrate analytics tracking",
       description="Add user behavior analytics to dashboard",
       owner="data-team",
       severity="medium"
   )
   session.add(analytics_task)
   analytics_task.labels.extend([analytics_label])
   session.commit()

   # Associate tasks with development phase
   dev_phase.tasks.extend([ui_task, api_task, analytics_task])
   session.commit()

   # Start work on tasks
   ui_task.status = "in_progress"
   ui_task.started_date = datetime.now().isoformat()
   ui_task.progress = 25
   session.commit()

   api_task.status = "in_progress"
   api_task.started_date = datetime.now().isoformat()
   api_task.progress = 60
   session.commit()

   # Complete analytics task
   analytics_task.status = "completed"
   analytics_task.progress = 100
   analytics_task.completion_date = datetime.now().isoformat()
   session.commit()

   # Query progress
   all_tasks = dev_phase.tasks
   completed_tasks = [t for t in all_tasks if t.status == "completed"]
   in_progress_tasks = [t for t in all_tasks if t.status == "in_progress"]

   # Display results
   print(f"🎯 Goal: {project_goal.title}")
   print(f"📊 Development Phase: {dev_phase.title}")
   print(f"📝 Total tasks: {len(all_tasks)}")
   print(f"✅ Completed: {len(completed_tasks)}")
   print(f"🔄 In Progress: {len(in_progress_tasks)}")
   print(f"📈 Overall Progress: {sum(t.progress for t in all_tasks) / len(all_tasks):.1f}%")

   # Tasks by label
   print("\n🏷️  Tasks by Label:")
   for label in [ui_label, backend_label, analytics_label]:
       label_tasks = session.query(Task).join(Task.labels).filter(Label.id == label.id).all()
       print(f"   {label.name}: {len(label_tasks)} tasks")

API Migration from Old System
----------------------------

**⚠️  IMPORTANT**: The old Node-based API has been **COMPLETELY REMOVED**. You must migrate to the Rails ActiveRecord API.

**Old API (REMOVED):**

.. code-block:: python

   # ❌ THIS NO LONGER EXISTS
   from todowrite import Node, create_node
   node = create_node(database, node_data)
   Node.where(status="in_progress")

**Actual SQLAlchemy ORM API:**

.. code-block:: python

   # ✅ USE THIS INSTEAD
   from todowrite import Task, create_engine, sessionmaker

   engine = create_engine("sqlite:///development_todowrite.db")
   Session = sessionmaker(bind=engine)
   session = Session()

   task = Task(title="My Task", owner="team")
   session.add(task)
   session.commit()

   in_progress_tasks = session.query(Task).filter(Task.status == "in_progress").all()

The SQLAlchemy ORM API provides:

* **🔒 Type Safety** - SQLAlchemy ORM models with comprehensive type hints
* **🔗 True Relationships** - Proper foreign keys and SQLAlchemy associations
* **⚡ Better Performance** - Optimized database queries with SQLAlchemy engine
* **📊 Rich Analytics** - Powerful aggregation and reporting with SQLAlchemy functions
* **🛡️ Data Integrity** - Enforced constraints and validation through SQLAlchemy
* **🎯 Standard ORM Patterns** - Familiar SQLAlchemy patterns for database operations

For complete schema documentation, see :doc:`ToDoWrite_Models_Data_Schema`.
