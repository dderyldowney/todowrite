import pytest
from afs_fastapi.services.cloud_integration import CloudIntegrationService

@pytest.fixture
def mock_config():
    return {
        "platform": "TestCloud",
        "endpoint": "https://test.cloud.com",
        "api_key": "test_key"
    }

@pytest.fixture
def service(mock_config):
    return CloudIntegrationService(mock_config)

def test_service_initialization(service, mock_config):
    assert service.config == mock_config
    assert not service.connected

def test_connect_success(service):
    assert service.connect()
    assert service.connected

def test_connect_failure_missing_config():
    service = CloudIntegrationService({"platform": "TestCloud"})
    assert not service.connect()
    assert not service.connected

def test_disconnect_success(service):
    service.connect()
    assert service.connected
    assert service.disconnect()
    assert not service.connected

def test_disconnect_not_connected(service):
    assert not service.connected
    assert service.disconnect() # Should return True as it's effectively disconnected
    assert not service.connected

def test_send_telemetry_data_success(service):
    service.connect()
    data = {"robot_id": "R1", "temp": 25.0}
    assert service.send_telemetry_data(data)

def test_send_telemetry_data_not_connected(service):
    data = {"robot_id": "R1", "temp": 25.0}
    assert not service.send_telemetry_data(data)

def test_receive_commands_success(service):
    service.connect()
    commands = service.receive_commands()
    assert "command" in commands
    assert "parameters" in commands

def test_receive_commands_not_connected(service):
    commands = service.receive_commands()
    assert commands == {}
