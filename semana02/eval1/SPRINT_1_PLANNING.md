# Sprint 1 Planning - Sistema de Monitoreo IoT (Bodega Industrial)

* **Proyecto:** Sistema de Monitoreo Ambiental de Bodega
* **Sprint Duración:** 1 Semana (Sprint 1)
* **Desarrollador Responsable:** Aleixs Carbonell (Developer / Product Owner / Scrum Master)
* **Fecha de Inicio:** Lunes de la Semana 2
* **Capacidad Estimada del Sprint:** 26 Story Points (~25-30 horas de desarrollo)

---

## 1. Sprint Goal (Objetivo del Sprint)

> **Sprint Goal:** Construir e integrar el núcleo funcional del sistema de monitoreo IoT (ingesta de datos, evaluación de umbrales térmicos y de humedad, y despacho de alertas) junto con el simulador de telemetría gaussiana y la prueba de integración a carga, garantizando una cobertura de pruebas $\ge 80\%$ y cero advertencias de análisis estático (`ruff` y `mypy`).

---

## 2. Historias de Usuario Seleccionadas (Sprint Backlog)

Para alcanzar el **Sprint Goal**, se han seleccionado **7 Historias de Usuario** del Product Backlog general. La selección prioritiza la funcionalidad central (*Must Have*) y las extensiones técnicas de arquitectura (*Should Have*):

| ID | Historia de Usuario | Prioridad (MoSCoW) | Story Points | Justificación Técnico-Operativa |
| :--- | :--- | :--- | :---: | :--- |
| **US-01** | Ingesta de Lectura de Sensor | Must Have | 3 | Proporciona la estructura de datos `SensorReading` y el almacenamiento en memoria `SensorRegistry`. |
| **US-02** | Detección de Anomalía por Temperatura | Must Have | 5 | Implementa el motor de reglas para la alerta principal ($T > 35.0\text{ }^\circ\text{C}$). |
| **US-03** | Detección de Anomalía por Humedad | Must Have | 3 | Extiende el motor de reglas para la segunda variable crítica ($H > 80.0\%$). |
| **US-05** | Gestor de Alertas por Consola | Must Have | 3 | Permite notificar eventos críticos en pantalla mediante la estrategia abstracta `AlertStrategy`. |
| **US-06** | Persistencia de Alertas en Log | Must Have | 2 | Garantiza el registro permanente e inmutable de emergencias en el archivo `alerts.log`. |
| **US-07** | Simulador de Telemetría Gaussiana | Should Have | 5 | Sustituye el hardware físico generando datos estocásticos para 10 sensores. |
| **US-08** | Motor de Integración (10x60) | Should Have | 5 | Integra todos los componentes y valida el flujo bajo carga durante 60 ciclos continuos. |

* **Total de Story Points en el Sprint 1:** 26 SP.
* *Nota de alcance:* La US-04 (Gestión Genérica), US-09 (Diagrama C4) y US-10 (Dashboard Web) quedan pospuestas o catalogadas como documentación post-desarrollo para no sobrecargar la capacidad.

---

## 3. Desglose de Tareas Técnicas (Task Breakdown $\le 4\text{ h}$)

Cada Historia de Usuario se desglosa en tareas de ingeniería concretas con una estimación de tiempo no mayor a 4 horas:

### US-01: Ingesta de Lectura de Sensor (3 SP)
* **Tarea 1.1:** Escribir pruebas unitarias iniciales en `test_registry.py` verificando almacenamiento y excepciones de tipo. *(Tiempo est.: 2 h)*
* **Tarea 1.2:** Crear dataclass `SensorReading` y la clase `SensorRegistry` con tipado estático en `registry.py`. *(Tiempo est.: 2 h)*

### US-02: Detección de Anomalía por Alta Temperatura (5 SP)
* **Tarea 2.1:** Diseñar pruebas unitarias en `test_detector.py` para umbrales térmicos (casos borde $35.0\text{ }^\circ\text{C}$ y $35.1\text{ }^\circ\text{C}$). *(Tiempo est.: 2 h)*
* **Tarea 2.2:** Implementar la clase `AnomalyDetector` inyectando los umbrales configurables por parámetro. *(Tiempo est.: 3 h)*

### US-03: Detección de Anomalía por Alta Humedad (3 SP)
* **Tarea 3.1:** Extender `test_detector.py` agregando escenarios Gherkin para la humedad ($80.0\%$ y $80.1\%$). *(Tiempo est.: 1.5 h)*
* **Tarea 3.2:** Actualizar el método `evaluate()` de `AnomalyDetector` para retornar la anomalía de tipo `HIGH_HUMIDITY`. *(Tiempo est.: 1.5 h)*

### US-05: Gestor de Alertas por Consola (3 SP)
* **Tarea 5.1:** Escribir pruebas con Mocks/Capsys en Pytest para capturar la salida estándar de consola en `test_alerts.py`. *(Tiempo est.: 2 h)*
* **Tarea 5.2:** Crear la interfaz abstracta `AlertStrategy` (ABC) y la implementación `ConsoleAlertStrategy` en `alerts.py`. *(Tiempo est.: 3 h)*

### US-06: Persistencia de Alertas en Archivo Log (2 SP)
* **Tarea 6.1:** Escribir test que verifique la creación física de `alerts.log` y el contenido de las líneas escritas. *(Tiempo est.: 2 h)*
* **Tarea 6.2:** Implementar `FileAlertStrategy` manejando la apertura segura de archivos en modo `append` (`"a"`). *(Tiempo est.: 2 h)*

### US-07: Simulador de Telemetría (Distribución Gaussiana) (5 SP)
* **Tarea 7.1:** Escribir pruebas unitarias estadísticas en `test_simulator.py` validando la media ($\mu$) y desviación ($\sigma$). *(Tiempo est.: 2 h)*
* **Tarea 7.2:** Implementar la clase `SensorSimulator` utilizando la función `random.gauss()` de la librería estándar de Python. *(Tiempo est.: 3 h)*

### US-08: Orquestación de Motor de Integración (10x60) (5 SP)
* **Tarea 8.1:** Crear script de orquestación `main.py` que instancie 10 sensores y ejecute el bucle de procesamiento. *(Tiempo est.: 3 h)*
* **Tarea 8.2:** Construir test de integración `test_integration.py` que valide la ejecución ininterrumpida de 600 lecturas totales. *(Tiempo est.: 4 h)*

---

## 4. Definition of Done (Criterios de Calidad Inquebrantables)

El incremento entregado al final de este Sprint solo se aceptará si cumple al 100% con la checklist oficial definida en `semana02/DEFINITION_OF_DONE.md`:

1. **Evidencia TDD:** Todo archivo de código fuente tiene su contraparte de prueba unitaria escrita previamente.
2. **Cobertra de Código:** `pytest --cov=semana02/eval1 --cov-fail-under=80` pasa sin errores.
3. **Estilo Linter:** `ruff check semana02/eval1/` no genera advertencias.
4. **Tipado Estático:** `mypy semana02/eval1/` aprueba con `disallow_untyped_defs = true`.
5. **Aislamiento en Git:** Cada historia de usuario desarrollada en su respectiva Feature Branch y fusionada mediante PR.