from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class SensorModel(Base):
    __tablename__ = "sensors"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    type: Mapped[str] = mapped_column(String(50))  # ej. 'temperature', 'humidity'
    name: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(100), default="Desconocida")
    threshold: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    # Relación: Un sensor tiene muchas lecturas
    readings: Mapped[list["ReadingModel"]] = relationship(
        back_populates="sensor", cascade="all, delete-orphan"
    )

    # ¡NUEVO! Relación: Un sensor tiene muchas
    # alertas (EL PUENTE BIDIRECCIONAL FALTANTE)
    alerts: Mapped[list["AlertModel"]] = relationship(
        back_populates="sensor", cascade="all, delete-orphan"
    )


class ReadingModel(Base):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sensor_id: Mapped[str] = mapped_column(ForeignKey("sensors.id"), index=True)
    value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(10))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    sensor: Mapped["SensorModel"] = relationship(back_populates="readings")


class AlertModel(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sensor_id: Mapped[str] = mapped_column(ForeignKey("sensors.id"), index=True)
    value: Mapped[float] = mapped_column(Float)
    threshold: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # <-- Generación automática en PostgreSQL/SQLite
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(20), default="open")
    sensor: Mapped["SensorModel"] = relationship(back_populates="alerts")
