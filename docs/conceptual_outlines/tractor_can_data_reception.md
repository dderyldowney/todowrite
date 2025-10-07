# Conceptual Outline: Tractor CAN Data Reception

## Feature: Tractor CAN Data Reception

**Purpose:** The AFS FastAPI system needs to reliably receive and interpret standard tractor operational data from the ISOBUS (ISO 11783) network. This capability is fundamental for real-time monitoring, data logging, and integration with broader farm management and autonomous control systems.

**High-Level Components Involved:**

1.  **ISOBUS Network:** The standardized CAN bus communication protocol for agricultural machinery.
2.  **Tractor ECU (TECU):** The Electronic Control Unit within the tractor responsible for interfacing with the ISOBUS network and providing tractor-specific data.
3.  **AFS FastAPI System:** Our application, which will connect to the ISOBUS network (likely via a gateway or direct CAN interface) to consume and process messages.

**Data Flow (Conceptual):**

*   Tractor's internal systems (e.g., engine, transmission) generate J1939 messages.
*   The TECU translates relevant J1939 data into ISOBUS Parameter Group Numbers (PGNs) and broadcasts them onto the ISOBUS network.
*   The AFS FastAPI system listens to the ISOBUS network, receives raw CAN frames, and then parses these frames to extract meaningful ISOBUS PGNs and Suspect Parameter Numbers (SPNs).
*   Parsed data is then made available for monitoring, storage, and further processing within the AFS FastAPI system.

## Scenario: Receiving Engine Speed Data

**Objective:** To verify that the AFS FastAPI system can successfully receive and correctly parse a specific, critical data point: the Engine Speed, broadcast by the Tractor ECU on the ISOBUS network.

**Conceptual Steps:**

1.  **System Connection:** The AFS FastAPI system establishes a connection to the ISOBUS network. This implies the presence of a physical or simulated CAN interface.
2.  **ECU Presence:** A Tractor ECU is active and recognized on the ISOBUS network, acting as a source of tractor data.
3.  **Data Broadcast:** The Tractor ECU broadcasts a standard ISOBUS message containing Engine Speed data (specifically, PGN 61444, SPN 190).
4.  **Reception and Parsing:** The AFS FastAPI system receives this broadcast message, identifies it as Engine Speed data, and extracts the numerical value for engine RPM.
5.  **Verification:** The extracted Engine Speed value matches the expected value that was broadcast by the simulated Tractor ECU.

**Expected Outcome:** The AFS FastAPI system reliably obtains accurate engine speed information from the ISOBUS network, demonstrating its foundational capability for tractor data acquisition.

## Future Considerations (Beyond this Scenario):

*   Handling other critical tractor data (e.g., vehicle speed, fuel level, GPS coordinates).
*   Implementing error handling for corrupted or unexpected messages.
*   Managing network traffic and message prioritization.
*   Integrating with a physical CAN interface.
*   Storing parsed data in a time-series database.
