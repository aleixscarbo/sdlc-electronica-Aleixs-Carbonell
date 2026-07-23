class SensorNotFoundError(Exception):
    pass

class SensorRegistry:
    def __init__(self):
        self._sensors = {}  # Simulamos una base de datos en memoria

    def get(self, sensor_id):
        if sensor_id not in self._sensors:
            raise SensorNotFoundError(f"Sensor no registrado: {sensor_id}")
        return self._sensors[sensor_id]