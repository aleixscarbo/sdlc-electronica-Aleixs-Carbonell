from datetime import datetime
from typing import Protocol

from app.models import ReadingModel


class ReadingRepository(Protocol):
    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        ...

    def list_for_sensor(self, sensor_id: str, limit: int = 50, offset: int = 0,
                         from_date: datetime | None = None, 
                         to_date: datetime | None = None) -> list[ReadingModel]:
        ...
        
    def get(self, reading_id: int) -> ReadingModel | None:
        ...
        
    def update(self, reading_id: int, data: dict) -> ReadingModel | None:
        ...
        
    def delete(self, reading_id: int) -> bool:
        ...