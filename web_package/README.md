# ToDoWrite Web Application

**Package Type**: `webapp` | **Package Name**: `todowrite-web` | **Status**: 🚧 In Development

Modern FastAPI-based web application for the ToDoWrite hierarchical task management system.

## Overview

This package provides a FastAPI-based web backend and frontend infrastructure for ToDoWrite, offering:

- **Dual-mode interface**: Simple Mode for non-programmers, Advanced Mode for power users
- **Visual relationship building**: Drag-and-drop task relationship management
- **Template system**: Pre-built project templates with customization
- **Real-time collaboration**: Multi-user support with live updates
- **Comprehensive REST API**: Full CRUD operations for all 12 ToDoWrite layers

## 📦 Package Context

This is the **web application** package of the ToDoWrite monorepo:

```
todowrite/                          # Monorepo root
├── lib_package/                    # Core library (dependency)
├── cli_package/                   # CLI interface (separate)
├── web_package/                   # ✅ This package (Web Application)
│   ├── src/todowrite_web/         # Web application source code
│   ├── .claude/                   # Independent development environment
│   └── README.md                  # This documentation
└── docs/                          # Project documentation
```

### Package Relationships
- **Dependencies**: `lib_package` (todowrite)
- **Independent Versioning**: Separate version lifecycle
- **Semantic Scope**: Uses `web` scope for commits
- **Development Environment**: Independent Claude configuration

## 🏗️ Architecture

### Current Structure
```
web_package/
├── src/
│   └── todowrite_web/           # Main Python package
│       ├── __init__.py
│       ├── api/                # API route modules
│       │   └── backend/        # FastAPI backend
│       │       ├── main.py     # FastAPI application entry point
│       │       ├── models.py   # Pydantic models
│       │       └── v1/         # API v1 endpoints
│       └── [frontend code]      # Planned React frontend
├── .claude/                     # Independent development environment
├── tests/                       # Test suite
├── pyproject.toml               # Python package configuration
└── README.md                    # This file
```

### Technology Stack
- **Backend**: FastAPI with async support
- **Database**: SQLAlchemy 2.0+ (SQLite/PostgreSQL)
- **Frontend**: React (planned)
- **API**: RESTful with WebSocket support (planned)
- **Testing**: pytest with comprehensive coverage

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite/web_package

# Install in development mode using uv (recommended)
uv sync --dev

# Or install with database dependencies using uv
uv sync --dev --extra postgres  # For PostgreSQL

# Or install using pip
pip install -e ".[dev]"
pip install -e ".[dev,postgres]"  # For PostgreSQL
```

## Development

### Setup Development Environment

```bash
# Install development dependencies using uv (recommended)
uv sync --dev

# Or install using pip
pip install -e ".[dev]"

# Run tests using uv
uv run pytest

# Run with coverage using uv
uv run pytest --cov=src/todowrite_web --cov-report=html

# Code formatting and linting using uv
uv run ruff check .
uv run ruff format .

# Or using pip directly
pytest
pytest --cov=src/todowrite_web --cov-report=html
ruff check .
ruff format .
```

### Running the Development Server

```bash
# Start the FastAPI development server using uv (recommended)
uv run uvicorn todowrite_web.main:app --reload --host 0.0.0.0 --port 8000

# Or using python directly
python -m uvicorn todowrite_web.main:app --reload

# Or using the shortcut
uvicorn todowrite_web.main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- OpenAPI schema: http://localhost:8000/openapi.json

## API Documentation

The web package provides a comprehensive REST API for ToDoWrite operations:

### Core Endpoints

- `GET /` - Health check and service information
- `GET /health` - Detailed health status
- `GET /api/v1/` - API version information

### CRUD Operations

All 12 ToDoWrite layers are exposed via RESTful API endpoints:

- **Goals**: `/api/v1/goals/`
- **Concepts**: `/api/v1/concepts/`
- **Contexts**: `/api/v1/contexts/`
- **Constraints**: `/api/v1/constraints/`
- **Requirements**: `/api/v1/requirements/`
- **Acceptance Criteria**: `/api/v1/acceptance-criteria/`
- **Interface Contracts**: `/api/v1/interface-contracts/`
- **Phases**: `/api/v1/phases/`
- **Steps**: `/api/v1/steps/`
- **Tasks**: `/api/v1/tasks/`
- **Subtasks**: `/api/v1/subtasks/`
- **Commands**: `/api/v1/commands/`

### Specialized Endpoints

- **Templates**: `/api/v1/templates/`
- **Relationships**: `/api/v1/relationships/`
- **Search**: `/api/v1/search/`
- **Collaboration**: `/api/v1/collaboration/`

## Configuration

### Environment Variables

```bash
# Database Configuration
DATABASE_URL=sqlite:///./todowrite.db
# or for PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/todowrite

# Development Settings
DEBUG=false
LOG_LEVEL=INFO

# CORS Settings (for frontend)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Database Setup

The web package uses SQLAlchemy 2.0+ with async support. Configure your database URL in the environment or `.env` file:

```bash
# SQLite (default)
DATABASE_URL=sqlite+aiosqlite:///./todowrite.db

# PostgreSQL
DATABASE_URL=postgresql+asyncpg://user:password@localhost/todowrite

# MySQL
DATABASE_URL=mysql+aiomysql://user:password@localhost/todowrite
```

## Frontend Development

The React frontend is located in the `frontend/` directory and is managed separately:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:3000 and will automatically connect to the backend API.

## Testing

### Running Tests

```bash
# Run all tests using uv (recommended)
uv run pytest

# Run specific test file using uv
uv run pytest tests/test_main.py

# Run with coverage using uv
uv run pytest --cov=src/todowrite_web

# Run integration tests using uv
uv run pytest tests/integration/

# Run API tests using uv
uv run pytest tests/api/

# Or using pip directly
pytest
pytest tests/test_main.py
pytest --cov=src/todowrite_web
pytest tests/integration/
pytest tests/api/
```

### Test Structure

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── api/           # API endpoint tests
├── fixtures/      # Test data and fixtures
└── conftest.py    # Pytest configuration
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Ensure code quality (`ruff check . && ruff format .`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Related Projects

- **todowrite**: Core Python library for hierarchical task management
- **todowrite_cli**: Command-line interface for ToDoWrite
- **todowrite_web**: Web frontend and API (this package)
