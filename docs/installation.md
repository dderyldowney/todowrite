# Installation

This document provides detailed instructions on how to install ToDoWrite, both as a standalone application and for development purposes.

## As a Standalone Application

To install ToDoWrite as a standalone application, you can use `pip`:

```bash
pip install todowrite
```

This will install the `todowrite` package and make the `todowrite` command-line interface (CLI) available in your terminal.

## For Development

If you plan to contribute to ToDoWrite or want to work with the source code, follow these steps to set up your development environment:

1.  **Clone the Repository**:
    First, clone the ToDoWrite GitHub repository to your local machine:

    ```bash
    git clone https://github.com/dderyldowney/todowrite.git
    cd todowrite
    ```

2.  **Install in Editable Mode**:
    Navigate into the cloned directory and install the package in "editable" mode. This allows you to make changes to the source code and have them immediately reflected without needing to reinstall the package.

    ```bash
    pip install -e .
    ```

3.  **Prerequisites**:
    Ensure you have the following prerequisites installed:

    *   **Python 3.12+**: ToDoWrite leverages modern Python features.
    *   **SQLAlchemy 2.0+**: The ORM used for database interactions.
    *   **Click 8.0+**: The library used for building the command-line interface.
    *   **Psycopg2 (for PostgreSQL support)**: The PostgreSQL adapter for Python.
    *   **Docker (for PostgreSQL integration tests)**: Required to run the automated PostgreSQL test suite.

    These dependencies will typically be installed automatically when you run `pip install -e .`, but it's good to be aware of them.
