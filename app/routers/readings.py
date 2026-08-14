from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_sensor_hub_service
from app.schemas import ReadingOut, ReadingUpdate
from app.services.core import SensorHubService

router = APIRouter(prefix="/readings", tags=["Readings"])


@router.get("/{reading_id}", response_model=ReadingOut)
def get_reading(
    reading_id: int,
    service: Annotated[SensorHubService, Depends(get_sensor_hub_service)],
) -> ReadingOut:
    reading = service.get_reading(reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
    return reading  # type: ignore


@router.patch("/{reading_id}", response_model=ReadingOut)
def update_reading(
    reading_id: int,
    payload: ReadingUpdate,
    service: Annotated[SensorHubService, Depends(get_sensor_hub_service)],
) -> ReadingOut:
    data = payload.model_dump(exclude_unset=True)
    reading = service.update_reading(reading_id, data)
    if not reading:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
    return reading  # type: ignore


@router.delete("/{reading_id}", status_code=204)
def delete_reading(
    reading_id: int,
    service: Annotated[SensorHubService, Depends(get_sensor_hub_service)],
) -> None:
    success = service.delete_reading(reading_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
