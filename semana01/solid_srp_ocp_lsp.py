from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class SensorReading:
    sensor_id: str
    value: float

# =====================================================================
# 1. PRINCIPIO DE RESPONSABILIDAD ÚNICA (SRP)
# =====================================================================

# ❌ MAL: Esta clase lee hardware virtual Y además guarda en archivos (Dos responsabilidades)
class ViolacionSRP:
    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id

    def read_and_save(self) -> str:
        # Simula lectura de hardware
        reading = f"{self.sensor_id},25.0"
        # Persistencia acoplada
        with open("log_srp_mal.txt", "w") as f:
            f.write(reading)
        return reading

#  BIEN: Separación absoluta de preocupaciones
class SensorReader:
    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id

    def get_reading(self) -> SensorReading:
        return SensorReading(self.sensor_id, 25.0)

class DataLogger:
    def save(self, reading: SensorReading) -> str:
        payload = f"{reading.sensor_id}:{reading.value}"
        # Simulación de persistencia limpia
        return f"Persistido con éxito: {payload}"


# =====================================================================
# 2. PRINCIPIO DE ABIERTO/CERRADO (OCP)
# =====================================================================

# ❌ MAL: Si queremos agregar alertas por Email, tenemos que modificar esta clase (rompe OCP)
class ViolacionOCP:
    def __init__(self, alert_type: str, threshold: float) -> None:
        self.alert_type = alert_type
        self.threshold = threshold

    def check_reading(self, reading: SensorReading) -> str:
        if reading.value > self.threshold:
            if self.alert_type == "CONSOLE":
                return f"Console Alert: Anomalia en {reading.sensor_id}"
            elif self.alert_type == "FILE":
                return f"File Alert: Anomalia en {reading.sensor_id}"
        return "Normal"

#  BIEN: Abierto a la extensión mediante polimorfismo
class AlertStrategy(ABC):
    @abstractmethod
    def send(self, message: str) -> str: ...

class ConsoleAlert(AlertStrategy):
    def send(self, message: str) -> str:
        return f"Console: {message}"

class FileAlert(AlertStrategy):
    def send(self, message: str) -> str:
        return f"File Log: {message}"

class AnomalyDetector:
    def __init__(self, alert: AlertStrategy, threshold: float) -> None:
        self._alert = alert
        self._threshold = threshold

    def check(self, reading: SensorReading) -> str:
        if reading.value > self._threshold:
            return self._alert.send(f"Anomalia en {reading.sensor_id}")
        return "Normal"


# =====================================================================
# 3. PRINCIPIO DE SUSTITUCIÓN DE LISKOV (LSP)
# =====================================================================

class BaseSensor(ABC):
    @abstractmethod
    def read(self) -> float: ...

# ❌ MAL: Modifica radicalmente el comportamiento esperado lanzando una excepción inesperada
class ViolacionLSP(BaseSensor):
    def read(self) -> float:
        # Provoca un crash si el sistema intenta leerlo de forma genérica
        raise RuntimeError("Error crítico de hardware de calibración")

#  BIEN: Ambas subclases se comportan exactamente como el padre estipula
class TemperatureSensor(BaseSensor):
    def read(self) -> float:
        return 36.5

class HumiditySensor(BaseSensor):
    def read(self) -> float:
        return 60.2

def process_sensor(sensor: BaseSensor) -> float:
    """Esta función opera de manera segura bajo LSP con cualquier subclase."""
    return sensor.read()