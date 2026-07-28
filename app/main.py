from fastapi import FastAPI
from pydantic import BaseModel, Field
# --- NUEVOS IMPORTS PARA LA BASE DE DATOS ---
from app.db import engine, Base
from app.models import ReadingModel  # Importamos los modelos para que SQLAlchemy sepa qué tablas crear

# Formatear la memoria: Crea el archivo .db y las tablas si no existen
Base.metadata.create_all(bind=engine)

# Inicialización del sistema
app = FastAPI(title="SensorHub API", version="0.1.0")

# Esquema de Entrada (Lo que el sensor nos envía)
class SensorReadingIn(BaseModel):
    sensor_id: str = Field(..., examples=["TEMP-01"])
    value: float
    unit: str = "C"

# Esquema de Salida (Lo que nosotros respondemos/guardamos)
class SensorReadingOut(SensorReadingIn):
    id: int

# Pin de lectura: Verificar si el sistema está encendido
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

# Pin de escritura: Recibir datos de un sensor
@app.post("/readings", response_model=SensorReadingOut, status_code=201)
def create_reading(reading: SensorReadingIn) -> SensorReadingOut:
    # Por ahora simulamos que se guardó devolviendo un ID fijo (1)
    # Mañana conectaremos esto a la memoria no volátil (Base de datos)
    return SensorReadingOut(id=1, **reading.model_dump())