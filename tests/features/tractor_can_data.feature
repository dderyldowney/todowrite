Feature: Tractor CAN Data Reception
  As the AFS FastAPI system
  I want to receive and interpret standard tractor data from the ISOBUS network
  So that I can monitor tractor status and integrate with farm management systems

  Scenario: Receiving Engine Speed Data
    Given the AFS FastAPI system is connected to an ISOBUS network
    And a Tractor ECU is present on the network
    When the Tractor ECU broadcasts Engine Speed (PGN 61444, SPN 190)
    Then the AFS FastAPI system should receive and correctly parse the Engine Speed value
