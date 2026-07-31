from datetime import datetime

from app.models import ReadingModel
from app.repositories.base import ReadingRepository


class ReadingService:
    """Lógica de negocio pura. Ignora si usamos SQL, Mongo o memoria RAM."""
    def __init__(self, repo: ReadingRepository) -> None:
        self._repo = repo

    def record(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        if value < -273.15:
            raise ValueError("Temperatura por debajo del cero absoluto")
        return self._repo.add(sensor_id, value, unit)

    def get_sensor_readings(self, sensor_id: str, limit: int, offset: int,
                             from_date: datetime | None, 
                             to_date: datetime | None) -> list[ReadingModel]:
        return self._repo.list_for_sensor(sensor_id, limit, offset, from_date, to_date)

    def get_reading(self, reading_id: int) -> ReadingModel | None:
        return self._repo.get(reading_id)

    def update_reading(self, reading_id: int, data: dict) -> ReadingModel | None:
        return self._repo.update(reading_id, data)

    def delete_reading(self, reading_id: int) -> bool:
        return self._repo.delete(reading_id)