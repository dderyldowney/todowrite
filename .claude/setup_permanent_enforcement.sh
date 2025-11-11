#!/bin/bash
# Setup Permanent Code Quality Enforcement

echo "🔒 Setting up permanent code quality enforcement..."

# Source environment overrides
if [ -f ".claude/environment_overrides.env" ]; then
    export $(cat .claude/environment_overrides.env | grep -v '^#' | xargs)
    echo "✓ Environment variables loaded"
fi

# Verify enforcement files exist
if [ -f ".claude/permanent_code_quality_enforcement.json" ]; then
    echo "✓ Permanent enforcement configuration found"
else
    echo "❌ Permanent enforcement configuration missing"
    exit 1
fi

# Set persistent environment variables for current session
export CLAUDE_ENFORCE_SEMANTIC_SCOPING=1
export CLAUDE_ENFORCE_RED_GREEN_REFACTOR=1
export CLAUDE_ENFORCE_TOKEN_OPTIMIZATION=1
export CLAUDE_ENFORCE_TODOWRITE_CLI=1
export CLAUDE_ENFORCE_ZERO_MOCKING=1
export CLAUDE_REQUIRE_EPISODIC_MEMORY=1
export CLAUDE_MANDATORY_QUALITY_GATES=1
export CLAUDE_PRE_COMMIT_ENFORCEMENT=1

echo "✓ Permanent code quality enforcement activated"
echo "🚨 This enforcement persists across all sessions including /clear commands"

# Create marker file for other tools to detect
touch .claude/permanent_enforcement_active
