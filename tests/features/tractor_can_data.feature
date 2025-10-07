Feature: Tractor CAN Data Reception
  As the AFS FastAPI system
  I want to receive and interpret standard tractor data from the ISOBUS network
  So that I can monitor tractor status and integrate with farm management systems

  Scenario: Receiving Engine Speed Data
    Given the AFS FastAPI system is connected to an ISOBUS network
    And a Tractor ECU is present on the network
    When the Tractor ECU broadcasts Engine Speed (PGN 61444, SPN 190)
    Then the AFS FastAPI system should receive and correctly parse the Engine Speed value

  Scenario: Receiving Vehicle Speed Data
    Given the AFS FastAPI system is connected to an ISOBUS network
    And a Tractor ECU is present on the network
    When the Tractor ECU broadcasts Vehicle Speed (PGN 65265, SPN 84)
    Then the AFS FastAPI system should receive and correctly parse the Vehicle Speed value

  Scenario: Receiving Fuel Level Data
    Given the AFS FastAPI system is connected to an ISOBUS network
    And a Tractor ECU is present on the network
    When the Tractor ECU broadcasts Fuel Level (PGN 65276, SPN 96)
    Then the AFS FastAPI system should receive and correctly parse the Fuel Level value

  Scenario: Receiving GPS Coordinates
    Given the AFS FastAPI system is connected to an ISOBUS network
    And a Tractor ECU is present on the network
    When the Tractor ECU broadcasts GPS Coordinates (PGN 65267, SPN 162, 163)
    Then the AFS FastAPI system should receive and correctly parse the GPS Coordinates value

  Scenario: Handling Corrupted CAN Messages
    Given the AFS FastAPI system is connected to an ISOBUS network
    And a Tractor ECU is present on the network
    When a corrupted CAN message is broadcast on the network
    Then the AFS FastAPI system should log the error and discard the message

  Scenario: Handling Unknown PGNs
    Given the AFS FastAPI system is connected to an ISOBUS network
    And a Tractor ECU is present on the network
    When an unknown PGN is broadcast on the network
    Then the AFS FastAPI system should log the unknown PGN and ignore the message

  Scenario: Receiving Multi-frame Messages
    Given the AFS FastAPI system is connected to an ISOBUS network
    And a Tractor ECU is present on the network
    When the Tractor ECU broadcasts a multi-frame message
    Then the AFS FastAPI system should receive and reassemble the complete message

  Scenario: Filtering Specific PGNs
    Given the AFS FastAPI system is configured to filter for specific PGNs
    And the AFS FastAPI system is connected to an ISOBUS network
    And a Tractor ECU is present on the network
    When multiple PGNs are broadcast on the network
    Then the AFS FastAPI system should only process the configured PGNs
