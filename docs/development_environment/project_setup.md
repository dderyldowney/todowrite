# Project Setup

This section guides you through setting up your development environment for the AFS FastAPI Agricultural Robotics Platform. Proper setup ensures you can effectively contribute to the project, run tests, and develop new features.

## 1. Cloning the Repository

First, you need to clone the project repository from GitHub. Ensure you have Git installed on your system.

```bash
git clone https://github.com/dderyldowney/afs_fastapi.git
cd afs_fastapi
```

## 2. Setting up a Virtual Environment

It is highly recommended to use a Python virtual environment to manage project dependencies. This isolates the project's dependencies from your system-wide Python installation, preventing conflicts.

### 2.1. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 2.2. Activate the Virtual Environment

*   **On macOS/Linux:**
    ```bash
    source .venv/bin/activate
    ```

*   **On Windows (Command Prompt):**
    ```bash
    .venv\Scripts\activate.bat
    ```

*   **On Windows (PowerShell):**
    ```bash
    .venv\Scripts\Activate.ps1
    ```

You will see `(.venv)` prefixed to your terminal prompt, indicating that the virtual environment is active.

## 3. Installing Dependencies

Once your virtual environment is active, install the project's dependencies using `pip`:

```bash
pip install -r requirements.txt
```

This command reads the `requirements.txt` file and installs all necessary Python packages.

## 4. Pre-commit Hooks Installation

The project uses pre-commit hooks to enforce code quality and consistency. These hooks run automatically before each commit.

To install the pre-commit hooks, ensure your virtual environment is active and run:

```bash
pre-commit install
```

This command sets up the hooks defined in `.pre-commit-config.yaml`.

## 5. Verifying Setup

After completing the above steps, you can verify your setup by running the project's tests and formatters:

```bash
pytest
./bin/formatall
```

If all tests pass and `formatall` reports no issues, your development environment is successfully set up.
