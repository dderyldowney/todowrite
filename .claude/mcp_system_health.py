#!/usr/bin/env python3
"""
MCP System Health Check - Complete System Analysis
Combines Gateway health check and Tools validation for complete MCP system status

This is the main health check script that provides:
1. Docker MCP Gateway connectivity analysis
2. STDIO server communication status
3. Actual tool functionality testing
4. Comprehensive system recommendations
"""

import subprocess
import sys
from pathlib import Path


def run_gateway_health_check() -> dict:
    """Run the MCP Gateway health check"""
    try:
        result = subprocess.run(
            ["python", str(Path(__file__).parent / "mcp_gateway_health_check.py")],
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Parse exit code to determine success
        gateway_success = result.returncode == 0

        # Extract key information from output
        lines = result.stdout.split("\n")
        status_line = next((line for line in lines if "Status:" in line), "")
        servers_line = next((line for line in lines if "Servers:" in line), "")
        tools_line = next((line for line in lines if "Tools Detected:" in line), "")

        return {
            "success": gateway_success,
            "status": status_line.split("Status:")[1].strip()
            if "Status:" in status_line
            else "unknown",
            "servers_info": servers_line.strip() if servers_line else "unknown",
            "tools_detected": tools_line.split("Tools Detected:")[1].strip()
            if "Tools Detected:" in tools_line
            else "unknown",
            "output": result.stdout,
        }

    except Exception as e:
        return {
            "success": False,
            "status": "error",
            "servers_info": "error",
            "tools_detected": "error",
            "output": str(e),
        }


def run_tools_validation() -> dict:
    """Run the MCP tools validation"""
    try:
        result = subprocess.run(
            ["python", str(Path(__file__).parent / "mcp_tools_validator.py"), "--quick"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Parse exit code and output
        tools_success = result.returncode == 0

        # Extract tool status
        lines = result.stdout.split("\n")
        git_status = "unknown"
        db_status = "unknown"

        for line in lines:
            if line.startswith("Git:"):
                git_status = "✅" if "✅" in line else "❌"
            elif line.startswith("Database:"):
                db_status = "✅" if "✅" in line else "❌"

        return {
            "success": tools_success,
            "git_status": git_status,
            "db_status": db_status,
            "output": result.stdout,
        }

    except Exception as e:
        return {"success": False, "git_status": "❌", "db_status": "❌", "output": str(e)}


def print_system_status():
    """Print comprehensive system status"""
    print("🚀 MCP SYSTEM HEALTH CHECK")
    print("=" * 60)

    # Run Gateway health check
    print("📡 Checking MCP Gateway & STDIO Servers...")
    gateway_result = run_gateway_health_check()

    if gateway_result["success"]:
        print("✅ Gateway health check completed")
        print(f"   Status: {gateway_result['status']}")
        print(f"   Servers: {gateway_result['servers_info']}")
        print(f"   Tools: {gateway_result['tools_detected']}")
    else:
        print("❌ Gateway health check failed")
        print(f"   Error: {gateway_result['output']}")

    print()

    # Run tools validation
    print("🛠️  Validating Available Tools...")
    tools_result = run_tools_validation()

    if tools_result["success"]:
        print("✅ Tools validation completed")
        print(f"   Git: {tools_result['git_status']}")
        print(f"   Database: {tools_result['db_status']}")
    else:
        print("❌ Tools validation failed")
        print(f"   Error: {tools_result['output']}")

    print()

    # Overall assessment
    gateway_ok = gateway_result["success"] and gateway_result["status"] in ["HEALTHY", "DEGRADED"]
    tools_ok = tools_result["success"]

    print("📊 OVERALL SYSTEM STATUS:")
    if gateway_ok and tools_ok:
        print("✅ MCP System is OPERATIONAL")
        print("   - Some MCP servers may need Gateway configuration")
        print("   - Core tools are available and functional")
        exit_code = 0
    elif tools_ok:
        print("⚠️  MCP System is PARTIALLY OPERATIONAL")
        print("   - Core tools available via built-ins")
        print("   - MCP Gateway servers need configuration")
        exit_code = 0
    else:
        print("❌ MCP System has ISSUES")
        print("   - Multiple components require attention")
        exit_code = 1

    print("\n🔧 RECOMMENDATIONS:")
    if not gateway_ok:
        print("- Configure MCP Gateway client for STDIO server communication")
        print("- Check Docker MCP Gateway container status")
        print("- Restart failing MCP containers")

    if gateway_result["status"] == "DEGRADED":
        print("- STDIO servers are restarting (waiting for Gateway client)")
        print("- This is expected behavior without Gateway configuration")

    if tools_ok:
        print("- ✅ Development can proceed with available tools")
        print("- MCP Gateway configuration will enhance capabilities")
    else:
        print("- Check basic system connectivity")
        print("- Verify Docker and database containers")

    print("\n📄 Detailed reports available:")
    print(f"   - Gateway: {Path(__file__).parent / 'mcp_gateway_health_report.md'}")
    print(f"   - Tools: {Path(__file__).parent / 'mcp_tools_validation_report.md'}")

    return exit_code


def main():
    """Main health check function"""
    import argparse

    parser = argparse.ArgumentParser(description="MCP System Health Check")
    parser.add_argument("--gateway-only", action="store_true", help="Run only Gateway health check")
    parser.add_argument("--tools-only", action="store_true", help="Run only tools validation")
    parser.add_argument("--reports", action="store_true", help="Generate detailed reports")

    args = parser.parse_args()

    if args.gateway_only:
        result = run_gateway_health_check()
        print(result["output"])
        sys.exit(0 if result["success"] else 1)
    elif args.tools_only:
        result = run_tools_validation()
        print(result["output"])
        sys.exit(0 if result["success"] else 1)
    elif args.reports:
        # Generate detailed reports
        print("📄 Generating detailed MCP system reports...")

        # Gateway report
        subprocess.run(
            ["python", str(Path(__file__).parent / "mcp_gateway_health_check.py"), "--report"]
        )

        # Tools report
        subprocess.run(
            ["python", str(Path(__file__).parent / "mcp_tools_validator.py"), "--report"]
        )

        print("✅ Reports generated successfully")
        sys.exit(0)
    else:
        # Run complete system health check
        exit_code = print_system_status()
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
