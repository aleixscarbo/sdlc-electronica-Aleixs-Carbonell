from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ReadingModel, SensorModel
from app.repositories.base import SensorHubRepository


class SQLSensorHubRepository(SensorHubRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    # --- SENSORES ---
    def add_sensor(self, sensor_id: str, type: str, name: str) -> SensorModel:
        sensor = SensorModel(id=sensor_id, type=type, name=name)
        self.session.add(sensor)
        self.session.commit()
        self.session.refresh(sensor)
        return sensor

    def get_sensor(self, sensor_id: str) -> SensorModel | None:
        return self.session.get(SensorModel, sensor_id)

    def list_sensors(self, limit: int = 50, offset: int = 0) -> list[SensorModel]:
        stmt = select(SensorModel).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def delete_sensor(self, sensor_id: str) -> bool:
        sensor = self.get_sensor(sensor_id)
        if sensor:
            self.session.delete(sensor)
            self.session.commit()
            return True
        return False

    # --- LECTURAS ---
    def add_reading(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(sensor_id=sensor_id, value=value, unit=unit)
        self.session.add(reading)
        self.session.commit()
        self.session.refresh(reading)
        return reading

    def get_reading(self, reading_id: int) -> ReadingModel | None:
        return self.session.get(ReadingModel, reading_id)

    def list_readings(
        self,
        sensor_id: str,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[ReadingModel]:
        stmt = select(ReadingModel).where(ReadingModel.sensor_id == sensor_id)
        if from_date:
            stmt = stmt.where(ReadingModel.created_at >= from_date)
        if to_date:
            stmt = stmt.where(ReadingModel.created_at <= to_date)
        stmt = stmt.offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def update_reading(self, reading_id: int, data: dict) -> ReadingModel | None:
        reading = self.get_reading(reading_id)
        if reading:
            for key, val in data.items():
                setattr(reading, key, val)
            self.session.commit()
            self.session.refresh(reading)
        return reading

    def delete_reading(self, reading_id: int) -> bool:
        reading = self.get_reading(reading_id)
        if reading:
            self.session.delete(reading)
            self.session.commit()
            return True
        return False
