"""
Pruebas Unitarias para Detección de Anomalías (TDD - Fase RED/GREEN)
"""

from unittest.mock import MagicMock

from app.models import SensorModel
from app.repositories.base import SensorHubRepository
from app.services.alerts import AlertNotificationStrategy
from app.services.core import SensorHubService


# 1. Creamos nuestro Spy personalizado
class SpyAlertStrategy(AlertNotificationStrategy):
    def __init__(self) -> None:
        self.alerts_sent: list[tuple[str, float, float]] = []

    def notify(self, sensor_id: str, value: float, threshold: float) -> None:
        self.alerts_sent.append((sensor_id, value, threshold))


def test_record_reading_triggers_alert_when_exceeding_threshold() -> None:
    mock_repo = MagicMock(spec=SensorHubRepository)
    mock_sensor = MagicMock(spec=SensorModel)
    mock_sensor.id = "SENSOR-01"
    mock_sensor.threshold = 30.0
    mock_sensor.location = "Bodega 1"  # <--- AÑADIDO
    mock_sensor.is_active = True  # <--- AÑADIDO
    mock_repo.get_sensor.return_value = mock_sensor

    spy_strategy = SpyAlertStrategy()
    service = SensorHubService(repo=mock_repo, alert_strategy=spy_strategy)

    service.record_reading(sensor_id="SENSOR-01", value=35.5, unit="C")

    # Verificamos la aserción usando nuestro Spy
    assert len(spy_strategy.alerts_sent) == 1
    assert spy_strategy.alerts_sent[0] == ("SENSOR-01", 35.5, 30.0)


def test_record_reading_no_alert_when_below_threshold() -> None:
    mock_repo = MagicMock(spec=SensorHubRepository)
    mock_sensor = MagicMock(spec=SensorModel)
    mock_sensor.id = "SENSOR-01"
    mock_sensor.threshold = 50.0
    mock_sensor.location = "Bodega 1"  # <--- AÑADIDO
    mock_sensor.is_active = True  # <--- AÑADIDO
    mock_repo.get_sensor.return_value = mock_sensor

    spy_strategy = SpyAlertStrategy()
    service = SensorHubService(repo=mock_repo, alert_strategy=spy_strategy)

    service.record_reading(sensor_id="SENSOR-01", value=45.0, unit="C")

    assert len(spy_strategy.alerts_sent) == 0
