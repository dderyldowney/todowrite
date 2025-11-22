#!/bin/bash
# Complete Session Verification - Run All Tests
# This script runs all verification tests sequentially

echo "🚀 COMPLETE SESSION VERIFICATION"
echo "================================"
echo "This will run all tests to verify session continuity"
echo ""

# Make scripts executable
chmod +x $PWD/.claude/verify_session_continuity.sh
chmod +x $PWD/.claude/quick_check.sh

echo "📋 Test Plan:"
echo "1. Environment Setup"
echo "2. Container Status"
echo "3. Database Connectivity"
echo "4. Models API Import"
echo "5. Data Verification"
echo "6. Functional Test"
echo "7. Models API Creation Test"
echo "8. Database Structure Test"
echo ""

read -p "Ready to run all tests? (y/N): " confirm
if [[ $confirm != [yY] ]]; then
    echo "Test cancelled."
    exit 0
fi

echo ""
echo "⏱️ Starting verification tests..."
echo ""

# Test 1: Quick check first
echo "⚡ Running Quick Check..."
bash $PWD/.claude/quick_check.sh
if [ $? -ne 0 ]; then
    echo "❌ Quick check failed - stopping tests"
    exit 1
fi
echo ""

# Test 2: Full verification
echo "🔄 Running Full Session Verification..."
bash $PWD/.claude/verify_session_continuity.sh
if [ $? -ne 0 ]; then
    echo "❌ Full verification failed"
    exit 1
fi
echo ""

# Test 3: Models API test
echo "📚 Testing Models API..."
source $PWD/.venv/bin/activate
export PYTHONPATH="lib_package/src:cli_package/src"
python3 $PWD/.claude/test_models_api.py
if [ $? -ne 0 ]; then
    echo "❌ Models API test failed"
    exit 1
fi
echo ""

# Test 4: Database structure test
echo "🗄️ Testing Database Structure..."
python3 $PWD/.claude/test_database_structure.py
if [ $? -ne 0 ]; then
    echo "❌ Database structure test failed"
    exit 1
fi
echo ""

echo "🎉 ALL TESTS COMPLETED SUCCESSFULLY!"
echo "================================="
echo "✅ Session continuity: VERIFIED"
echo "✅ Environment: Configured correctly"
echo "✅ Container: Running and accessible"
echo "✅ Database: Connected with full structure"
echo "✅ Models API: Working perfectly"
echo "✅ Data: Intact with proper relationships"
echo "✅ Functionality: Creating and storing items"
echo ""
echo "🚀 Your ToDoWrite PostgreSQL Backend System is FULLY OPERATIONAL!"
echo "📋 Session context has been perfectly preserved from the previous chat."
