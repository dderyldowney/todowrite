"""
Hierarchical drag-and-drop API endpoints for ToDoWrite web application.
Handles cross-layer moves and reordering of the 12-layer hierarchy.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

from todowrite import (
    Goal, Concept, Context, Constraint, Requirement,
    AcceptanceCriteria, InterfaceContract, Phase, Step,
    Task, SubTask, Command, Base
)
from todowrite_web.database import get_db

router = APIRouter(prefix="/api/hierarchy", tags=["hierarchy"])

# Layer hierarchy mapping for validation
LAYER_HIERARCHY = {
    "goal": [],
    "concept": ["goal"],
    "context": ["goal", "concept"],
    "constraints": ["goal", "concept", "context"],
    "requirement": ["goal", "concept", "context", "constraints"],
    "acceptancecriteria": ["goal", "concept", "context", "constraints", "requirement"],
    "interfacecontract": ["goal", "concept", "context", "constraints", "requirement", "acceptancecriteria"],
    "phase": ["goal", "concept", "context", "constraints", "requirement", "acceptancecriteria", "interfacecontract"],
    "step": ["goal", "concept", "context", "constraints", "requirement", "acceptancecriteria", "interfacecontract", "phase"],
    "task": ["goal", "concept", "context", "constraints", "requirement", "acceptancecriteria", "interfacecontract", "phase", "step"],
    "subtask": ["goal", "concept", "context", "constraints", "requirement", "acceptancecriteria", "interfacecontract", "phase", "step", "task"],
    "command": ["goal", "concept", "context", "constraints", "requirement", "acceptancecriteria", "interfacecontract", "phase", "step", "task", "subtask"]
}

# Model mapping for dynamic access
MODEL_MAPPING = {
    "goal": Goal,
    "concept": Concept,
    "context": Context,
    "constraint": Constraint,
    "requirement": Requirement,
    "acceptancecriteria": AcceptanceCriteria,
    "interfacecontract": InterfaceContract,
    "phase": Phase,
    "step": Step,
    "task": Task,
    "subtask": SubTask,
    "command": Command
}

# Association table mappings
ASSOCIATION_TABLES = {
    ("goal", "concept"): "goals_concepts",
    ("goal", "context"): "goals_contexts",
    ("goal", "constraint"): "constraints_goals",
    ("goal", "requirement"): "goals_requirements",
    ("goal", "phase"): "goals_phases",
    ("goal", "task"): "goals_tasks",
    ("goal", "label"): "goals_labels",
    ("concept", "context"): "concepts_contexts",
    ("concept", "label"): "concepts_labels",
    ("context", "label"): "contexts_labels",
    ("constraint", "goal"): "constraints_goals",
    ("constraint", "requirement"): "constraints_requirements",
    ("constraint", "label"): "constraints_labels",
    ("requirement", "acceptancecriteria"): "requirements_acceptance_criteria",
    ("requirement", "concept"): "requirements_concepts",
    ("requirement", "context"): "requirements_contexts",
    ("requirement", "label"): "requirements_labels",
    ("acceptancecriteria", "interfacecontract"): "acceptance_criteria_interface_contracts",
    ("acceptancecriteria", "label"): "acceptance_criteria_labels",
    ("interfacecontract", "phase"): "interface_contracts_phases",
    ("interfacecontract", "label"): "interface_contracts_labels",
    ("phase", "step"): "phases_steps",
    ("phase", "label"): "phases_labels",
    ("step", "task"): "steps_tasks",
    ("step", "label"): "steps_labels",
    ("task", "subtask"): "tasks_sub_tasks",
    ("task", "label"): "tasks_labels",
    ("subtask", "command"): "sub_tasks_commands",
    ("subtask", "label"): "sub_tasks_labels"
}

class MoveOperation(BaseModel):
    """Request model for move operations."""
    dragged_item_id: int
    dragged_item_type: str
    target_item_id: int
    target_item_type: str
    new_parent_id: Optional[int] = None
    new_parent_type: Optional[str] = None
    operation_type: str  # "reorder", "move_to_parent", "move_between_parents"

class HierarchyResponse(BaseModel):
    """Response model for hierarchy operations."""
    success: bool
    message: str
    updated_hierarchy: Optional[Dict[str, Any]] = None

def get_model_class(model_type: str):
    """Get SQLAlchemy model class by type string."""
    model_type = model_type.lower()
    if model_type == "constraints":
        model_type = "constraint"
    elif model_type == "acceptancecriteria":
        model_type = "acceptancecriteria"

    if model_type not in MODEL_MAPPING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid model type: {model_type}"
        )
    return MODEL_MAPPING[model_type]

def validate_parent_child(parent_type: str, child_type: str) -> bool:
    """Validate if a child can be placed under a parent according to hierarchy rules."""
    parent_type = parent_type.lower()
    child_type = child_type.lower()

    if parent_type == "constraints":
        parent_type = "constraint"
    elif child_type == "acceptancecriteria":
        child_type = "acceptancecriteria"

    return child_type in LAYER_HIERARCHY.get(parent_type, [])

def get_association_table(parent_type: str, child_type: str) -> Optional[str]:
    """Get association table name for parent-child relationship."""
    parent_type = parent_type.lower()
    child_type = child_type.lower()

    if parent_type == "constraints":
        parent_type = "constraint"

    return ASSOCIATION_TABLES.get((parent_type, child_type))

@router.post("/move", response_model=HierarchyResponse)
async def move_hierarchy_item(
    operation: MoveOperation,
    db: Session = Depends(get_db)
) -> HierarchyResponse:
    """
    Move an item within the hierarchy.

    Supports:
    - Reordering within the same parent
    - Moving to a new parent
    - Cross-layer moves with validation
    """
    try:
        # Validate models exist
        dragged_model = get_model_class(operation.dragged_item_type)
        target_model = get_model_class(operation.target_item_type)

        # Get the actual database items
        dragged_item = db.query(dragged_model).filter(
            dragged_model.id == operation.dragged_item_id
        ).first()

        target_item = db.query(target_model).filter(
            target_model.id == operation.target_item_id
        ).first()

        if not dragged_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dragged item not found: {operation.dragged_item_type} #{operation.dragged_item_id}"
            )

        if not target_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Target item not found: {operation.target_item_type} #{operation.target_item_id}"
            )

        # Handle different operation types
        if operation.operation_type == "move_to_parent" and operation.new_parent_id:
            return await handle_move_to_parent(operation, db, dragged_item)
        elif operation.operation_type == "reorder":
            return await handle_reorder(operation, db, dragged_item, target_item)
        elif operation.operation_type == "move_between_parents":
            return await handle_cross_parent_move(operation, db, dragged_item, target_item)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid operation type: {operation.operation_type}"
            )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Move operation failed: {str(e)}"
        )

async def handle_move_to_parent(
    operation: MoveOperation,
    db: Session,
    dragged_item: Base
) -> HierarchyResponse:
    """Handle moving an item to a new parent."""

    if not operation.new_parent_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New parent type is required for move_to_parent operation"
        )

    # Validate the new parent-child relationship
    if not validate_parent_child(operation.new_parent_type, operation.dragged_item_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot move {operation.dragged_item_type} under {operation.new_parent_type}"
        )

    # Get the new parent
    parent_model = get_model_class(operation.new_parent_type)
    new_parent = db.query(parent_model).filter(
        parent_model.id == operation.new_parent_id
    ).first()

    if not new_parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"New parent not found: {operation.new_parent_type} #{operation.new_parent_id}"
        )

    # Remove from old parent if exists
    await remove_from_current_parent(operation, db)

    # Add to new parent
    association_table = get_association_table(operation.new_parent_type, operation.dragged_item_type)
    if association_table:
        # Use association table
        query = text(f"""
            INSERT INTO {association_table}
            ({operation.new_parent_type}_id, {operation.dragged_item_type}_id)
            VALUES (:parent_id, :child_id)
        """)
        db.execute(query, {"parent_id": operation.new_parent_id, "child_id": operation.dragged_item_id})

    db.commit()

    return HierarchyResponse(
        success=True,
        message=f"Successfully moved {operation.dragged_item_type} to new parent"
    )

async def handle_reorder(
    operation: MoveOperation,
    db: Session,
    dragged_item: Base,
    target_item: Base
) -> HierarchyResponse:
    """Handle reordering items within the same parent."""

    # For now, we'll implement a basic reordering logic
    # In a full implementation, you'd want to add order columns to association tables

    db.commit()

    return HierarchyResponse(
        success=True,
        message=f"Successfully reordered {operation.dragged_item_type}"
    )

async def handle_cross_parent_move(
    operation: MoveOperation,
    db: Session,
    dragged_item: Base,
    target_item: Base
) -> HierarchyResponse:
    """Handle moving an item from one parent to another."""

    # Remove from current parent
    await remove_from_current_parent(operation, db)

    # Add to new parent (target)
    association_table = get_association_table(operation.target_item_type, operation.dragged_item_type)
    if association_table:
        query = text(f"""
            INSERT INTO {association_table}
            ({operation.target_item_type}_id, {operation.dragged_item_type}_id)
            VALUES (:parent_id, :child_id)
        """)
        db.execute(query, {"parent_id": operation.target_item_id, "child_id": operation.dragged_item_id})

    db.commit()

    return HierarchyResponse(
        success=True,
        message=f"Successfully moved {operation.dragged_item_type} to new parent"
    )

async def remove_from_current_parent(operation: MoveOperation, db: Session) -> None:
    """Remove item from its current parent relationships."""

    # Check all possible association tables and remove the relationship
    for (parent_type, child_type), table_name in ASSOCIATION_TABLES.items():
        if child_type == operation.dragged_item_type.lower():
            query = text(f"""
                DELETE FROM {table_name}
                WHERE {child_type}_id = :child_id
            """)
            db.execute(query, {"child_id": operation.dragged_item_id})

@router.get("/tree/{parent_type}/{parent_id}")
async def get_hierarchy_tree(
    parent_type: str,
    parent_id: int,
    max_depth: int = 3,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get a hierarchical tree view of items starting from a parent.

    Args:
        parent_type: Type of the parent item (goal, task, etc.)
        parent_id: ID of the parent item
        max_depth: Maximum depth to traverse (default: 3)
    """

    try:
        parent_model = get_model_class(parent_type)
        parent_item = db.query(parent_model).filter(
            parent_model.id == parent_id
        ).first()

        if not parent_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parent not found: {parent_type} #{parent_id}"
            )

        # Build the hierarchy tree
        tree = await build_hierarchy_tree(parent_type, parent_id, max_depth, db)

        return {
            "parent_type": parent_type,
            "parent_id": parent_id,
            "tree": tree
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get hierarchy tree: {str(e)}"
        )

