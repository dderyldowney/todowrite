#!/bin/bash
# INTELLIGENT MCP SERVER STARTUP - Only starts missing servers
# This script prevents duplicate server instances

echo "🔧 **INTELLIGENT MCP SERVER STARTUP**"
echo "===================================="

# Function to check if a Docker container is running
check_docker_container() {
    local container_name="$1"
    if docker ps --format "table {{.Names}}" | grep -q "^${container_name}$"; then
        return 0  # Running
    else
        return 1  # Not running
    fi
}

# Function to check if a local process is running
check_local_process() {
    local process_pattern="$1"
    if pgrep -f "$process_pattern" > /dev/null; then
        return 0  # Running
    else
        return 1  # Not running
    fi
}

# Function to check if a launchd service is running
check_launchd_service() {
    local service_name="$1"
    local status_line=$(launchctl list | grep "com.user.mcp.${service_name}")

    if [ -z "$status_line" ]; then
        return 1  # Service not found
    fi

    local status=$(echo "$status_line" | awk '{print $1}')
    local pid=$(echo "$status_line" | awk '{print $2}')

    # Status "-" or "0" means not running, any positive number means running
    if [ "$status" = "-" ] || [ "$status" = "0" ] || [ "$status" = "-" ]; then
        return 1  # Not running
    else
        return 0  # Running (PID should be in $pid)
    fi
}

# Function to start launchd service
start_launchd_service() {
    local service_name="$1"

    if check_launchd_service "$service_name"; then
        echo "✅ $service_name (launchd): Already running"
    else
        echo "🚀 Starting $service_name (launchd)..."
        launchctl start "com.user.mcp.$service_name"
        sleep 2  # Give it time to start
        if check_launchd_service "$service_name"; then
            echo "✅ $service_name (launchd): Started successfully"
        else
            echo "❌ $service_name (launchd): Failed to start"
        fi
    fi
}

# Function to start Docker container if not running
start_docker_container() {
    local container_name="$1"
    local image_name="$2"

    if check_docker_container "$container_name"; then
        echo "✅ $container_name: Already running"
    else
        echo "🚀 Starting $container_name..."
        # Check if container exists but is stopped
        if docker ps -a --format "{{.Names}}" | grep -q "^${container_name}$"; then
            docker start "$container_name"
        else
            docker run -d --name "$container_name" --restart unless-stopped "$image_name"
        fi

        if check_docker_container "$container_name"; then
            echo "✅ $container_name: Started successfully"
        else
            echo "❌ $container_name: Failed to start"
        fi
    fi
}

# Function to start local MCP server if not running
start_local_mcp_server() {
    local server_name="$1"
    local server_path="$2"
    local start_command="$3"

    if check_local_process "$server_name"; then
        echo "✅ $server_name: Already running"
    else
        echo "🚀 Starting $server_name..."
        if [ -f "$server_path" ]; then
            cd "$(dirname "$server_path")"
            nohup $start_command > "/tmp/${server_name}.log" 2>&1 &
            sleep 2  # Give it time to start
            if check_local_process "$server_name"; then
                echo "✅ $server_name: Started successfully"
            else
                echo "❌ $server_name: Failed to start"
            fi
        else
            echo "❌ $server_name: Server file not found at $server_path"
        fi
    fi
}

echo "📋 Checking existing MCP servers..."

# === DOCKER CONTAINERS ===
echo ""
echo "🐳 Checking Docker containers..."

# PostgreSQL (always needed)
if check_docker_container "mcp-postgres"; then
    echo "✅ mcp-postgres: Already running"
else
    echo "🚀 Starting mcp-postgres..."
    # Check if container exists but is stopped
    if docker ps -a --format "{{.Names}}" | grep -q "^mcp-postgres$"; then
        docker start mcp-postgres
    else
        docker run -d --name mcp-postgres -e POSTGRES_USER=mcp_user -e POSTGRES_PASSWORD=mcp_secure_password_2024 -e POSTGRES_DB=todowrite -p 5433:5432 postgres:16-alpine
    fi

    if check_docker_container "mcp-postgres"; then
        echo "✅ mcp-postgres: Started successfully"
    else
        echo "❌ mcp-postgres: Failed to start"
    fi
fi

# Context7
start_docker_container "mcp-context7" "mcp/context7:latest"

# SQLite
start_docker_container "mcp-sqlite" "mcp/sqlite:latest"

# === LAUNCHD-MANAGED MCP SERVERS ===
echo ""
echo "🚀 Checking launchd-managed MCP servers..."

# Start only the services that are registered and not running
start_launchd_service "agentic-control-framework"
start_launchd_service "circleci-mcp-server"
start_launchd_service "kaggle-mcp"
start_launchd_service "chrome-devtools"
start_launchd_service "ailint"
start_launchd_service "agentmode"
start_launchd_service "cargo-mcp"
start_launchd_service "crates"
start_launchd_service "rust-docs"
start_launchd_service "ai-pair-programmer"

# === STANDALONE MCP SERVERS (not managed by launchd) ===
echo ""
echo "💻 Checking standalone MCP servers..."

# Note: Most MCP servers are now managed by launchd, so this section is minimal
# Add any standalone servers here that are not managed by launchd

# === DOCKER MCP GATEWAY ===
echo ""
echo "🌐 Checking Docker MCP Gateway..."

if check_local_process "docker mcp gateway"; then
    echo "✅ Docker MCP Gateway: Already running"
else
    echo "🚀 Starting Docker MCP Gateway..."
    nohup docker mcp gateway run --enable-all-servers --long-lived > /tmp/mcp_gateway.log 2>&1 &
    sleep 5  # Give it time to start
    if check_local_process "docker mcp gateway"; then
        echo "✅ Docker MCP Gateway: Started successfully"
    else
        echo "❌ Docker MCP Gateway: Failed to start"
    fi
fi

# === SUMMARY ===
echo ""
echo "📊 **SERVER STATUS SUMMARY**"
echo "============================"

docker_containers=$(docker ps --format "table {{.Names}}" | grep -c "mcp")
local_processes=$(ps aux | grep -E "(mcp|kaggle|agentmode|agentic-control|circleci|chrome-devtools|ailint)" | grep -v grep | wc -l)

echo "🐳 Docker containers running: $docker_containers"
echo "💻 Local processes running: $local_processes"

# Show running servers
echo ""
echo "📋 Currently running servers:"
echo "🐳 Docker containers:"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep "mcp" || echo "  (none)"

echo ""
echo "🚀 launchd-managed MCP services:"
launchctl list | grep "com.user.mcp" | awk '{print "  " $3 " (PID: " $1 ", Status: " $1 ")"}' || echo "  (none)"

echo ""
echo "💻 Other MCP processes:"
ps aux | grep -E "(docker.*mcp|gateway)" | grep -v grep | awk '{print "  " $11 " (PID: " $2 ")"}' || echo "  (none)"

echo ""
echo "✅ **INTELLIGENT MCP SERVER STARTUP COMPLETE**"
