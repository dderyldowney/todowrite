# Cloud Integration Module Documentation

## Overview

This document provides comprehensive documentation for the AFS FastAPI cloud integration module (`afs_fastapi/services/cloud_integration.py`). It covers API usage, configuration, and troubleshooting guidelines for agricultural engineers and developers.

## API Usage

### `CloudIntegrationService` Class

*   **`__init__(self, config: Dict[str, Any])`**:
    *   Initializes the service with a configuration dictionary.
    *   `config`: Dictionary containing cloud platform details (e.g., `platform`, `endpoint`, `api_key`).

*   **`connect(self) -> bool`**:
    *   Establishes a connection to the configured cloud platform.
    *   Returns `True` on successful connection, `False` otherwise.

*   **`disconnect(self) -> bool`**:
    *   Closes the connection to the cloud platform.
    *   Returns `True` on successful disconnection, `False` if not connected.

*   **`send_telemetry_data(self, data: Dict[str, Any]) -> bool`**:
    *   Sends telemetry data to the cloud platform.
    *   `data`: Dictionary containing telemetry data (e.g., `robot_id`, `sensor_readings`).
    *   Includes retry mechanism for transient failures.
    *   Returns `True` if data is sent successfully, `False` otherwise.

*   **`receive_commands(self) -> Dict[str, Any]`**:
    *   Receives commands from the cloud platform.
    *   Returns a dictionary of commands or an empty dictionary if no commands are received or an error occurs.

*   **`synchronize_field_boundaries(self, field_data: Dict[str, Any]) -> bool`**:
    *   Synchronizes field boundary data with the cloud platform.
    *   `field_data`: Dictionary containing field boundary information.
    *   Includes simulated conflict resolution.
    *   Returns `True` on successful synchronization, `False` otherwise.

## Configuration

Cloud integration is configured via a dictionary passed to the `CloudIntegrationService` constructor. Key configuration parameters include:

*   `platform` (str): Name of the cloud platform (e.g., "AWS_IOT").
*   `endpoint` (str): API endpoint URL for the cloud service.
*   `api_key` (str): Authentication key for API access.

**Example Configuration (Python)**:

```python
cloud_config = {
    "platform": "AWS_IOT",
    "endpoint": "https://iot.us-east-1.amazonaws.com",
    "api_key": os.environ.get("AWS_IOT_API_KEY")
}
service = CloudIntegrationService(cloud_config)
```

## Troubleshooting

*   **Connection Errors**: Verify `endpoint` and `api_key` in configuration. Check network connectivity to the cloud platform.
*   **Data Transmission Failures**: Review logs for specific error messages. Ensure data format matches expected schema. Check cloud service status.
*   **Synchronization Conflicts**: Analyze conflict resolution logs. Adjust synchronization strategy if conflicts are frequent.
*   **Authentication Issues**: Ensure API keys are valid and not expired. Verify IAM roles and permissions in the cloud platform.
