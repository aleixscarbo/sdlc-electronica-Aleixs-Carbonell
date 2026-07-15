import json
from dataclasses import dataclass, replace
from enum import Enum, auto
from typing import Protocol

# 1. Definición de Tipos (Enums)
class SensorType(Enum):
    TEMPERATURE = auto()
    HUMIDITY = auto()

# 2. Dataclass Inmutable (Estructura de datos)
@dataclass(frozen=True)
class Reading:
    sensor_id: str
    value: float
    sensor_type: SensorType

# 3. Protocolo (Interfaz)
class Transport(Protocol):
    def send(self, payload: bytes) -> None: ...

# --- EJERCICIO: 5 FUNCIONES PURAS ---

# Función Pura 0 (Ejemplo base): Serialización a bytes
def to_frame(r: Reading) -> bytes:
    return f"{r.sensor_id}:{r.value:.2f}".encode()

# Función Pura 1: Conversión de Unidades (Celsius a Fahrenheit)
def to_fahrenheit(r: Reading) -> float:
    if r.sensor_type != SensorType.TEMPERATURE:
        raise ValueError("Conversión solo válida para temperatura.")
    return (r.value * 9 / 5) + 32.0

# Función Pura 2: Detección de Umbral (Alarma de hardware)
def is_over_threshold(r: Reading, threshold: float = 40.0) -> bool:
    return r.value > threshold

# Función Pura 3: Serialización a JSON (Ideal para APIs)
def to_json(r: Reading) -> str:
    # r.sensor_type.name extrae el string "TEMPERATURE" o "HUMIDITY"
    payload = {
        "id": r.sensor_id,
        "value": round(r.value, 2),
        "type": r.sensor_type.name
    }
    return json.dumps(payload)

# Función Pura 4: Calibración por Offset
def apply_offset(r: Reading, offset: float) -> Reading:
    # Como la dataclass es 'frozen', no podemos hacer r.value += offset.
    # Usamos la función 'replace' nativa de Python para generar un objeto nuevo.
    return replace(r, value=r.value + offset)

# Función Pura 5: Validación de Nomenclatura del Sensor
def is_valid_sensor(r: Reading) -> bool:
    # Un sensor válido en nuestra planta debe empezar con "SNS-"
    return r.sensor_id.startswith("SNS-")