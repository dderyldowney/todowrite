#!/usr/bin/env python3
"""
MCP Server Health Check and Startup Wait
Ensures all MCP servers are available before proceeding with development
"""

import subprocess
import time


class MCPServerHealthChecker:
    """Check health and availability of MCP servers"""

    def __init__(self):
        self.mcp_servers = {
            "context7": {"port": 3001, "health_endpoint": "/health"},
            "filesystem": {"port": 3002, "health_endpoint": "/health"},
            "git-server": {"port": 3003, "health_endpoint": "/health"},
            "github-server": {"port": 3004, "health_endpoint": "/health"},
            "playwright": {"port": 3005, "health_endpoint": "/health"},
            "sqlite-server": {"port": 3006, "health_endpoint": "/health"},
            "rust-filesystem": {"port": 3007, "health_endpoint": "/health"},
            "python-refactoring": {"port": 3008, "health_endpoint": "/health"},
        }
        self.max_wait_time = 120  # 2 minutes
        self.check_interval = 5  # 5 seconds

    def check_docker_container(self, service_name: str) -> bool:
        """Check if Docker container is running"""
        container_name = f"mcp-{service_name}"
        try:
            result = subprocess.run(
                [
                    "docker",
                    "ps",
                    "--filter",
                    f"name={container_name}",
                    "--filter",
                    "status=running",
                    "--quiet",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return bool(result.stdout.strip())
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            return False

    def check_port_availability(self, port: int) -> bool:
        """Check if port is open and service is responding"""
        try:
            import socket

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex(("localhost", port))
            sock.close()
            return result == 0
        except OSError:
            return False

    def check_mcp_server_tools(self, service_name: str) -> dict | None:
        """Try to query MCP server for its tools list"""
        try:
            # This would require actual MCP protocol implementation
            # For now, just check if the container is running and port is open
            container_running = self.check_docker_container(service_name)
            if not container_running:
                return {"status": "error", "message": f"Container {service_name} not running"}

            server_info = self.mcp_servers[service_name]
            port_open = self.check_port_availability(server_info["port"])
            if not port_open:
                return {"status": "error", "message": f"Port {server_info['port']} not accessible"}

            return {"status": "healthy", "message": f"{service_name} is responding"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def wait_for_all_servers(self) -> dict[str, dict]:
        """Wait for all MCP servers to be healthy"""
        print("🔍 Waiting for MCP servers to be available...")
        results = {}
        start_time = time.time()

        while time.time() - start_time < self.max_wait_time:
            all_healthy = True
            pending_servers = []

            for service_name in self.mcp_servers:
                if service_name not in results or results[service_name]["status"] != "healthy":
                    health = self.check_mcp_server_tools(service_name)
                    results[service_name] = health

                    if health["status"] == "healthy":
                        print(f"✅ {service_name}: {health['message']}")
                    else:
                        all_healthy = False
                        pending_servers.append(service_name)
                        if service_name not in results:
                            print(f"⏳ {service_name}: {health['message']}")

            if all_healthy:
                print(f"✅ All {len(self.mcp_servers)} MCP servers are healthy!")
                break

            if pending_servers:
                remaining_time = self.max_wait_time - (time.time() - start_time)
                print(
                    f"⏳ Waiting for {len(pending_servers)} servers... ({int(remaining_time)}s remaining)"
                )
                time.sleep(self.check_interval)

        return results

    def generate_health_report(self, results: dict[str, dict]) -> str:
        """Generate a health report of all MCP servers"""
        healthy_count = sum(1 for r in results.values() if r["status"] == "healthy")
        total_count = len(self.mcp_servers)

        report = f"""
# MCP Server Health Report
Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}

## Summary
- Healthy Servers: {healthy_count}/{total_count}
- Health Rate: {(healthy_count / total_count) * 100:.1f}%

## Server Status
"""

        for service_name, health in results.items():
            status_icon = "✅" if health["status"] == "healthy" else "❌"
            report += f"- {status_icon} **{service_name}**: {health['message']}\n"

        report += "\n## Service Endpoints\n"
        for service_name, config in self.mcp_servers.items():
            report += f"- {service_name}: http://localhost:{config['port']}\n"

        return report


def wait_for_mcp_servers() -> bool:
    """Wait for MCP servers and return True if all healthy"""
    checker = MCPServerHealthChecker()
    results = checker.wait_for_all_servers()

    healthy_count = sum(1 for r in results.values() if r["status"] == "healthy")
    total_count = len(checker.mcp_servers)

    if healthy_count == total_count:
        print("✅ All MCP servers are ready!")
        return True
    else:
        print(f"⚠️  Only {healthy_count}/{total_count} MCP servers are healthy")
        print("\n" + checker.generate_health_report(results))
        return False


if __name__ == "__main__":
    success = wait_for_mcp_servers()
    exit(0 if success else 1)
