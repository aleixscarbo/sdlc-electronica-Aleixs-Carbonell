import datetime
from abc import ABC, abstractmethod


class AlertStrategy(ABC):
    """Interfaz abstracta para el envío de alertas (Patrón Strategy)."""
    
    @abstractmethod
    def send_alert(self, sensor_id: str, anomaly_type: str) -> None:
        pass


class ConsoleAlertStrategy(AlertStrategy):
    """Implementación concreta que emite alertas por la salida estándar."""
    
    def send_alert(self, sensor_id: str, anomaly_type: str) -> None:
        print(f"[CRITICAL] {sensor_id}: Anomalía detectada ({anomaly_type})")


class FileAlertStrategy(AlertStrategy):
    """Implementación concreta que persiste alertas en un archivo log."""
    
    def __init__(self, filepath: str = "alerts.log") -> None:
        self.filepath = filepath

    def send_alert(self, sensor_id: str, anomaly_type: str) -> None:
        timestamp = datetime.datetime.now().isoformat()
        with open(self.filepath, "a", encoding="utf-8") as file:
            file.write(f"[{timestamp}] - ALERTA - {sensor_id} - {anomaly_type}\n")


class AlertManager:
    """Gestor de contexto que utiliza una estrategia de alerta inyectada."""
    
    def __init__(self, strategy: AlertStrategy) -> None:
        self.strategy = strategy

    def process_anomaly(self, sensor_id: str, anomaly_type: str) -> None:
        """Despacha la alerta usando la estrategia configurada."""
        self.strategy.send_alert(sensor_id, anomaly_type)