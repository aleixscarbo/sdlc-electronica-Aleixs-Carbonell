from typing import Protocol

from app.models import ReadingModel


class ReadingRepository(Protocol):
    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        ...

    def list_for_sensor(self, sensor_id: str) -> list[ReadingModel]:
        ...