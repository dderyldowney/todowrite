# Database Configuration

ToDoWrite is designed to be flexible with its database backend, supporting both SQLite for development and PostgreSQL for production environments. The database connection is primarily configured via the `db_url` parameter in the `ToDoWrite` class constructor or by setting the `TODOWRITE_DATABASE_URL` environment variable.

## Connection Priority

When initializing the `ToDoWrite` application, the database URL is determined in the following order of priority:

1.  **Explicit `db_url` parameter**: If a `db_url` is passed directly to the `ToDoWrite()` constructor, it will be used.
2.  **`TODOWRITE_DATABASE_URL` environment variable**: If no `db_url` is provided to the constructor, the system checks for the `TODOWRITE_DATABASE_URL` environment variable.
3.  **Default SQLite**: If neither of the above is provided, ToDoWrite defaults to using a SQLite database named `todowrite.db` in the current working directory.

## SQLite (Default)

SQLite is an excellent choice for local development, testing, and single-user applications due to its file-based nature and zero-configuration setup.

### Usage

To use SQLite, you typically don't need any explicit configuration. Simply initialize the `ToDoWrite` application without arguments:

```python
from todowrite.app import ToDoWrite

# Uses default SQLite database (e.g., todowrite.db in the current directory)
app = ToDoWrite()

# The database file will be created automatically upon init_database() call
app.init_database()
```

You can also specify a custom path for your SQLite database file:

```python
from todowrite.app import ToDoWrite

# Specify a custom SQLite database file path
app = ToDoWrite("sqlite:///path/to/my_custom_database.db")
app.init_database()
```

## PostgreSQL

PostgreSQL is a powerful, open-source relational database system highly recommended for production deployments due to its robustness, scalability, and advanced features.

### Configuration

To connect ToDoWrite to a PostgreSQL database, you need to provide a PostgreSQL connection string.

#### Using Environment Variable (Recommended for Deployment)

Setting the `TODOWRITE_DATABASE_URL` environment variable is the most common and recommended way to configure PostgreSQL for deployment. This keeps sensitive database credentials out of your codebase.

```bash
export TODOWRITE_DATABASE_URL="postgresql://user:password@host:port/database_name"
# Example:
export TODOWRITE_DATABASE_URL="postgresql://todowrite:todowrite@localhost:5432/todowrite_db"
```

Once the environment variable is set, initialize `ToDoWrite` without arguments:

```python
from todowrite.app import ToDoWrite

# ToDoWrite will automatically pick up the TODOWRITE_DATABASE_URL
app = ToDoWrite()
app.init_database()
```

#### Configuring Programmatically

You can also pass the PostgreSQL connection string directly to the `ToDoWrite` constructor:

```python
from todowrite.app import ToDoWrite

db_url = "postgresql://user:password@localhost:5432/my_todowrite_db"
app = ToDoWrite(db_url)
app.init_database()
```

### Connection String Format

A typical PostgreSQL connection string follows this format:

`postgresql://user:password@host:port/database_name`

*   `user`: Your PostgreSQL username.
*   `password`: Your PostgreSQL password.
*   `host`: The hostname or IP address of your PostgreSQL server (e.g., `localhost`, `db.example.com`).
*   `port`: The port your PostgreSQL server is listening on (default is `5432`).
*   `database_name`: The name of the database you want to connect to.
