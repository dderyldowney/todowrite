todowrite.core.exceptions module
=================================

.. automodule:: todowrite.core.exceptions
   :members:
   :show-inheritance:
   :undoc-members:

Exception Hierarchy
-------------------

Below is the complete exception hierarchy for the ToDoWrite library:

**Base Exception**
    - **ToDoWriteError**: Base exception class for all ToDoWrite errors

**Node-related Exceptions**
    - **NodeError**: Base exception for node-related errors
        - **NodeNotFoundError**: Raised when a node is not found
        - **InvalidNodeError**: Raised when node data is invalid

**Storage-related Exceptions**
    - **StorageError**: Base exception for storage-related errors
        - **DatabaseError**: Raised for database-related errors
        - **YAMLError**: Raised for YAML-related errors

**Other Exceptions**
    - **SchemaError**: Raised for schema validation errors
    - **ConfigurationError**: Raised for configuration-related errors
    - **CLIError**: Raised for CLI-related errors
    - **TokenOptimizationError**: Raised for token optimization errors

Usage Examples
--------------

Here are recommended ways to import and use exceptions:

**Option 1: Import from main todowrite module (Recommended)**

.. code-block:: python

    from todowrite import DatabaseError, NodeNotFoundError

    try:
        # Your code here
        pass
    except DatabaseError as e:
        print(f"Database error: {e}")

**Option 2: Import from todowrite.core.exceptions module**

.. code-block:: python

    from todowrite.core.exceptions import DatabaseError, NodeNotFoundError

    try:
        # Your code here
        pass
    except DatabaseError as e:
        print(f"Database error: {e}")

**Option 3: Import all exceptions for comprehensive error handling**

.. code-block:: python

    from todowrite.core.exceptions import (
        ToDoWriteError,
        NodeError,
        StorageError,
        DatabaseError,
        YAMLError,
        NodeNotFoundError,
        InvalidNodeError,
        SchemaError,
        ConfigurationError,
        CLIError,
        TokenOptimizationError
    )

    def handle_errors():
        try:
            # Your code here
            pass
        except NodeNotFoundError as e:
            print(f"Node not found: {e.node_id}")
        except DatabaseError as e:
            print(f"Database error: {e}")
            if e.original_exception:
                print(f"Original error: {e.original_exception}")
        except ToDoWriteError as e:
            print(f"General ToDoWrite error: {e}")
