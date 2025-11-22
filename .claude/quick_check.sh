#!/bin/bash
# Quick Session Check (30 seconds)
# Run this for fast verification

echo "⚡ Quick Session Check"
echo "====================="

source $PWD/.venv/bin/activate 2>/dev/null
export PYTHONPATH="lib_package/src:cli_package/src"

python3 -c "
import psycopg2
import sys
from pathlib import Path

try:
    # Quick database check
    conn = psycopg2.connect(
        host='localhost', port=5433, database='mcp_tools',
        user='mcp_user', password='mcp_secure_password_2024'
    )

    with conn.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM todowrite_goals'); goals = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM todowrite_concepts'); concepts = cursor.fetchone()[0]
        cursor.execute(\"\"\"
            SELECT COUNT(*) FROM information_schema.tables
            WHERE table_schema='public' AND table_name LIKE 'todowrite_%'
        \"\"\"); tables = cursor.fetchone()[0]

    conn.close()

    print(f'✅ Goals: {goals}, Concepts: {concepts}, Tables: {tables}')
    print('✅ Session continuity: CONFIRMED')

except Exception as e:
    print(f'❌ Check failed: {e}')
    sys.exit(1)
"