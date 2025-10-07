from typing import Any

import can

from afs_fastapi.equipment.can_interface import CanBusManager  # type: ignore


class FarmTractor:
    """
    Represents a farm tractor with various controls and capabilities.
    Integrates with CanBusManager for CAN bus communication.
    """

    def __init__(
        self,
        tractor_id: str,
        make: str,
        model: str,
        can_interface: str = "socketcan",
        can_channel: str = "can0",
        can_bitrate: int = 500000,
    ):
        self.tractor_id = tractor_id
        self.make = make
        self.model = model
        self.engine_on = False
        self.speed = 0.0  # km/h
        self.gps_location: dict[str, float] = {"latitude": 0.0, "longitude": 0.0}
        self.implement_attached = False
        self.implement_position = "up"
        self.can_manager = CanBusManager(can_interface, can_channel, can_bitrate)

    def start_engine(self) -> str:
        if not self.engine_on:
            self.engine_on = True
            return f"Tractor {self.tractor_id} engine started."
        return f"Tractor {self.tractor_id} engine is already on."

    def stop_engine(self) -> str:
        if self.engine_on:
            self.engine_on = False
            self.speed = 0.0
            return f"Tractor {self.tractor_id} engine stopped."
        return f"Tractor {self.tractor_id} engine is already off."

    def set_speed(self, speed: float) -> str:
        if self.engine_on:
            self.speed = max(0.0, speed)
            return f"Tractor {self.tractor_id} speed set to {self.speed} km/h."
        return f"Tractor {self.tractor_id} engine is off. Cannot set speed."

    def update_gps_location(self, latitude: float, longitude: float) -> str:
        self.gps_location["latitude"] = latitude
        self.gps_location["longitude"] = longitude
        return f"Tractor {self.tractor_id} GPS location updated to {latitude}, {longitude}."

    def attach_implement(self) -> str:
        if not self.implement_attached:
            self.implement_attached = True
            return f"Tractor {self.tractor_id} implement attached."
        return f"Tractor {self.tractor_id} already has an implement attached."

    def detach_implement(self) -> str:
        if self.implement_attached:
            self.implement_attached = False
            self.implement_position = "up"
            return f"Tractor {self.tractor_id} implement detached."
        return f"Tractor {self.tractor_id} has no implement attached."

    def set_implement_position(self, position: str) -> str:
        if self.implement_attached and position in ["up", "down"]:
            self.implement_position = position
            return f"Tractor {self.tractor_id} implement position set to {position}."
        return f"Tractor {self.tractor_id} cannot set implement position. Check if implement is attached and position is valid."

    def get_status(self) -> dict[str, Any]:
        return {
            "tractor_id": self.tractor_id,
            "make": self.make,
            "model": self.model,
            "engine_on": self.engine_on,
            "speed": self.speed,
            "gps_location": self.gps_location,
            "implement_attached": self.implement_attached,
            "implement_position": self.implement_position,
            "can_bus_connected": self.can_manager.bus is not None,
        }

    def connect_can_bus(self) -> str:
        self.can_manager.connect()
        return (
            f"CAN bus connection status for {self.tractor_id}: {self.can_manager.bus is not None}"
        )

    def disconnect_can_bus(self) -> str:
        self.can_manager.disconnect()
        return (
            f"CAN bus connection status for {self.tractor_id}: {self.can_manager.bus is not None}"
        )

    def send_can_message(self, arb_id: int, data: list[int]) -> str:
        if self.can_manager.bus:
            message = can.Message(arbitration_id=arb_id, data=data, is_extended_id=False)
            if self.can_manager.send_message(message):
                return f"Tractor {self.tractor_id} sent CAN message: ID={arb_id}, Data={data}"
            return f"Tractor {self.tractor_id} failed to send CAN message."
        return f"Tractor {self.tractor_id} CAN bus not connected."
