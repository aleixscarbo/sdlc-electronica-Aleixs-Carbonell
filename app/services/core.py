from datetime import datetime

from app.models import AlertModel, ReadingModel, SensorModel
from app.repositories.base import SensorHubRepository
from app.services.alerts import AlertStrategy, ConsoleAlertStrategy


class SensorHubService:
    """Lógica de negocio central. Audita la integridad relacional y anomalías."""

    # Inyección de dependencias (OCP: La estrategia por defecto es ConsoleAlertStrategy)
    def __init__(
        self,
        repo: SensorHubRepository,
        alert_strategy: AlertStrategy = ConsoleAlertStrategy(),
    ) -> None:
        self._repo = repo
        self._alert_strategy = alert_strategy

    # --- SENSORES ---
    def create_sensor(
        self, sensor_id: str, type: str, name: str, threshold: float | None = None
    ) -> SensorModel:
        if self._repo.get_sensor(sensor_id):
            raise ValueError(f"El sensor con ID '{sensor_id}' ya existe.")
        return self._repo.add_sensor(sensor_id, type, name, threshold)

    def get_sensor(self, sensor_id: str) -> SensorModel | None:
        return self._repo.get_sensor(sensor_id)

    def get_all_sensors(self, limit: int, offset: int) -> list[SensorModel]:
        return self._repo.list_sensors(limit, offset)

    def remove_sensor(self, sensor_id: str) -> bool:
        return self._repo.delete_sensor(sensor_id)

    # --- LECTURAS Y ANOMALÍAS ---
    def record_reading(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        # 1. Validación de integridad relacional
        sensor = self._repo.get_sensor(sensor_id)
        if not sensor:
            raise ValueError(f"El sensor '{sensor_id}' no existe. Créalo primero.")

        # 2. Detección de Anomalías (Feature Semana 5)
        if sensor.threshold is not None and value > sensor.threshold:
            self._alert_strategy.send_alert(sensor_id, value, sensor.threshold)

        # 3. Persistencia
        return self._repo.add_reading(sensor_id, value, unit)

    def get_sensor_readings(
        self,
        sensor_id: str,
        limit: int,
        offset: int,
        from_date: datetime | None,
        to_date: datetime | None,
    ) -> list[ReadingModel]:
        if not self._repo.get_sensor(sensor_id):
            raise ValueError(f"El sensor '{sensor_id}' no existe.")
        return self._repo.list_readings(sensor_id, limit, offset, from_date, to_date)

    def get_reading(self, reading_id: int) -> ReadingModel | None:
        return self._repo.get_reading(reading_id)

    def update_reading(self, reading_id: int, data: dict) -> ReadingModel | None:
        return self._repo.update_reading(reading_id, data)

    def delete_reading(self, reading_id: int) -> bool:
        return self._repo.delete_reading(reading_id)

    # --- ALERTAS ---
    def get_sensor_alerts(self, sensor_id: str) -> list[AlertModel]:
        if not self._repo.get_sensor(sensor_id):
            raise ValueError(f"El sensor '{sensor_id}' no existe.")
        return self._repo.list_alerts(sensor_id)