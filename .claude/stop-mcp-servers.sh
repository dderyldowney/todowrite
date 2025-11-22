#!/bin/bash
# MCP Docker Servers Stop Script
# Stops all configured MCP Docker services

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

# Check if docker-compose file exists
check_compose_file() {
    if [[ ! -f "$COMPOSE_FILE" ]]; then
        log_error "Docker compose file not found: $COMPOSE_FILE"
        exit 1
    fi
}

# Stop MCP services
stop_services() {
    log_info "Stopping MCP Docker services..."

    cd "$SCRIPT_DIR"

    # Stop and remove containers
    if docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" down --remove-orphans; then
        log_success "MCP services stopped successfully"
    else
        log_warning "Some MCP services may not have been running"
    fi

    # Remove stopped containers to clean up
    log_info "Removing stopped MCP containers..."
    docker container prune -f --filter "label=com.docker.compose.project=$PROJECT_NAME" >/dev/null 2>&1 || true
}

# Clean up unused resources (optional)
cleanup_resources() {
    if [[ "${1:-}" == "--cleanup" ]]; then
        log_info "Cleaning up unused Docker resources..."

        # Remove unused volumes (be careful - this removes data)
        log_warning "This will remove all unused Docker volumes. Data will be lost!"
        read -p "Continue with volume cleanup? [y/N] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker volume prune -f
            log_success "Unused volumes removed"
        fi

        # Remove unused networks
        docker network prune -f
        log_success "Unused networks removed"
    fi
}

# Show final status
show_final_status() {
    log_info "Checking for any remaining MCP containers..."

    local remaining_containers
    remaining_containers=$(docker ps -a --filter "name=mcp-" --format "{{.Names}}" 2>/dev/null || true)

    if [[ -n "$remaining_containers" ]]; then
        log_warning "Found remaining MCP containers:"
        echo "$remaining_containers"
        echo ""
        log_info "To force remove them: docker rm -f \$(docker ps -a --filter 'name=mcp-' -q)"
    else
        log_success "All MCP containers have been stopped and removed"
    fi
}

# Main execution
main() {
    echo "🛑 Stopping MCP Docker Servers"
    echo "=============================="

    check_compose_file
    stop_services
    cleanup_resources "$@"
    show_final_status

    log_success "MCP Docker servers have been stopped!"
    echo ""
    echo "💡 To restart MCP services, run: ./start-mcp-servers.sh"
    echo "💡 To start with cleanup: ./stop-mcp-servers.sh --cleanup"
}

# Handle script interruption
trap 'log_warning "Script interrupted."' INT TERM

# Run main function
main "$@"