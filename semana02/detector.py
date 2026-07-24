from dataclasses import dataclass

@dataclass
class SensorReading:
    sensor_id: str
    temperature: float
    humidity: float

class AnomalyDetector:
    def __init__(self, temp_threshold: float, humidity_threshold: float):
        self.temp_threshold = temp_threshold
        self.humidity_threshold = humidity_threshold

    def evaluate(self, reading: SensorReading):
        if reading.temperature > self.temp_threshold:
            return {"is_anomaly": True, "type": "HIGH_TEMPERATURE"}
        return {"is_anomaly": False, "type": "NORMAL"}