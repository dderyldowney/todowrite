# Claude Code Configuration for AFS FastAPI

This file contains project-specific instructions for Claude Code sessions working on the **AFS FastAPI robotic agriculture platform**.

## Mandatory Universal Requirements

**Authoritative Source**: All universal agent requirements, including TDD workflows, commit standards, documentation practices, and environment setup, are defined in **`AGENTS.md`**. You must load and adhere to these rules. This file only contains overrides or instructions specific to Claude.

---

## Claude-Specific Instructions

### Format-First Generation Standards

**Requirement**: All generated content must emerge in final quality-controlled form.

**NO FORMATTING CYCLES**: Generate all code, tests, and documentation pre-formatted to quality standards.

1.  **Code Generation**: Apply Black, isort, Ruff compliance during creation
2.  **Type Safety**: Include proper type annotations from initial generation
3.  **Agricultural Context**: Embed domain-specific examples and scenarios
4.  **Quality Standards**: Meet enterprise-grade requirements immediately

### Pre-Formatted Generation Templates

**Python Code Template**:
'''python
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

class AgriculturalComponent:
    """Agricultural robotics component for tractor coordination.

    Provides functionality for multi-tractor field operations with
    safety compliance and performance optimization.
    """

    def __init__(self, equipment_id: str) -> None:
        """Initialize agricultural equipment interface."""
        self.equipment_id = equipment_id
        self.operational_status = "ready"

    def coordinate_field_operation(self, operation_data: Dict[str, Any]) -> bool:
        """Execute coordinated field operation with fleet synchronization."""
        return True
'''

**Test Generation Template**:
'''python
import pytest
from afs_fastapi.equipment.farm_tractors import FarmTractor

class TestAgriculturalOperation:
    """Test agricultural equipment operations for field coordination."""

    def test_tractor_field_coordination(self) -> None:
        """Test multi-tractor coordination during field cultivation."""
        # RED: Describe desired agricultural behavior
        tractor = FarmTractor(equipment_id="FIELD_CULTIVATOR_01")

        # Test agricultural operation
        result = tractor.execute_cultivation_pattern()

        assert result is True
        assert tractor.field_status == "cultivation_complete"
'''

### Code Documentation Requirements

**Educational Code Explanations**: All code generated must be explained both **overall** and **individually**. Explanations should be concise with the dual purpose of teaching while building this real-world professional project.

### Claude Command Integration

The platform provides universal session management commands available to all AI agents, as defined in `AGENTS.md` and `SESSION_SUMMARY.md`.

**Claude Code Specific Integration**:
- Commands are executable via bash: `./bin/commandname`
- Select commands are available as slash commands: `/loadsession`, `/whereweare`, `/updatedocs`
- Command triggers are stored in `.claude/commands/` with complete specifications.
