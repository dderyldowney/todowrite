#!/bin/bash
echo "🔧 VS Code Terminal Fix Script"
echo "=============================="

echo ""
echo "1. Killing existing VS Code terminal processes..."
pkill -f "vscode" 2>/dev/null || true
pkill -f "Code Helper" 2>/dev/null || true

echo ""
echo "2. Resetting terminal state..."
stty sane 2>/dev/null || true
reset 2>/dev/null || true

echo ""
echo "3. Testing basic shell functionality..."
if zsh -c "echo '✅ zsh works'" 2>/dev/null; then
    echo "✅ zsh is functional"
else
    echo "❌ zsh has issues"
fi

echo ""
echo "4. Testing .zshrc sourcing..."
if zsh -c "source ~/.zshrc && echo '✅ .zshrc sources correctly'" 2>/dev/null; then
    echo "✅ .zshrc is healthy"
else
    echo "❌ .zshrc has issues"
fi

echo ""
echo "🎯 Recommended actions:"
echo "1. In VS Code: Press Ctrl+Shift+P → 'Terminal: Kill Active Terminal'"
echo "2. Then: Ctrl+Shift+P → 'Terminal: Create New Terminal'"
echo "3. If still broken: Restart VS Code entirely"
echo "4. As last resort: Create a new terminal profile in VS Code settings"

echo ""
echo "📝 Alternative: Use bash instead of zsh in VS Code:"
echo "   In VS Code settings: \"terminal.integrated.defaultProfile.osx\": \"bash\""

echo ""
echo "✅ Terminal fix script completed!"
