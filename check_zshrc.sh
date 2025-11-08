#!/bin/bash
echo "Checking .zshrc for syntax errors..."

# Try to check syntax with zsh
if command -v zsh >/dev/null 2>&1; then
    echo "Using zsh to check syntax..."
    zsh -n "$HOME/.zshrc" 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ No syntax errors found in .zshrc"
    else
        echo "❌ Syntax errors found in .zshrc"
        echo "Exit code: $?"
    fi
else
    echo "❌ zsh not found"
fi

# Try to read the file in chunks
echo ""
echo "First 30 lines of .zshrc:"
if [ -f "$HOME/.zshrc" ]; then
    head -30 "$HOME/.zshrc" 2>&1 || echo "Could not read .zshrc"
else
    echo ".zshrc file not found"
fi

echo ""
echo "Checking for common syntax issues..."
if [ -f "$HOME/.zshrc" ]; then
    # Check for unmatched quotes
    echo "Checking for unmatched quotes..."
    grep -n '"\|'\|`' "$HOME/.zshrc" | head -10

    # Check for incomplete if statements
    echo ""
    echo "Checking for incomplete if statements..."
    grep -n "if.*then\|fi" "$HOME/.zshrc" | head -5

    # Check for incomplete loops
    echo ""
    echo "Checking for incomplete loops..."
    grep -n "for.*in\|do\|done" "$HOME/.zshrc" | head -5
    grep -n "while.*do\|done" "$HOME/.zshrc" | head -5
fi
