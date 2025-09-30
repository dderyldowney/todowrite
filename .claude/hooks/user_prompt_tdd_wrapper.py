#!/usr/bin/env python3
"""
Claude Code UserPromptSubmit Hook Wrapper for TDD Enforcement

This wrapper adapts the TDD enforcement validator to work as a Claude Code hook,
intercepting user prompts that request code generation and ensuring Test-First
Development methodology is followed.

Hook Lifecycle: UserPromptSubmit
- Triggers when user submits a prompt to Claude Code
- Analyzes prompt content to detect code generation requests
- Blocks prompts requesting implementation without test-first approach
- Allows prompts that follow RED-GREEN-REFACTOR methodology

Agricultural Context:
Safety-critical multi-tractor coordination systems require bulletproof reliability.
This hook ensures ALL code generation—human or AI—starts with tests first.
"""

from __future__ import annotations

import json
import re
import sys


class TDDPromptValidator:
    """
    Validates user prompts follow Test-First Development methodology.

    Analyzes prompt content to detect implementation requests and ensures
    they follow RED-GREEN-REFACTOR pattern for agricultural robotics code.
    """

    def __init__(self):
        self.implementation_keywords = [
            r"\badd\s+(?:a\s+)?(?:new\s+)?(?:function|class|method|feature|module|component)",
            r"\bimplement\s+",
            r"\bcreate\s+(?:a\s+)?(?:new\s+)?(?:function|class|method|feature|module|component)",
            r"\bwrite\s+(?:a\s+)?(?:new\s+)?(?:function|class|method|feature|code)",
            r"\bbuild\s+(?:a\s+)?(?:new\s+)?(?:function|class|method|feature|component)",
            r"\bgenerate\s+(?:a\s+)?(?:new\s+)?(?:function|class|method|feature|code)",
        ]

        self.test_keywords = [
            r"\btest",
            r"\btdd\b",
            r"\bred\s+phase",
            r"\bfailing\s+test",
            r"\btest[\s-]first",
            r"\bred-green-refactor",
            r"\bfollowing\s+tdd",
        ]

        self.allowed_without_tests = [
            r"\bexplain\s+",
            r"\bdescribe\s+",
            r"\bwhat\s+(?:is|does)",
            r"\bhow\s+(?:does|do)",
            r"\bwhy\s+",
            r"\bread\s+",
            r"\bshow\s+",
            r"\blist\s+",
            r"\bfind\s+",
            r"\bsearch\s+",
            r"\bgrep\s+",
            r"\bfix\s+the\s+hooks",  # Allow hook fixing without tests
            r"\brefactor\s+",
            r"\bformat\s+",
            r"\bdocument\s+",
        ]

    def is_implementation_request(self, prompt: str) -> bool:
        """Check if prompt requests code implementation."""
        prompt_lower = prompt.lower()

        # First check if it's explicitly allowed without tests
        for pattern in self.allowed_without_tests:
            if re.search(pattern, prompt_lower):
                return False

        # Then check for implementation keywords
        for pattern in self.implementation_keywords:
            if re.search(pattern, prompt_lower):
                return True

        return False

    def mentions_tests(self, prompt: str) -> bool:
        """Check if prompt mentions tests or TDD methodology."""
        prompt_lower = prompt.lower()

        for pattern in self.test_keywords:
            if re.search(pattern, prompt_lower):
                return True

        return False

    def validate_prompt(self, prompt: str) -> tuple[bool, str]:
        """
        Validate prompt follows TDD methodology.

        Args:
            prompt: User prompt text

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if this is an implementation request
        if not self.is_implementation_request(prompt):
            # Not an implementation request - allow it
            return True, ""

        # It's an implementation request - check for TDD methodology
        if self.mentions_tests(prompt):
            # Mentions tests - likely following TDD
            return True, ""

        # Implementation request without test-first approach
        error_msg = """
🚫 TDD METHODOLOGY VIOLATION DETECTED

AFS FastAPI requires Test-First Development for all agricultural robotics code.

Your prompt requests code implementation without mentioning tests.

📋 Required Approach (RED-GREEN-REFACTOR):
1. RED Phase: Write failing test describing desired behavior
2. GREEN Phase: Implement minimal code to pass test
3. REFACTOR Phase: Enhance code quality while maintaining tests

🔧 How to Fix:
Rephrase your prompt to explicitly request test-first development:

Example: "Following TDD methodology, help me implement multi-tractor coordination"
Example: "Write failing tests first, then implement field allocation logic"
Example: "Using RED-GREEN-REFACTOR, add ISOBUS communication feature"

📖 Reference: TDD_WORKFLOW.md for agricultural robotics TDD patterns

⚠️  This enforcement ensures safety-critical agricultural robotics reliability.
"""
        return False, error_msg


def main():
    """
    Main Claude Code hook execution for UserPromptSubmit.

    Reads hook input JSON, validates prompt follows TDD methodology,
    and blocks non-compliant implementation requests.
    """
    try:
        # Read hook input data from stdin
        hook_data = json.loads(sys.stdin.read())

        # Extract user prompt from hook data
        # Hook data structure: {"prompt": "user's prompt text", ...}
        user_prompt = hook_data.get("prompt", "")

        if not user_prompt:
            # No prompt data - allow operation
            sys.exit(0)

        # Validate prompt follows TDD methodology
        validator = TDDPromptValidator()
        is_valid, error_message = validator.validate_prompt(user_prompt)

        if not is_valid:
            # Print error message to stderr
            print(error_message, file=sys.stderr)
            # Block the operation
            sys.exit(1)

        # Prompt is valid - allow operation
        sys.exit(0)

    except json.JSONDecodeError:
        # Invalid JSON input - don't block on hook errors
        print("TDD Hook Warning: Invalid JSON input", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        # Hook error - don't block operation
        print(f"TDD Hook Error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
