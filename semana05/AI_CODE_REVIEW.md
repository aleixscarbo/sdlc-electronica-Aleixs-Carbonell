# Revisión de Código Asistida por IA - SensorHub

**Archivo analizado:** `app/services/core.py`
**Fecha:** 13 de Agosto de 2026

## 1. Hallazgos del Code Review (IA) y Veredicto (Humano)

* **Hallazgo 1: SQL Injection en actualización de lecturas - Falta de whitelist de campos**
  * *Línea:* 50
  * *Descripción:* El método `update_reading()` acepta un diccionario sin validar qué campos pueden actualizarse. Un cliente malicioso podría intentar modificar campos críticos como `sensor_id`, `created_at` o metadata de auditoría.
  * *Veredicto Humano:* **RECHAZADO**
  * *Justificación:* La IA "alucina" el riesgo de inyección SQL y falta de whitelist porque ignora nuestro contexto arquitectónico. En nuestro diseño, `data` proviene de un esquema Pydantic (`ReadingUpdate`) en el Router, el cual ya blinda los campos permitidos. Además, SQLAlchemy 2.x parametriza todas las consultas automáticamente, haciendo imposible la inyección SQL clásica.

* **Hallazgo 2: Race Condition - Validación no atómica antes de insert**
  * *Línea:* 30-32
  * *Descripción:* En `record_reading()`, se valida la existencia del sensor con `get_sensor()` pero existe una ventana de tiempo entre la validación y `add_reading()` donde el sensor podría ser eliminado por otra transacción concurrente.
  * *Veredicto Humano:* **RECHAZADO (Mitigado por Arquitectura)**
  * *Justificación:* Aunque teóricamente correcto en altísima concurrencia, resolverlo con bloqueos manuales (`SELECT FOR UPDATE`) en el servicio añadiría complejidad innecesaria. La base de datos (PostgreSQL) maneja esto mediante llaves foráneas (`Foreign Keys`). Si ocurre la condición de carrera, el repositorio lanzará un `IntegrityError` que la capa superior puede manejar.

* **Hallazgo 3: Falta de validación de rangos de paginación - Riesgo de DoS**
  * *Línea:* 18 y 34
  * *Descripción:* Los métodos que listan datos aceptan un `limit` y `offset` sin restricciones de tope máximo, permitiendo extraer toda la base de datos en una sola consulta.
  * *Veredicto Humano:* **RECHAZADO**
  * *Justificación:* Excelente concepto, pero en el lugar equivocado. En FastAPI, los topes de paginación (`limit <= 100`) se manejan en la capa de Enrutamiento usando restricciones `Query(le=100)`. Mantendremos el servicio agnóstico de las reglas HTTP.

* **Hallazgo 4: Retorno de bool implícito sin manejar error de base de datos**
  * *Línea:* 21 y 53
  * *Descripción:* `remove_sensor` confía ciegamente en que el repositorio devuelve `True`/`False`, pero no envuelve la llamada en un bloque `try/except` para atrapar caídas de conexión o bloqueos de tabla.
  * *Veredicto Humano:* **ACEPTADO**
  * *Justificación:* Buen punto. El servicio debe ser el "amortiguador" de las excepciones técnicas. Debería capturar errores de `SQLAlchemyError` desde el repositorio y traducirlos a excepciones de negocio personalizadas para no filtrar detalles técnicos de la BD al Router.

* **Hallazgo 5: Ausencia de sanitización de entradas en ID y nombres**
  * *Línea:* 12
  * *Descripción:* `create_sensor` acepta strings crudos. Faltan protecciones contra caracteres especiales, nombres de 10,000 caracteres o XSS.
  * *Veredicto Humano:* **RECHAZADO**
  * *Justificación:* Mismo falso positivo que el Hallazgo 1. La limpieza y validación de expresiones regulares (Regex) y longitud máxima (max_length) vive en nuestros modelos Pydantic (Capa de Presentación).

* **Hallazgo 6: Validación redundante o faltante de fechas**
  * *Línea:* 34
  * *Descripción:* Si el cliente envía un `from_date` posterior a `to_date`, la base de datos hará una consulta inútil que consumirá recursos para devolver un arreglo vacío. 
  * *Veredicto Humano:* **ACEPTADO**
  * *Justificación:* Hallazgo muy válido. Esta es pura lógica de negocio. El servicio debe validar explícitamente que `from_date <= to_date` y lanzar un `ValueError` inmediato (para ahorrar recursos de BD).

* **Hallazgo 7: Eliminación física de datos en lugar de Soft Delete (Hard Delete)**
  * *Línea:* 21 y 53
  * *Descripción:* Borrar datos con `delete_sensor` o `delete_reading` es un "Hard Delete". Se pierden los registros de auditoría y se rompe el compliance de históricos en IoT.
  * *Veredicto Humano:* **ACEPTADO**
  * *Justificación:* Observación de arquitectura de alto nivel (Senior). En un sistema IoT real, la telemetría no se borra. Se debe proponer una refactorización futura para agregar un campo `is_deleted` (Soft Delete) en los modelos de SQLAlchemy.

## 2. Casos Borde y Nuevos Tests Integrados

La IA identificó los siguientes escenarios que no estaban cubiertos:

1. **Sensor inexistente en `record_reading()`** - Registrar lectura para sensor_id que nunca existió.
2. **Valores extremos en `record_reading()`** - Entradas matemáticas atípicas `value = float('nan')`, `value = float('inf')`.
3. **Parámetros de paginación malformados en `get_sensor_readings()`** - `limit = 0`, `offset = -1`.
4. **Fechas ilógicas en consultas históricas** - `from_date > to_date`.
5. **Colisión de IDs en `create_sensor()`** - Intentar crear un sensor que ya existe.

*Resultado:* Pendiente de implementación.