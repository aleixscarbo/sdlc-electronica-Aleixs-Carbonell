# Pruebas de Prompting - Semana 05
**Objetivo:** Contrastar la generación de código de un LLM (En este caso el Chat de GitHub Copilot en VS Code) utilizando prompts genéricos vs. prompts estructurados (Contexto + Tarea + Restricciones + Entrega).

---

## Tarea 1: Lógica de Dominio (Validación Física con Pydantic)
El problema: Actualmente, la API podría aceptar una lectura de humedad del 500%, lo cual es termodinámicamente imposible. Necesitamos blindar la entrada de datos.

### Prueba con Prompt Pobre
**Prompt utilizado:** > Escribe código para que la humedad no pase de 100 en pydantic.

**Resultado generado por la IA:**
Voy a ajustar la validación del esquema para que la humedad quede acotada al rango válido antes de que llegue al servicio.

Sí. En este proyecto ya está implementado así en __init__.py: la validación de humedad se hace dentro del validador de Pydantic.

```python
class ReadingBase(BaseModel):
    value: float | None = None
    unit: str | None = None

    @model_validator(mode="after")
    def check_physics(self) -> "ReadingBase":
        if self.unit is None or self.value is None:
            return self

        unit_upper = self.unit.upper()

        if unit_upper == "%":
            if self.value < 0 or self.value > 100:
                raise ValueError(
                    "Física inválida: La humedad debe estar entre 0% y 100%"
                )

        self.unit = unit_upper
        return self
```

Esto hace que, por ejemplo:

{"value": 101, "unit": "%"} -> error
{"value": 100, "unit": "%"} -> válido
{"value": -1, "unit": "%"} -> error
Si quieres, también te puedo dejar una versión más estricta con Field(ge=0, le=100) para validar directamente en el campo value.

### Prueba con Prompt Bueno
**Prompt utilizado:**
> CONTEXTO: API FastAPI (Python 3.12) para gestión de sensores. Uso de Pydantic V2 para validación de esquemas de entrada.
> TAREA: Escribe un `model_validator` (o `field_validator`) para la clase `ReadingCreate` que asegure que, si el campo `unit` es igual a `"%"` (humedad), el campo `value` esté estrictamente entre 0.0 y 100.0.
> RESTRICCIONES: Si la validación falla, debe levantar un `ValueError` con un mensaje descriptivo y profesional. Type hints completos.
> ENTREGA: Solo el código del validador de Pydantic, sin explicaciones ni texto introductorio.

**Resultado generado por la IA:**
```python
@model_validator(mode="after")
def validate_humidity_range(self) -> "ReadingCreate":
    """Valida que si la unidad es '%', el valor esté entre 0.0 y 100.0"""
    if self.unit and self.unit.upper() == "%":
        if self.value is not None and (self.value < 0.0 or self.value > 100.0):
            raise ValueError(
                "La humedad relativa debe estar entre 0.0% y 100.0%"
            )
    return self
```

---

## Tarea 2: Capa de Persistencia (Consulta Analítica en SQLAlchemy 2.0)
El problema: Ya tenemos operaciones CRUD básicas, pero SensorHub necesita empezar a entregar métricas. Queremos el promedio de lecturas de un sensor en las últimas 24 horas.

### Prueba con Prompt Pobre
**Prompt utilizado:** > Haz una función para sacar el promedio de las lecturas de la base de datos de un sensor usando el timestamp.

**Resultado generado por la IA:**
Promedio de lecturas por sensor y timestamp
He dejado la funcionalidad en la capa del repositorio y la API:

Repositorio: sql.py
Contrato: base.py
Servicio: core.py
Endpoint: sensors.py
Modelo de salida: __init__.py
La lógica principal es esta:

```python
def average_readings(
    self,
    sensor_id: str,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
) -> float | None:
    stmt = select(func.avg(ReadingModel.value)).where(
        ReadingModel.sensor_id == sensor_id
    )
    if from_date:
        stmt = stmt.where(ReadingModel.created_at >= from_date)
    if to_date:
        stmt = stmt.where(ReadingModel.created_at <= to_date)

    average = self.session.execute(stmt).scalar_one()
    return float(average) if average is not None else None
```

