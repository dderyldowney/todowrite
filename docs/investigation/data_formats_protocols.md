# Data Formats and Protocols for Agricultural Cloud Communication

## Overview

This document details the data formats and communication protocols to be utilized for integrating AFS FastAPI with agricultural cloud platforms. Standardization and efficiency are key to reliable data exchange.

## Data Formats

1.  **JSON (JavaScript Object Notation)**:
    *   **Primary Format**: JSON will be the primary data interchange format due to its human-readability, widespread adoption, and efficient parsing by modern programming languages.
    *   **Structure**: Data payloads will follow a well-defined schema, ensuring consistency across different data types (telemetry, commands, geospatial data).
    *   **Examples**: 
        ```json
        {
            "robotId": "R1",
            "timestamp": "2025-10-07T12:00:00Z",
            "sensorData": {
                "soilMoisture": 0.45,
                "airTemp": 22.5
            }
        }
        ```

2.  **GeoJSON (Geographic JSON)**:
    *   **Geospatial Data**: GeoJSON will be used for representing geographical features such as field boundaries, obstacle locations, and mission paths.
    *   **Compatibility**: Ensures compatibility with GIS systems and mapping services.

3.  **ISOXML (ISO 11783-10)**:
    *   **Agricultural Standard**: While JSON is primary for real-time data, ISOXML will be considered for batch data exchange with Farm Management Information Systems (FMIS) where industry-standard compliance is required.
    *   **Conversion**: Mechanisms for converting between internal JSON formats and ISOXML will be developed if necessary.

## Communication Protocols

1.  **HTTPS (Hypertext Transfer Protocol Secure)**:
    *   **Primary Protocol**: HTTPS will be used for all RESTful API interactions with cloud platforms, ensuring encrypted and authenticated communication.
    *   **Methods**: Standard HTTP methods (GET, POST, PUT, DELETE) will be employed for data retrieval, submission, and updates.

2.  **MQTT (Message Queuing Telemetry Transport)**:
    *   **IoT Telemetry**: MQTT will be utilized for lightweight, real-time telemetry streaming from robotic systems to cloud IoT hubs.
    *   **Publish/Subscribe**: Leverages a publish/subscribe model for efficient one-to-many and many-to-one communication.
    *   **Quality of Service (QoS)**: Support for different QoS levels to ensure message delivery reliability.

3.  **WebSockets**:
    *   **Real-time Control**: WebSockets may be considered for low-latency, bidirectional communication required for real-time remote control commands.

## Security Considerations

*   All communication will be encrypted using TLS.
*   API keys and authentication tokens will be securely managed and transmitted.
