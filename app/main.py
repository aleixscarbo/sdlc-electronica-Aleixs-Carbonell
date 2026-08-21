from typing import Any

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.logger import logger
from app.models import AlertModel, ReadingModel, SensorModel  # noqa: F401
from app.routers import readings, sensors
from app.services.exceptions import SensorAlreadyExistsError, SensorNotFoundError

app = FastAPI(title="SensorHub API", version="1.0.0")

@app.exception_handler(SensorNotFoundError)
def sensor_not_found_handler(
    request: Request, exc: SensorNotFoundError
) -> JSONResponse:
    logger.warning(f"Sensor no encontrado: {exc}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
    )

@app.exception_handler(SensorAlreadyExistsError)
def sensor_already_exists_handler(
    request: Request, exc: SensorAlreadyExistsError
) -> JSONResponse:
    logger.warning(f"Conflicto, sensor ya existe: {exc}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)}
    )

@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)) -> dict[str, Any]:
    """Endpoint de salud y métricas básicas (RF-7)."""
    health_data: dict[str, Any] = {"status": "ok"}
    try:
        # 1. Verificar latido de la base de datos
        db.execute(text("SELECT 1"))
        health_data["db_status"] = "ok"
        
        # 2. Métrica: Conteo de sensores activos
        stmt = select(func.count(SensorModel.id)).where(SensorModel.is_active)
        active_sensors = db.scalar(stmt)
        health_data["active_sensors"] = active_sensors or 0
    except Exception as e:
        logger.error(f"Fallo crítico en BD durante health_check: {e}")
        health_data["db_status"] = "error"
        health_data["active_sensors"] = 0
        
    return health_data

app.include_router(sensors.router)
app.include_router(readings.router)