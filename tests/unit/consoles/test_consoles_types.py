import pytest
from afs_fastapi.consoles.console_types import ConsoleType, get_console_type, CommandConsole

def test_console_type_enum():
    assert ConsoleType.BASIC.value == "basic"
    assert ConsoleType.ADVANCED.value == "advanced"
    assert ConsoleType.PREMIUM.value == "premium"

def test_get_console_type_valid():
    assert get_console_type("basic") == ConsoleType.BASIC
    assert get_console_type("advanced") == ConsoleType.ADVANCED
    assert get_console_type("premium") == ConsoleType.PREMIUM

def test_get_console_type_invalid():
    with pytest.raises(ValueError) as exc_info:
        get_console_type("invalid")
    assert "Invalid console type" in str(exc_info.value)

def test_get_console_type_case_insensitive():
    assert get_console_type("BASIC") == ConsoleType.BASIC
    assert get_console_type("Advanced") == ConsoleType.ADVANCED

def test_command_console_initialization():
    console = CommandConsole(1, "Irrigation")
    assert console.console_id == 1
    assert console.system == "Irrigation"

def test_command_console_activate():
    console = CommandConsole(1, "Irrigation")
    result = console.activate()
    assert result == "Control Console 1 for Irrigation system is activated."

def test_command_console_deactivate():
    console = CommandConsole(1, "Irrigation")
    result = console.deactivate()
    assert result == "Control Console 1 for Irrigation system is deactivated."