import pytest
from afs_fastapi.equipment.farm_tractors import FarmTractor


@pytest.fixture
def tractor():
    """
    Pytest fixture to create a fresh instance of FarmTractor for each test.
    """
    return FarmTractor(
        "John Deere", "Model X", 2023, "https://manual.johndeere.com"
    )


def test_start_stop_engine_workflow(tractor):
    """
    Test the end-to-end workflow of starting and stopping the engine, ensuring all systems reset.
    """
    # Start the engine
    assert tractor.start_engine() == "Engine started."
    assert tractor.engine_on

    # Engage PTO and hydraulics with engine running
    assert tractor.engage_power_takeoff() == "Power Take-Off (PTO) engaged."
    assert tractor.power_takeoff
    assert tractor.activate_hydraulics() == "Hydraulics activated."
    assert tractor.hydraulics

    # Stop the engine and validate reset
    assert tractor.stop_engine() == "Engine stopped. Tractor is now reset."
    assert not tractor.engine_on
    assert tractor.gear == 0
    assert tractor.speed == 0
    assert not tractor.power_takeoff
    assert not tractor.hydraulics

    # Attempt to stop the engine again without starting
    with pytest.raises(ValueError, match="Engine is already off."):
        tractor.stop_engine()


def test_complete_gear_and_speed_workflow(tractor):
    """
    Test transitioning through gears and adjusting speed under valid and invalid conditions.
    """
    # Start the engine
    assert tractor.start_engine() == "Engine started."
    assert tractor.engine_on

    # Change gear and accelerate
    assert tractor.change_gear(3) == "Gear changed to 3."
    assert tractor.gear == 3
    assert tractor.accelerate(15) == "Speed increased to 15 mph."
    assert tractor.speed == 15

    # Attempt invalid operations
    with pytest.raises(ValueError, match="Gear must be between 0 and 10."):
        tractor.change_gear(11)
    with pytest.raises(
        ValueError, match="Acceleration must be a positive value."
    ):
        tractor.accelerate(-5)

    # Brake to reduce speed
    assert tractor.brake(10) == "Speed decreased to 5 mph."
    assert tractor.speed == 5

    # Stop the engine, which resets speed and gear
    assert tractor.stop_engine() == "Engine stopped. Tractor is now reset."
    assert not tractor.engine_on
    assert tractor.gear == 0
    assert tractor.speed == 0


def test_power_takeoff_and_hydraulics_full_workflow(tractor):
    """
    Test a full workflow of using PTO and hydraulics.
    """
    # Start the engine
    assert tractor.start_engine() == "Engine started."
    assert tractor.engine_on

    # Activate PTO
    assert tractor.engage_power_takeoff() == "Power Take-Off (PTO) engaged."
    assert tractor.power_takeoff

    # Deactivate PTO
    assert (
        tractor.disengage_power_takeoff() == "Power Take-Off (PTO) disengaged."
    )
    assert not tractor.power_takeoff

    # Activate and deactivate hydraulics
    assert tractor.activate_hydraulics() == "Hydraulics activated."
    assert tractor.hydraulics
    assert tractor.deactivate_hydraulics() == "Hydraulics deactivated."
    assert not tractor.hydraulics

    # Attempt invalid operations when PTO is already disengaged
    with pytest.raises(ValueError, match="PTO is already disengaged."):
        tractor.disengage_power_takeoff()

    # Attempt invalid operations when hydraulics are already deactivated
    with pytest.raises(
        ValueError, match="Hydraulics are already deactivated."
    ):
        tractor.deactivate_hydraulics()

    # Stop the engine
    assert tractor.stop_engine() == "Engine stopped. Tractor is now reset."
    assert not tractor.engine_on
    assert not tractor.power_takeoff
    assert not tractor.hydraulics


def test_end_to_end_combined_workflow(tractor):
    """
    Test a combined end-to-end workflow that involves starting the engine,
    accelerating, changing gears, activating hydraulics and PTO, and stopping the tractor.
    """
    # Start the engine
    assert tractor.start_engine() == "Engine started."
    assert tractor.engine_on

    # Change gears and accelerate
    assert tractor.change_gear(2) == "Gear changed to 2."
    assert tractor.gear == 2
    assert tractor.accelerate(10) == "Speed increased to 10 mph."
    assert tractor.speed == 10

    # Activate PTO and hydraulics
    assert tractor.engage_power_takeoff() == "Power Take-Off (PTO) engaged."
    assert tractor.power_takeoff
    assert tractor.activate_hydraulics() == "Hydraulics activated."
    assert tractor.hydraulics

    # Brake and reduce speed
    assert tractor.brake(5) == "Speed decreased to 5 mph."
    assert tractor.speed == 5

    # Stop the engine and confirm system reset
    assert tractor.stop_engine() == "Engine stopped. Tractor is now reset."
    assert not tractor.engine_on
    assert tractor.speed == 0
    assert tractor.gear == 0
    assert not tractor.power_takeoff
    assert not tractor.hydraulics

    # Attempt invalid operations after engine is off
    with pytest.raises(
        ValueError, match="Cannot change gears while the engine is off."
    ):
        tractor.change_gear(1)
    with pytest.raises(
        ValueError, match="Cannot accelerate while the engine is off."
    ):
        tractor.accelerate(5)


def test_string_representation(tractor):
    """
    Test the string representation of the tractor during various states.
    """
    # Default state
    expected_str = (
        "Tractor John Deere Model X (2023)\n"
        "Engine: Off\n"
        "Speed: 0 mph\n"
        "Gear: 0\n"
        "PTO: Disengaged\n"
        "Hydraulics: Deactivated\n"
        "Manual URL: https://manual.johndeere.com"
    )
    assert str(tractor) == expected_str

    # After starting engine, changing gear, and activating systems
    tractor.start_engine()
    tractor.change_gear(3)
    tractor.accelerate(15)
    tractor.engage_power_takeoff()
    tractor.activate_hydraulics()

    expected_str = (
        "Tractor John Deere Model X (2023)\n"
        "Engine: On\n"
        "Speed: 15 mph\n"
        "Gear: 3\n"
        "PTO: Engaged\n"
        "Hydraulics: Activated\n"
        "Manual URL: https://manual.johndeere.com"
    )
    assert str(tractor) == expected_str
