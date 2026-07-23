from typing import Dict, Any

class SensorNotFoundError(Exception):
    """Excepción lanzada cuando se consulta un sensor inexistente."""
    pass

class SensorRegistry:
    def __init__(self) -> None:
        # Diccionario fuertemente tipado
        self._sensors: Dict[str, Any] = {}

    def get(self, sensor_id: str) -> Any:
        """
        Recupera un sensor por su ID.
        Lanza SensorNotFoundError si no existe.
        """
        if sensor_id not in self._sensors:
            raise SensorNotFoundError(f"Sensor no registrado: {sensor_id}")
        return self._sensors[sensor_id]