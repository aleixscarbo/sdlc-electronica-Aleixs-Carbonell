# app/services/exceptions.py


class SensorNotFoundError(Exception):
    """Lanzada cuando un sensor no existe en la base de datos."""

    def __init__(self, sensor_id: str):
        self.sensor_id = sensor_id
        super().__init__(f"El sensor '{sensor_id}' no existe.")


class SensorAlreadyExistsError(Exception):
    """Lanzada cuando se intenta crear un sensor que ya existe."""

    def __init__(self, sensor_id: str):
        self.sensor_id = sensor_id
        super().__init__(f"El sensor con ID '{sensor_id}' ya existe.")
