#!/usr/bin/env python3
"""
AI Communication Compression Utilities for AFS FastAPI

Provides token-efficient response formatting and context-aware output optimization
for agricultural robotics platform communications.

Features:
- Rolling summary generation
- Context-aware response modes
- Token-selective content filtering
- Agricultural domain preservation
"""

import json
import re
from pathlib import Path


class ResponseCompressor:
    """
    Token-efficient response formatter with agricultural context preservation.

    Implements hybrid compression techniques inspired by HyCo₂ and FastKV
    for optimal balance between token efficiency and domain-specific content.
    """

    def __init__(self, project_root: Path | None = None):
        self.project_root = project_root or Path.cwd()
        self.context_dir = self.project_root / ".claude" / "context"
        self.session_state_file = self.context_dir / "session_state.json"
        self.reference_map_file = self.context_dir / "reference_map.json"

        # Load compression configuration
        self.session_state = self._load_session_state()
        self.reference_map = self._load_reference_map()

    def _load_session_state(self) -> dict:
        """Load current session state for context-aware compression."""
        if self.session_state_file.exists():
            try:
                with open(self.session_state_file) as f:
                    return json.load(f)
            except (OSError, json.JSONDecodeError):
                pass
        return {"compression_stats": {}, "rolling_summary": {}}

    def _load_reference_map(self) -> dict:
        """Load reference map for smart cross-reference resolution."""
        if self.reference_map_file.exists():
            try:
                with open(self.reference_map_file) as f:
                    return json.load(f)
            except (OSError, json.JSONDecodeError):
                pass
        return {"smart_references": {}, "cross_reference_resolution": {}}

    def compress_command_output(self, command: str, output: str, mode: str = "brief") -> str:
        """
        Compress command output using context-aware filtering.

        Args:
            command: Command name for context-specific optimization
            output: Original command output
            mode: Compression mode (brief, standard, detailed)

        Returns:
            Optimized output with agricultural context preserved
        """
        if mode == "detailed":
            return output

        # Apply command-specific compression
        if "strategic" in command:
            return self._compress_strategic_output(output, mode)
        elif "test" in command:
            return self._compress_test_output(output, mode)
        elif "git" in command:
            return self._compress_git_output(output, mode)
        else:
            return self._compress_generic_output(output, mode)

    def _compress_strategic_output(self, output: str, mode: str) -> str:
        """Compress strategic command output preserving priority information."""
        lines = output.split("\n")

        if mode == "brief":
            # Extract only high-priority items and completion stats
            compressed = []
            high_priority_count = 0
            completed_count = 0

            for line in lines:
                if "[HIGH]" in line and "○" in line:
                    # Keep high priority pending items
                    compressed.append(line.strip())
                    high_priority_count += 1
                elif "●" in line and "COMPLETE" in line:
                    completed_count += 1
                elif "Total Strategic TODOs:" in line or "Pending:" in line:
                    compressed.append(line.strip())

            # Add summary if not present
            if high_priority_count > 0:
                compressed.insert(0, f"🎯 {high_priority_count} HIGH priority objectives active")
            if completed_count > 0:
                compressed.append(f"✅ {completed_count} objectives completed")

            return "\n".join(compressed)

        return output

    def _compress_test_output(self, output: str, mode: str) -> str:
        """Compress test output preserving critical failure information."""
        if mode == "brief":
            # Extract pass/fail counts and critical failures only
            lines = output.split("\n")
            compressed = []

            for line in lines:
                # Keep test result summaries
                if re.search(r"\d+\s+(passed|failed|error)", line, re.IGNORECASE):
                    compressed.append(line.strip())
                # Keep FAILED test names
                elif "FAILED" in line and "::" in line:
                    compressed.append(f"❌ {line.strip()}")
                # Keep critical warnings
                elif "warning" in line.lower() and any(
                    keyword in line.lower()
                    for keyword in ["agricultural", "safety", "iso", "critical"]
                ):
                    compressed.append(f"⚠️ {line.strip()}")

            return "\n".join(compressed) if compressed else "✅ Tests passing"

        return output

    def _compress_git_output(self, output: str, mode: str) -> str:
        """Compress git output preserving essential status information."""
        if mode == "brief":
            lines = output.split("\n")
            compressed = []
            file_count = 0

            for line in lines:
                if line.strip():
                    file_count += 1
                    # Keep only file count for brief mode
                    if file_count <= 3:  # Show first 3 files
                        compressed.append(line.strip())

            if file_count > 3:
                compressed.append(f"... and {file_count - 3} more files")

            return "\n".join(compressed) if compressed else "Clean working directory"

        return output

    def _compress_generic_output(self, output: str, mode: str) -> str:
        """Apply generic compression preserving agricultural keywords."""
        if mode == "brief":
            lines = output.split("\n")
            compressed = []

            # Preserve lines with agricultural/safety keywords
            agricultural_keywords = [
                "agricultural",
                "tractor",
                "equipment",
                "safety",
                "iso",
                "isobus",
                "compliance",
                "emergency",
                "critical",
            ]

            for line in lines:
                if any(keyword in line.lower() for keyword in agricultural_keywords):
                    compressed.append(line.strip())
                elif len(compressed) < 5:  # Keep first 5 lines if no keywords
                    compressed.append(line.strip())

            return "\n".join(compressed)

        return output

    def create_rolling_summary(self, new_content: str, max_tokens: int = 200) -> str:
        """
        Create rolling summary using Factory.ai-inspired persistent state.

        Args:
            new_content: New content to incorporate
            max_tokens: Maximum token budget for summary

        Returns:
            Compressed rolling summary
        """
        # Estimate token count (rough approximation: 1 token ≈ 4 characters)
        estimated_tokens = len(new_content) // 4

        if estimated_tokens <= max_tokens:
            return new_content

        # Create compressed summary
        lines = new_content.split("\n")
        key_points = []

        for line in lines:
            # Preserve lines with action words and agricultural context
            if any(
                word in line.lower()
                for word in [
                    "implemented",
                    "created",
                    "fixed",
                    "enhanced",
                    "optimized",
                    "agricultural",
                    "tractor",
                    "safety",
                    "compliance",
                ]
            ):
                key_points.append(line.strip())

        # If still too long, take first few key points
        summary = "\n".join(key_points[:5])

        # Update session state
        self.session_state.setdefault("rolling_summary", {})["recent_activity"] = summary
        self._save_session_state()

        return summary

    def get_context_recommendations(self, user_input: str) -> dict[str, str | list[str]]:
        """
        Provide context loading recommendations based on user input.

        Args:
            user_input: User's request or query

        Returns:
            Recommendations for optimal context level and expansions
        """
        input_lower = user_input.lower()

        # Detect context expansion triggers
        expansion_keywords = self.reference_map.get("expansion_triggers", {})

        # Default to essential context
        recommended_level = "essential"
        expansions = []

        # Check for expansion triggers
        if any(keyword in input_lower for keyword in expansion_keywords.get("user_requests", [])):
            recommended_level = "full"
        elif any(keyword in input_lower for keyword in expansion_keywords.get("task_keywords", [])):
            recommended_level = "expanded"

        # Identify specific expansions needed
        if "iso" in input_lower or "compliance" in input_lower:
            expansions.append("ISO_11783_references")
        if "test" in input_lower:
            expansions.append("testing_framework")
        if "agricultural" in input_lower or "tractor" in input_lower:
            expansions.append("agricultural_context")

        return {
            "recommended_level": recommended_level,
            "specific_expansions": expansions,
            "reasoning": f"Detected keywords requiring {recommended_level} context level",
        }

    def _save_session_state(self) -> None:
        """Save updated session state."""
        self.context_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.session_state_file, "w") as f:
                json.dump(self.session_state, f, indent=2)
        except OSError:
            pass  # Graceful failure


def main():
    """CLI interface for response compression utilities."""
    import sys

    if len(sys.argv) < 3:
        print("Usage: response_compressor.py <command> <output_file> [mode]")
        print("Modes: brief, standard, detailed")
        sys.exit(1)

    command = sys.argv[1]
    output_file = sys.argv[2]
    mode = sys.argv[3] if len(sys.argv) > 3 else "brief"

    compressor = ResponseCompressor()

    try:
        with open(output_file) as f:
            output = f.read()

        compressed = compressor.compress_command_output(command, output, mode)
        print(compressed)

    except OSError as e:
        print(f"Error reading output file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
