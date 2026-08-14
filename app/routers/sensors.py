from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import get_sensor_hub_service
from app.schemas import AlertOut, ReadingCreate, ReadingOut, SensorCreate, SensorOut
from app.services.core import SensorHubService

router = APIRouter(prefix="/sensors", tags=["Sensors"])


# --- RUTAS DE SENSORES ---
@router.post("/", response_model=SensorOut, status_code=201)
def create_sensor(
    payload: SensorCreate,
    service: Annotated[SensorHubService, Depends(get_sensor_hub_service)],
) -> SensorOut:
    try:
        return service.create_sensor(
            payload.id, payload.type, payload.name, payload.threshold
        )  # type: ignore
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e  # 409 Conflict


@router.get("/", response_model=list[SensorOut])
def list_sensors(
    service: Annotated[SensorHubService, Depends(get_sensor_hub_service)],
    limit: int = 50,
    offset: int = 0,
) -> list[SensorOut]:  # type: ignore
    return service.get_all_sensors(limit, offset)  # type: ignore


# --- RUTAS DE LECTURAS (Dependientes de un sensor) ---
@router.post("/{sensor_id}/readings", response_model=ReadingOut, status_code=201)
def record_reading(
    sensor_id: str,
    payload: ReadingCreate,
    service: Annotated[SensorHubService, Depends(get_sensor_hub_service)],
) -> ReadingOut:
    try:
        return service.record_reading(sensor_id, payload.value, payload.unit)  # type: ignore
    except ValueError as e:
        # Pydantic lanza ValidationError antes de llegar aquí,
        # pero capturamos errores de lógica (ej. sensor no existe)
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/{sensor_id}/readings", response_model=list[ReadingOut])
def list_sensor_readings(
    sensor_id: str,
    service: Annotated[SensorHubService, Depends(get_sensor_hub_service)],
    limit: int = 50,
    offset: int = 0,
    from_date: Annotated[datetime | None, Query(alias="from")] = None,
    to_date: Annotated[datetime | None, Query(alias="to")] = None,
) -> list[ReadingOut]:  # type: ignore
    try:
        return service.get_sensor_readings(sensor_id, limit, offset, from_date, to_date)  # type: ignore
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


# --- RUTAS DE ALERTAS ---
@router.get("/{sensor_id}/alerts", response_model=list[AlertOut])
def get_sensor_alerts(
    sensor_id: str,
    service: Annotated[SensorHubService, Depends(get_sensor_hub_service)],
) -> list[AlertOut]:  # type: ignore
    try:
        return service.get_sensor_alerts(sensor_id)  # type: ignore
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e