"""
Estrategias de Alerta (Patrón Strategy / OCP)
"""
from typing import Protocol

from app.repositories.base import SensorHubRepository


class AlertStrategy(Protocol):
    """Interfaz abstracta para el envío de alertas."""

    def send_alert(self, sensor_id: str, value: float, threshold: float) -> None:
        ...


class ConsoleAlertStrategy:
    """Implementación simple para desarrollo y testing (Mockeable)."""

    def send_alert(self, sensor_id: str, value: float, threshold: float) -> None:
        print(f" [ALERTA] Sensor {sensor_id} excedió el umbral ({threshold}). Lectura: {value}")


class DatabaseAlertStrategy:
    """Implementación real que guarda la alerta en la Base de Datos."""

    def __init__(self, repo: SensorHubRepository) -> None:
        self._repo = repo

    def send_alert(self, sensor_id: str, value: float, threshold: float) -> None:
        self._repo.add_alert(sensor_id, value, threshold)
        print(f" [BD] Alerta guardada para {sensor_id}: Valor {value} > Umbral {threshold}")