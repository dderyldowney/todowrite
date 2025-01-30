# afs_fastapi/consoles/console_types.py
from enum import Enum

class ConsoleType(Enum):
    BASIC = "basic"
    ADVANCED = "advanced"
    PREMIUM = "premium"

def get_console_type(console_type_str: str) -> ConsoleType:
    try:
        return ConsoleType(console_type_str.lower())
    except ValueError:
        raise ValueError(f"Invalid console type: {console_type_str}")

class CommandConsole:
    def __init__(self, console_id: int, system: str):
        self.console_id = console_id
        self.system = system

    def activate(self):
        return f"Control Console {self.console_id} for {self.system} system is activated."

    def deactivate(self):
        return f"Control Console {self.console_id} for {self.system} system is deactivated."
