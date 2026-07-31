from datetime import datetime

import pytest

from app.models import ReadingModel
from app.services.readings import ReadingService


class FakeRepository:
    """Implementación falsa (en RAM) para aislar las pruebas de la Base de Datos."""
    def __init__(self) -> None:
        self.readings: list[ReadingModel] = []
        self.next_id = 1

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(id=self.next_id, sensor_id=sensor_id, 
                               value=value, unit=unit)
        self.readings.append(reading)
        self.next_id += 1
        return reading

    def list_for_sensor(self, sensor_id: str, limit: int = 50, offset: int = 0, 
                        from_date: datetime | None = None, 
                        to_date: datetime | None = None) -> list[ReadingModel]:
        # Para las pruebas, hacemos un filtrado básico por sensor
        return [r for r in self.readings if r.sensor_id == sensor_id]
        
    def get(self, reading_id: int) -> ReadingModel | None:
        for reading in self.readings:
            if reading.id == reading_id:
                return reading
        return None
        
    def update(self, reading_id: int, data: dict) -> ReadingModel | None:
        reading = self.get(reading_id)
        if reading:
            for key, val in data.items():
                setattr(reading, key, val)
        return reading
        
    def delete(self, reading_id: int) -> bool:
        reading = self.get(reading_id)
        if reading:
            self.readings.remove(reading)
            return True
        return False

# --- PRUEBAS DEL OSCILOSCOPIO ---

def test_record_reading_success() -> None:
    fake_repo = FakeRepository()
    service = ReadingService(repo=fake_repo)
    result = service.record("TEMP-01", 25.0, "C")
    assert result.id == 1
    assert result.value == 25.0
    assert len(fake_repo.readings) == 1

def test_record_reading_below_absolute_zero_raises_error() -> None:
    fake_repo = FakeRepository()
    service = ReadingService(repo=fake_repo)
    with pytest.raises(ValueError, match="Temperatura por debajo del cero absoluto"):
        service.record("TEMP-01", -300.0, "C")

def test_get_sensor_readings() -> None:
    fake_repo = FakeRepository()
    service = ReadingService(repo=fake_repo)
    service.record("TEMP-01", 25.0, "C")
    service.record("TEMP-01", 26.0, "C")
    
    results = service.get_sensor_readings("TEMP-01", 50, 0, None, None)
    assert len(results) == 2

def test_get_reading() -> None:
    fake_repo = FakeRepository()
    service = ReadingService(repo=fake_repo)
    reading = service.record("TEMP-01", 25.0, "C")
    
    result = service.get_reading(reading.id) # type: ignore
    assert result is not None
    assert result.value == 25.0

def test_update_reading() -> None:
    fake_repo = FakeRepository()
    service = ReadingService(repo=fake_repo)
    reading = service.record("TEMP-01", 25.0, "C")
    
    updated = service.update_reading(reading.id, {"unit": "F"}) # type: ignore
    assert updated is not None
    assert updated.unit == "F"

def test_delete_reading() -> None:
    fake_repo = FakeRepository()
    service = ReadingService(repo=fake_repo)
    reading = service.record("TEMP-01", 25.0, "C")
    
    success = service.delete_reading(reading.id) # type: ignore
    assert success is True
    assert service.get_reading(reading.id) is None # type: ignore