from datetime import datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import AlertModel, ReadingModel, SensorModel
from app.repositories.base import SensorHubRepository


class SQLSensorHubRepository(SensorHubRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    # --- SENSORES ---
    def add_sensor(
        self,
        sensor_id: str,
        type: str,
        name: str,
        location: str,
        threshold: float | None = None,
    ) -> SensorModel:
        sensor = SensorModel(
            id=sensor_id, type=type, name=name, location=location, threshold=threshold
        )
        try:
            self.session.add(sensor)
            self.session.commit()
            self.session.refresh(sensor)
            return sensor
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def get_sensor(self, sensor_id: str) -> SensorModel | None:
        return self.session.get(SensorModel, sensor_id)

    def list_sensors(self, limit: int = 50, offset: int = 0) -> list[SensorModel]:
        stmt = (
            select(SensorModel).where(SensorModel.is_active).offset(offset).limit(limit)
        )
        return list(self.session.scalars(stmt).all())

    def delete_sensor(self, sensor_id: str) -> bool:
        sensor = self.get_sensor(sensor_id)
        if sensor and sensor.is_active:
            try:
                sensor.is_active = False  # SOFT DELETE
                self.session.commit()
                return True
            except SQLAlchemyError as e:
                self.session.rollback()
                raise e
        return False

    # --- LECTURAS ---
    def add_reading(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(sensor_id=sensor_id, value=value, unit=unit)
        try:
            self.session.add(reading)
            self.session.commit()
            self.session.refresh(reading)
            return reading
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

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

    def update_reading(
        self, reading_id: int, data: dict[str, Any]
    ) -> ReadingModel | None:
        reading = self.get_reading(reading_id)
        if reading:
            try:
                for key, val in data.items():
                    setattr(reading, key, val)
                self.session.commit()
                self.session.refresh(reading)
                return reading
            except SQLAlchemyError as e:
                self.session.rollback()
                raise e
        return None

    def delete_reading(self, reading_id: int) -> bool:
        reading = self.get_reading(reading_id)
        if reading:
            try:
                self.session.delete(reading)
                self.session.commit()
                return True
            except SQLAlchemyError as e:
                self.session.rollback()
                raise e
        return False

    # --- ALERTAS ---
    def add_alert(self, sensor_id: str, value: float, threshold: float) -> AlertModel:
        alert = AlertModel(sensor_id=sensor_id, value=value, threshold=threshold)
        try:
            self.session.add(alert)
            self.session.commit()
            self.session.refresh(alert)
            return alert
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def list_alerts(self, sensor_id: str) -> list[AlertModel]:
        stmt = select(AlertModel).where(AlertModel.sensor_id == sensor_id)
        return list(self.session.scalars(stmt).all())

    def get_alert(self, alert_id: int) -> AlertModel | None:
        return self.session.get(AlertModel, alert_id)

    def update_alert(self, alert_id: int, data: dict[str, Any]) -> AlertModel | None:
        alert = self.get_alert(alert_id)
        if alert:
            try:
                for key, val in data.items():
                    setattr(alert, key, val)
                self.session.commit()
                self.session.refresh(alert)
                return alert
            except SQLAlchemyError as e:
                self.session.rollback()
                raise e
        return None

    def list_active_alerts(self, sensor_id: str) -> list[AlertModel]:
        stmt = select(AlertModel).where(
            AlertModel.sensor_id == sensor_id,
            AlertModel.status.in_(["open", "acknowledged"]),
        )
        return list(self.session.scalars(stmt).all())

    # --- ESTADÍSTICAS (RF-6) ---
    def get_sensor_statistics(
        self,
        sensor_id: str,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> dict[str, float]:
        stmt = select(
            func.min(ReadingModel.value).label("min"),
            func.max(ReadingModel.value).label("max"),
            func.avg(ReadingModel.value).label("avg"),
        ).where(ReadingModel.sensor_id == sensor_id)

        if from_date:
            stmt = stmt.where(ReadingModel.created_at >= from_date)
        if to_date:
            stmt = stmt.where(ReadingModel.created_at <= to_date)

        # scalar_one_or_none() devuelve una tupla con (min, max, avg)
        result = self.session.execute(stmt).one_or_none()

        # Si no hay lecturas, SQL devuelve (None, None, None)
        if not result or result.min is None:
            return {"min": 0.0, "max": 0.0, "avg": 0.0}

        return {
            "min": round(result.min, 2),
            "max": round(result.max, 2),
            "avg": round(result.avg, 2),
        }
