"""
Estrategias de Alerta (Patrón Strategy / OCP)
"""
from typing import Protocol

from app.logger import logger
from app.repositories.base import SensorHubRepository


class AlertNotificationStrategy(Protocol):
    """Interfaz abstracta para el envío de alertas."""

    def notify(self, sensor_id: str, value: float, threshold: float) -> None:
        ...


class ConsoleAlertStrategy:
    """Implementación simple para desarrollo y testing (Mockeable)."""

    def notify(self, sensor_id: str, value: float, threshold: float) -> None:
        logger.info(
            f"[ALERTA] Sensor {sensor_id} excedió el umbral ({threshold}). Lectura: {value}"
        )


class DatabaseAlertStrategy:
    """Implementación real que guarda la alerta en la Base de Datos."""

    def __init__(self, repo: SensorHubRepository) -> None:
        self._repo = repo

    def notify(self, sensor_id: str, value: float, threshold: float) -> None:
        self._repo.add_alert(sensor_id, value, threshold)
        logger.warning(
            f"[BD] Alerta guardada para {sensor_id}: Valor {value} > Umbral {threshold}"
        )