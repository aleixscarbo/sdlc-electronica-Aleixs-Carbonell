from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.repositories.sql import SQLSensorHubRepository
from app.services.core import SensorHubService


# --- INYECCIÓN DE DEPENDENCIAS ---
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_sensor_hub_service(db: Annotated[Session, Depends(get_db)]) -> SensorHubService:
    repo = SQLSensorHubRepository(db)
    return SensorHubService(repo)