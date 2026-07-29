import pytest

from app.models import ReadingModel
from app.services.readings import ReadingService


class FakeRepository:
    """Implementación falsa (en RAM) para aislar las pruebas de la Base de Datos."""
    def __init__(self)-> None:  
        self.readings: list[ReadingModel] = []
        self.next_id = 1

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        # Usamos el modelo ORM directamente en RAM sin conectarlo a SQL
        reading = ReadingModel(id=self.next_id, sensor_id=sensor_id, 
                               value=value, unit=unit)
        self.readings.append(reading)
        self.next_id += 1
        return reading

    def list_for_sensor(self, sensor_id: str) -> list[ReadingModel]:
        return [r for r in self.readings if r.sensor_id == sensor_id]

# --- PRUEBAS DEL OSCILOSCOPIO ---

def test_record_reading_success() -> None:
    # Arrange: Conectamos el circuito falso al servicio
    fake_repo = FakeRepository()
    service = ReadingService(repo=fake_repo)
    
    # Act: Inyectamos una señal válida
    result = service.record("TEMP-01", 25.0, "C")
    
    # Assert: Verificamos los voltajes resultantes
    assert result.id == 1
    assert result.value == 25.0
    assert len(fake_repo.readings) == 1

def test_record_reading_below_absolute_zero_raises_error() -> None:
    # Arrange
    fake_repo = FakeRepository()
    service = ReadingService(repo=fake_repo)
    
    # Act & Assert: El circuito debe rechazar la señal antes de tocar la memoria
    with pytest.raises(ValueError, match="Temperatura por debajo del cero absoluto"):
        service.record("TEMP-01", -300.0, "C")