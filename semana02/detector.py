from dataclasses import dataclass
from typing import Any


@dataclass
class SensorReading:
    """Estructura de datos inmutable para la telemetría de un sensor."""
    sensor_id: str
    temperature: float
    humidity: float

class AnomalyDetector:
    """Motor de evaluación de reglas de negocio para anomalías ambientales."""
    
    def __init__(
        self, 
        temp_threshold: float = 35.0, 
        humidity_threshold: float = 80.0
    ) -> None:
        self.temp_threshold = temp_threshold
        self.humidity_threshold = humidity_threshold

    def evaluate(self, reading: SensorReading) -> dict[str, Any]:
        """Evalúa si la lectura excede los umbrales configurados."""
        if reading.temperature > self.temp_threshold:
            return {"is_anomaly": True, "type": "HIGH_TEMPERATURE"}
        return {"is_anomaly": False, "type": "NORMAL"}