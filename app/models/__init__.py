from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class SensorModel(Base):
    __tablename__ = "sensors"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    type: Mapped[str] = mapped_column(String(50))  # ej. 'temperature', 'humidity'
    name: Mapped[str] = mapped_column(String(100))

    # Relación: Un sensor tiene muchas lecturas
    readings: Mapped[list["ReadingModel"]] = relationship(
        back_populates="sensor", cascade="all, delete-orphan"
    )


class ReadingModel(Base):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sensor_id: Mapped[str] = mapped_column(ForeignKey("sensors.id"))
    value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(10))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Relación: Una lectura pertenece a un sensor
    sensor: Mapped["SensorModel"] = relationship(back_populates="readings")