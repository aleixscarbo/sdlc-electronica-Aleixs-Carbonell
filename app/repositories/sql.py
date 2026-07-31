from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ReadingModel
from app.repositories.base import ReadingRepository


class SQLReadingRepository(ReadingRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(sensor_id=sensor_id, value=value, unit=unit)
        self.session.add(reading)
        self.session.commit()
        self.session.refresh(reading)
        return reading

    def list_for_sensor(self, sensor_id: str, limit: int = 50, offset: int = 0,
                         from_date: datetime | None = None, 
                         to_date: datetime | None = None) -> list[ReadingModel]:
        stmt = select(ReadingModel).where(ReadingModel.sensor_id == sensor_id)
        if from_date:
            stmt = stmt.where(ReadingModel.created_at >= from_date)
        if to_date:
            stmt = stmt.where(ReadingModel.created_at <= to_date)
        stmt = stmt.offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def get(self, reading_id: int) -> ReadingModel | None:
        return self.session.get(ReadingModel, reading_id)

    def update(self, reading_id: int, data: dict) -> ReadingModel | None:
        reading = self.get(reading_id)
        if reading:
            for key, val in data.items():
                setattr(reading, key, val)
            self.session.commit()
            self.session.refresh(reading)
        return reading

    def delete(self, reading_id: int) -> bool:
        reading = self.get(reading_id)
        if reading:
            self.session.delete(reading)
            self.session.commit()
            return True
        return False