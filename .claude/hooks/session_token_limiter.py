#!/usr/bin/env python3
"""
Session startup hook that monitors and limits token usage
Runs automatically to enforce token discipline
"""

from pathlib import Path


def main():
    print("🔒 TOKEN LIMITER: Enforcing token discipline...")

    # Quick session analysis
    try:
        # Count potential context sources
        python_files = len(list(Path().rglob("*.py")))
        md_files = len(list(Path().rglob("*.md")))
        json_files = len(list(Path().rglob("*.json")))

        total_files = python_files + md_files + json_files

        # Rough token estimation
        estimated_tokens = total_files * 800  # Conservative estimate

        print("📊 Context Analysis:")
        print(f"   Python files: {python_files}")
        print(f"   Markdown files: {md_files}")
        print(f"   JSON files: {json_files}")
        print(f"   Estimated tokens: {estimated_tokens:,}")

        # Token discipline recommendations
        if estimated_tokens > 30000:
            print("\n⚠️  HIGH TOKEN USAGE DETECTED!")
            print("🎯 MANDATORY DISCIPLINE:")
            print("   ✓ Use specific file paths, not broad searches")
            print("   ✓ Limit to 1-2 files per query")
            print("   ✓ Use Read() with offset/limit for large files")
            print("   ✓ Use Grep() instead of reading entire files")
            print("   ✓ Consider /clear if context is bloated")
            print("   ✓ Use local tools (bash, grep, sed)")

            if estimated_tokens > 50000:
                print("\n🚨 EMERGENCY: Run token reduction now!")
                print("   python .claude/emergency_token_reduction.py")

        elif estimated_tokens > 15000:
            print("\n💡 MODERATE USAGE - Stay focused:")
            print("   ✓ Keep queries specific")
            print("   ✓ Use targeted file paths")

        else:
            print("\n✅ Token usage looks good - maintain discipline")

        # MCP server recommendation
        print("\n🔧 MCP SERVER OPTIMIZATION:")
        print("   Use specific servers: docker mcp gateway run --servers context7,github")
        print(
            "   Full suite only when needed: --servers context7,docker,github,git,filesystem,postgres,SQLite,hugging-face,playwright"
        )

        print("\n💰 TOKEN-SAVING COMMANDS:")
        print("   Monitor: python .claude/token_monitor.py")
        print("   Emergency: python .claude/emergency_token_reduction.py")
        print("   Quick tips: python .claude/token_monitor.py quick")

    except Exception as e:
        print(f"⚠️  Error analyzing tokens: {e}")
        print("💡 Still apply token discipline principles")


if __name__ == "__main__":
    main()
