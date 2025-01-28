# afs_fastapi/consoles/console_types.py
class CommandConsole:
    def __init__(self, console_id: int, system: str):
        self.console_id = console_id
        self.system = system

    def activate(self):
        return f"Control Console {self.console_id} for {self.system} system is activated."

    def deactivate(self):
        return f"Control Console {self.console_id} for {self.system} system is deactivated."
