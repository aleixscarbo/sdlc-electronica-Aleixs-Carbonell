"""
Pruebas unitarias para SensorHubService.
Patrón: Arrange-Act-Assert (AAA) con mocks de SensorHubRepository.
"""

import math
from unittest.mock import MagicMock

import pytest

from app.models import ReadingModel, SensorModel
from app.repositories.base import SensorHubRepository
from app.services.core import SensorHubService


class TestRecordReadingSensorNotFound:
    """Test 1: record_reading lanza ValueError si el sensor no existe."""

    def test_record_reading_raises_when_sensor_does_not_exist(self) -> None:
        # Arrange: Crear mock del repositorio y simular que get_sensor retorna None
        mock_repo: MagicMock = MagicMock(spec=SensorHubRepository)
        mock_repo.get_sensor.return_value = None
        
        service: SensorHubService = SensorHubService(repo=mock_repo)
        sensor_id: str = "nonexistent_sensor"
        value: float = 25.5
        unit: str = "C"

        # Act & Assert: Verificar que se lanza ValueError
        with pytest.raises(ValueError, 
                           match="El sensor 'nonexistent_sensor' no existe"):
            service.record_reading(sensor_id=sensor_id, value=value, unit=unit)

        # Assert: Verificar que get_sensor fue llamado exactamente una vez
        mock_repo.get_sensor.assert_called_once_with(sensor_id)
        # Verificar que add_reading NUNCA fue llamado
        mock_repo.add_reading.assert_not_called()


class TestGetSensorReadingsSensorNotFound:
    """Test 2: get_sensor_readings lanza ValueError si el sensor no existe."""

    def test_get_sensor_readings_raises_when_sensor_does_not_exist(self) -> None:
        # Arrange: Crear mock del repositorio
        mock_repo: MagicMock = MagicMock(spec=SensorHubRepository)
        mock_repo.get_sensor.return_value = None
        
        service: SensorHubService = SensorHubService(repo=mock_repo)
        sensor_id: str = "nonexistent_sensor"
        limit: int = 10
        offset: int = 0

        # Act & Assert: Verificar que se lanza ValueError
        with pytest.raises(ValueError, 
                           match="El sensor 'nonexistent_sensor' no existe"):
            service.get_sensor_readings(
                sensor_id=sensor_id,
                limit=limit,
                offset=offset,
                from_date=None,
                to_date=None,
            )

        # Assert: Verificar que get_sensor fue llamado una vez
        mock_repo.get_sensor.assert_called_once_with(sensor_id)
        # Verificar que list_readings NUNCA fue llamado
        mock_repo.list_readings.assert_not_called()


class TestCreateSensorAlreadyExists:
    """Test 3: create_sensor lanza ValueError si el ID ya existe."""

    def test_create_sensor_raises_when_sensor_already_exists(self) -> None:
        # Arrange: Crear mock que simula sensor existente
        mock_repo: MagicMock = MagicMock(spec=SensorHubRepository)
        existing_sensor: SensorModel = MagicMock(spec=SensorModel)
        existing_sensor.id = "SENSOR-001"
        existing_sensor.type = "temperature"
        existing_sensor.name = "Room Temperature"
        
        mock_repo.get_sensor.return_value = existing_sensor
        
        service: SensorHubService = SensorHubService(repo=mock_repo)
        sensor_id: str = "SENSOR-001"
        sensor_type: str = "temperature"
        sensor_name: str = "Duplicate Sensor"

        # Act & Assert: Verificar que se lanza ValueError
        with pytest.raises(ValueError, match="El sensor con ID 'SENSOR-001' ya existe"):
            service.create_sensor(
                sensor_id=sensor_id,
                type=sensor_type,
                name=sensor_name,
            )

        # Assert: Verificar que get_sensor fue llamado una vez
        mock_repo.get_sensor.assert_called_once_with(sensor_id)
        # Verificar que add_sensor NUNCA fue llamado
        mock_repo.add_sensor.assert_not_called()


