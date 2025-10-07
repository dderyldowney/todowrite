import numpy as np


class LightweightEdgeAnalytics:
    """
    A conceptual lightweight analytics model for edge devices in agricultural robotics.
    This model performs anomaly detection on sensor data (e.g., soil moisture).
    """

    def __init__(self, threshold: float = 0.30, window_size: int = 5):
        """
        Initializes the analytics model with a threshold and window size.

        Args:
            threshold (float): The anomaly detection threshold. If the average
                               of the last `window_size` readings falls below this,
                               an anomaly is detected.
            window_size (int): The number of recent readings to consider for the average.
        """
        self.threshold = threshold
        self.window_size = window_size
        self.data_buffer: list[float] = []

    def process_sensor_data(self, sensor_reading: float) -> bool:
        """
        Processes a single sensor reading and checks for anomalies.

        Args:
            sensor_reading (float): The current sensor reading (e.g., soil moisture percentage).

        Returns:
            bool: True if an anomaly is detected, False otherwise.
        """
        self.data_buffer.append(sensor_reading)

        # Keep the buffer size limited to window_size
        if len(self.data_buffer) > self.window_size:
            self.data_buffer.pop(0)

        if len(self.data_buffer) == self.window_size:
            average_reading = np.mean(self.data_buffer)
            if average_reading < self.threshold:
                print(
                    f"Anomaly Detected: Average reading ({average_reading:.2f}) below threshold ({self.threshold:.2f})"
                )
                return True
        return False


class EdgeControlLogic:
    """
    A conceptual class for developing local control logic based on edge insights.

    Secure Communication between Edge and Cloud:
    - **Encryption**: Use TLS/SSL for all data in transit.
    - **Authentication**: Implement device-level authentication using X.509 certificates or secure tokens.
    - **Authorization**: Utilize cloud IAM/RBAC policies to control device access to cloud resources (e.g., IoT Hub, Pub/Sub).
    - **API Keys/Tokens**: Securely manage and rotate API keys or tokens for cloud service interactions.
    """

    def __init__(self, device_id: str):
        self.device_id = device_id
        print(f"EdgeControlLogic initialized for device: {self.device_id}")

    def trigger_irrigation(self, anomaly_detected: bool, current_reading: float):
        """
        Simulates triggering localized irrigation based on anomaly detection.
        """
        if anomaly_detected:
            print(
                f"[Device {self.device_id}] Triggering localized irrigation due to low soil moisture ({current_reading:.2f})..."
            )
        else:
            print(
                f"[Device {self.device_id}] Soil moisture ({current_reading:.2f}) is normal. No irrigation needed."
            )


# Example Usage:
if __name__ == "__main__":
    analytics_model = LightweightEdgeAnalytics(threshold=0.25, window_size=3)
    control_logic = EdgeControlLogic(device_id="SensorNode-001")

    # Simulate sensor data over time
    sensor_data_stream = [
        0.40,
        0.38,
        0.35,  # Normal readings
        0.30,
        0.28,
        0.22,  # Dropping readings
        0.19,
        0.18,
        0.20,  # Anomaly range
        0.30,
        0.32,
        0.35,  # Recovery
    ]

    print("Starting sensor data processing and control...")
    for i, reading in enumerate(sensor_data_stream):
        print(f"\n[{i+1}] Current Reading: {reading:.2f}", end=", ")
        is_anomaly = analytics_model.process_sensor_data(reading)
        control_logic.trigger_irrigation(is_anomaly, reading)
