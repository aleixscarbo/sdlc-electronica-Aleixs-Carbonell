from datetime import datetime

from app.models import ReadingModel, SensorModel
from app.repositories.base import SensorHubRepository


class SensorHubService:
    """Lógica de negocio central. Audita la integridad relacional."""
    def __init__(self, repo: SensorHubRepository) -> None:
        self._repo = repo

    # --- SENSORES ---
    def create_sensor(self, sensor_id: str, type: str, name: str) -> SensorModel:
        if self._repo.get_sensor(sensor_id):
            raise ValueError(f"El sensor con ID '{sensor_id}' ya existe.")
        return self._repo.add_sensor(sensor_id, type, name)

    def get_sensor(self, sensor_id: str) -> SensorModel | None:
        return self._repo.get_sensor(sensor_id)

    def get_all_sensors(self, limit: int, offset: int) -> list[SensorModel]:
        return self._repo.list_sensors(limit, offset)

    def remove_sensor(self, sensor_id: str) -> bool:
        return self._repo.delete_sensor(sensor_id)

    # --- LECTURAS ---
    def record_reading(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        # Validación de integridad relacional: ¿Existe el sensor?
        if not self._repo.get_sensor(sensor_id):
            raise ValueError(f"El sensor '{sensor_id}' no existe. Créalo primero.")
        # (Nota: La validación termodinámica ya la hizo Pydantic en los Schemas)
        return self._repo.add_reading(sensor_id, value, unit)

    def get_sensor_readings(self, sensor_id: str, limit: int, offset: int, 
                            from_date: datetime | None, 
                            to_date: datetime | None) -> list[ReadingModel]:
        if not self._repo.get_sensor(sensor_id):
            raise ValueError(f"El sensor '{sensor_id}' no existe.")
        return self._repo.list_readings(sensor_id, limit, offset, from_date, to_date)

    def get_reading(self, reading_id: int) -> ReadingModel | None:
        return self._repo.get_reading(reading_id)

    def update_reading(self, reading_id: int, data: dict) -> ReadingModel | None:
        return self._repo.update_reading(reading_id, data)

    def remove_reading(self, reading_id: int) -> bool:
        return self._repo.delete_reading(reading_id)