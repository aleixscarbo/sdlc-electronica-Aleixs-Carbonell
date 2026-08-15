from fastapi import FastAPI

# Importamos modelos explícitamente para evitar 
# solapamiento y que SQLAlchemy los registre
from app.models import AlertModel, ReadingModel, SensorModel  # noqa: F401
from app.routers import readings, sensors

# Crear todas las tablas en la base de datos al arrancar la aplicación  
# Base.metadata.create_all(bind=engine)

# 1. Inicializar la app
app = FastAPI(title="SensorHub API", version="1.0.0")


# ---> INYECCIÓN DEL HEALTH CHECK PARA RENDER <---
@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Endpoint para que la nube de Render sepa que la API está viva."""
    return {"status": "ok"}


# ------------------------------------------------

# 2. Soldar los pines (Registrar los routers)
app.include_router(sensors.router)
app.include_router(readings.router)
