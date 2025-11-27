"""
Enumerated types for ToDoWrite models.

This module defines the Python enums that correspond to the database ENUM types.
These provide type safety and ensure only valid values are used throughout the application.
"""

from __future__ import annotations

from enum import StrEnum


class StatusEnum(StrEnum):
    """Enum for status values."""

    PLANNED = "planned"
    PENDING = "pending"
    ACTIVE = "active"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"


class SeverityEnum(StrEnum):
    """Enum for severity values."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class WorkTypeEnum(StrEnum):
    """Enum for work type values."""

    FRONTEND = "frontend"
    BACKEND = "backend"
    FULL_STACK = "full-stack"
    DEVOPS = "devops"
    DATABASE = "database"
    SECURITY = "security"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    ARCHITECTURE = "architecture"
    PAYMENT = "payment"
    UI_UX = "ui_ux"
    DESIGN = "design"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    PLANNING = "planning"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"
