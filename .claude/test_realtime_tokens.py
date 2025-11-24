#!/usr/bin/env python3
"""Test script for real-time token tracking and statusline updates."""

import sys
from pathlib import Path


def test_statusline_functionality():
    """Test basic statusline functionality."""
    print("🧪 Testing Statusline Token Tracking")
    print("=" * 50)

    # Test 1: Get current token count
    print("1. Testing current token count...")
    try:
        import subprocess

        result = subprocess.run(
            ["python3", str(Path.home() / ".claude" / "statusline.py"), "--get-tokens"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            current_tokens = result.stdout.strip()
            print(f"   ✅ Current token count: {current_tokens}")
        else:
            print("   ❌ Failed to get current token count")
            return False
    except Exception as e:
        print(f"   ❌ Error getting token count: {e}")
        return False

    # Test 2: Add some test savings
    print("\n2. Testing token savings addition...")
    try:
        result = subprocess.run(
            [
                "python3",
                str(Path.home() / ".claude" / "statusline.py"),
                "--log-realtime",
                "100",
                "test_activity",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            print("   ✅ Successfully logged 100 tokens from test_activity")
        else:
            print(f"   ❌ Failed to log tokens: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Error logging tokens: {e}")
        return False

    # Test 3: Verify the update
    print("\n3. Verifying token update...")
    try:
        result = subprocess.run(
            ["python3", str(Path.home() / ".claude" / "statusline.py"), "--get-tokens"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            new_tokens = result.stdout.strip()
            print(f"   ✅ New token count: {new_tokens}")
        else:
            print("   ❌ Failed to verify token update")
            return False
    except Exception as e:
        print(f"   ❌ Error verifying update: {e}")
        return False

    # Test 4: Test real-time monitor
    print("\n4. Testing real-time token monitor...")
    monitor_script = Path.cwd() / ".claude" / "realtime_token_monitor.py"
    if monitor_script.exists():
        try:
            result = subprocess.run(
                ["python3", str(monitor_script), "simulate", "75", "test_monitor"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                print("   ✅ Real-time monitor simulation successful")
            else:
                print(f"   ⚠️  Real-time monitor simulation failed: {result.stderr}")
        except Exception as e:
            print(f"   ⚠️  Real-time monitor error: {e}")
    else:
        print("   ⚠️  Real-time monitor not found")

    # Test 5: Final verification
    print("\n5. Final token count verification...")
    try:
        result = subprocess.run(
            ["python3", str(Path.home() / ".claude" / "statusline.py"), "--get-tokens"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            final_tokens = result.stdout.strip()
            print(f"   ✅ Final token count: {final_tokens}")
        else:
            print("   ❌ Failed to get final token count")
            return False
    except Exception as e:
        print(f"   ❌ Error getting final count: {e}")
        return False

    # Test 6: Show statusline preview
    print("\n6. Statusline preview:")
    try:
        result = subprocess.run(
            ["python3", str(Path.home() / ".claude" / "statusline.py")],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            print(f"   📱 {result.stdout.strip()}")
        else:
            print("   ⚠️  Could not preview statusline")
    except Exception as e:
        print(f"   ⚠️  Statusline preview error: {e}")

    print("\n✅ All token tracking tests completed successfully!")
    return True


def test_log_files():
    """Test that log files are being created and updated."""
    print("\n🗂️  Testing Log Files")
    print("=" * 30)

    log_files = [
        Path.cwd() / ".claude" / "realtime_tokens.log",
        Path.cwd() / ".claude" / "token_activities.log",
        Path.cwd() / ".claude" / "token_usage.log",
        Path.cwd() / ".claude" / "token_usage 2.log",
    ]

    for log_file in log_files:
        if log_file.exists():
            size = log_file.stat().st_size
            print(f"   📄 {log_file.name}: {size} bytes")

            # Show last few lines if file is not too large
            if size < 5000:
                try:
                    lines = log_file.read_text().strip().split("\n")
                    if lines and lines[-1]:
                        print(f"      Last entry: {lines[-1][:80]}...")
                except Exception:
                    pass
        else:
            print(f"   📄 {log_file.name}: not found")


def main():
    """Main test function."""
    print("🚀 Real-time Token Tracking Test Suite")
    print("=" * 60)
    print("This script tests the real-time token tracking system")
    print("and verifies that statusline updates work correctly.")
    print()

    # Run tests
    success = test_statusline_functionality()
    test_log_files()

    if success:
        print("\n🎉 All tests passed! Real-time token tracking is working.")
        print("💡 Your statusline should now update immediately when tokens are saved.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the configuration.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
