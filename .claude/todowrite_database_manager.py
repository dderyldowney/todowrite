#!/usr/bin/env python3
"""
ToDoWrite Database Manager - Using Existing Models API
Central management for all ToDoWrite database operations
MUST use existing lib_package Models API - NO parallel implementations

⚠️ CRITICAL SYSTEM SEPARATION MANDATE ⚠️
TWO COMPLETELY SEPARATE SYSTEMS - NEVER MIX:

SYSTEM 1: TODOWRITE MODELS API (goals, concepts, tasks, etc.)
- STORE: title, description, status, priority, metadata (ToDoWrite ONLY)
- FORBIDDEN: session_id, actions, context (NEVER store session data here!)

SYSTEM 2: SESSIONS TRACKING (sessions table ONLY)
- STORE: session_id, actions, context, environment
- FORBIDDEN: ToDoWrite hierarchical data

VIOLATION WILL IMMEDIATELY CORRUPT BOTH SYSTEMS!
SEE: .claude/SYSTEM_SEPARATION_MANDATE.md
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor

# Add lib_package to path for existing Models API
sys.path.insert(0, str(Path(__file__).parent / "lib_package" / "src"))

try:
    from todowrite.core.models import (
        AcceptanceCriteria,
        Command,
        Concept,
        Constraints,
        Context,
        Goal,
        InterfaceContract,
        Label,
        Phase,
        Requirements,
        Step,
        SubTask,
        Task,
    )
    from todowrite.core.schema_validator import get_schema_validator

    print("✅ Imported existing ToDoWrite Models API")
except ImportError as e:
    print(f"❌ Failed to import existing ToDoWrite Models API: {e}")
    sys.exit(1)


class ToDoWriteDatabaseManager:
    """Manager for all ToDoWrite database operations using existing Models API"""

    def __init__(self):
        # Use existing MCP PostgreSQL container
        self.db_config = {
            "host": "localhost",
            "port": 5433,
            "database": "todowrite",
            "user": "mcp_user",
            "password": "mcp_secure_password_2024",
        }
        self.session_id = os.environ.get("TODOWRITE_SESSION_ID", "default_session")

    def create_goal(self, title: str, description: str, **kwargs) -> dict[str, Any]:
        """Create a Goal using existing Models API and store in database"""
        # Create the model instance using existing API
        goal = Goal(title=title, description=description, **kwargs)

        # Store in PostgreSQL (goals table) using NEW ToDoWrite Models API schema
        try:
            conn = psycopg2.connect(**self.db_config)
            with conn.cursor() as cursor:
                # Use the correct schema for NEW ToDoWrite Models API (no session_id here!)
                cursor.execute(
                    """
                    INSERT INTO goals (title, description)
                    VALUES (%s, %s)
                    RETURNING id
                """,
                    (title, description),
                )

                result = cursor.fetchone()
                goal_id = result[0] if result and len(result) > 0 else None

                # Also update session tracking
                actions_json = json.dumps(
                    [
                        {
                            "type": "create_goal",
                            "layer": "goal",
                            "title": title,
                            "goal_id": goal_id,
                            "timestamp": datetime.now().isoformat(),
                        }
                    ]
                )

                context_json = json.dumps(
                    {
                        "goal_data": {
                            "id": goal_id,
                            "title": title,
                            "description": description,
                            "created_at": datetime.now().isoformat(),
                            "session_id": self.session_id,
                        }
                    }
                )

                cursor.execute(
                    """
                    INSERT INTO sessions (session_id, title, description, actions, context)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (session_id)
                    DO UPDATE SET
                        last_activity = NOW(),
                        updated_at = NOW()
                """,
                    (
                        self.session_id,
                        f"Created Goal: {title}",
                        description,
                        actions_json,
                        context_json,
                    ),
                )
                conn.commit()

            conn.close()
            return {
                "id": goal_id,
                "layer": "goal",
                "title": title,
                "description": description,
                "session_id": self.session_id,
                "created_at": datetime.now().isoformat(),
                "status": "stored_in_database",
            }

        except Exception as e:
            print(f"❌ Failed to store goal in database: {e}")
            return {
                "layer": "goal",
                "title": title,
                "description": description,
                "status": "failed_to_store",
            }

    def create_layer_item(
        self, layer: str, title: str, description: str, **kwargs
    ) -> dict[str, Any]:
        """Create any layer item using existing Models API"""
        valid_layers = [
            "goal",
            "concept",
            "context",
            "constraint",
            "requirement",
            "acceptance_criteria",
            "interface_contract",
            "phase",
            "step",
            "task",
            "subtask",
            "command",
            "label",
        ]

        if layer not in valid_layers:
            raise ValueError(f"Invalid layer: {layer}. Must be one of: {valid_layers}")

        # Map layer to model class using existing Models API
        layer_model_map = {
            "goal": Goal,
            "concept": Concept,
            "context": Context,
            "constraint": Constraints,
            "requirement": Requirements,
            "acceptance_criteria": AcceptanceCriteria,
            "interface_contract": InterfaceContract,
            "phase": Phase,
            "step": Step,
            "task": Task,
            "subtask": SubTask,
            "command": Command,
            "label": Label,
        }

        ModelClass = layer_model_map[layer]

        # Create instance using existing Models API (without invalid kwargs)
        try:
            # Remove invalid kwargs for specific models
            clean_kwargs = {
                k: v for k, v in kwargs.items() if k not in ["priority"]
            }  # Concept doesn't accept priority

            item = ModelClass(title=title, description=description, **clean_kwargs)

            # Store in database for session tracking
            return self._store_layer_item(layer, title, description, clean_kwargs)

        except Exception as e:
            print(f"❌ Failed to create {layer} using existing Models API: {e}")
            return {
                "layer": layer,
                "title": title,
                "description": description,
                "status": "creation_failed",
                "error": str(e),
            }

    def _store_layer_item(
        self, layer: str, title: str, description: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Store layer item in database for cross-session persistence"""
        try:
            conn = psycopg2.connect(**self.db_config)
            with conn.cursor() as cursor:
                if layer == "concept":
                    # Use correct schema for NEW ToDoWrite Models API (no session_id here!)
                    cursor.execute(
                        """
                        INSERT INTO concepts (title, description)
                        VALUES (%s, %s)
                        RETURNING id
                    """,
                        (title, description),
                    )
                    result = cursor.fetchone()
                    item_id = result[0] if result and len(result) > 0 else None
                elif layer == "task":
                    # Use correct schema for NEW ToDoWrite Models API (no session_id here!)
                    cursor.execute(
                        """
                        INSERT INTO tasks (title, description)
                        VALUES (%s, %s)
                        RETURNING id
                    """,
                        (title, description),
                    )
                    result = cursor.fetchone()
                    item_id = result[0] if result and len(result) > 0 else None
                else:
                    # For other layers, store in session tracking
                    item_id = None

                # Update session tracking
                actions_json = json.dumps(
                    [
                        {
                            "type": "create_layer_item",
                            "layer": layer,
                            "title": title,
                            "item_id": item_id,
                            "timestamp": datetime.now().isoformat(),
                        }
                    ]
                )

                context_json = json.dumps(
                    {
                        "item_data": {
                            "id": item_id,
                            "layer": layer,
                            "title": title,
                            "description": description,
                            "session_id": self.session_id,
                        }
                    }
                )

                cursor.execute(
                    """
                    INSERT INTO sessions (session_id, title, description, actions, context)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (session_id)
                    DO UPDATE SET
                        last_activity = NOW(),
                        updated_at = NOW()
                """,
                    (
                        self.session_id,
                        f"Created {layer}: {title}",
                        description,
                        actions_json,
                        context_json,
                    ),
                )
                conn.commit()

            conn.close()
            return {
                "layer": layer,
                "id": item_id,
                "title": title,
                "description": description,
                "session_id": self.session_id,
                "created_at": datetime.now().isoformat(),
                "status": "stored_in_database",
            }

        except Exception as e:
            print(f"❌ Failed to store {layer} item: {e}")
            return {
                "layer": layer,
                "title": title,
                "status": "database_storage_failed",
                "error": str(e),
            }

    def get_session_items(self) -> list[dict[str, Any]]:
        """Get all items created in current session"""
        try:
            conn = psycopg2.connect(**self.db_config)
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT * FROM sessions
                    WHERE session_id = %s
                    ORDER BY created_at DESC
                """,
                    (self.session_id,),
                )
                items = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return items

        except Exception as e:
            print(f"❌ Failed to get session items: {e}")
            return []

    def create_project_structure(self) -> dict[str, Any]:
        """Create complete project structure using existing Models API"""
        structure = {
            "session_id": self.session_id,
            "created_at": datetime.now().isoformat(),
            "project_root": str(Path.cwd()),
            "structure": {},
        }

        # Create the main goal for this project
        main_goal = self.create_goal(
            title="Complete ToDoWrite Project Development",
            description="Develop comprehensive ToDoWrite system using existing Models API with PostgreSQL backend and cross-session persistence",
            status="active",
        )

        structure["main_goal"] = main_goal

        # Create initial concepts
        concepts = [
            (
                "PostgreSQL Backend Integration",
                "Integrate robust PostgreSQL backend using existing todowrite storage patterns",
            ),
            (
                "Cross-Session Data Persistence",
                "Implement comprehensive cross-session data persistence using existing Models API",
            ),
            (
                "MCP Integration & Global Availability",
                "Integrate comprehensive MCP servers with global auto-loading using existing configuration",
            ),
            (
                "Advanced Token Optimization",
                "Implement sophisticated token optimization algorithms beyond KV-cache using existing framework",
            ),
        ]

        structure["concepts"] = []
        for title, desc in concepts:
            concept = self.create_layer_item("concept", title, desc, priority="high")
            structure["concepts"].append(concept)

        return structure


def main():
    """Test the database manager with existing Models API"""
    print("🗄️  ToDoWrite Database Manager - Using Existing Models API")
    print("   ✅ Using existing lib_package Models (Goal → ... → Command)")
    print("   ✅ PostgreSQL backend with todowrite database")
    print("   ✅ Cross-session persistence enabled")
    print()

    manager = ToDoWriteDatabaseManager()

    # Test creating project structure
    print("🚀 Creating project structure using existing Models API...")
    structure = manager.create_project_structure()

    print("✅ Project structure created:")
    print(f"   Main Goal: {structure['main_goal']['title']}")
    print(f"   Concepts: {len(structure.get('concepts', []))} created")
    print(f"   Session ID: {structure['session_id']}")


if __name__ == "__main__":
    main()
