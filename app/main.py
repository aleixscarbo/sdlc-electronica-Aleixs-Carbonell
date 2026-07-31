from fastapi import FastAPI

from app.db import Base, engine

# Importamos los routers
from app.routers import readings, sensors

# 1. Crear tablas físicas en la base de datos
Base.metadata.create_all(bind=engine)

# 2. Inicializar la app
app = FastAPI(title="SensorHub API", version="1.0.0")

# 3. Soldar los pines (Registrar los routers)
app.include_router(sensors.router)
app.include_router(readings.router)