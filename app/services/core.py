from datetime import datetime

from app.models import ReadingModel, SensorModel
from app.repositories.base import SensorHubRepository
from app.services.alerts import AlertNotificationStrategy, ConsoleAlertStrategy
from app.services.exceptions import SensorAlreadyExistsError, SensorNotFoundError


class SensorHubService:
    """Lógica de negocio central. Audita la integridad relacional y anomalías."""

    def __init__(
        self,
        repo: SensorHubRepository,
        alert_strategy: AlertNotificationStrategy | None = None,
    ) -> None:
        self._repo = repo
        self._alert_strategy = alert_strategy or ConsoleAlertStrategy()

    def create_sensor(
        self, sensor_id: str, type: str, name: str, threshold: float | None = None
    ) -> SensorModel:
        if self._repo.get_sensor(sensor_id):
            raise SensorAlreadyExistsError(sensor_id)
        return self._repo.add_sensor(sensor_id, type, name, threshold)

    def get_sensor(self, sensor_id: str) -> SensorModel | None:
        return self._repo.get_sensor(sensor_id)

    def get_all_sensors(self, limit: int, offset: int) -> list[SensorModel]:
        return self._repo.list_sensors(limit, offset)

    def remove_sensor(self, sensor_id: str) -> bool:
        return self._repo.delete_sensor(sensor_id)

    def record_reading(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        sensor = self._repo.get_sensor(sensor_id)
        if not sensor:
            raise SensorNotFoundError(sensor_id)

        if sensor.threshold is not None and value > sensor.threshold:
            self._alert_strategy.notify(sensor_id, value, sensor.threshold)

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
            raise SensorNotFoundError(sensor_id)
        return self._repo.list_readings(sensor_id, limit, offset, from_date, to_date)

    def get_reading(self, reading_id: int) -> ReadingModel | None:
        return self._repo.get_reading(reading_id)

    def update_reading(self, reading_id: int, data: dict) -> ReadingModel | None:
        return self._repo.update_reading(reading_id, data)

    def delete_reading(self, reading_id: int) -> bool:
        return self._repo.delete_reading(reading_id)
