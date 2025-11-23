#!/usr/bin/env python3
"""
HAL Enforcement Hook - Mandatory Token Optimization Enforcement
Automatically runs HAL token optimization during development
Integrates with session management and development workflow
"""

import os
import sys
import time
import subprocess
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT =_PATH = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class HALEnforcementHook:
    """
    Automatic HAL enforcement system
    Ensures mandatory token optimization is always active
    """

    def __init__(self):
        """Initialize HAL enforcement hook"""
        self.hal_script = PROJECT_ROOT / ".claude" / "hal_token_optimizer.py"
        self.enforcement_interval = 120  # Check every 2 minutes
        self.last_check = 0
        self.session_active = True
        self.violation_count = 0

    def check_and_enforce(self):
        """Check session and enforce HAL token limits"""
        try:
            # Only run HAL if session is active
            if not self.session_active:
                return

            current_time = time.time()
            if current_time - self.last_check < self.enforcement_interval:
                return  # Too recent to check again

            self.last_check = current_time

            # Run HAL analysis
            result = subprocess.run(
                [sys.executable, str(self.hal_script), "--analyze"],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT
            )

            if result.returncode != 0:
                print("⚠️  HAL enforcement error:")
                print(result.stderr)
                return

            # Parse output for violations
            output = result.stdout
            if "CRITICAL" in output:
                self.violation_count += 1
                self._handle_critical_violation(output)
            elif "WARNING" in output:
                self._handle_warning(output)

        except Exception as e:
            print(f"⚠️  HAL enforcement error: {e}")

    def _handle_critical_violation(self, output: str):
        """Handle critical token violations"""
        print("🚨 HAL CRITICAL VIOLATION DETECTED")
        print("📋 Immediate action required:")
        print("  • Reduce conversation context")
        print("  • Clear unnecessary history")
        print("  • Use more concise prompts")

        # Log violation
        self._log_violation("CRITICAL", output)

    def _handle_warning(self, output: str):
        """Handle token warnings"""
        print("⚠️  HAL WARNING - Approaching limits")
        self._log_violation("WARNING", output)

    def _log_violation(self, level: str, output: str):
        """Log violation for tracking"""
        try:
            log_file = PROJECT_ROOT / ".claude" / "hal_violations.log"
            with open(log_file, 'a') as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {level}\n")
                f.write(f"{output}\n")
                f.write("-" * 50 + "\n")
        except Exception:
            pass  # Silently fail logging

    def start_monitoring(self):
        """Start continuous HAL monitoring"""
        print("🤖 HAL Enforcement Hook Started")
        print(f"🔍 Monitoring interval: {self.enforcement_interval}s")
        print("🛡️  Token protection: ACTIVE")

        try:
            while self.session_active:
                self.check_and_enforce()
                time.sleep(self.enforcement_interval)
        except KeyboardInterrupt:
            print("\n🛑 HAL enforcement stopped")

    def run_immediate_check(self):
        """Run immediate HAL check"""
        self.check_and_enforce()

    def generate_status_report(self) -> dict:
        """Generate current HAL status report"""
        try:
            result = subprocess.run(
                [sys.executable, str(self.hal_script), "--report"],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT
            )

            if result.returncode == 0:
                return {
                    'status': 'operational',
                    'report': result.stdout,
                    'violations': self.violation_count,
                    'last_check': self.last_check
                }
            else:
                return {
                    'status': 'error',
                    'error': result.stderr,
                    'violations': self.violation_count
                }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'violations': self.violation_count
            }


def main():
    """Command line interface for HAL enforcement hook"""
    import argparse

    hook = HALEnforcementHook()

    parser = argparse.ArgumentParser(description="HAL Enforcement Hook")
    parser.add_argument("--monitor", action="store_true", help="Start continuous monitoring")
    parser.add_argument("--check", action="store_true", help="Run immediate check")
    parser.add_argument("--status", action="store_true", help="Show HAL status")

    args = parser.parse_args()

    if args.monitor:
        hook.start_monitoring()
    elif args.check:
        hook.run_immediate_check()
        print("✅ HAL check completed")
    elif args.status:
        status = hook.generate_status_report()
        print("📊 HAL Status:")
        print(f"  Status: {status['status'].upper()}")
        print(f"  Violations: {status['violations']}")

        if 'report' in status:
            print(f"  Report:\n{status['report']}")
        elif 'error' in status:
            print(f"  Error: {status['error']}")
    else:
        # Default: run immediate check
        hook.run_immediate_check()


if __name__ == "__main__":
    main()