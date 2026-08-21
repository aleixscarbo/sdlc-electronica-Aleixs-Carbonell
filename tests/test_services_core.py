"""
Pruebas unitarias para SensorHubService.
Patrón: Arrange-Act-Assert (AAA) con mocks de SensorHubRepository.
"""

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from app.models import ReadingModel, SensorModel
from app.repositories.base import SensorHubRepository
from app.services.core import SensorHubService
from app.services.exceptions import SensorAlreadyExistsError, SensorNotFoundError


class TestCreateSensor:
    """Pruebas para create_sensor."""

    def test_create_sensor_success(self) -> None:
        mock_repo = MagicMock(spec=SensorHubRepository)
        mock_repo.get_sensor.return_value = None

        mock_sensor = MagicMock(spec=SensorModel)
        mock_sensor.id = "S1"
        mock_sensor.type = "temp"
        mock_sensor.name = "Prueba"
        mock_sensor.location = "Bodega 1"
        mock_sensor.threshold = 30.0
        mock_sensor.is_active = True
        mock_repo.add_sensor.return_value = mock_sensor

        service = SensorHubService(repo=mock_repo)

        # Act
        result = service.create_sensor("S1", "temp", "Prueba", "Bodega 1", 30.0)

        # Assert
        assert result.id == "S1"
        assert result.location == "Bodega 1"
        mock_repo.add_sensor.assert_called_once_with(
            "S1", "temp", "Prueba", "Bodega 1", 30.0
        )

    def test_create_sensor_already_exists(self) -> None:
        mock_repo = MagicMock(spec=SensorHubRepository)
        mock_sensor = MagicMock(spec=SensorModel)
        mock_sensor.id = "S1"
        mock_repo.get_sensor.return_value = mock_sensor

        service = SensorHubService(repo=mock_repo)

        with pytest.raises(SensorAlreadyExistsError):
            service.create_sensor("S1", "temp", "Prueba", "Bodega 1", 30.0)


class TestGetSensor:
    """Pruebas para consulta de sensores."""

    def test_get_sensor(self) -> None:
        mock_repo = MagicMock(spec=SensorHubRepository)
        mock_sensor = MagicMock(spec=SensorModel)
        mock_repo.get_sensor.return_value = mock_sensor

        service = SensorHubService(repo=mock_repo)
        assert service.get_sensor("S1") is mock_sensor
        mock_repo.get_sensor.assert_called_once_with("S1")

    def test_get_all_sensors(self) -> None:
        mock_repo = MagicMock(spec=SensorHubRepository)
        mock_repo.list_sensors.return_value = []

        service = SensorHubService(repo=mock_repo)
        assert service.get_all_sensors(50, 0) == []
        mock_repo.list_sensors.assert_called_once_with(50, 0)


class TestRemoveSensor:
    """Pruebas para remove_sensor (ahora verifica Soft Delete por medio del repo)."""

    def test_remove_sensor_success(self) -> None:
        mock_repo = MagicMock(spec=SensorHubRepository)
        mock_repo.delete_sensor.return_value = True

        service = SensorHubService(repo=mock_repo)
        assert service.remove_sensor("S1") is True
        mock_repo.delete_sensor.assert_called_once_with("S1")

    def test_remove_sensor_not_found(self) -> None:
        mock_repo = MagicMock(spec=SensorHubRepository)
        mock_repo.delete_sensor.return_value = False

        service = SensorHubService(repo=mock_repo)
        assert service.remove_sensor("S1") is False


class TestRecordReading:
    """Pruebas para record_reading y disparo de alertas."""

    def test_record_reading_raises_when_sensor_does_not_exist(self) -> None:
        mock_repo = MagicMock(spec=SensorHubRepository)
        mock_repo.get_sensor.return_value = None

        service = SensorHubService(repo=mock_repo)

        with pytest.raises(SensorNotFoundError, match="El sensor 'S1' no existe."):
            service.record_reading(sensor_id="S1", value=25.5, unit="C")

    def test_record_reading_success_no_alert(self) -> None:
        mock_repo = MagicMock(spec=SensorHubRepository)
        mock_sensor = MagicMock(spec=SensorModel)
        mock_sensor.threshold = 50.0  # Umbral alto
        mock_repo.get_sensor.return_value = mock_sensor

        mock_reading = MagicMock(spec=ReadingModel)
        mock_repo.add_reading.return_value = mock_reading

        mock_strategy = MagicMock()

        service = SensorHubService(repo=mock_repo, alert_strategy=mock_strategy)
        result = service.record_reading("S1", 25.5, "C")  # Lectura baja, no hay alerta

        assert result is mock_reading
        mock_repo.add_reading.assert_called_once_with("S1", 25.5, "C")
        mock_strategy.notify.assert_not_called()

    def test_record_reading_triggers_alert(self) -> None:
        mock_repo = MagicMock(spec=SensorHubRepository)
        mock_sensor = MagicMock(spec=SensorModel)
        mock_sensor.threshold = 30.0  # Umbral bajo
        mock_repo.get_sensor.return_value = mock_sensor

        mock_strategy = MagicMock()
        service = SensorHubService(repo=mock_repo, alert_strategy=mock_strategy)

        service.record_reading("S1", 35.0, "C")  # Supera el umbral

        # Asegura que la alerta se disparó correctamente
        mock_strategy.notify.assert_called_once_with("S1", 35.0, 30.0)


class TestGetSensorReadings:
    """Pruebas para listado de lecturas."""

    def test_get_sensor_readings_success(self) -> None:
        mock_repo = MagicMock(spec=SensorHubRepository)
        mock_repo.get_sensor.return_value = MagicMock(spec=SensorModel)
        mock_repo.list_readings.return_value = []

        service = SensorHubService(repo=mock_repo)
        dt = datetime.now()

        result = service.get_sensor_readings("S1", 50, 0, dt, dt)
        assert result == []
        mock_repo.list_readings.assert_called_once_with("S1", 50, 0, dt, dt)

    def test_get_sensor_readings_sensor_not_found(self) -> None:
        mock_repo = MagicMock(spec=SensorHubRepository)
        mock_repo.get_sensor.return_value = None

        service = SensorHubService(repo=mock_repo)
        with pytest.raises(SensorNotFoundError):
            service.get_sensor_readings("S1", 50, 0, None, None)


class TestReadingOperations:
    """Pruebas para CRUD individual de lecturas."""

    def test_get_reading(self) -> None:
        mock_repo = MagicMock(spec=SensorHubRepository)
        mock_repo.get_reading.return_value = MagicMock(spec=ReadingModel)
        service = SensorHubService(repo=mock_repo)

        assert service.get_reading(1) is not None
        mock_repo.get_reading.assert_called_once_with(1)

    def test_update_reading(self) -> None:
        mock_repo = MagicMock(spec=SensorHubRepository)
        mock_repo.update_reading.return_value = MagicMock(spec=ReadingModel)
        service = SensorHubService(repo=mock_repo)

        assert service.update_reading(1, {"value": 10}) is not None
        mock_repo.update_reading.assert_called_once_with(1, {"value": 10})

    def test_delete_reading(self) -> None:
        mock_repo = MagicMock(spec=SensorHubRepository)
        mock_repo.delete_reading.return_value = True
        service = SensorHubService(repo=mock_repo)

        assert service.delete_reading(1) is True
        mock_repo.delete_reading.assert_called_once_with(1)