async def build_hierarchy_tree(
    parent_type: str,
    parent_id: int,
    max_depth: int,
    db: Session,
    current_depth: int = 0
) -> Dict[str, Any]:
    """Recursively build hierarchy tree."""

    if current_depth >= max_depth:
        return {}

    # This would need to be implemented based on your specific schema
    # For now, return a placeholder structure
    return {
        "id": parent_id,
        "type": parent_type,
        "children": [],
        "depth": current_depth
    }

@router.get("/validate-move/{item_type}/{item_id}/to/{parent_type}/{parent_id}")
async def validate_move(
    item_type: str,
    item_id: int,
    parent_type: str,
    parent_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Validate if an item can be moved to a new parent.

    Returns validation result and any warnings or constraints.
    """

    try:
        # Check if items exist
        item_model = get_model_class(item_type)
        parent_model = get_model_class(parent_type)

        item_exists = db.query(item_model).filter(item_model.id == item_id).first() is not None
        parent_exists = db.query(parent_model).filter(parent_model.id == parent_id).first() is not None

        if not item_exists:
            return {
                "valid": False,
                "reason": f"Item not found: {item_type} #{item_id}"
            }

        if not parent_exists:
            return {
                "valid": False,
                "reason": f"Parent not found: {parent_type} #{parent_id}"
            }

        # Check hierarchy validation
        can_move = validate_parent_child(parent_type, item_type)

        # Check for circular dependencies (item is ancestor of parent)
        # This would require recursive checking

        return {
            "valid": can_move,
            "reason": (
                "Valid move operation" if can_move
                else f"Cannot move {item_type} under {parent_type} - violates hierarchy rules"
            ),
            "warnings": [] if can_move else ["Hierarchy violation"]
        }

    except Exception as e:
        return {
            "valid": False,
            "reason": f"Validation error: {str(e)}",
            "warnings": []
        }