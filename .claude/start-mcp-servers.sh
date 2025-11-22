#!/bin/bash
# MCP Docker Servers Startup Script
# Starts all configured MCP Docker services

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="${SCRIPT_DIR}/mcp-docker-compose.yml"
PROJECT_NAME="todowrite-mcp"

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker is not running. Please start Docker daemon first."
        exit 1
    fi
    log_success "Docker daemon is running"
}

# Check if docker-compose file exists
check_compose_file() {
    if [[ ! -f "$COMPOSE_FILE" ]]; then
        log_error "Docker compose file not found: $COMPOSE_FILE"
        exit 1
    fi
    log_success "Found MCP docker-compose configuration"
}

# Load environment variables
load_env_vars() {
    local env_file="${SCRIPT_DIR}/.env"
    if [[ -f "$env_file" ]]; then
        log_info "Loading environment variables from $env_file"
        # shellcheck source=/dev/null
        source "$env_file"
    else
        log_warning "No .env file found at $env_file. Using environment variables from shell."
    fi
}

# Pull latest images
pull_images() {
    log_info "Pulling latest MCP Docker images..."

    # List of images to pull
    local images=(
        "mcp/context7:latest"
        "mcp/filesystem:latest"
        "mcp/git:latest"
        "ghcr.io/github/github-mcp-server:latest"
        "mcp/playwright:latest"
        "mcp/sqlite:latest"
        "mcp/rust-mcp-filesystem:latest"
        "mcp/mcp-python-refactoring:latest"
    )

    for image in "${images[@]}"; do
        log_info "Pulling $image..."
        if docker pull "$image"; then
            log_success "Pulled $image"
        else
            log_warning "Failed to pull $image (may not exist locally)"
        fi
    done
}

# Start MCP services
start_services() {
    log_info "Starting MCP Docker services..."

    cd "$SCRIPT_DIR"

    # Start services in detached mode
    if docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" up -d; then
        log_success "MCP services started successfully"
    else
        log_error "Failed to start MCP services"
        exit 1
    fi
}

# Wait for services to start
wait_for_startup() {
    log_info "Waiting for MCP services to start..."

    local services=(
        "context7"
        "filesystem"
        "git-server"
        "github-server"
        "playwright"
        "sqlite-server"
        "rust-filesystem"
        "python-refactoring"
    )

    local max_wait=60  # 1 minute max wait
    local wait_interval=5

    for service_name in "${services[@]}"; do
        local wait_time=0
        local container_name="mcp-$service_name"

        log_info "Waiting for $service_name..."

        while [[ $wait_time -lt $max_wait ]]; do
            if docker ps --filter "name=$container_name" --filter "status=running" --quiet | grep -q .; then
                log_success "$service_name is running"
                break
            fi

            if [[ $wait_time -eq 0 ]]; then
                log_info "$service_name starting up..."
            fi

            sleep "$wait_interval"
            wait_time=$((wait_time + wait_interval))
        done

        if [[ $wait_time -ge $max_wait ]]; then
            log_warning "$service_name did not start within ${max_wait}s"
        fi
    done
}

# Show status
show_status() {
    log_info "MCP Services Status:"
    echo ""

    cd "$SCRIPT_DIR"
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" ps

    echo ""
    log_info "MCP Service Endpoints:"
    echo "  Context7:        http://localhost:3001"
    echo "  Filesystem:      http://localhost:3002"
    echo "  Git Server:      http://localhost:3003"
    echo "  GitHub Server:   http://localhost:3004"
    echo "  Playwright:      http://localhost:3005"
    echo "  SQLite:          http://localhost:3006"
    echo "  Rust Filesystem: http://localhost:3007"
    echo "  Python Refactor: http://localhost:3008"
    echo ""

    log_info "MCP Network: mcp-network (172.20.0.0/16)"
}

# Main execution
main() {
    echo "🚀 Starting MCP Docker Servers"
    echo "================================"

    check_docker
    check_compose_file
    load_env_vars
    pull_images
    start_services
    wait_for_startup
    show_status

    log_success "MCP Docker servers are now running!"
    echo ""
    echo "💡 To stop all MCP services, run: ./stop-mcp-servers.sh"
    echo "💡 To view logs, run: docker-compose -f mcp-docker-compose.yml -p todowrite-mcp logs -f [service-name]"
    echo "💡 To restart a specific service: docker restart mcp-[service-name]"
}

# Handle script interruption
trap 'log_warning "Script interrupted. MCP services may be in an inconsistent state."' INT TERM

# Run main function
main "$@"
