"""
FastAPI Main Application for ToDoWrite Web Interface

This is the main entry point for the ToDoWrite web backend.
"""

from __future__ import annotations


from fastapi import FastAPI

app: FastAPI = FastAPI(
    title="ToDoWrite Web API",
    description="Web API for ToDoWrite hierarchical task management system",
    version="0.1.0",
)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint for health check."""
    return {"message": "ToDoWrite Web API is running"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "todowrite-web"}
