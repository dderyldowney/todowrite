#!/usr/bin/env python3
"""
Lightweight token monitor and limiter
Monitors session token usage and provides recommendations
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class TokenMonitor:
    def __init__(self):
        self.max_tokens = 25000  # Conservative limit
        self.warning_threshold = 20000
        self.emergency_threshold = 50000
        self.log_file = Path(".claude/token_usage.log")

    def check_session_health(self):
        """Check current session token health"""
        print("🔍 TOKEN MONITOR: Checking session health...")

        # Estimate current session size
        try:
            # Count files in current working directory
            result = subprocess.run(
                [
                    "find",
                    ".",
                    "-maxdepth",
                    "2",
                    "-name",
                    "*.py",
                    "-o",
                    "-name",
                    "*.md",
                    "-o",
                    "-name",
                    "*.json",
                ],
                capture_output=True,
                text=True,
            )
            file_count = len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0

            # Check .claude directory size
            try:
                claude_size = subprocess.run(
                    ["du", "-sb", ".claude"], capture_output=True, text=True
                )
                claude_kb = (
                    int(claude_size.stdout.split()[0]) / 1024 if claude_size.stdout.strip() else 0
                )
            except:
                claude_kb = 0

            # Estimate token usage (rough approximation)
            estimated_tokens = (file_count * 1000) + (claude_kb * 2)  # Rough estimate

            print("📊 Session Analysis:")
            print(f"   Python/MD/JSON files: {file_count}")
            print(f"   .claude directory size: {claude_kb:.1f} KB")
            print(f"   Estimated session tokens: {estimated_tokens:,}")

            # Provide recommendations
            if estimated_tokens > self.emergency_threshold:
                self.emergency_recommendations()
            elif estimated_tokens > self.warning_threshold:
                self.warning_recommendations()
            else:
                print("   ✅ Token usage is within acceptable limits")

            return estimated_tokens

        except Exception as e:
            print(f"   ❌ Error analyzing session: {e}")
            return 0

    def emergency_recommendations(self):
        """Emergency token reduction recommendations"""
        print("\n🚨 EMERGENCY: Token usage is critically high!")
        print("   IMMEDIATE ACTIONS REQUIRED:")
        print("   1. Type: /clear (restart session)")
        print("   2. Run: python .claude/emergency_token_reduction.py")
        print("   3. Use specific file paths instead of broad searches")
        print("   4. Limit to 1-2 files per query")
        print("   5. Disable MCP servers when not needed")

    def warning_recommendations(self):
        """Warning level recommendations"""
        print("\n⚠️  WARNING: Token usage is elevated")
        print("   RECOMMENDATIONS:")
        print("   1. Be more specific with file paths")
        print("   2. Use grep instead of reading entire files")
        print("   3. Clear session with /clear if not needed")
        print("   4. Use focused queries")

    def log_usage(self, tokens):
        """Log token usage"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "tokens": tokens,
                "directory": os.getcwd(),
            }

            if not self.log_file.exists():
                self.log_file.parent.mkdir(exist_ok=True)

            with open(self.log_file, "a") as f:
                json.dump(log_entry, f)
                f.write("\n")
        except Exception as e:
            print(f"⚠️  Could not log token usage: {e}")

    def quick_optimization_tips(self):
        """Show quick optimization tips"""
        print("\n💡 QUICK TOKEN OPTIMIZATION:")
        print("✓ Use file paths instead of broad searches")
        print("✓ Use Read() with offset/limit for large files")
        print("✓ Use Grep() for pattern searching")
        print("✓ Limit context to 1-3 files maximum")
        print("✓ Use /clear to restart clean sessions")
        print("✓ Disable MCP servers when not needed")
        print("✓ Use local tools (bash, grep, sed) when possible")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        monitor = TokenMonitor()
        monitor.quick_optimization_tips()
        return

    monitor = TokenMonitor()
    tokens = monitor.check_session_health()
    monitor.log_usage(tokens)

    if tokens > monitor.emergency_threshold:
        print("\n🔄 Run this for immediate reduction:")
        print("python .claude/emergency_token_reduction.py")


if __name__ == "__main__":
    main()
