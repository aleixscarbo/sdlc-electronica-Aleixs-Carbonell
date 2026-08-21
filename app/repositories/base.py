from datetime import datetime
from typing import Any, Protocol

from app.models import AlertModel, ReadingModel, SensorModel


class SensorHubRepository(Protocol):
    # --- SENSORES ---
    def add_sensor(
        self,
        sensor_id: str,
        type: str,
        name: str,
        location: str,
        threshold: float | None = None,
    ) -> SensorModel: ...
    def get_sensor(self, sensor_id: str) -> SensorModel | None: ...
    def list_sensors(self, limit: int = 50, offset: int = 0) -> list[SensorModel]: ...
    def delete_sensor(self, sensor_id: str) -> bool: ...

    # --- LECTURAS ---
    def add_reading(self, sensor_id: str, value: float, unit: str) -> ReadingModel: ...
    def get_reading(self, reading_id: int) -> ReadingModel | None: ...
    def list_readings(
        self,
        sensor_id: str,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[ReadingModel]: ...
    def update_reading(
        self, reading_id: int, data: dict[str, Any]
    ) -> ReadingModel | None: ...
    def delete_reading(self, reading_id: int) -> bool: ...

    # --- ALERTAS ---
    def add_alert(
        self, sensor_id: str, value: float, threshold: float
    ) -> AlertModel: ...
    def get_alert(self, alert_id: int) -> AlertModel | None: ...
    def update_alert(
        self, alert_id: int, data: dict[str, Any]
    ) -> AlertModel | None: ...
    def list_alerts(self, sensor_id: str) -> list[AlertModel]: ...
    def list_active_alerts(self, sensor_id: str) -> list[AlertModel]: ...

    # --- ESTADÍSTICAS (RF-6) ---
    def get_sensor_statistics(
        self,
        sensor_id: str,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> dict[str, float]: ...
