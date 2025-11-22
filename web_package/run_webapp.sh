#!/bin/bash

# ToDoWrite Web App Setup and Run Script
# This script sets up and runs both the FastAPI backend and React frontend

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKEND_HOST="127.0.0.1"
BACKEND_PORT="8000"
FRONTEND_HOST="localhost"
FRONTEND_PORT="3000"
REQUIRED_PYTHON_MAJOR_VERSION="3"
REQUIRED_PYTHON_MINOR_VERSION="12"
REQUIRED_NODE_VERSION="18"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    print_status "Checking Python version..."

    if ! command_exists python3; then
        print_error "Python 3 is not installed"
        exit 1
    fi

    local python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    local major=$(echo $python_version | cut -d. -f1)
    local minor=$(echo $python_version | cut -d. -f2)

    # Compare major and minor version numbers
    if [[ "$major" != "$REQUIRED_PYTHON_MAJOR_VERSION" ]] || [[ "$minor" < "$REQUIRED_PYTHON_MINOR_VERSION" ]]; then
        print_error "Python $REQUIRED_PYTHON_MAJOR_VERSION.$REQUIRED_PYTHON_MINOR_VERSION+ is required, but found $python_version"
        exit 1
    fi

    print_success "Python $python_version found"
}

# Function to check Node.js version
check_node_version() {
    print_status "Checking Node.js version..."

    if ! command_exists node; then
        print_error "Node.js is not installed"
        exit 1
    fi

    local node_version=$(node -v | sed 's/v//')
    local major=$(echo $node_version | cut -d. -f1)

    if [[ "$major" -lt "$REQUIRED_NODE_VERSION" ]]; then
        print_error "Node.js $REQUIRED_NODE_VERSION+ is required, but found $node_version"
        exit 1
    fi

    print_success "Node.js $node_version found"
}

# Function to set up environment
setup_environment() {
    print_status "Setting up environment..."

    # Check if we're in the right directory
    if [[ ! -f "pyproject.toml" || ! -d "frontend" ]]; then
        print_error "Please run this script from the web_package directory"
        exit 1
    fi

    # Activate virtual environment if it exists
    if [[ -f "../.venv/bin/activate" ]]; then
        print_status "Activating virtual environment..."
        source ../.venv/bin/activate
        print_success "Virtual environment activated"
    else
        print_warning "No virtual environment found, using system Python"
    fi

    # Set PYTHONPATH to include lib_package and cli_package
    export PYTHONPATH="../lib_package/src:../cli_package/src:${PYTHONPATH:-}"

    # Check PostgreSQL database
    if [[ -z "${TODOWRITE_DATABASE_URL:-}" ]]; then
        print_warning "TODOWRITE_DATABASE_URL not set, loading PostgreSQL environment..."
        if [[ -f "../.claude/postgresql_env.sh" ]]; then
            source ../.claude/postgresql_env.sh
            print_success "PostgreSQL environment loaded"
        else
            print_error "PostgreSQL environment file not found"
            print_error "Please ensure PostgreSQL is running and TODOWRITE_DATABASE_URL is set"
            exit 1
        fi
    fi

    print_success "Environment setup complete"
}

# Function to install backend dependencies
install_backend_deps() {
    print_status "Installing backend dependencies..."

    # Install the web package in development mode
    pip install -e .

    # Ensure todowrite is available
    if ! python -c "import todowrite" 2>/dev/null; then
        print_warning "todowrite package not found, installing from parent directory..."
        pip install -e ..
    fi

    print_success "Backend dependencies installed"
}

# Function to install frontend dependencies
install_frontend_deps() {
    print_status "Installing frontend dependencies..."

    cd frontend
    npm install
    cd ..

    print_success "Frontend dependencies installed"
}

# Function to run database health check
check_database() {
    print_status "Checking database connection..."

    # Try to connect to the database
    if python -c "
import os
from sqlalchemy import create_engine, text

try:
    engine = create_engine(os.environ['TODOWRITE_DATABASE_URL'])
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('Database connection successful')
except Exception as e:
    print(f'Database connection failed: {e}')
    exit(1)
" 2>/dev/null; then
        print_success "Database connection verified"
    else
        print_error "Database connection failed"
        print_error "Please ensure PostgreSQL is running and accessible"
        exit 1
    fi
}

