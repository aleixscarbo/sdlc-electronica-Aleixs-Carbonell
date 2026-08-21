from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import get_sensor_hub_service
from app.schemas import (
    AlertOut,
    AlertUpdate,
    ReadingCreate,
    ReadingOut,
    SensorCreate,
    SensorOut,
)
from app.services.core import SensorHubService

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.post("/", response_model=SensorOut, status_code=201)
def create_sensor(
    payload: SensorCreate,
    service: Annotated[SensorHubService, Depends(get_sensor_hub_service)],
) -> SensorOut:
    sensor = service.create_sensor(
        payload.id, payload.type, payload.name, payload.location, payload.threshold
    )
    return SensorOut.model_validate(sensor)


@router.get("/", response_model=list[SensorOut])
def list_sensors(
    service: Annotated[SensorHubService, Depends(get_sensor_hub_service)],
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> list[SensorOut]:
    sensors = service.get_all_sensors(limit, offset)
    return [SensorOut.model_validate(s) for s in sensors]


@router.post("/{sensor_id}/readings", response_model=ReadingOut, status_code=201)
def create_sensor_reading(
    sensor_id: str,
    payload: ReadingCreate,
    service: Annotated[SensorHubService, Depends(get_sensor_hub_service)],
) -> ReadingOut:
    reading = service.record_reading(sensor_id, payload.value, payload.unit)
    return ReadingOut.model_validate(reading)


@router.get("/{sensor_id}/readings", response_model=list[ReadingOut])
def list_sensor_readings(
    sensor_id: str,
    service: Annotated[SensorHubService, Depends(get_sensor_hub_service)],
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    from_date: Annotated[datetime | None, Query(alias="from")] = None,
    to_date: Annotated[datetime | None, Query(alias="to")] = None,
) -> list[ReadingOut]:
    readings = service.get_sensor_readings(sensor_id, limit, offset, from_date, to_date)
    return [ReadingOut.model_validate(r) for r in readings]


@router.get("/{sensor_id}/alerts", response_model=list[AlertOut], status_code=200)
def get_sensor_alerts(
    sensor_id: str,
    service: Annotated[SensorHubService, Depends(get_sensor_hub_service)],
) -> list[AlertOut]:
    """Obtiene todas las alertas activas (open o acknowledged) de un sensor."""
    try:
        alerts = service.get_active_alerts(sensor_id)
        return [AlertOut.model_validate(a) for a in alerts]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.patch(
    "/{sensor_id}/alerts/{alert_id}", response_model=AlertOut, status_code=200
)
def update_sensor_alert(
    sensor_id: str,
    alert_id: int,
    update_data: AlertUpdate,
    service: Annotated[SensorHubService, Depends(get_sensor_hub_service)],
) -> AlertOut:
    """Actualiza el estado de una alerta específica."""
    try:
        # El servicio se encarga de validar que 
        # el estado sea permitido (open, acknowledged, resolved)
        updated_alert = service.update_alert_status(alert_id, update_data.status)
        return AlertOut.model_validate(updated_alert)
    except ValueError as e:
        # Si el error es por estado no permitido, devolvemos un 400 Bad Request
        if "Estado no permitido" in str(e):
            raise HTTPException(status_code=400, detail=str(e)) from e
        # Si no encuentra la alerta, devolvemos un 404 Not Found
        raise HTTPException(status_code=404, detail=str(e)) from e
