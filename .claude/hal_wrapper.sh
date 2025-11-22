#!/bin/bash
# HAL Preprocessing Wrapper - MANDATORY for all file operations

# Check if HAL preprocessing is enabled
if [[ "$HAL_PREPROCESSING_MANDATORY" != "true" ]]; then
    echo "❌ HAL preprocessing is MANDATORY. Enable with HAL_PREPROCESSING_MANDATORY=true"
    exit 1
fi

# Detect package context
PACKAGE_CONTEXT=${PACKAGE_CONTEXT:-root}
MAX_FILES=${MAX_FILES:-100}
MAX_CONTEXT_CHARS=${MAX_CONTEXT_CHARS:-2000}

# Run HAL preprocessor
python3 .claude/hal_preprocessor.py "$@" --package-context "$PACKAGE_CONTEXT" --max-files "$MAX_FILES" --max-chars "$MAX_CONTEXT_CHARS"
