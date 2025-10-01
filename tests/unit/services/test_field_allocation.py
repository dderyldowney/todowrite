"""
RED-phase scaffold for FieldAllocationCRDT API presence.

Agricultural Context:
- Placeholder ensures test-first trail for CRDT field allocation work.
- Keeps suite informative without forcing implementation prematurely.
"""

from __future__ import annotations

import pytest


def test_field_allocation_crdt_placeholder_api_exists():
    """Verify placeholder class exists and methods are not implemented yet."""
    from afs_fastapi.services.field_allocation import FieldAllocationCRDT

    crdt = FieldAllocationCRDT(field_id="field_001")

    with pytest.raises(NotImplementedError):
        crdt.claim("cell_A1", owner_id="tractor_001")

    with pytest.raises(NotImplementedError):
        crdt.release("cell_A1", owner_id="tractor_001")

    with pytest.raises(NotImplementedError):
        crdt.merge(crdt)

    with pytest.raises(NotImplementedError):
        crdt.owner_of("cell_A1")

    with pytest.raises(NotImplementedError):
        crdt.assigned_sections("tractor_001")

    with pytest.raises(NotImplementedError):
        crdt.serialize()

    with pytest.raises(NotImplementedError):
        FieldAllocationCRDT.deserialize({})
