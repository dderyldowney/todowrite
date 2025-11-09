# ToDoWrite Web Package

This package provides the web frontend for the ToDoWrite hierarchical task management system.

## Structure

- `backend/` - FastAPI backend application
- `frontend/` - React frontend application
- `shared/` - Shared types and utilities
- `docker-compose.yml` - Development environment setup
- `nginx.conf` - Production reverse proxy configuration

## Development

### Backend Development

```bash
cd backend
pip install -e .
python -m uvicorn todowrite_web.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Docker Development

```bash
docker-compose up --build
```

## Features

- **Dual-mode interface**: Simple mode for non-programmers, Advanced mode for power users
- **Template system**: Pre-built project templates for common scenarios
- **Visual relationship building**: Drag-and-drop interface for creating dependencies
- **Real-time search**: Full-text search across all project data
- **Import/Export**: YAML and JSON support with full metadata preservation

## Architecture

This follows the existing monorepo structure with `lib_package` and `cli_package`, adding `web_package` as the third package. The backend leverages existing SQLAlchemy models and validation schemas from the core library.
