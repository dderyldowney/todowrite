#!/bin/bash
# MCP System Verification Script
# MANDATE: ALWAYS VERIFY BEFORE ACTING

echo "🔍 MCP System Verification"
echo "=========================="

# Check PostgreSQL container
echo "📊 Checking PostgreSQL container..."
if docker ps --filter "name=mcp-postgres" --format "{{.Names}}" | grep -q "mcp-postgres"; then
    echo "✅ mcp-postgres: Running"

    # Check database connectivity and data integrity
    if docker exec mcp-postgres psql -U mcp_user -d todowrite -c "SELECT 1;" >/dev/null 2>&1; then
        echo "✅ Database: Connected"

        # Check data integrity
        goals_count=$(docker exec mcp-postgres psql -U mcp_user -d todowrite -tA -c "SELECT COUNT(*) FROM goals;")
        tables_count=$(docker exec mcp-postgres psql -U mcp_user -d todowrite -tA -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';")

        echo "📈 Data Integrity:"
        echo "   - Goals: $goals_count"
        echo "   - Tables: $tables_count"

        if [ "$goals_count" -gt 0 ] && [ "$tables_count" -eq 42 ]; then
            echo "✅ Data: Intact (42 tables, goals present)"
        else
            echo "⚠️  Data: Possible corruption - investigate immediately"
        fi
    else
        echo "❌ Database: Not connected"
    fi
else
    echo "❌ mcp-postgres: Not running - START WITH: docker start mcp-postgres"
fi

# Check MCP Gateway configuration
echo ""
echo "🔌 Checking MCP Gateway configuration..."
if [ -f ~/.docker/mcp/registry.yaml ]; then
    echo "✅ Registry file: Exists"
    if grep -q "context7:" ~/.docker/mcp/registry.yaml; then
        echo "✅ Registry: Contains context7"
    else
        echo "⚠️  Registry: Missing context7 entry"
    fi
else
    echo "❌ Registry file: Missing - RUN MCP GATEWAY SETUP"
fi

# Check required tools
echo ""
echo "🛠️  Checking required tools..."
if command -v socat >/dev/null 2>&1; then
    echo "✅ socat: Available"
else
    echo "❌ socat: Missing - INSTALL WITH: brew install socat"
fi

if command -v docker >/dev/null 2>&1; then
    echo "✅ docker: Available"
else
    echo "❌ docker: Missing - INSTALL DOCKER"
fi

if command -v docker-mcp >/dev/null 2>&1; then
    echo "✅ docker-mcp: Available"
else
    echo "❌ docker-mcp: Missing - INSTALL DOCKER MCP TOOLKIT"
fi

echo ""
echo "🎯 Summary: System verification complete"
echo "MANDATE: ALWAYS verify before taking action to prevent data loss"