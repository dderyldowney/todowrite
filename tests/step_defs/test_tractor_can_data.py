import pytest
from pytest_bdd import given, parsers, scenario, then, when

from afs_fastapi.core.can_parser import CanParser


# Scenarios
@scenario("../features/tractor_can_data.feature", "Receiving Engine Speed Data")
def test_receiving_engine_speed_data():
    pass


# Fixtures
@pytest.fixture
def afs_fastapi_system():
    """Represents the AFS FastAPI system instance."""
    return {"can_messages_received": [], "can_parser": CanParser()}


@pytest.fixture
def isobus_network():
    """Represents the simulated ISOBUS network."""
    return {"connected": False, "messages_on_bus": []}


@pytest.fixture
def tractor_ecu():
    """Represents a simulated Tractor ECU."""
    return {"present": False, "engine_speed": None}


# Given Steps
@given("the AFS FastAPI system is connected to an ISOBUS network")
def system_connected_to_isobus(afs_fastapi_system, isobus_network):
    isobus_network["connected"] = True
    # In a real implementation, this would establish a connection
    pass


@given("a Tractor ECU is present on the network")
def tractor_ecu_present(tractor_ecu, isobus_network):
    tractor_ecu["present"] = True
    # In a real implementation, this would involve ECU discovery
    pass


# When Steps
@when(parsers.parse("the Tractor ECU broadcasts Engine Speed (PGN {pgn:d}, SPN {spn:d})"))
def ecu_broadcasts_engine_speed(tractor_ecu, isobus_network, pgn, spn):
    # Simulate a CAN message for Engine Speed
    simulated_engine_speed_value = 2000  # Example value
    isobus_network["messages_on_bus"].append(
        {"pgn": pgn, "spn": spn, "value": simulated_engine_speed_value}
    )
    # In a real implementation, the ECU would send a message to the bus
    pass


# Then Steps
@then(
    parsers.parse(
        "the AFS FastAPI system should receive and correctly parse the Engine Speed value"
    )
)
def system_receives_and_parses_engine_speed(afs_fastapi_system, isobus_network):
    # Simulate the AFS FastAPI system processing messages from the bus
    for message in isobus_network["messages_on_bus"]:
        parsed_message = afs_fastapi_system["can_parser"].parse_message(message)
        if parsed_message:
            afs_fastapi_system["can_messages_received"].append(parsed_message)

    assert len(afs_fastapi_system["can_messages_received"]) > 0
    received_message = afs_fastapi_system["can_messages_received"][0]
    assert received_message["pgn"] == 61444
    assert received_message["spn"] == 190
    assert received_message["parsed_data"]["engine_speed"] == 2000
