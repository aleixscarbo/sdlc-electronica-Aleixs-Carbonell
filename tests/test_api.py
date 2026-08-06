import time

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def get_unique_id() -> str:
    """Genera un ID único para evitar conflictos si corremos el test varias veces"""
    return f"TEST-{int(time.time() * 1000)}"


def test_full_integration_workflow() -> None:
    sensor_id = get_unique_id()

    # 1. Crear Sensor (POST)
    response = client.post(
        "/sensors/", json={"id": sensor_id, "type": "temp", "name": "Prueba"}
    )
    assert response.status_code == 201

    # Conflicto: Crear mismo sensor (409)
    response_conflict = client.post(
        "/sensors/", json={"id": sensor_id, "type": "temp", "name": "Prueba"}
    )
    assert response_conflict.status_code == 409

    # 2. Listar Sensores (GET)
    response = client.get("/sensors/")
    assert response.status_code == 200
    assert len(response.json()) > 0

    # 3. Crear Lectura (POST)
    response = client.post(
        f"/sensors/{sensor_id}/readings", json={"value": 25.5, "unit": "C"}
    )
    assert response.status_code == 201
    reading_id = response.json()["id"]

    # 4. Listar Lecturas (GET)
    response = client.get(f"/sensors/{sensor_id}/readings")
    assert response.status_code == 200
    assert len(response.json()) >= 1

    # 5. Obtener Lectura Específica (GET)
    response = client.get(f"/readings/{reading_id}")
    assert response.status_code == 200
    assert response.json()["value"] == 25.5

    # 6. Actualizar Lectura (PATCH)
    response = client.patch(f"/readings/{reading_id}", json={"unit": "F"})
    assert response.status_code == 200
    assert response.json()["unit"] == "F"

    # 7. Borrar Lectura (DELETE)
    response = client.delete(f"/readings/{reading_id}")
    assert response.status_code == 204


def test_error_handlers() -> None:
    """Verifica que el sistema rechace peticiones a objetos que no existen"""
    assert (
        client.post(
            "/sensors/FAKE/readings", json={"value": 10, "unit": "C"}
        ).status_code
        == 404
    )
    assert client.get("/sensors/FAKE/readings").status_code == 404

    assert client.get("/readings/99999").status_code == 404
    assert client.patch("/readings/99999", json={"unit": "C"}).status_code == 404
    assert client.delete("/readings/99999").status_code == 404


def test_physics_validation() -> None:
    """Verifica que Pydantic aplique las leyes de la termodinámica"""
    sensor_id = get_unique_id()
    client.post(
        "/sensors/", json={"id": sensor_id, "type": "temp", "name": "Test Físico"}
    )

    # Intentamos registrar -300 °C (Falla de Pydantic -> 422 Unprocessable Entity)
    response = client.post(
        f"/sensors/{sensor_id}/readings", json={"value": -300.0, "unit": "C"}
    )
    assert response.status_code == 422
    assert "Física inválida" in response.text
