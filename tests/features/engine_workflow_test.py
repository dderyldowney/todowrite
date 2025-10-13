"""Feature tests for engine workflow and state management."""

import pytest

from afs_fastapi.equipment.farm_tractors import FarmTractor


@pytest.fixture
def tractor() -> FarmTractor:
    """Pytest fixture to create a fresh instance of FarmTractor for each test."""
    return FarmTractor("John Deere", "Model X", 2023, "https://manual.johndeere.com")


def test_engine_start(tractor: FarmTractor):
    """Test starting the engine."""
    # Initial state
    assert not tractor.engine_on  # Engine is off by default

    # Start the engine
    assert tractor.start_engine() == "Engine started."
    assert tractor.engine_on  # Engine should now be ON

    # Attempt to start the engine again - should raise ValueError
    with pytest.raises(ValueError, match="Engine is already running."):
        tractor.start_engine()


def test_engine_stop(tractor: FarmTractor):
    """Test stopping the engine and the system reset."""
    # Initial state (engine is off by default)
    assert not tractor.engine_on

    # Attempting to stop the engine when it is already off
    with pytest.raises(ValueError, match="Engine is already off."):
        tractor.stop_engine()

    # Start the engine
    assert tractor.start_engine() == "Engine started."
    assert tractor.engine_on

    # Stop the engine
    assert tractor.stop_engine() == "Engine stopped. Tractor is now reset."
    assert not tractor.engine_on  # Engine should now be OFF
    assert tractor.speed == 0  # Speed is reset to 0
    assert tractor.gear == 0  # Gear is reset to neutral
    assert not tractor.power_takeoff  # PTO should be disengaged
    assert not tractor.hydraulics  # Hydraulics should be deactivated


def test_engine_dependency_for_operations(tractor: FarmTractor):
    """Test that engine-dependent operations cannot proceed unless the engine is running."""
    # Ensure engine is off
    assert not tractor.engine_on

    # Attempt to change gears with the engine off
    with pytest.raises(ValueError, match="Cannot change gears while the engine is off."):
        tractor.change_gear(2)

    # Attempt to accelerate with the engine off
    with pytest.raises(ValueError, match="Cannot accelerate while the engine is off."):
        tractor.accelerate(10)

    # Attempt to brake with the engine off
    with pytest.raises(ValueError, match="Cannot brake while the engine is off."):
        tractor.brake(5)

    # Attempt to activate PTO with the engine off
    with pytest.raises(ValueError, match="Cannot engage PTO while the engine is off."):
        tractor.engage_power_takeoff()

    # Attempt to activate hydraulics with the engine off
    with pytest.raises(ValueError, match="Cannot activate hydraulics while the engine is off."):
        tractor.activate_hydraulics()

    # Start the engine
    assert tractor.start_engine() == "Engine started."
    assert tractor.engine_on

    # Now all operations should proceed without errors
    assert tractor.change_gear(2) == "Gear changed to 2."
    assert tractor.accelerate(10) == "Speed increased to 10 mph."
    assert tractor.brake(5) == "Speed decreased to 5 mph."
    assert tractor.engage_power_takeoff() == "Power Take-Off (PTO) engaged."
    assert tractor.activate_hydraulics() == "Hydraulics activated."


def test_engine_state_after_reset(tractor: FarmTractor):
    """Test that stopping the engine resets the tractor's state."""
    # Start the engine
    assert tractor.start_engine() == "Engine started."
    assert tractor.engine_on

    # Make some changes to the state
    assert tractor.change_gear(3) == "Gear changed to 3."
    assert tractor.accelerate(20) == "Speed increased to 20 mph."
    assert tractor.engage_power_takeoff() == "Power Take-Off (PTO) engaged."
    assert tractor.activate_hydraulics() == "Hydraulics activated."

    # Now stop the engine
    assert tractor.stop_engine() == "Engine stopped. Tractor is now reset."

    # Verify that the state is fully reset
    assert not tractor.engine_on  # Engine should be OFF
    assert tractor.gear == 0  # Gear should be reset to neutral
    assert tractor.speed == 0  # Speed should be reset to 0
    assert not tractor.power_takeoff  # PTO should be disengaged
    assert not tractor.hydraulics  # Hydraulics should be deactivated


def test_restart_engine_after_stopping(tractor: FarmTractor):
    """Test that the engine can be restarted after it has been stopped."""
    # Start the engine
    assert tractor.start_engine() == "Engine started."
    assert tractor.engine_on

    # Stop the engine
    assert tractor.stop_engine() == "Engine stopped. Tractor is now reset."
    assert not tractor.engine_on  # Engine should now be OFF

    # Restart the engine
    assert tractor.start_engine() == "Engine started."
    assert tractor.engine_on  # Engine should now be ON again
