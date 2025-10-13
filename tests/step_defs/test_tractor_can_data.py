import pytest
from pytest_bdd import given, parsers, scenario, then, when

from afs_fastapi.core.can_parser import CanParser


# Scenarios
@scenario("../features/tractor_can_data.feature", "Receiving <Data Type> Data")
def test_receiving_data_type_data():
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
    """Sets the ISOBUS network to connected."""
    isobus_network["connected"] = True
    pass


@given("a Tractor ECU is present on the network")
def tractor_ecu_present(tractor_ecu, isobus_network):
    """Sets the tractor ECU to present on the network."""
    tractor_ecu["present"] = True
    pass


# When Steps
@when(
    parsers.parse(
        "the Tractor ECU broadcasts {data_type} (PGN {pgn:d}, SPN {spn:d}) with value {value:d}"
    )
)
def ecu_broadcasts_data_with_value(tractor_ecu, isobus_network, data_type, pgn, spn, value):
    """Simulates the ECU broadcasting data with a specific value."""
    isobus_network["messages_on_bus"].append(
        {"pgn": pgn, "spn": spn, "value": value, "data_type": data_type}
    )


# Then Steps
@then(
    parsers.parse(
        "the AFS FastAPI system should receive and correctly parse the {data_type} value as {value:d}"
    )
)
def system_receives_and_parses_data(afs_fastapi_system, isobus_network, data_type, value):
    """Verifies that the AFS FastAPI system correctly receives and parses the CAN data."""
    for message in isobus_network["messages_on_bus"]:
        parsed_message = afs_fastapi_system["can_parser"].parse_message(message)
        if parsed_message:
            afs_fastapi_system["can_messages_received"].append(parsed_message)

    assert len(afs_fastapi_system["can_messages_received"]) > 0
    # Find the message corresponding to the current data_type and value
    found_message = next(
        (
            msg
            for msg in afs_fastapi_system["can_messages_received"]
            if msg.get("data_type") == data_type
            and msg.get("parsed_data", {}).get(data_type.lower().replace(" ", "_")) == value
        ),
        None,
    )

    assert found_message is not None
    assert found_message["parsed_data"][data_type.lower().replace(" ", "_")] == value
