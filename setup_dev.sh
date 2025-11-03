#!/bin/bash
# ToDoWrite Development Environment Setup

echo "🚀 Setting up ToDoWrite development environment..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Install packages in development mode
echo "📦 Installing packages in development mode..."
pip install -e "$SCRIPT_DIR/lib_package"
pip install -e "$SCRIPT_DIR/cli_package"

# Set up PYTHONPATH permanently
echo "🔧 Setting up permanent PYTHONPATH..."

# Add to shell profile if not already there
SHELL_PROFILE=""
if [[ -f "$HOME/.zshrc" ]]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [[ -f "$HOME/.bashrc" ]]; then
    SHELL_PROFILE="$HOME/.bashrc"
elif [[ -f "$HOME/.bash_profile" ]]; then
    SHELL_PROFILE="$HOME/.bash_profile"
fi

if [[ -n "$SHELL_PROFILE" ]]; then
    # Remove existing todowrite PYTHONPATH entries if any
    if grep -q "TODOWRITE_PYTHONPATH" "$SHELL_PROFILE"; then
        echo "🗑️  Removing existing ToDoWrite PYTHONPATH entries..."
        sed -i.tmp '/# ToDoWrite development environment/,/# End ToDoWrite development environment/d' "$SHELL_PROFILE"
        rm -f "$SHELL_PROFILE.tmp"
    fi

    # Add new PYTHONPATH configuration
    echo "" >> "$SHELL_PROFILE"
    echo "# ToDoWrite development environment" >> "$SHELL_PROFILE"
    echo "export TODOWRITE_PYTHONPATH=\"$SCRIPT_DIR/lib_package:$SCRIPT_DIR/cli_package\"" >> "$SHELL_PROFILE"
    echo "export PYTHONPATH=\"\$TODOWRITE_PYTHONPATH:\$PYTHONPATH\"" >> "$SHELL_PROFILE"
    echo "# End ToDoWrite development environment" >> "$SHELL_PROFILE"
    echo "✅ Added to $SHELL_PROFILE"
    echo "🔄 Please restart your shell or run: source $SHELL_PROFILE"
else
    echo "⚠️  Could not find shell profile. Please manually add:"
    echo "export TODOWRITE_PYTHONPATH=\"$SCRIPT_DIR/lib_package:$SCRIPT_DIR/cli_package\""
    echo "export PYTHONPATH=\"\$TODOWRITE_PYTHONPATH:\$PYTHONPATH\""
fi

# Set current session PYTHONPATH
export TODOWRITE_PYTHONPATH="$SCRIPT_DIR/lib_package:$SCRIPT_DIR/cli_package"
export PYTHONPATH="$TODOWRITE_PYTHONPATH:$PYTHONPATH"

# Verify installation
echo ""
echo "✅ Verifying installation..."
python -c "import todowrite; print('✅ todowrite package found')"
python -c "import todowrite_cli; print('✅ todowrite_cli package found')"

echo ""
echo "🎯 ToDoWrite development environment setup complete!"
echo ""
echo "🚀 Available commands:"
echo "   todowrite --help                    # CLI help"
echo "   python -m pytest tests/           # Run tests"
echo "   ruff check .                       # Code quality check"
echo "   npx pyright .                      # Type checking"
echo ""
echo "📁 Development packages are now installed in editable mode"
echo "🔧 PYTHONPATH is permanently configured for this project"
