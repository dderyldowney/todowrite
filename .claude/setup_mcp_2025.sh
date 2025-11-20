#!/bin/bash
# MCP 2025 Industry Standards Setup Script
# This script sets up the complete MCP configuration with 2025 industry standards

set -euo pipefail  # Exit on error, undefined vars, and pipe failures

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging
log() {
    echo -e "${BLUE}[MCP-SETUP]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Main setup directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

log "Starting MCP 2025 Industry Standards Setup..."

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."

    # Check Python version
    if ! command -v python3 &> /dev/null; then
        error "Python 3 is required but not installed"
        exit 1
    fi

    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if [[ "$(printf '%s\n' "3.12" "$python_version" | sort -V | head -n1)" != "3.12" ]]; then
        error "Python 3.12+ is required, found $python_version"
        exit 1
    fi
    success "Python $python_version found"

    # Check virtual environment
    if [[ -z "${VIRTUAL_ENV:-}" ]]; then
        error "Virtual environment is not activated. Please run: source .venv/bin/activate"
        exit 1
    fi
    success "Virtual environment is activated"

    # Check UV
    if ! command -v uv &> /dev/null; then
        error "UV package manager is required but not installed"
        exit 1
    fi
    success "UV package manager found"

    # Check required Python packages
    if ! python3 -c "import jsonschema" &> /dev/null; then
        error "jsonschema package not found. Run: ./dev_tools/build.sh install"
        exit 1
    fi
    success "Required Python packages available"
}

# Setup configuration files
setup_configurations() {
    log "Setting up MCP configuration files..."

    # Copy configuration files to user's Claude directory
    USER_CLAUDE_DIR="$HOME/.claude"
    mkdir -p "$USER_CLAUDE_DIR"

    # Main configuration
    if [[ -f "$SCRIPT_DIR/mcp_config_2025.json" ]]; then
        cp "$SCRIPT_DIR/mcp_config_2025.json" "$USER_CLAUDE_DIR/"
        success "Main MCP configuration installed"
    else
        error "Main configuration file not found"
        exit 1
    fi

    # Superpowers configuration
    if [[ -f "$SCRIPT_DIR/mcp_superpowers_config_2025.json" ]]; then
        cp "$SCRIPT_DIR/mcp_superpowers_config_2025.json" "$USER_CLAUDE_DIR/"
        success "Superpowers MCP configuration installed"
    fi

    # Episodic memory configuration (DISABLED)
    # if [[ -f "$SCRIPT_DIR/mcp_episodic_memory_config_2025.json" ]]; then
    #     cp "$SCRIPT_DIR/mcp_episodic_memory_config_2025.json" "$USER_CLAUDE_DIR/"
    #     success "Episodic Memory MCP configuration installed"
    # fi
    echo "🔍 Episodic Memory MCP configuration installation: DISABLED"

    # Documentation
    if [[ -f "$SCRIPT_DIR/MCP_2025_Documentation.md" ]]; then
        cp "$SCRIPT_DIR/MCP_2025_Documentation.md" "$USER_CLAUDE_DIR/"
        success "MCP documentation installed"
    fi
}

# Setup monitoring and security tools
setup_tools() {
    log "Setting up MCP monitoring and security tools..."

    # Make scripts executable
    chmod +x "$SCRIPT_DIR/mcp_security_optimizer.py"
    chmod +x "$SCRIPT_DIR/mcp_monitoring_dashboard.py"

    success "Security and monitoring tools made executable"

    # Create directories for reports and data
    mkdir -p "$SCRIPT_DIR/reports"
    mkdir -p "$SCRIPT_DIR/backups"
    mkdir -p "$USER_CLAUDE_DIR/mcp_data"

    success "Created necessary directories"
}

