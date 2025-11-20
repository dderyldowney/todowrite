"""FastAPI backend for ToDoWrite web application."""

import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Import ToDoWrite models using the modern API
from todowrite import (
    Goal,
    Task,
    Concept,
    Context,
    Constraints,
    Requirements,
    AcceptanceCriteria,
    InterfaceContract,
    Phase,
    Step,
    SubTask,
    Command,
    Label,
)

# Database configuration - PostgreSQL required for web application
DATABASE_URL = os.environ.get("TODOWRITE_DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("TODOWRITE_DATABASE_URL environment variable must be set for PostgreSQL")

if not DATABASE_URL.startswith("postgresql://"):
    raise ValueError("Web application requires PostgreSQL database. Please set TODOWRITE_DATABASE_URL to a PostgreSQL connection string.")

# Create PostgreSQL engine with optimized settings
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=False,  # Set to True for SQL debugging in development
)
SessionLocal = sessionmaker(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    yield
    # Shutdown
    engine.dispose()


# FastAPI application with CORS support for React frontend
app = FastAPI(
    title="ToDoWrite Web API",
    description="Modern REST API for hierarchical task management",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include hierarchy API for drag-and-drop functionality
# app.include_router(hierarchy_router)


def get_database_session() -> Session:
    """Dependency for database session."""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


# Pydantic models for API request/response
from pydantic import BaseModel
from typing import Optional, List

# Import hierarchy API for drag-and-drop functionality
# from todowrite_web.api.hierarchy import router as hierarchy_router


class ItemBase(BaseModel):
    """Base model for all ToDoWrite items."""
    title: str
    description: Optional[str] = None
    owner: Optional[str] = None
    severity: Optional[str] = None
    status: str = "planned"
    progress: int = 0


class ItemCreate(ItemBase):
    """Model for creating new items."""
    layer: str


class ItemResponse(ItemBase):
    """Model for item responses."""
    id: int
    layer: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# API endpoints
@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "ToDoWrite Web API - Modern hierarchical task management"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "todowrite-web-api"}


@app.get("/api/items")
async def list_items(
    layer: Optional[str] = None,
    owner: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 20,
    db: Session = Depends(get_database_session),
) -> List[ItemResponse]:
    """List ToDoWrite items with optional filtering."""
    model_map = {
        "goal": Goal,
        "task": Task,
        "concept": Concept,
        "context": Context,
        "constraints": Constraints,
        "requirements": Requirements,
        "acceptancecriteria": AcceptanceCriteria,
        "interfacecontract": InterfaceContract,
        "phase": Phase,
        "step": Step,
        "subtask": SubTask,
        "command": Command,
        "label": Label,
    }

    if layer and layer.lower() not in model_map:
        raise HTTPException(status_code=400, detail=f"Unknown layer: {layer}")

    items = []
    models_to_query = [model_map.get(layer.lower())] if layer else list(model_map.values())

    for model_class in models_to_query:
        if not model_class:
            continue

        query = db.query(model_class)

        # Apply filters
        if owner:
            query = query.filter(model_class.owner == owner)
        if status:
            query = query.filter(model_class.status == status)

        results = query.limit(limit).all()

        for item in results:
            items.append(
                ItemResponse(
                    id=item.id,
                    layer=model_class.__name__.lower(),
                    title=getattr(item, "title", getattr(item, "name", "No title")),
                    description=getattr(item, "description", None),
                    owner=getattr(item, "owner", None),
                    severity=getattr(item, "severity", None),
                    status=getattr(item, "status", "unknown"),
                    progress=getattr(item, "progress", 0),
                    created_at=str(getattr(item, "created_at", "")),
                    updated_at=str(getattr(item, "updated_at", "")),
                )
            )

    return items


@app.get("/api/items/{item_id}")
async def get_item(
    item_id: int,
    db: Session = Depends(get_database_session),
) -> ItemResponse:
    """Get a specific item by ID."""
    model_classes = [
        Goal,
        Task,
        Concept,
        Context,
        Constraints,
        Requirements,
        AcceptanceCriteria,
        InterfaceContract,
        Phase,
        Step,
        SubTask,
        Command,
        Label,
    ]

    for model_class in model_classes:
        item = db.query(model_class).filter(model_class.id == item_id).first()
        if item:
            return ItemResponse(
                id=item.id,
                layer=model_class.__name__.lower(),
                title=getattr(item, "title", getattr(item, "name", "No title")),
                description=getattr(item, "description", None),
                owner=getattr(item, "owner", None),
                severity=getattr(item, "severity", None),
                status=getattr(item, "status", "unknown"),
                progress=getattr(item, "progress", 0),
                created_at=str(getattr(item, "created_at", "")),
                updated_at=str(getattr(item, "updated_at", "")),
            )

    raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")


@app.post("/api/items")
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_database_session),
) -> ItemResponse:
    """Create a new item."""
    model_map = {
        "goal": Goal,
        "task": Task,
        "concept": Concept,
        "context": Context,
        "constraints": Constraints,
        "requirements": Requirements,
        "acceptancecriteria": AcceptanceCriteria,
        "interfacecontract": InterfaceContract,
        "phase": Phase,
        "step": Step,
        "subtask": SubTask,
        "command": Command,
        "label": Label,
    }

    layer_lower = item.layer.lower()
    if layer_lower not in model_map:
        raise HTTPException(status_code=400, detail=f"Unknown layer: {item.layer}")

    model_class = model_map[layer_lower]

    # Create the item using the modern ToDoWrite Models API
    db_item = model_class(
        title=item.title,
        description=item.description,
        owner=item.owner,
        severity=item.severity,
        status=item.status,
        progress=item.progress,
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return ItemResponse(
        id=db_item.id,
        layer=item.layer,
        title=db_item.title,
        description=db_item.description,
        owner=db_item.owner,
        severity=db_item.severity,
        status=db_item.status,
        progress=db_item.progress,
        created_at=str(db_item.created_at),
        updated_at=str(db_item.updated_at),
    )


@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_database_session)) -> dict[str, int]:
    """Get database statistics."""
    model_map = {
        "goals": Goal,
        "tasks": Task,
        "concepts": Concept,
        "contexts": Context,
        "constraints": Constraints,
        "requirements": Requirements,
        "acceptance_criteria": AcceptanceCriteria,
        "interface_contracts": InterfaceContract,
        "phases": Phase,
        "steps": Step,
        "sub_tasks": SubTask,
        "commands": Command,
        "labels": Label,
    }

    stats = {}
    total = 0

    for name, model_class in model_map.items():
        count = db.query(model_class).count()
        stats[name] = count
        total += count

    stats["total"] = total
    return stats


if __name__ == "__main__":
    uvicorn.run(
        "todowrite_web.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )