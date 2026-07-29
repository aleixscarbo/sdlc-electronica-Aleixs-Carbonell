from app.models import ReadingModel
from app.repositories.base import ReadingRepository


class ReadingService:
    """Lógica de negocio. Depende de la abstracción del repositorio (DIP)."""
    
    def __init__(self, repo: ReadingRepository) -> None:
        # Inyección de dependencias: Le pasamos el "chip" de memoria desde afuera
        self._repo = repo

    def record(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        # Validación de reglas de negocio
        if value < -273.15:
            raise ValueError("Temperatura por debajo del cero absoluto")
        
        # Delegamos la persistencia a la abstracción
        return self._repo.add(sensor_id, value, unit)