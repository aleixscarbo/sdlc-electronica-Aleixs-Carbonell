"""
Pruebas Unitarias para Detección de Anomalías (TDD - Fase RED)
"""
import pytest
from unittest.mock import MagicMock

from app.services.core import SensorHubService
from app.repositories.base import SensorHubRepository
from app.models import SensorModel

def test_record_reading_triggers_alert_when_exceeding_threshold() -> None:
    # Arrange: Simulamos un sensor con un umbral (threshold) de 30.0
    mock_repo = MagicMock(spec=SensorHubRepository)
    mock_sensor = MagicMock(spec=SensorModel)
    mock_sensor.id = "SENSOR-01"
    mock_sensor.threshold = 30.0 
    mock_repo.get_sensor.return_value = mock_sensor
    
    # Simulamos nuestra estrategia de alertas
    mock_alert_strategy = MagicMock()
    
    # Inyectamos el repositorio y la estrategia en el servicio
    service = SensorHubService(repo=mock_repo, alert_strategy=mock_alert_strategy)
    
    # Act: Registramos una lectura de 35.5 (SUPERIOR al umbral)
    service.record_reading(sensor_id="SENSOR-01", value=35.5, unit="C")
    
    # Assert: La estrategia debió haber sido llamada para enviar la alerta
    mock_alert_strategy.send_alert.assert_called_once()

def test_record_reading_no_alert_when_below_threshold() -> None:
    # Arrange: Simulamos un sensor con un umbral de 30.0
    mock_repo = MagicMock(spec=SensorHubRepository)
    mock_sensor = MagicMock(spec=SensorModel)
    mock_sensor.id = "SENSOR-01"
    mock_sensor.threshold = 30.0 
    mock_repo.get_sensor.return_value = mock_sensor
    
    mock_alert_strategy = MagicMock()
    service = SensorHubService(repo=mock_repo, alert_strategy=mock_alert_strategy)
    
    # Act: Registramos una lectura de 25.0 (INFERIOR al umbral)
    service.record_reading(sensor_id="SENSOR-01", value=25.0, unit="C")
    
    # Assert: La estrategia NO debió haber sido llamada
    mock_alert_strategy.send_alert.assert_not_called()