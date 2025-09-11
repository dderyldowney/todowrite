"""
Run the Automated Farming System API with Uvicorn.

Usage
-----
- Run with defaults: ``python -m afs_fastapi``
- Custom host/port via env vars:
  - ``AFS_API_HOST`` (default: 127.0.0.1)
  - ``AFS_API_PORT`` (default: 8000)
  - ``AFS_API_RELOAD`` (true/false, default: false)
  - ``AFS_API_LOG_LEVEL`` (debug/info/warning/error, default: info)
"""

from __future__ import annotations

import os
from typing import Literal

import uvicorn


def _env_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "on"}


def main() -> None:
    """Start the FastAPI app using Uvicorn."""
    host = os.getenv("AFS_API_HOST", "127.0.0.1")
    port_str = os.getenv("AFS_API_PORT", "8000")
    reload = _env_bool("AFS_API_RELOAD", False)
    log_level: Literal[
        "critical", "error", "warning", "info", "debug", "trace"
    ] = os.getenv(
        "AFS_API_LOG_LEVEL", "info"
    ).lower()  # type: ignore[assignment]
    try:
        port = int(port_str)
    except ValueError:
        raise SystemExit(f"Invalid AFS_API_PORT value: {port_str!r}")

    uvicorn.run(
        "afs_fastapi.api.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level,
    )


if __name__ == "__main__":
    main()
