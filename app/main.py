from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.models import AlertModel, ReadingModel, SensorModel  # noqa: F401
from app.routers import readings, sensors
from app.services.exceptions import SensorAlreadyExistsError, SensorNotFoundError

app = FastAPI(title="SensorHub API", version="1.0.0")


@app.exception_handler(SensorNotFoundError)
def sensor_not_found_handler(
    request: Request, exc: SensorNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
    )


@app.exception_handler(SensorAlreadyExistsError)
def sensor_already_exists_handler(
    request: Request, exc: SensorAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)}
    )


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(sensors.router)
app.include_router(readings.router)
