#!/bin/bash
echo "✅ Validating MCP Configuration..."
for config in .claude/*config_2025.json; do
    if [[ -f "$config" ]]; then
        echo "Validating $(basename "$config")..."
        python3 -m json.tool "$config" > /dev/null && echo "✅ Valid" || echo "❌ Invalid"
    fi
done
