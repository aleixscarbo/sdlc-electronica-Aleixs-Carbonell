import time
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from app.db import Base, engine
from app.main import app

# ---> INYECCIÓN PARA EL ENTORNO DE PRUEBAS <---
# Como la API ya no crea las tablas, obligamos a que la
# suite de pruebas construya las suyas en el SQLite temporal.
Base.metadata.create_all(bind=engine)


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


def get_unique_id() -> str:
    """Genera un ID único para evitar conflictos si corremos el test varias veces"""
    return f"TEST-{int(time.time() * 1000)}"


@pytest.mark.anyio
async def test_full_integration_workflow(client: AsyncClient) -> None:
    sensor_id = get_unique_id()

    # 1. Crear Sensor (POST) - Con location añadido
    response = await client.post(
        "/sensors/",
        json={
            "id": sensor_id,
            "type": "temp",
            "name": "Prueba",
            "location": "Bodega 1",
        },
    )
    assert response.status_code == 201

    # Conflicto: Crear mismo sensor (409)
    response_conflict = await client.post(
        "/sensors/",
        json={
            "id": sensor_id,
            "type": "temp",
            "name": "Prueba",
            "location": "Bodega 1",
        },
    )
    assert response_conflict.status_code == 409

    # 2. Listar Sensores (GET)
    response = await client.get("/sensors/")
    assert response.status_code == 200
    assert any(s["id"] == sensor_id for s in response.json())

    # 3. Agregar Lectura al Sensor (POST)
    response = await client.post(
        f"/sensors/{sensor_id}/readings", json={"value": 25.5, "unit": "C"}
    )
    assert response.status_code == 201
    reading_id = response.json()["id"]

    # 4. Listar Lecturas del Sensor (GET)
    response = await client.get(f"/sensors/{sensor_id}/readings")
    assert response.status_code == 200
    assert len(response.json()) > 0

    # 5. Obtener una lectura en específico (GET)
    response = await client.get(f"/readings/{reading_id}")
    assert response.status_code == 200
    assert response.json()["value"] == 25.5

    # 6. Actualizar Lectura (PATCH)
    response = await client.patch(f"/readings/{reading_id}", json={"unit": "F"})
    assert response.status_code == 200
    assert response.json()["unit"] == "F"

    # 7. Borrar Lectura (DELETE)
    response = await client.delete(f"/readings/{reading_id}")
    assert response.status_code == 204


@pytest.mark.anyio
async def test_error_handlers(client: AsyncClient) -> None:
    """Verifica que el sistema rechace peticiones a objetos que no existen"""
    assert (
        await client.post("/sensors/FAKE/readings", json={"value": 10, "unit": "C"})
    ).status_code == 404
    assert (await client.get("/sensors/FAKE/readings")).status_code == 404

    assert (await client.get("/readings/99999")).status_code == 404
    assert (
        await client.patch("/readings/99999", json={"unit": "C"})
    ).status_code == 404
    assert (await client.delete("/readings/99999")).status_code == 404


@pytest.mark.anyio
async def test_physics_validation(client: AsyncClient) -> None:
    """Verifica que Pydantic aplique las leyes de la termodinámica"""
    sensor_id = get_unique_id()
    await client.post(
        "/sensors/",
        json={
            "id": sensor_id,
            "type": "temp",
            "name": "Prueba",
            "location": "Bodega 1",
        },
    )

    # Temperatura en Celsius bajo 0 absoluto
    res = await client.post(
        f"/sensors/{sensor_id}/readings", json={"value": -300, "unit": "C"}
    )
    assert res.status_code == 422

    # Humedad fuera de rango
    res = await client.post(
        f"/sensors/{sensor_id}/readings", json={"value": 150, "unit": "%"}
    )
    assert res.status_code == 422

@pytest.mark.anyio
async def test_health_check_metrics(client: AsyncClient) -> None:
    """Verifica que el endpoint de salud devuelva métricas de la BD (RF-7)."""
    # Creamos un sensor para asegurar que haya al menos 1 activo
    sensor_id = get_unique_id()
    await client.post(
        "/sensors/",
        json={
            "id": sensor_id,
            "type": "temp",
            "name": "Sensor Health",
            "location": "Site A",
        },
    )

    # Consultamos el endpoint de salud
    response = await client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ok"
    assert "db_status" in data, "Falta el estado de la base de datos"
    assert data["db_status"] == "ok"
    assert "active_sensors" in data, "Falta la métrica de sensores activos"
    assert isinstance(data["active_sensors"], int)
    assert data["active_sensors"] >= 1