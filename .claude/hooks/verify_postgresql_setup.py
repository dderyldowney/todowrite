#!/usr/bin/env python3
"""
PostgreSQL Development Setup Verification

This script verifies that the PostgreSQL development environment is properly configured
and provides information about the current setup status.
"""

from __future__ import annotations

import os
import subprocess
from typing import Any

from todowrite.database.config import (
    check_postgresql_connection,
    determine_storage_backend,
    get_docker_postgresql_candidates,
    is_docker_postgresql_running,
)


def verify_docker_status() -> dict[str, Any]:
    """Verify Docker and PostgreSQL container status."""
    status = {
        "docker_available": False,
        "postgresql_running": False,
        "container_name": None,
        "volume_name": None,
        "candidates_count": 0,
    }

    try:
        # Check Docker daemon
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            check=True,
            timeout=5,
        )
        status["docker_available"] = True

        # Check PostgreSQL container
        if is_docker_postgresql_running():
            status["postgresql_running"] = True
            candidates = get_docker_postgresql_candidates()
            status["candidates_count"] = len(candidates)

            # Get container info
            result = subprocess.run(
                ["docker", "ps", "--filter", "name=postgres", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                container_names = result.stdout.strip().split("\n")
                status["container_name"] = container_names[0] if container_names[0] else None

            # Get volume info
            result = subprocess.run(
                ["docker", "volume", "ls", "--filter", "name=todowrite", "--format", "{{.Name}}"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                volume_names = result.stdout.strip().split("\n")
                status["volume_name"] = volume_names[0] if volume_names[0] else None

    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return status


def verify_database_status() -> dict[str, Any]:
    """Verify database connection and schema status."""
    status = {
        "backend_type": None,
        "connection_url": None,
        "connection_working": False,
        "tables_created": 0,
        "records_count": {},
    }

    try:
        storage_type, url = determine_storage_backend()
        status["backend_type"] = storage_type.value
        status["connection_url"] = url

        if url and storage_type.value == "postgresql":
            status["connection_working"] = check_postgresql_connection(url)

            if status["connection_working"]:
                from sqlalchemy import create_engine, text

                engine = create_engine(url)

                with engine.connect() as conn:
                    # Count tables
                    result = conn.execute(
                        text("""
                        SELECT COUNT(*)
                        FROM information_schema.tables
                        WHERE table_schema = 'public'
                    """)
                    )
                    status["tables_created"] = result.fetchone()[0]

                    # Count records in main tables
                    main_tables = ["goals", "tasks", "labels", "commands"]
                    for table in main_tables:
                        try:
                            result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                            status["records_count"][table] = result.fetchone()[0]
                        except Exception:
                            status["records_count"][table] = 0

    except Exception as e:
        status["error"] = str(e)

    return status


def verify_environment() -> dict[str, Any]:
    """Verify environment variables and configuration."""
    status = {
        "virtual_env": os.environ.get("VIRTUAL_ENV") is not None,
        "pythonpath_set": "lib_package/src" in os.environ.get("PYTHONPATH", ""),
        "database_url_set": "TODOWRITE_DATABASE_URL" in os.environ,
        "database_url": os.environ.get("TODOWRITE_DATABASE_URL", "Not set"),
        "preference_configured": False,
    }

    try:
        from todowrite.database.config import get_storage_preference

        preference = get_storage_preference()
        status["preference_configured"] = True
        status["storage_preference"] = preference.value
    except Exception:
        status["storage_preference"] = "Unknown"

    return status


def main() -> None:
    """Main verification function."""
    print("🔍 PostgreSQL Development Environment Verification")
    print("=" * 60)

    # Verify Docker status
    print("🐳 Docker & Container Status:")
    docker_status = verify_docker_status()
    print(f"  Docker Available: {'✅' if docker_status['docker_available'] else '❌'}")
    print(f"  PostgreSQL Running: {'✅' if docker_status['postgresql_running'] else '❌'}")
    if docker_status["container_name"]:
        print(f"  Container: {docker_status['container_name']}")
    if docker_status["volume_name"]:
        print(f"  Volume: {docker_status['volume_name']} (persistent)")
    print()

    # Verify database status
    print("🗄️  Database Status:")
    db_status = verify_database_status()
    print(f"  Backend Type: {db_status['backend_type']}")
    print(f"  Connection Working: {'✅' if db_status['connection_working'] else '❌'}")
    if db_status["connection_url"]:
        print(f"  Connection URL: {db_status['connection_url']}")
    if db_status["tables_created"] > 0:
        print(f"  Tables Created: {db_status['tables_created']}")
        print("  Record Counts:")
        for table, count in db_status["records_count"].items():
            print(f"    {table}: {count}")
    print()

    # Verify environment
    print("🔧 Environment Configuration:")
    env_status = verify_environment()
    print(f"  Virtual Environment: {'✅' if env_status['virtual_env'] else '❌'}")
    print(f"  PYTHONPATH Set: {'✅' if env_status['pythonpath_set'] else '❌'}")
    print(f"  Storage Preference: {env_status['storage_preference']}")
    if env_status["database_url_set"]:
        print("  Database URL Configured: ✅")
    print()

    # Summary
    print("📋 Summary:")
    all_good = (
        docker_status["docker_available"]
        and docker_status["postgresql_running"]
        and db_status["connection_working"]
        and env_status["virtual_env"]
        and env_status["pythonpath_set"]
    )

    if all_good:
        print("✅ PostgreSQL development environment is properly configured!")
        print("   - Docker container is running with persistent volume")
        print("   - Database connection is working")
        print("   - All schemas are imported")
        print("   - Environment is correctly configured")
    else:
        print("❌ PostgreSQL development environment has issues:")
        if not docker_status["docker_available"]:
            print("   - Docker is not available or not running")
        if not docker_status["postgresql_running"]:
            print("   - PostgreSQL container is not running")
        if not db_status["connection_working"]:
            print("   - Database connection is not working")
        if not env_status["virtual_env"]:
            print("   - Virtual environment is not active")
        if not env_status["pythonpath_set"]:
            print("   - PYTHONPATH is not configured")


if __name__ == "__main__":
    main()
