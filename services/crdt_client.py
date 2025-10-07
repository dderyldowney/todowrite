import httpx

from afs_fastapi.models.field_segment import FieldSegment  # type: ignore


class CrdtClient:
    """
    Client for interacting with the CRDT FastAPI endpoints.
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def add_segment(self, segment: FieldSegment) -> dict[str, str]:
        response = await self.client.post("/crdt/segments", json=segment.model_dump())
        response.raise_for_status()
        return response.json()

    async def assign_segment(self, segment_id: str, tractor_id: str) -> dict[str, str]:
        response = await self.client.post(
            "/crdt/assign", params={"segment_id": segment_id, "tractor_id": tractor_id}
        )
        response.raise_for_status()
        return response.json()

    async def release_segment(self, segment_id: str, tractor_id: str) -> dict[str, str]:
        response = await self.client.post(
            "/crdt/release", params={"segment_id": segment_id, "tractor_id": tractor_id}
        )
        response.raise_for_status()
        return response.json()

    async def complete_segment(self, segment_id: str, tractor_id: str) -> dict[str, str]:
        response = await self.client.post(
            "/crdt/complete", params={"segment_id": segment_id, "tractor_id": tractor_id}
        )
        response.raise_for_status()
        return response.json()

    async def get_allocated_segments(self, tractor_id: str) -> list[FieldSegment]:
        response = await self.client.get(f"/crdt/segments/allocated/{tractor_id}")
        response.raise_for_status()
        return [FieldSegment(**data) for data in response.json()]

    async def get_unallocated_segments(self) -> list[FieldSegment]:
        response = await self.client.get("/crdt/segments/unallocated")
        response.raise_for_status()
        return [FieldSegment(**data) for data in response.json()]

    async def get_completed_segments(self) -> list[FieldSegment]:
        response = await self.client.get("/crdt/segments/completed")
        response.raise_for_status()
        return [FieldSegment(**data) for data in response.json()]

    async def merge_crdt_state(self, other_state: dict[str, FieldSegment]) -> dict[str, str]:
        # Convert FieldSegment objects to dictionaries for JSON serialization
        serializable_state = {k: v.model_dump() for k, v in other_state.items()}
        response = await self.client.post("/crdt/merge", json=serializable_state)
        response.raise_for_status()
        return response.json()
