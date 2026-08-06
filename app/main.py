from fastapi import FastAPI

# Importamos los routers
from app.routers import readings, sensors

# 1. Inicializar la app
app = FastAPI(title="SensorHub API", version="1.0.0")

# ---> INYECCIÓN DEL HEALTH CHECK PARA RENDER <---
@app.get("/health")
def health_check():
    """Endpoint para que la nube de Render sepa que la API está viva."""
    return {"status": "ok"}
# ------------------------------------------------

# 2. Soldar los pines (Registrar los routers)
app.include_router(sensors.router)
app.include_router(readings.router)
