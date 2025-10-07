"""
Edge software module for data aggregation and local processing on agricultural gateways.
"""

from __future__ import annotations

import json
import random
import time
from typing import Any

# Local imports - ignore type checking until stubs are created
from afs_fastapi.monitoring.edge_analytics import (  # type: ignore
    EdgeControlLogic,
    LightweightEdgeAnalytics,
)
from afs_fastapi.monitoring.sensor_interface import (  # type: ignore
    LoRaWANSensorInterface,
    MQTTSensorInterface,
)


class EdgeGatewaySoftware:
    """
    Conceptual edge software for data aggregation and local processing on agricultural gateways.
    """

    gateway_id: str
    sensors: list[Any]  # Can be either MQTTSensorInterface or LoRaWANSensorInterface
    analytics_model: LightweightEdgeAnalytics
    control_logic: EdgeControlLogic
    data_buffer: list[dict[str, Any]]
    cloud_connected: bool

    def __init__(self, gateway_id: str, sensors_config: list[dict[str, Any]]) -> None:
        self.gateway_id = gateway_id
        self.sensors = []
        self.analytics_model = LightweightEdgeAnalytics(threshold=0.25, window_size=3)
        self.control_logic = EdgeControlLogic(device_id=gateway_id)
        self.data_buffer = []  # For offline buffering
        self.cloud_connected = True  # Conceptual: assume connected initially

        for config in sensors_config:
            device_id = config["device_id"]
            sensor_type = config["sensor_type"]
            protocol = config["protocol"]

            if protocol == "MQTT":
                self.sensors.append(MQTTSensorInterface(device_id, sensor_type))
            elif protocol == "LoRaWAN":
                self.sensors.append(LoRaWANSensorInterface(device_id, sensor_type))
            else:
                print(f"Unsupported protocol: {protocol}")

        print(
            f"EdgeGatewaySoftware initialized for gateway {self.gateway_id} with {len(self.sensors)} sensors."
        )

    def connect_all_sensors(self) -> None:
        """Connect to all configured sensors."""
        for sensor in self.sensors:
            try:
                sensor.connect()
            except Exception as e:
                print(f"Error connecting to sensor {sensor.device_id}: {e}")

    def disconnect_all_sensors(self) -> None:
        """Disconnect from all sensors."""
        for sensor in self.sensors:
            try:
                sensor.disconnect()
            except Exception as e:
                print(f"Error disconnecting from sensor {sensor.device_id}: {e}")

    def send_to_cloud(self, data: dict[str, Any]) -> bool:
        """
        Conceptual method to send data to the cloud. Simulates network issues.
        """
        if self.cloud_connected and random.random() > 0.1:  # Simulate 10% chance of network failure
            print(f"[Cloud] Sending data from {self.gateway_id} to cloud: {json.dumps(data)}")
            return True
        else:
            print(
                f"[Cloud] Cloud connection unavailable or failed for {self.gateway_id}. Buffering data."
            )
            return False

    def synchronize_data(self) -> None:
        """
        Synchronizes buffered data with the cloud when connectivity is restored.
        """
        if not self.cloud_connected:
            print("[Sync] Attempting to re-establish cloud connection...")
            if random.random() > 0.3:  # Simulate 70% chance of reconnection success
                self.cloud_connected = True
                print("[Sync] Cloud connection re-established.")
            else:
                print("[Sync] Cloud connection still unavailable.")
                return

        if self.cloud_connected and self.data_buffer:
            print(f"[Sync] Synchronizing {len(self.data_buffer)} buffered items with cloud...")
            while self.data_buffer:
                buffered_item = self.data_buffer.pop(0)
                if self.send_to_cloud(buffered_item):
                    print("[Sync] Sent buffered item to cloud.")
                else:
                    self.data_buffer.insert(0, buffered_item)  # Put it back if sending fails
                    print("[Sync] Failed to send buffered item. Retrying later.")
                    break
            if not self.data_buffer:
                print("[Sync] All buffered data synchronized.")

    def aggregate_data(self, raw_data: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Aggregates raw sensor data. This is a conceptual aggregation.
        In a real scenario, this might involve averaging, filtering, or combining data.
        """
        aggregated_output: dict[str, Any] = {
            "gateway_id": self.gateway_id,
            "timestamp": raw_data[0]["timestamp"] if raw_data else None,
            "readings": {},
        }
        for data in raw_data:
            sensor_type = data["sensor_type"]
            if sensor_type not in aggregated_output["readings"]:
                aggregated_output["readings"][sensor_type] = []
            aggregated_output["readings"][sensor_type].append(data["value"])

        # Conceptual: calculate averages for each sensor type
        for sensor_type, values in aggregated_output["readings"].items():
            aggregated_output["readings"][sensor_type] = sum(values) / len(values)

        return aggregated_output

    def process_data_locally(self, aggregated_data: dict[str, Any]) -> None:
        """
        Processes aggregated data locally using analytics models and triggers control logic.
        """
        print(f"\n--- Local Processing for Gateway {self.gateway_id} ---")
        for sensor_type, value in aggregated_data["readings"].items():
            print(f"Processing {sensor_type}: {value}")
            # Assuming analytics model is primarily for soil moisture for this example
            if sensor_type == "soil_moisture":
                is_anomaly = self.analytics_model.process_sensor_data(value)
                self.control_logic.trigger_irrigation(is_anomaly, value)
            else:
                print(f"No specific analytics model for {sensor_type} yet.")

    def run(self, interval_seconds: int = 5, iterations: int = 3) -> None:
        """
        Run the edge gateway software for a specified number of iterations.

        Args:
            interval_seconds: Time to wait between iterations in seconds.
            iterations: Number of data collection/processing cycles to run.
        """
        self.connect_all_sensors()
        for i in range(iterations):
            print(f"\n--- Iteration {i+1} ---")
            self.synchronize_data()  # Attempt to sync buffered data first

            raw_readings = []
            for sensor in self.sensors:
                try:
                    raw_readings.append(sensor.read_data())
                except ConnectionError as e:
                    print(f"Skipping sensor {sensor.device_id}: {e}")

            if raw_readings:
                aggregated_data = self.aggregate_data(raw_readings)
                print(f"Aggregated Data: {json.dumps(aggregated_data, indent=2)}")
                self.process_data_locally(aggregated_data)

                # Attempt to send to cloud, buffer if fails
                if not self.send_to_cloud(aggregated_data):
                    self.data_buffer.append(aggregated_data)
                    print(f"Data buffered. Buffer size: {len(self.data_buffer)}")
            else:
                print("No raw readings to process.")
            time.sleep(interval_seconds)
        self.disconnect_all_sensors()
        self.synchronize_data()  # Final sync attempt


# Example Usage:
if __name__ == "__main__":
    sensors_config: list[dict[str, str]] = [
        {"device_id": "SM-001", "sensor_type": "soil_moisture", "protocol": "MQTT"},
        {"device_id": "AT-001", "sensor_type": "air_temperature", "protocol": "LoRaWAN"},
    ]

    gateway: EdgeGatewaySoftware = EdgeGatewaySoftware(
        gateway_id="FarmGateway-001", sensors_config=sensors_config
    )
    gateway.run(interval_seconds=2, iterations=2)
