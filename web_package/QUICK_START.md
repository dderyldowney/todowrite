# ToDoWrite Web App Quick Start Guide

## Overview

The ToDoWrite Web App provides a modern web interface for hierarchical task management with:

- **Backend**: FastAPI with PostgreSQL database
- **Frontend**: React + TypeScript + Vite with Tailwind CSS
- **Features**: Drag-and-drop task management, real-time updates, responsive design

## Prerequisites

### System Requirements

- **Python**: 3.12+ (required)
- **Node.js**: 18+ (required)
- **PostgreSQL**: Running database server (required)
- **Git**: For version control

### Database Setup

The web app requires a PostgreSQL database. Ensure you have:

1. PostgreSQL server running
2. Database created with proper tables/migrations
3. `TODOWRITE_DATABASE_URL` environment variable set

Example database URL:
```bash
export TODOWRITE_DATABASE_URL="postgresql://username:password@localhost:5432/todowrite"
```

## Quick Start

### 1. Navigate to Web App Directory

```bash
cd web_package
```

### 2. Run the Setup & Start Script

```bash
chmod +x run_webapp.sh stop_webapp.sh
./run_webapp.sh
```

This script will:
- ✅ Check Python and Node.js versions
- ✅ Set up the environment
- ✅ Install backend and frontend dependencies
- ✅ Verify database connection
- ✅ Start both backend and frontend services
- ✅ Open the web app in your browser

### 3. Access the Web App

Once started, you can access:

- **🌐 Frontend Application**: http://localhost:3000
- **📊 Backend API**: http://127.0.0.1:8000
- **📖 API Documentation**: http://127.0.0.1:8000/docs

## Manual Setup (Alternative)

If you prefer to set up manually:

### Backend Setup

```bash
# Activate virtual environment
source ../.venv/bin/activate

# Set environment variables
export PYTHONPATH="../lib_package/src:../cli_package/src"
export TODOWRITE_DATABASE_URL="postgresql://..."

# Install dependencies
pip install -e .
pip install -e ..  # Ensure todowrite package is available

# Start backend
python -m uvicorn todowrite_web.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
cd ..
```

## Web App Features

### 📋 Dashboard
- Overview of all tasks and goals
- Progress tracking
- Quick actions

### 🎯 Goals Management
- Create, edit, and delete goals
- Hierarchical goal structure
- Progress tracking

### ✅ Tasks Management
- Create and manage tasks
- Assign to goals
- Status tracking
- Priority management

### 📅 Calendar View
- Timeline view of tasks and goals
- Deadline management
- Milestone tracking

### 🎨 Modern UI
- Responsive design
- Dark/light theme support
- Drag-and-drop functionality
- Keyboard shortcuts

## API Endpoints

### Core Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/items` - List all items (with filtering)
- `GET /api/items/{id}` - Get specific item
- `POST /api/items` - Create new item
- `GET /api/stats` - Database statistics

### Filtering Examples

```bash
# Get all tasks
curl "http://127.0.0.1:8000/api/items?layer=task"

# Get items by owner
curl "http://127.0.0.1:8000/api/items?owner=yourname"

# Get items by status
curl "http://127.0.0.1:8000/api/items?status=in_progress"
```

## Development

### Running Tests

```bash
# Backend tests
pip install -e ".[dev]"
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting and formatting
ruff check .
ruff format .

# Frontend linting
cd frontend
npm run lint
```

### Building for Production

```bash
# Frontend build
cd frontend
npm run build
cd ..

# Backend deployment
# The FastAPI app can be deployed with gunicorn or similar
pip install gunicorn
gunicorn todowrite_web.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check PostgreSQL is running
   pg_ctl status

   # Check environment variable
   echo $TODOWRITE_DATABASE_URL
   ```

2. **Port Already in Use**
   ```bash
   # Find what's using the port
   lsof -ti :8000  # Backend
   lsof -ti :3000  # Frontend

   # Kill the process
   kill -9 <PID>
   ```

3. **Python Module Not Found**
   ```bash
   # Ensure virtual environment is active
   source ../.venv/bin/activate

   # Install todowrite package
   pip install -e ..
   ```

4. **Node.js Version Too Old**
   ```bash
   # Update Node.js (using nvm)
   nvm install 18
   nvm use 18
   ```

### Logs

- **Backend logs**: `backend.log`
- **Frontend logs**: `frontend.log`
- **Application logs**: Check browser console for frontend errors

### Getting Help

1. Check the logs for error messages
2. Verify all prerequisites are met
3. Ensure PostgreSQL is running and accessible
4. Check that ports 3000 and 8000 are available

## Scripts Reference

### `run_webapp.sh`

```bash
./run_webapp.sh              # Full setup and start
./run_webapp.sh --start-only # Start only (skip setup)
./run_webapp.sh --help       # Show help
```

### `stop_webapp.sh`

```bash
./stop_webapp.sh              # Stop services
./stop_webapp.sh --cleanup-logs # Stop and remove logs
./stop_webapp.sh --help      # Show help
```

## Architecture

### Backend Structure
```
src/todowrite_web/
├── main.py          # FastAPI application entry point
├── database.py      # Database configuration
└── api/
    └── hierarchy.py # Hierarchy management API
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/  # Reusable components
│   ├── pages/      # Page components
│   ├── App.tsx     # Main application
│   └── main.tsx    # Entry point
├── package.json    # Dependencies
└── vite.config.ts  # Vite configuration
```

## Contributing

1. Follow the existing code style
2. Add tests for new features
3. Update documentation
4. Use conventional commit messages
5. Ensure all quality checks pass before submitting

## License

This project follows the same license as the main ToDoWrite project.