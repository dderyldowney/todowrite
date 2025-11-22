#!/bin/bash

# ToDoWrite Web App Stop Script
# This script stops both the FastAPI backend and React frontend

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Function to stop service by PID file
stop_service() {
    local service_name=$1
    local pid_file=$2

    if [[ -f "$pid_file" ]]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            print_status "Stopping $service_name (PID: $pid)..."
            kill "$pid"

            # Wait for graceful shutdown
            local timeout=10
            while [[ $timeout -gt 0 ]] && kill -0 "$pid" 2>/dev/null; do
                sleep 1
                ((timeout--))
            done

            # Force kill if still running
            if kill -0 "$pid" 2>/dev/null; then
                print_warning "$service_name didn't stop gracefully, force killing..."
                kill -9 "$pid"
            fi

            print_success "$service_name stopped"
        else
            print_warning "$service_name PID $pid not running"
        fi
        rm -f "$pid_file"
    else
        print_warning "No PID file found for $service_name"
    fi
}

# Function to stop by port
stop_by_port() {
    local service_name=$1
    local port=$2

    print_status "Checking for $service_name processes on port $port..."

    # Find processes using the port
    local pids=$(lsof -ti ":$port" 2>/dev/null || true)

    if [[ -n "$pids" ]]; then
        for pid in $pids; do
            print_status "Stopping $service_name process (PID: $pid)..."
            kill "$pid" 2>/dev/null || true
        done

        # Wait and force kill if needed
        sleep 2
        pids=$(lsof -ti ":$port" 2>/dev/null || true)
        if [[ -n "$pids" ]]; then
            print_warning "Force killing remaining $service_name processes..."
            for pid in $pids; do
                kill -9 "$pid" 2>/dev/null || true
            done
        fi

        print_success "$service_name processes on port $port stopped"
    else
        print_status "No $service_name processes found on port $port"
    fi
}

# Function to cleanup log files
cleanup_logs() {
    if [[ "${1:-}" == "--cleanup-logs" ]]; then
        print_status "Cleaning up log files..."
        rm -f backend.log frontend.log
        print_success "Log files cleaned up"
    fi
}

# Function to show final status
show_status() {
    echo ""
    echo "✅ ToDoWrite Web App has been stopped"
    echo ""

    # Check if anything is still running on the ports
    local backend_running=$(lsof -ti ":8000" 2>/dev/null || true)
    local frontend_running=$(lsof -ti ":3000" 2>/dev/null || true)

    if [[ -n "$backend_running" ]]; then
        print_warning "Backend processes may still be running on port 8000"
    fi

    if [[ -n "$frontend_running" ]]; then
        print_warning "Frontend processes may still be running on port 3000"
    fi

    if [[ -z "$backend_running" && -z "$frontend_running" ]]; then
        print_success "All services stopped successfully"
    fi

    echo ""
}

# Main execution
main() {
    echo "🛑 ToDoWrite Web App Stop Script"
    echo "==============================="
    echo ""

    # Check if we're in the right directory
    if [[ ! -f "pyproject.toml" ]]; then
        print_error "Please run this script from the web_package directory"
        exit 1
    fi

    # Stop services by PID files first (graceful shutdown)
    stop_service "Backend" "backend.pid"
    stop_service "Frontend" "frontend.pid"

    # Force cleanup by port (backup method)
    stop_by_port "Backend" "8000"
    stop_by_port "Frontend" "3000"

    # Cleanup logs if requested
    cleanup_logs "$@"

    # Show final status
    show_status
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --cleanup-logs  Also remove log files"
        echo "  --help, -h      Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0               Stop services"
        echo "  $0 --cleanup-logs Stop services and remove logs"
        echo ""
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac
