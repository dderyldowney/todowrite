"""
FastAPI main application for ToDoWrite web interface.

This is a minimal FastAPI application that provides the web API for the ToDoWrite system.
"""

from fastapi import FastAPI

from todowrite_web.backend.models import HealthResponse

app = FastAPI(
    title="ToDoWrite API",
    description="API for ToDoWrite task management system",
    version="0.1.0",
)


@app.get("/", response_model=HealthResponse)
async def root() -> HealthResponse:
    """Root endpoint with health check."""
    return HealthResponse(status="healthy", message="ToDoWrite API is running")


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="healthy", message="ToDoWrite API is running")
