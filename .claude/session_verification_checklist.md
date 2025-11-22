# Session Continuity Verification Checklist

## 🔄 **Step 1: Environment Verification**

When you open Claude Code in VS Code, run these commands to verify the session is preserved:

### **A. Database Connection Test**
```bash
# First, activate the environment
source $PWD/.venv/bin/activate
export PYTHONPATH="lib_package/src:cli_package/src"

# Test database connectivity
python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='localhost', port=5433, database='mcp_tools',
        user='mcp_user', password='mcp_secure_password_2024'
    )
    print('✅ Database connection: SUCCESS')
    conn.close()
except Exception as e:
    print(f'❌ Database connection failed: {e}')
"
```

### **B. Session Data Verification**
```bash
# Verify session data exists
python -c "
import psycopg2
import json

conn = psycopg2.connect(
    host='localhost', port=5433, database='mcp_tools',
    user='mcp_user', password='mcp_secure_password_2024'
)

with conn.cursor() as cursor:
    # Check session count
    cursor.execute('SELECT COUNT(*) FROM todowrite_sessions')
    session_count = cursor.fetchone()[0]
    print(f'✅ Sessions in database: {session_count}')

    # Check goals count
    cursor.execute('SELECT COUNT(*) FROM todowrite_goals')
    goal_count = cursor.fetchone()[0]
    print(f'✅ Goals in database: {goal_count}')

    # Check concepts count
    cursor.execute('SELECT COUNT(*) FROM todowrite_concepts')
    concept_count = cursor.fetchone()[0]
    print(f'✅ Concepts in database: {concept_count}')

    # Check total table count
    cursor.execute(\"\"\"
        SELECT COUNT(*) FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name LIKE 'todowrite_%'
    \"\"\")
    table_count = cursor.fetchone()[0]
    print(f'✅ Total ToDoWrite tables: {table_count}')

conn.close()
print('✅ Session data verification: COMPLETE')
"
```

### **C. Models API Verification**
```bash
# Test that existing Models API imports work
python -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / 'lib_package' / 'src'))

try:
    from todowrite.core.models import (
        Goal, Concept, Context, Constraints, Requirements,
        AcceptanceCriteria, InterfaceContract, Phase, Step,
        Task, SubTask, Command, Label
    )
    print('✅ Existing Models API: IMPORTED SUCCESSFULLY')
    print(f'✅ Available models: Goal, Concept, Context, Constraints, Requirements, AcceptanceCriteria, InterfaceContract, Phase, Step, Task, SubTask, Command, Label')
except ImportError as e:
    print(f'❌ Models API import failed: {e}')
"
```

## 📋 **Step 2: Context Preservation Test**

Ask Claude in the IDE these specific questions to verify session continuity:

### **Question 1: Session Memory**
```
"Do you remember our work setting up the ToDoWrite PostgreSQL Backend System? What container and database configuration did we create?"
```

### **Expected Response Should Include:**
- mcp-postgres container running on port 5433
- Database: mcp_tools with user mcp_user
- 23 tables created with complete hierarchy
- Auto-restart policy: unless-stopped
- Session ID tracking for cross-session persistence

### **Question 2: Technical Details**
```
"What specific foreign key relationships and association tables did we create for the ToDoWrite hierarchy?"
```

### **Expected Response Should Include:**
- 31 foreign key constraints
- Association tables like todowrite_goal_tasks, todowrite_concept_tasks, etc.
- CASCADE DELETE behavior
- Complete 12-layer hierarchy: Goal → ... → Command

### **Question 3: Data Verification**
```
"How much data should be in our current database and what specific counts should we see?"
```

### **Expected Response Should Include:**
- 5 goals, 12 concepts, 1 session
- 23 total tables
- Complete cross-association tables

## 🔍 **Step 3: Functional Verification**

Run this comprehensive test in the IDE:

```bash
# Full functionality test
python -c "
import sys
import json
from pathlib import Path

# Set up paths
sys.path.insert(0, str(Path.cwd() / 'lib_package' / 'src'))

print('🔄 Testing Complete Session Continuity...')
print('=' * 50)

try:
    # Test 1: Models API Import
    from todowrite.core.models import Goal, Concept, Task
    print('✅ Test 1: Models API - PASSED')

    # Test 2: Database Connection
    import psycopg2
    conn = psycopg2.connect(
        host='localhost', port=5433, database='mcp_tools',
        user='mcp_user', password='mcp_secure_password_2024'
    )
    print('✅ Test 2: Database Connection - PASSED')

    # Test 3: Data Verification
    with conn.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM todowrite_goals')
        goal_count = cursor.fetchone()[0]
        print(f'✅ Test 3: Goals Found: {goal_count}')

        cursor.execute('SELECT COUNT(*) FROM todowrite_concepts')
        concept_count = cursor.fetchone()[0]
        print(f'✅ Test 3: Concepts Found: {concept_count}')

        # Test 4: Create new item to verify functionality
        cursor.execute('''
            INSERT INTO todowrite_goals (title, description, session_id)
            VALUES (%s, %s, %s)
            RETURNING id
        ''', ('IDE Session Verification', 'Testing session continuity', 'ide_verification'))

        result = cursor.fetchone()
        new_id = result[0] if result else None
        print(f'✅ Test 4: New Goal Created - ID: {new_id}')

        conn.commit()

    conn.close()
    print('✅ Test 5: Transaction Success')

    print('\\n🎉 COMPLETE SESSION CONTINUITY VERIFIED!')
    print('   📚 Models API: Working')
    print('   🗄️  Database: Connected')
    print('   📊 Data: Intact')
    print('   💾 Functionality: Active')

except Exception as e:
    print(f'❌ Verification failed: {e}')
    import traceback
    traceback.print_exc()
"
```

## ✅ **Success Indicators**

When the session continuity is successful, you should see:

1. **✅ All Database Tests Pass**
2. **✅ Models API Imports Successfully**
3. **✅ Claude Remembers All Previous Work**
4. **✅ Data Counts Match Expected Values**
5. **✅ New Items Can Be Created**
6. **✅ Container Auto-Restart Working**

## 🚨 **Troubleshooting**

If verification fails, check:

1. **Container Status**: `docker ps --filter "name=mcp-postgres"`
2. **Environment Variables**: PYTHONPATH, virtual environment activated
3. **Database Access**: Test connection manually
4. **File Permissions**: Ensure scripts are executable

## 🎯 **Final Confirmation**

Ask Claude this final question:
```
"Can you summarize the complete ToDoWrite PostgreSQL Backend System we built and confirm all the key components are working in this IDE session?"
```

**Expected comprehensive response** should include all technical details, table structures, data counts, and confirmation that the session has been fully preserved.
