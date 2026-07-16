from abc import ABC, abstractmethod
from typing import Protocol
from dataclasses import dataclass

@dataclass(frozen=True)
class SensorReading:
    sensor_id: str
    value: float

# =====================================================================
# 1. PRINCIPIO DE SEGREGACIÓN DE INTERFACES (ISP)
# =====================================================================

# ❌ MAL: Interfaz "gorda" o monolítica
class FatSensorInterface(ABC):
    @abstractmethod
    def read(self) -> float: ...
    @abstractmethod
    def write(self, data: float) -> None: ...
    @abstractmethod
    def calibrate(self) -> None: ...
    @abstractmethod
    def reset(self) -> None: ...

#  BIEN: Interfaces segregadas (pequeñas y específicas)
class Readable(ABC):
    @abstractmethod
    def read(self) -> float: ...

class Writable(ABC):
    @abstractmethod
    def write(self, data: float) -> None: ...

class Calibratable(ABC):
    @abstractmethod
    def calibrate(self) -> None: ...

# Aplicación: Un sensor simple solo hereda lo que necesita
class SimpleTempSensor(Readable):
    def read(self) -> float:
        return 22.5

# Aplicación: Un actuador complejo puede heredar múltiples interfaces
class SmartThermostat(Readable, Writable, Calibratable):
    def __init__(self) -> None:
        self.temp = 22.5

    def read(self) -> float:
        return self.temp

    def write(self, data: float) -> None:
        self.temp = data

    def calibrate(self) -> None:
        self.temp = 0.0


# =====================================================================
# 2. PRINCIPIO DE INVERSIÓN DE DEPENDENCIAS (DIP)
# =====================================================================

# Abstracción (El "Socket" I2C/SPI de nuestro software)
class DataRepository(Protocol):
    def save(self, reading: SensorReading) -> None: ...
    def get_latest(self, sensor_id: str) -> SensorReading | None: ...

# Módulo de Alto Nivel
class DataProcessor:
    """Depende de la abstraccion (Protocol), no de una implementacion concreta."""
    def __init__(self, repository: DataRepository) -> None:
        self._repo = repository  # Inyección de dependencias

    def process_and_save(self, reading: SensorReading) -> None:
        # Aquí iría lógica compleja (ej. promedios, validaciones)
        self._repo.save(reading)

    def retrieve_last(self, sensor_id: str) -> SensorReading | None:
        return self._repo.get_latest(sensor_id)

# Módulo de Bajo Nivel (Implementación real para Tests)
class InMemoryRepository:
    """Base de datos falsa que vive en la memoria RAM (Ideal para pruebas rápidas)."""
    def __init__(self) -> None:
        self.db: dict[str, SensorReading] = {}

    def save(self, reading: SensorReading) -> None:
        self.db[reading.sensor_id] = reading

    def get_latest(self, sensor_id: str) -> SensorReading | None:
        return self.db.get(sensor_id)