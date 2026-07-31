from collections.abc import Generator
from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.db import Base, SessionLocal, engine
from app.models import ReadingModel
from app.repositories.sql import SQLReadingRepository
from app.services.readings import ReadingService

# Inicializar memoria física
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SensorHub API", version="0.3.0")


# --- ESQUEMAS DE ENTRADA/SALIDA (Pydantic) ---
class ReadingCreate(BaseModel):
    value: float
    unit: str = "C"


class ReadingUpdate(BaseModel):
    value: float | None = None
    unit: str | None = None


class ReadingOut(BaseModel):
    id: int
    sensor_id: str
    value: float
    unit: str
    created_at: datetime

    # Permite que Pydantic lea directamente del modelo de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


# --- INYECCIÓN DE DEPENDENCIAS (El Cableado de Energía) ---
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_reading_service(
    db: Annotated[Session, Depends(get_db)]
) -> ReadingService:
    repo = SQLReadingRepository(db)
    return ReadingService(repo)


# --- ENDPOINTS REST ---

@app.post("/sensors/{id}/readings", response_model=ReadingOut, status_code=201)
def create_reading(
    id: str,
    payload: ReadingCreate,
    service: Annotated[ReadingService, Depends(get_reading_service)],
) -> ReadingModel:
    try:
        return service.record(sensor_id=id, value=payload.value, unit=payload.unit)
    except ValueError as e:
        # El "from e" rastrea el error original (Soluciona B904)
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/sensors/{id}/readings", response_model=list[ReadingOut])
def list_readings(
    id: str,
    service: Annotated[ReadingService, Depends(get_reading_service)],
    limit: int = 50,
    offset: int = 0,
    from_date: Annotated[datetime | None, Query(alias="from")] = None,
    to_date: Annotated[datetime | None, Query(alias="to")] = None,
) -> list[ReadingModel]:
    return service.get_sensor_readings(id, limit, offset, from_date, to_date)


@app.get("/readings/{id}", response_model=ReadingOut)
def get_reading(
    id: int,
    service: Annotated[ReadingService, Depends(get_reading_service)],
) -> ReadingModel:
    reading = service.get_reading(id)
    if not reading:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
    return reading


@app.patch("/readings/{id}", response_model=ReadingOut)
def update_reading(
    id: int,
    payload: ReadingUpdate,
    service: Annotated[ReadingService, Depends(get_reading_service)],
) -> ReadingModel:
    data = payload.model_dump(exclude_unset=True)
    reading = service.update_reading(id, data)
    if not reading:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
    return reading


@app.delete("/readings/{id}", status_code=204)
def delete_reading(
    id: int,
    service: Annotated[ReadingService, Depends(get_reading_service)],
) -> None:
    success = service.delete_reading(id)
    if not success:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")