class TestRecordReadingInfiniteValue:
    """Test 4: Validar que record_reading maneja valor infinito."""

    def test_record_reading_with_positive_infinity_value(self) -> None:
        # Arrange: Crear mock del repositorio con sensor existente
        mock_repo: MagicMock = MagicMock(spec=SensorHubRepository)
        existing_sensor: SensorModel = MagicMock(spec=SensorModel)
        existing_sensor.id = "SENSOR-001"
        mock_repo.get_sensor.return_value = existing_sensor
        
        # Simular que add_reading retorna una lectura
        reading: ReadingModel = MagicMock(spec=ReadingModel)
        reading.id = 1
        reading.value = float("inf")
        mock_repo.add_reading.return_value = reading
        
        service: SensorHubService = SensorHubService(repo=mock_repo)
        sensor_id: str = "SENSOR-001"
        value: float = float("inf")
        unit: str = "C"

        # Act: Llamar a record_reading con valor infinito
        result: ReadingModel = service.record_reading(
            sensor_id=sensor_id,
            value=value,
            unit=unit,
        )

        # Assert: Verificar que se llamó a add_reading (actualmente sin validación)
        assert result.value == float("inf")
        mock_repo.get_sensor.assert_called_once_with(sensor_id)
        mock_repo.add_reading.assert_called_once_with(sensor_id, value, unit)

    def test_record_reading_with_nan_value(self) -> None:
        # Arrange: Crear mock del repositorio con sensor existente
        mock_repo: MagicMock = MagicMock(spec=SensorHubRepository)
        existing_sensor: SensorModel = MagicMock(spec=SensorModel)
        existing_sensor.id = "SENSOR-001"
        mock_repo.get_sensor.return_value = existing_sensor
        
        # Simular que add_reading retorna una lectura
        reading: ReadingModel = MagicMock(spec=ReadingModel)
        reading.id = 2
        reading.value = float("nan")
        mock_repo.add_reading.return_value = reading
        
        service: SensorHubService = SensorHubService(repo=mock_repo)
        sensor_id: str = "SENSOR-001"
        value: float = float("nan")
        unit: str = "C"

        # Act: Llamar a record_reading con valor NaN
        result: ReadingModel = service.record_reading(
            sensor_id=sensor_id,
            value=value,
            unit=unit,
        )

        # Assert: Verificar que se llamó a add_reading (actualmente sin validación)
        assert math.isnan(result.value)
        mock_repo.get_sensor.assert_called_once_with(sensor_id)
        mock_repo.add_reading.assert_called_once_with(sensor_id, value, unit)


class TestRemoveSensorCallsRepository:
    """Test 5: remove_sensor llama correctamente a repo.delete_sensor."""

    def test_remove_sensor_calls_repository_delete_sensor(self) -> None:
        # Arrange: Crear mock que simula eliminación exitosa
        mock_repo: MagicMock = MagicMock(spec=SensorHubRepository)
        mock_repo.delete_sensor.return_value = True
        
        service: SensorHubService = SensorHubService(repo=mock_repo)
        sensor_id: str = "SENSOR-001"

        # Act: Llamar a remove_sensor
        result: bool = service.remove_sensor(sensor_id=sensor_id)

        # Assert: Verificar que el resultado es True
        assert result is True
        # Verificar que delete_sensor fue llamado exactamente una vez con el sensor_id
        mock_repo.delete_sensor.assert_called_once_with(sensor_id)

    def test_remove_sensor_returns_false_when_not_found(self) -> None:
        # Arrange: Crear mock que simula sensor no encontrado
        mock_repo: MagicMock = MagicMock(spec=SensorHubRepository)
        mock_repo.delete_sensor.return_value = False
        
        service: SensorHubService = SensorHubService(repo=mock_repo)
        sensor_id: str = "nonexistent_sensor"

        # Act: Llamar a remove_sensor
        result: bool = service.remove_sensor(sensor_id=sensor_id)

        # Assert: Verificar que el resultado es False
        assert result is False
        # Verificar que delete_sensor fue llamado una vez
        mock_repo.delete_sensor.assert_called_once_with(sensor_id)
