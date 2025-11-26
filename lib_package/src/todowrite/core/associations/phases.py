"""
Phase association tables.

This module contains association tables for phase relationships.
"""

from __future__ import annotations

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Table,
)

from todowrite.core.models.base import Base

# Phase < Step associations
phases_steps = Table(
    "phases_steps",  # Phase < Step (alphabetical)
    Base.metadata,
    Column("phase_id", Integer, ForeignKey("phases.id")),
    Column("step_id", Integer, ForeignKey("steps.id")),
)

# InterfaceContract + Phase = interface_contracts_phases
interface_contracts_phases = Table(
    "interface_contracts_phases",
    Base.metadata,
    Column(
        "interface_contract_id", Integer, ForeignKey("interface_contracts.id")
    ),
    Column("phase_id", Integer, ForeignKey("phases.id")),
)
