from typing import Any

from detector import SensorReading


class SensorNotFoundError(Exception):
    """Excepción lanzada cuando se busca un sensor que no existe."""
    pass


class SensorRegistry:
    """Almacén en memoria para el historial de telemetría de los sensores."""

    def __init__(self) -> None:
        # Diccionario que mapea un ID de sensor a su lista de lecturas
        self._data: dict[str, list[SensorReading]] = {}

    def get_sensor(self, sensor_id: str) -> Any:
        """Recupera el historial de un sensor o lanza una excepción si no existe."""
        if sensor_id not in self._data:
            raise SensorNotFoundError(f"El sensor {sensor_id} no está registrado.")
        return self._data[sensor_id]

    def add_reading(self, reading: SensorReading) -> None:
        """Registra una nueva lectura en el historial del sensor correspondiente."""
        if reading.sensor_id not in self._data:
            self._data[reading.sensor_id] = []
        self._data[reading.sensor_id].append(reading)