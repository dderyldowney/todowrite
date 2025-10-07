import can


class CanBusManager:
    """
    Manages CAN bus communication for agricultural equipment.
    Supports various CAN interfaces and provides methods for sending and receiving messages.
    """

    def __init__(self, interface: str = "socketcan", channel: str = "can0", bitrate: int = 500000):
        """
        Initializes the CAN bus manager.

        Args:
            interface (str): The CAN interface to use (e.g., 'socketcan', 'pcan', 'kvaser').
            channel (str): The CAN channel to connect to (e.g., 'can0' for socketcan).
            bitrate (int): The bitrate of the CAN bus (e.g., 500000 for 500 kbit/s).
        """
        self.interface = interface
        self.channel = channel
        self.bitrate = bitrate
        self.bus: can.BusABC | None = None
        self.notifier: can.Notifier | None = None

    def connect(self) -> None:
        """
        Connects to the CAN bus.
        """
        try:
            self.bus = can.interface.Bus(
                interface=self.interface, channel=self.channel, bitrate=self.bitrate
            )
            print(
                f"Successfully connected to CAN bus: {self.interface} on {self.channel} at {self.bitrate} bps"
            )
        except Exception as e:
            print(f"Failed to connect to CAN bus: {e}")
            self.bus = None

    def disconnect(self) -> None:
        """
        Disconnects from the CAN bus.
        """
        if self.notifier:
            self.notifier.stop()
            self.notifier = None
        if self.bus:
            self.bus.shutdown()
            self.bus = None
            print("Disconnected from CAN bus.")

    def send_message(self, message: can.Message) -> bool:
        """
        Sends a CAN message.

        Args:
            message (can.Message): The CAN message to send.

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """
        if not self.bus:
            print("CAN bus not connected. Cannot send message.")
            return False
        try:
            self.bus.send(message)
            return True
        except can.CanError as e:
            print(f"Failed to send CAN message: {e}")
            return False

    def add_listener(self, listener: can.Listener) -> None:
        """
        Adds a listener to receive CAN messages.

        Args:
            listener (can.Listener): The listener object to add.
        """
        if not self.bus:
            print("CAN bus not connected. Cannot add listener.")
            return
        if not self.notifier:
            self.notifier = can.Notifier(self.bus, [listener])
        else:
            self.notifier.add_listener(listener)

    def remove_listener(self, listener: can.Listener) -> None:
        """
        Removes a listener from receiving CAN messages.

        Args:
            listener (can.Listener): The listener object to remove.
        """
        if self.notifier:
            self.notifier.remove_listener(listener)
            if not self.notifier.listeners:
                self.notifier.stop()
                self.notifier = None
