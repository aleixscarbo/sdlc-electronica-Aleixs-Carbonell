"""
Estrategias de Alerta (Patrón Strategy / OCP)
"""
from typing import Protocol

class AlertStrategy(Protocol):
    """Interfaz abstracta para el envío de alertas."""
    def send_alert(self, sensor_id: str, value: float, threshold: float) -> None:
        ...

class ConsoleAlertStrategy:
    """Implementación simple para desarrollo y testing (Mockeable)."""
    def send_alert(self, sensor_id: str, value: float, threshold: float) -> None:
        print(f"⚠️ [ALERTA] Sensor {sensor_id} excedió el umbral ({threshold}). Lectura: {value}")