from fastapi import FastAPI

from app.db import Base, engine

# Importamos los routers
from app.routers import readings, sensors

# 1. Inicializar la app
app = FastAPI(title="SensorHub API", version="1.0.0")

# 2. Soldar los pines (Registrar los routers)
app.include_router(sensors.router)
app.include_router(readings.router)