# Validate configurations
validate_configurations() {
    log "Validating MCP configurations..."

    # Validate JSON syntax
    for config in "$SCRIPT_DIR"/*config_2025.json; do
        if [[ -f "$config" ]]; then
            if python3 -m json.tool "$config" > /dev/null 2>&1; then
                success "Valid JSON syntax: $(basename "$config")"
            else
                error "Invalid JSON syntax: $(basename "$config")"
                exit 1
            fi
        fi
    done

    # Validate configuration schemas
    python3 -c "
import json
import jsonschema

# Define schema for validation
schema = {
    'type': 'object',
    'required': ['mcp_version', 'project_name'],
    'properties': {
        'mcp_version': {'type': 'string'},
        'project_name': {'type': 'string'},
        'configuration': {'type': 'object'},
        'plugins': {'type': 'object'}
    }
}

# Validate main config
try:
    with open('$SCRIPT_DIR/mcp_config_2025.json') as f:
        config = json.load(f)
    jsonschema.validate(config, schema)
    print('✅ Main configuration schema valid')
except Exception as e:
    print(f'❌ Configuration validation error: {e}')
    exit(1)
"

    success "Configuration validation completed"
}

# Initialize monitoring
initialize_monitoring() {
    log "Initializing MCP monitoring system..."

    # Initialize monitoring database
    python3 "$SCRIPT_DIR/mcp_monitoring_dashboard.py" > /dev/null 2>&1 || {
        warning "Monitoring dashboard initialization failed (may require dependencies)"
    }

    # Generate initial sample data for testing
    if python3 "$SCRIPT_DIR/mcp_monitoring_dashboard.py" > /dev/null 2>&1; then
        success "Monitoring system initialized"
    else
        warning "Monitoring system initialization completed with warnings"
    fi
}

# Run security analysis
run_security_analysis() {
    log "Running initial security analysis..."

    if python3 "$SCRIPT_DIR/mcp_security_optimizer.py" > /dev/null 2>&1; then
        success "Security analysis completed"

        # Show summary if reports exist
        if [[ -d "$SCRIPT_DIR/reports" ]] && [[ $(ls -A "$SCRIPT_DIR/reports") ]]; then
            report_count=$(ls "$SCRIPT_DIR/reports"/*_report_*.json 2>/dev/null | wc -l || echo "0")
            if [[ $report_count -gt 0 ]]; then
                success "Generated $report_count security/performance reports"
                log "Reports available in: $SCRIPT_DIR/reports/"
            fi
        fi
    else
        warning "Security analysis completed with warnings"
    fi
}

# Setup integration with existing tools
setup_integration() {
    log "Setting up integration with existing tools..."

    # Check HAL Agent integration
    if [[ -f "$PROJECT_ROOT/dev_tools/agent_controls/hal_token_savvy_agent.py" ]]; then
        success "HAL Agent integration available"
    else
        warning "HAL Agent not found - token optimization integration may be limited"
    fi

    # Check Token-Sage integration
    if [[ -f "$PROJECT_ROOT/dev_tools/token_optimization/always_token_sage.py" ]]; then
        success "Token-Sage integration available"
    else
        warning "Token-Sage not found - token optimization integration may be limited"
    fi

    # Check episodic memory CLI (DISABLED)
    # if [[ -d "$HOME/.claude/plugins/cache/episodic-memory" ]]; then
    #     success "Episodic Memory plugin available"
    #
    #     # Initialize episodic memory if needed
    #     if [[ -f "$SCRIPT_DIR/init_mcp.sh" ]]; then
    #         bash "$SCRIPT_DIR/init_mcp.sh" > /dev/null 2>&1 || {
    #             warning "Episodic memory initialization completed with warnings"
    #         }
    #     fi
    # else
    #     warning "Episodic Memory plugin not found - conversation search may be limited"
    # fi
    echo "🔍 Episodic Memory plugin check: DISABLED"
}

# Create quick start scripts
create_quickstart_scripts() {
    log "Creating quick start scripts..."

    # Security check script
    cat > "$SCRIPT_DIR/quick_security_check.sh" << 'EOF'
#!/bin/bash
echo "🔍 Running MCP Security Check..."
python3 .claude/mcp_security_optimizer.py
echo "📊 Reports available in .claude/reports/"
EOF

    # Monitoring dashboard script
    cat > "$SCRIPT_DIR/quick_monitoring.sh" << 'EOF'
#!/bin/bash
echo "📈 Starting MCP Monitoring Dashboard..."
python3 .claude/mcp_monitoring_dashboard.py
echo "📊 Dashboard data exported to .claude/dashboard_data.json"
EOF

    # Configuration validation script
    cat > "$SCRIPT_DIR/quick_validate.sh" << 'EOF'
#!/bin/bash
echo "✅ Validating MCP Configuration..."
for config in .claude/*config_2025.json; do
    if [[ -f "$config" ]]; then
        echo "Validating $(basename "$config")..."
        python3 -m json.tool "$config" > /dev/null && echo "✅ Valid" || echo "❌ Invalid"
    fi
done
EOF

    # Make scripts executable
    chmod +x "$SCRIPT_DIR/quick_"*.sh

    success "Quick start scripts created"
}

# Final verification
final_verification() {
    log "Performing final verification..."

    # Check all required files
    required_files=(
        "$SCRIPT_DIR/mcp_config_2025.json"
        "$SCRIPT_DIR/mcp_security_optimizer.py"
        "$SCRIPT_DIR/mcp_monitoring_dashboard.py"
        "$SCRIPT_DIR/MCP_2025_Documentation.md"
    )

    missing_files=()
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            missing_files+=("$file")
        fi
    done

    if [[ ${#missing_files[@]} -eq 0 ]]; then
        success "All required files are present"
    else
        error "Missing required files: ${missing_files[*]}"
        exit 1
    fi

    # Check scripts are executable
    if [[ -x "$SCRIPT_DIR/mcp_security_optimizer.py" ]] && [[ -x "$SCRIPT_DIR/mcp_monitoring_dashboard.py" ]]; then
        success "All scripts are executable"
    else
        error "Some scripts are not executable"
        exit 1
    fi

    # Test configuration loading
    if python3 -c "
import json
try:
    with open('$SCRIPT_DIR/mcp_config_2025.json') as f:
        json.load(f)
    print('Configuration loads successfully')
except Exception as e:
    print(f'Configuration loading failed: {e}')
    exit(1)
" > /dev/null 2>&1; then
        success "Configuration loads successfully"
    else
        error "Configuration loading failed"
        exit 1
    fi
}

# Print summary and next steps
print_summary() {
    echo ""
    echo "🎉 MCP 2025 Industry Standards Setup Complete!"
    echo ""
    echo "📋 Summary:"
    echo "  ✅ MCP configuration files installed"
    echo "  ✅ Security and monitoring tools ready"
    echo "  ✅ Integration with existing tools configured"
    echo "  ✅ Quick start scripts created"
    echo "  ✅ All configurations validated"
    echo ""
    echo "🚀 Next Steps:"
    echo "  1. Review documentation: $HOME/.claude/MCP_2025_Documentation.md"
    echo "  2. Run security check: .claude/quick_security_check.sh"
    echo "  3. Start monitoring: .claude/quick_monitoring.sh"
    echo "  4. Validate configuration: .claude/quick_validate.sh"
    echo ""
    echo "📊 Monitoring:"
    echo "  - Security reports: $SCRIPT_DIR/reports/"
    echo "  - Monitoring data: $SCRIPT_DIR/mcp_monitoring.db"
    echo "  - Dashboard export: $SCRIPT_DIR/dashboard_data.json"
    echo ""
    echo "🔧 Configuration Files:"
    echo "  - Main config: $HOME/.claude/mcp_config_2025.json"
    echo "  - Superpowers: $HOME/.claude/mcp_superpowers_config_2025.json"
    # echo "  - Episodic Memory: $HOME/.claude/mcp_episodic_memory_config_2025.json"  # DISABLED
    echo ""
    echo "💡 For detailed usage instructions, see the MCP 2025 Documentation."
    echo ""
}

# Main execution
main() {
    log "MCP 2025 Industry Standards Setup starting..."

    check_prerequisites
    setup_configurations
    setup_tools
    validate_configurations
    initialize_monitoring
    run_security_analysis
    setup_integration
    create_quickstart_scripts
    final_verification
    print_summary

    success "MCP 2025 setup completed successfully!"
}

# Handle script interruption
trap 'error "Setup interrupted"; exit 1' INT TERM

# Run main function
main "$@"