Y ya queda expuesto como endpoint:
```bash
GET /sensors/{sensor_id}/average?from=2026-08-01T00:00:00+00:00&to=2026-08-12T23:59:59+00:00
```

Respuesta esperada:
```json
{
  "sensor_id": "SENSOR-01",
  "average": 20.0
}
```

### Prueba con Prompt Bueno
**Prompt utilizado:**
> CONTEXTO: API FastAPI (Python 3.12) conectada a PostgreSQL. SQLAlchemy 2.0 con sintaxis de nueva generación (`select()`). El modelo es `ReadingModel` con columnas `id`, `sensor_id`, `value` (float), y `timestamp` (datetime).
> TAREA: Escribe una función asíncrona `get_average_reading_last_24h` para la capa de Repositorio que calcule el promedio matemático del campo `value` para un `sensor_id` específico en las últimas 24 horas.
> RESTRICCIONES: Usar estrictamente la sintaxis 2.0 de SQLAlchemy con `func.avg`. La función debe retornar un `float`, o `None` si no hay registros en ese periodo. Type hints completos.
> ENTREGA: Solo el código de la función en Python, sin dependencias externas ni explicaciones.

**Resultado generado por la IA:**
I’ll provide the exact repository function in the required SQLAlchemy 2.0 style, consistent with your schema and typing constraints.

async def get_average_reading_last_24h(self, sensor_id: str) -> float | None:
now: datetime = datetime.now(timezone.utc)
cutoff: datetime = now - timedelta(hours=24)

```python
stmt = (
    select(func.avg(ReadingModel.value))
    .where(ReadingModel.sensor_id == sensor_id)
    .where(ReadingModel.timestamp >= cutoff)
    .where(ReadingModel.timestamp <= now)
)

result = await self.session.execute(stmt)
average: float | None = result.scalar_one_or_none()

if average is None:
    return None

return float(average)
```

---

## Tarea 3: Aseguramiento de Calidad (Prueba de Integración End-to-End)
El problema: En la Semana 4 creamos el endpoint /health para que el balanceador de carga de Render no cancelara el despliegue. Necesitamos auditar ese endpoint con Pytest para evitar regresiones.

### Prueba con Prompt Pobre
**Prompt utilizado:** > Haz un test para el health check de la api de FastAPI.

**Resultado generado por la IA:**
He agregado el test test_health_check() al archivo test_api.py. El test:

```python
def test_health_check() -> None:
    """Verifica que el endpoint de healthcheck está disponible y funciona"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

Realiza una petición GET al endpoint /health
Verifica que el status code sea 200
Verifica que la respuesta sea exactamente {"status": "ok"}
El test está colocado al inicio de los tests unitarios, lo que es una buena práctica para validar primero la salud básica de la API.

### Prueba con Prompt Bueno
**Prompt utilizado:**
> CONTEXTO: API FastAPI (Python 3.12), módulo de pruebas automatizadas con Pytest utilizando `TestClient` de `fastapi.testclient`.
> TAREA: Escribe una función de prueba de integración `test_health_check_returns_200` que consuma el endpoint GET `/health` de la aplicación.
> RESTRICCIONES: El código debe estar comentado separando las fases del patrón Arrange-Act-Assert (AAA). Debe afirmar (assert) que el HTTP status code es 200 y que la respuesta JSON contiene una llave de estado exitoso.
> ENTREGA: Solo el código de la prueba unitaria, sin texto adicional.

**Resultado generado por la IA:**
I will add the integration test directly in the project’s existing Pytest style so it matches the current API test setup.

def test_health_check_returns_200() -> None:
#Arrange
#El cliente de pruebas ya está configurado para la aplicación FastAPI.

```python
# Act
response = client.get("/health")

# Assert
assert response.status_code == 200
assert response.json()["status"] == "ok"
```