# Function to start backend
start_backend() {
    print_status "Starting FastAPI backend..."

    # Start backend in background
    PYTHONPATH="src:$PYTHONPATH" python -m uvicorn todowrite_web.main:app \
        --host "$BACKEND_HOST" \
        --port "$BACKEND_PORT" \
        --reload \
        > backend.log 2>&1 &

    BACKEND_PID=$!
    echo $BACKEND_PID > backend.pid

    print_success "Backend started on http://$BACKEND_HOST:$BACKEND_PORT"
    print_status "Backend PID: $BACKEND_PID"
    print_status "Backend logs: backend.log"
}

# Function to start frontend
start_frontend() {
    print_status "Starting React frontend..."

    cd frontend
    npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..

    echo $FRONTEND_PID > frontend.pid

    print_success "Frontend started on http://$FRONTEND_HOST:$FRONTEND_PORT"
    print_status "Frontend PID: $FRONTEND_PID"
    print_status "Frontend logs: frontend.log"
}

# Function to wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."

    # Wait for backend
    print_status "Waiting for backend health check..."
    timeout=30
    while [[ $timeout -gt 0 ]]; do
        if curl -s "http://$BACKEND_HOST:$BACKEND_PORT/health" >/dev/null 2>&1; then
            print_success "Backend is ready"
            break
        fi
        sleep 1
        ((timeout--))
    done

    if [[ $timeout -eq 0 ]]; then
        print_error "Backend failed to start within 30 seconds"
        print_error "Check backend.log for details"
        return 1
    fi

    # Wait for frontend
    print_status "Waiting for frontend to be ready..."
    timeout=30
    while [[ $timeout -gt 0 ]]; do
        if curl -s "http://$FRONTEND_HOST:$FRONTEND_PORT" >/dev/null 2>&1; then
            print_success "Frontend is ready"
            break
        fi
        sleep 1
        ((timeout--))
    done

    if [[ $timeout -eq 0 ]]; then
        print_warning "Frontend may still be starting (this is normal)"
    fi
}

# Function to show status
show_status() {
    echo ""
    echo "🎉 ToDoWrite Web App is running!"
    echo ""
    echo "📊 Backend API: http://$BACKEND_HOST:$BACKEND_PORT"
    echo "🌐 Frontend:    http://$FRONTEND_HOST:$FRONTEND_PORT"
    echo "📖 API Docs:    http://$BACKEND_HOST:$BACKEND_PORT/docs"
    echo ""
    echo "🔍 To view the web application, open: http://$FRONTEND_HOST:$FRONTEND_PORT"
    echo ""
    echo "📝 Logs:"
    echo "   Backend:  backend.log"
    echo "   Frontend: frontend.log"
    echo ""
    echo "🛑 To stop the application, run: ./stop_webapp.sh"
    echo ""
}

# Function to cleanup on exit
cleanup() {
    print_status "Cleaning up..."

    if [[ -f backend.pid ]]; then
        local backend_pid=$(cat backend.pid)
        if kill -0 $backend_pid 2>/dev/null; then
            print_status "Stopping backend (PID: $backend_pid)..."
            kill $backend_pid
        fi
        rm -f backend.pid
    fi

    if [[ -f frontend.pid ]]; then
        local frontend_pid=$(cat frontend.pid)
        if kill -0 $frontend_pid 2>/dev/null; then
            print_status "Stopping frontend (PID: $frontend_pid)..."
            kill $frontend_pid
        fi
        rm -f frontend.pid
    fi

    print_success "Cleanup complete"
    exit 0
}

# Trap signals for cleanup
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    echo "🚀 ToDoWrite Web App Setup & Run Script"
    echo "======================================"
    echo ""

    # Check if we should only start services (skip setup)
    if [[ "${1:-}" == "--start-only" ]]; then
        print_status "Starting services only (skipping setup)..."
        setup_environment
        start_backend
        start_frontend
        wait_for_services
        show_status

        # Keep script running and wait for signals
        print_status "Web app is running. Press Ctrl+C to stop."
        while true; do
            sleep 1
        done
    fi

    # Full setup and start
    check_python_version
    check_node_version
    setup_environment
    install_backend_deps
    install_frontend_deps
    check_database
    start_backend
    start_frontend
    wait_for_services
    show_status

    # Keep script running and wait for signals
    print_status "Web app is running. Press Ctrl+C to stop."
    while true; do
        sleep 1
    done
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --start-only    Skip setup and start services only"
        echo "  --help, -h      Show this help message"
        echo ""
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac