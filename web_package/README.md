# ToDoWrite Web Application - (todowrite_web)

A modern web-based task management application that provides an online calendar-like interface for hierarchical task management.

## Architecture

### Backend (FastAPI)
- **FastAPI**: Modern Python web framework for high-performance APIs
- **PostgreSQL**: Production-grade database for persistent storage
- **SQLAlchemy**: Modern ORM with connection pooling and optimization
- **ToDoWrite Models API**: Integration with the modern ToDoWrite library

### Frontend (React)
- **React 18**: Modern React with hooks and functional components
- **TypeScript**: Type-safe development with full type coverage
- **Tailwind CSS**: Utility-first CSS framework for rapid UI development
- **Vite**: Fast development server and build tooling
- **React Query**: Powerful data fetching and state management

## Features

### Hierarchical Task Management
- **🎯 Modern Drag-and-Drop Interface**: Full 12-layer hierarchy reorganization
- **🔀 Cross-Layer Moves**: Drag Commands between SubTasks, Tasks between Steps, etc.
- **📊 Expandable/Collapsible View**: Clean nested interface like Notion/Jira
- **⚡ Real-time Validation**: Prevents invalid hierarchy moves
- **🎨 Visual Hierarchy**: Color-coded layers with intuitive icons
- **⌨️ Keyboard Shortcuts**: Power user features with command palette

### Drag-and-Drop Capabilities
- **Within Same Level**: Reorder Tasks within a Step, Steps within a Phase
- **Cross-Level Moves**: Promote/demote items between layers
- **Cross-Parent Moves**: Drag Commands between different SubTasks
- **Bulk Operations**: Multi-select and move multiple items
- **Smart Validation**: Ensures hierarchy rules are followed

### Dashboard
- Overview of all tasks and goals
- Status breakdown and statistics
- Recent activity feed
- Quick action buttons

### Task Management
- Comprehensive task listing with filtering
- Search functionality across all task attributes
- Status, owner, and priority filtering
- Progress tracking visualization

### Goal Tracking
- High-level goal visualization
- Progress indicators and milestones
- Goal categorization and status tracking
- Performance metrics

## Database Configuration

The web application **requires PostgreSQL** and connects to the same database as the CLI:

```bash
# Set the PostgreSQL environment variable
export TODOWRITE_DATABASE_URL="postgresql://todowrite:todowrite_dev_password@localhost:5432/todowrite"

# The FastAPI backend will automatically validate the connection
# and use optimized connection pooling settings
```

## Development Setup

### Prerequisites
- PostgreSQL database running
- Node.js 18+ for frontend
- Python 3.12+ for backend
- UV package manager

### Backend Setup
```bash
# Navigate to the web package
cd web_package

# Activate virtual environment
source $PWD/.venv/bin/activate

# Set up Python path
export PYTHONPATH="lib_package/src:cli_package/src"

# Install dependencies
uv sync --dev

# Start the FastAPI backend
uv run uvicorn src.todowrite_web.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd web_package/frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

## API Endpoints

### Items Management
- `GET /api/items` - List all items with optional filtering
- `GET /api/items/{id}` - Get specific item by ID
- `POST /api/items` - Create new item
- `GET /api/stats` - Get database statistics

### Health Checks
- `GET /` - API information
- `GET /health` - Health check endpoint

## Development Tools

### Backend
- **Ruff**: Fast Python linter and formatter
- **Bandit**: Security linter for Python
- **Pytest**: Testing framework with async support
- **Mypy**: Static type checking

### Frontend
- **ESLint**: JavaScript/TypeScript linting
- **TypeScript**: Static type checking
- **Vitest**: Fast unit testing framework
- **Tailwind CSS**: Utility-first styling

## Production Deployment

### Environment Variables
```bash
# Required: PostgreSQL connection
export TODOWRITE_DATABASE_URL="postgresql://user:password@localhost:5432/todowrite"

# Optional: FastAPI settings
export FASTAPI_ENV="production"
export LOG_LEVEL="info"
```

### Build Process
```bash
# Backend (no build needed - runs directly)
# Frontend
cd web_package/frontend
npm run build
```

## Integration with CLI

The web application shares the same PostgreSQL database as the CLI, ensuring:
- Real-time synchronization between web and CLI
- Consistent data models and relationships
- Seamless workflow between interfaces

## Security Considerations

- PostgreSQL connection requires proper authentication
- CORS configured for development (localhost:3000)
- Input validation on all API endpoints
- SQL injection protection via SQLAlchemy ORM
- Type safety via TypeScript and Pydantic models

## Performance Optimizations

### Backend
- Database connection pooling (10 base connections, 20 overflow)
- Efficient query patterns with modern SQLAlchemy
- Response caching for static data
- Optimized database indexes

### Frontend
- React Query for efficient data fetching
- Code splitting via dynamic imports
- Optimized bundle sizes with Vite
- Lazy loading for large datasets

## Tech Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| Database | PostgreSQL | Persistent data storage |
| Backend | FastAPI + SQLAlchemy | REST API with database integration |
| Frontend | React + TypeScript | Modern user interface |
| Styling | Tailwind CSS | Utility-first CSS framework |
| Build | Vite + UV | Fast development and build tools |
| Testing | Pytest + Vitest | Comprehensive test coverage |

## Contributing

Follow the same development standards as the main ToDoWrite project:
- Use the ToDoWrite Models API exclusively
- Maintain full type coverage
- Write tests with real implementations (no mocking)
- Follow conventional commit messages
- Ensure all linting and type checking passes
