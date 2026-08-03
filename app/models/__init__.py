from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String
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
    # CAMBIO 1: Agregamos index=True a sensor_id para consultas rápidas
    sensor_id: Mapped[str] = mapped_column(ForeignKey("sensors.id"), index=True)
    value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(10))
    # CAMBIO 2: Forzamos la zona horaria UTC explícitamente con lambda
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc))

    # Relación: Una lectura pertenece a un sensor
    sensor: Mapped["SensorModel"] = relationship(back_populates="readings")