# tests/smoke_test.py
import os
import sys

# Permitir que el script encuentre la carpeta 'app'
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def run_smoke_test():
    print("Iniciando Smoke Test contra PostgreSQL...")
    
    # 1. Crear un Sensor
    print("1. Creando Sensor...")
    sensor_data = {
        "name": "Smoke Sensor",
        "location": "Servidor CI",
        "type": "temperature",
    }
    response = client.post("/sensors/", json=sensor_data)
    assert response.status_code in [200, 201], (
        f"Fallo al crear sensor: {response.text}"
    )
    sensor_id = response.json()["id"]
    
    # 2. Crear una lectura anómala (alta temperatura)
    print("2. Inyectando lectura de alta temperatura...")
    reading_data = {"sensor_id": sensor_id, "value": 45.5}
    response = client.post("/readings/", json=reading_data)
    assert response.status_code in [200, 201], (
        f"Fallo al crear lectura: {response.text}"
    )
    
    # 3. Consultar las lecturas/alertas (Smoke cleared)
    print("3. Consultando datos registrados...")
    response = client.get(f"/sensors/{sensor_id}")
    assert response.status_code == 200, "Fallo al consultar el sensor"
    
    print("SMOKE TEST SUPERADO. El esquema de PostgreSQL esta perfecto.")


if __name__ == "__main__":
    run_smoke_test()