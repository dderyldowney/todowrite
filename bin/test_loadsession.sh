#!/bin/bash

# test_loadsession.sh - Comprehensive Test Suite for loadsession Command
# Tests both successful execution and failure scenarios

set -e

# Colors for test output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
print_test_header() {
    echo -e "${BLUE}┌─────────────────────────────────────────────────────────┐${NC}"
    echo -e "${BLUE}│ $1${NC}"
    echo -e "${BLUE}└─────────────────────────────────────────────────────────┘${NC}"
    echo
}

print_test_result() {
    local test_name="$1"
    local result="$2"
    local details="$3"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [ "$result" = "PASS" ]; then
        echo -e "${GREEN}✅ PASS: $test_name${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}❌ FAIL: $test_name${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    if [ -n "$details" ]; then
        echo -e "${CYAN}   Details: $details${NC}"
    fi
    echo
}

run_test() {
    local test_name="$1"
    local command="$2"
    local expected_exit_code="$3"
    local expected_output_pattern="$4"

    echo -e "${YELLOW}🧪 Running: $test_name${NC}"
    echo -e "${CYAN}   Command: $command${NC}"

    # Capture both stdout and stderr, and exit code
    local output
    local exit_code
    set +e
    output=$(eval "$command" 2>&1)
    exit_code=$?
    set -e

    echo -e "${CYAN}   Exit Code: $exit_code (expected: $expected_exit_code)${NC}"

    # Check exit code
    if [ "$exit_code" -eq "$expected_exit_code" ]; then
        # Check output pattern if provided
        if [ -n "$expected_output_pattern" ]; then
            if echo "$output" | grep -q "$expected_output_pattern"; then
                print_test_result "$test_name" "PASS" "Exit code and output pattern matched"
            else
                print_test_result "$test_name" "FAIL" "Output pattern '$expected_output_pattern' not found"
                echo -e "${RED}   Actual output excerpt:${NC}"
                echo "$output" | head -3 | sed 's/^/     /'
            fi
        else
            print_test_result "$test_name" "PASS" "Exit code matched"
        fi
    else
        print_test_result "$test_name" "FAIL" "Expected exit code $expected_exit_code, got $exit_code"
    fi

    echo "----------------------------------------"
    echo
}

# Main test execution
main() {
    print_test_header "AFS FastAPI loadsession Command Test Suite"

    echo -e "${BLUE}🎯 Testing loadsession command functionality and failure scenarios${NC}"
    echo -e "${BLUE}📋 Validating enterprise-grade error handling and success patterns${NC}"
    echo

    # Test 1: Successful execution (current working scenario)
    print_test_header "TEST 1: Successful loadsession Execution"
    run_test "Successful loadsession with SESSION_SUMMARY.md present" \
             "bin/loadsession" \
             0 \
             "Session Context Successfully Restored"

    # Test 2: Missing SESSION_SUMMARY.md
    print_test_header "TEST 2: Missing SESSION_SUMMARY.md Scenario"

    # Backup SESSION_SUMMARY.md temporarily
    if [ -f "SESSION_SUMMARY.md" ]; then
        mv SESSION_SUMMARY.md SESSION_SUMMARY.md.backup
        echo -e "${YELLOW}📁 Temporarily moved SESSION_SUMMARY.md for testing${NC}"
    fi

    run_test "loadsession with missing SESSION_SUMMARY.md" \
             "bin/loadsession" \
             1 \
             "SESSION_SUMMARY.md not found"

    # Restore SESSION_SUMMARY.md
    if [ -f "SESSION_SUMMARY.md.backup" ]; then
        mv SESSION_SUMMARY.md.backup SESSION_SUMMARY.md
        echo -e "${GREEN}📁 Restored SESSION_SUMMARY.md${NC}"
        echo
    fi

    # Test 3: loadsession script permissions
    print_test_header "TEST 3: Script Permissions Verification"

    # Check if script is executable
    if [ -x "bin/loadsession" ]; then
        print_test_result "loadsession executable permissions" "PASS" "Script has executable permissions"
    else
        print_test_result "loadsession executable permissions" "FAIL" "Script lacks executable permissions"
    fi

    # Test 4: Content verification
    print_test_header "TEST 4: Content Extraction Verification"

    # Capture loadsession output for content analysis
    local loadsession_output
    loadsession_output=$(bin/loadsession 2>&1)

    # Check for key content indicators
    local content_tests=(
        "v0.1.3.*Stable Release:Version information extraction"
        "129.*tests:Test count extraction"
        "Zero linting warnings:Quality status extraction"
        "Test-First Development:Methodology identification"
        "synchronization infrastructure:Strategic priority extraction"
        "distributed systems:Foundation status extraction"
    )

    for test_pattern in "${content_tests[@]}"; do
        local pattern="${test_pattern%:*}"
        local description="${test_pattern#*:}"

        if echo "$loadsession_output" | grep -q "$pattern"; then
            print_test_result "$description" "PASS" "Pattern '$pattern' found in output"
        else
            print_test_result "$description" "FAIL" "Pattern '$pattern' not found in output"
        fi
    done

    # Test 5: Output format verification
    print_test_header "TEST 5: Output Format Standards"

    # Check for professional formatting elements
    local format_tests=(
        "🚀.*AFS FastAPI:Header formatting"
        "✅.*SESSION_SUMMARY.md found:Success indicator formatting"
        "📊.*Current Platform Status:Status section formatting"
        "🎯.*Strategic Priority:Priority section formatting"
        "✨.*Enterprise Platform Ready:Completion formatting"
    )

    for test_pattern in "${format_tests[@]}"; do
        local pattern="${test_pattern%:*}"
        local description="${test_pattern#*:}"

        if echo "$loadsession_output" | grep -q "$pattern"; then
            print_test_result "$description" "PASS" "Format element present"
        else
            print_test_result "$description" "FAIL" "Format element missing"
        fi
    done

    # Test 6: Error handling with corrupted SESSION_SUMMARY.md
    print_test_header "TEST 6: Corrupted File Handling"

    # Create temporary corrupted file
    echo "corrupted content" > SESSION_SUMMARY.md.corrupt
    mv SESSION_SUMMARY.md SESSION_SUMMARY.md.backup2
    mv SESSION_SUMMARY.md.corrupt SESSION_SUMMARY.md

    run_test "loadsession with corrupted SESSION_SUMMARY.md" \
             "bin/loadsession" \
             0 \
             "Session Context Successfully Restored"

    # Note: The current loadsession script is robust and will still execute
    # but won't find the expected patterns

    # Restore proper file
    mv SESSION_SUMMARY.md.backup2 SESSION_SUMMARY.md

    # Final results summary
    print_test_header "TEST RESULTS SUMMARY"

    echo -e "${BLUE}📊 Test Execution Summary:${NC}"
    echo -e "   Total Tests Run: ${CYAN}$TESTS_RUN${NC}"
    echo -e "   Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "   Tests Failed: ${RED}$TESTS_FAILED${NC}"

    local success_rate=0
    if [ "$TESTS_RUN" -gt 0 ]; then
        success_rate=$((TESTS_PASSED * 100 / TESTS_RUN))
    fi
    echo -e "   Success Rate: ${CYAN}$success_rate%${NC}"
    echo

    if [ "$TESTS_FAILED" -eq 0 ]; then
        echo -e "${GREEN}🎉 All tests passed! loadsession command is functioning correctly.${NC}"
        exit 0
    else
        echo -e "${RED}⚠️  Some tests failed. Review output above for details.${NC}"
        exit 1
    fi
}

# Execute main function
main "$@"
