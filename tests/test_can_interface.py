import unittest
from unittest.mock import MagicMock, patch

from equipment.can_interface import CanBusManager


class TestCanBusManager(unittest.TestCase):
    @patch("can.interface.Bus")
    def test_connect_success(self, mock_bus):
        """Test successful connection to the CAN bus."""
        manager = CanBusManager()
        manager.connect()
        mock_bus.assert_called_once_with(interface="socketcan", channel="can0", bitrate=500000)
        self.assertIsNotNone(manager.bus)
        self.assertEqual(manager.breaker.current_state, "closed")

    @patch("can.interface.Bus", side_effect=Exception("Connection failed"))
    def test_connect_failure(self, mock_bus):
        """Test failed connection to the CAN bus."""
        manager = CanBusManager()
        manager.connect()
        mock_bus.assert_called_once_with(interface="socketcan", channel="can0", bitrate=500000)
        self.assertIsNone(manager.bus)
        self.assertEqual(manager.breaker.current_state, "open")

    def test_disconnect(self):
        """Test disconnection from the CAN bus."""
        manager = CanBusManager()
        bus_mock = MagicMock()
        notifier_mock = MagicMock()
        manager.bus = bus_mock
        manager.notifier = notifier_mock
        manager.disconnect()
        bus_mock.shutdown.assert_called_once()
        notifier_mock.stop.assert_called_once()
        self.assertIsNone(manager.bus)
        self.assertIsNone(manager.notifier)
        self.assertEqual(manager.breaker.current_state, "open")

    @patch("equipment.can_interface.CanBusManager._send_message_with_retry", return_value=True)
    def test_send_reliable_message_success(self, mock_send_with_retry):
        """Test sending a reliable message successfully."""
        manager = CanBusManager()
        message = MagicMock()
        result = manager.send_reliable_message(message)
        self.assertTrue(result)
        mock_send_with_retry.assert_called_once_with(message)

    @patch("equipment.can_interface.CanBusManager._send_message_with_retry")
    def test_send_reliable_message_circuit_open(self, mock_send_with_retry):
        """Test that send_reliable_message returns False when the circuit is open."""
        manager = CanBusManager()
        manager.breaker.open()
        message = MagicMock()
        result = manager.send_reliable_message(message)
        self.assertFalse(result)
        mock_send_with_retry.assert_not_called()

    @patch("can.Notifier")
    def test_add_listener(self, mock_notifier):
        """Test adding a listener."""
        manager = CanBusManager()
        manager.bus = MagicMock()
        listener = MagicMock()
        manager.add_listener(listener)
        self.assertIsNotNone(manager.notifier)
        mock_notifier.assert_called_once_with(manager.bus, [listener])

    def test_add_listener_no_bus(self):
        """Test adding a listener when the bus is not connected."""
        manager = CanBusManager()
        listener = MagicMock()
        manager.add_listener(listener)
        self.assertIsNone(manager.notifier)

    @patch("can.Notifier")
    def test_add_listener_existing_notifier(self, mock_notifier):
        """Test adding a listener when a notifier already exists."""
        manager = CanBusManager()
        manager.bus = MagicMock()
        manager.notifier = mock_notifier
        listener = MagicMock()
        manager.add_listener(listener)
        mock_notifier.add_listener.assert_called_once_with(listener)

    def test_remove_listener(self):
        """Test removing a listener."""
        manager = CanBusManager()
        listener = MagicMock()
        notifier_mock = MagicMock()
        notifier_mock.listeners = [listener, MagicMock()]
        manager.notifier = notifier_mock
        manager.remove_listener(listener)
        notifier_mock.remove_listener.assert_called_once_with(listener)
        notifier_mock.stop.assert_not_called()

    def test_remove_listener_last(self):
        """Test removing the last listener stops the notifier."""
        manager = CanBusManager()
        listener = MagicMock()
        notifier_mock = MagicMock()
        # Configure the mock so that after removing the listener, the list is empty
        notifier_mock.listeners = []
        manager.notifier = notifier_mock

        manager.remove_listener(listener)

        notifier_mock.remove_listener.assert_called_once_with(listener)
        notifier_mock.stop.assert_called_once()
        self.assertIsNone(manager.notifier)

    def test_remove_listener_no_notifier(self):
        """Test removing a listener when there is no notifier."""
        manager = CanBusManager()
        listener = MagicMock()
        manager.remove_listener(listener)
        self.assertIsNone(manager.notifier)


if __name__ == "__main__":
    unittest.main()
