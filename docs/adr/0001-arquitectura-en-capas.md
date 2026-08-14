# ADR 0001: Arquitectura en Capas Decoplada para SensorHub

* **Estado:** Aceptado
* **Fecha:** 14 de Agosto de 2026
* **Autores:** Aleixs Carbonell Montaño (Ingeniero Backend / IoT)
* **Proyecto:** SensorHub (API REST Telemetría IoT)

---

## Contexto y Problema

SensorHub nació como una API REST encargada de recibir, validar, almacenar y consultar métricas físicas (temperatura, humedad, presión) enviadas por dispositivos y sensores embebidos. En la fase inicial de desarrollo, la lógica de base de datos y la validación HTTP solían mezclarse en un solo archivo, generando los siguientes problemas:

1. **Acoplamiento Fuerte a la Infraestructura:** La lógica de negocio dependía directamente del motor de persistencia (SQLite en desarrollo local).
2. **Dificultad para Pruebas Unitarias:** Era imposible probar las reglas de negocio (ej. límites termodinámicos o integridad relacional) sin levantar una base de datos real o realizar escrituras en disco.
3. **Riesgo en Migraciones:** El requerimiento de migrar hacia PostgreSQL en producción (vía Render.com) amenazaba con romper la API si las consultas SQL estaban esparcidas por los endpoints.

---

## Decisión Arquitectónica

Se decide implementar una **Arquitectura en Capas Decoplada** con flujo unidireccional de dependencias:

$$\text{Routers (HTTP)} \longrightarrow \text{Services (Lógica)} \longrightarrow \text{Repositories (Persistencia)} \longrightarrow \text{Models (ORM / DB)}$$

### Detalles de la Implementación:
1. **Capa de Presentación (`app/routers/`):** FastAPI + Pydantic. Responsable exclusivo del protocolo HTTP, códigos de estado (200, 404, 422) y serialización/validación de esquemas JSON.
2. **Capa de Dominio/Servicio (`app/services/`):** `SensorHubService`. Contiene la lógica de negocio pura e integridad relacional. No conoce a FastAPI ni a SQLAlchemy.
3. **Capa de Persistencia (`app/repositories/`):** Implementa el patrón Repositorio detrás de una abstracción (`SensorHubRepository` usando la interfaz abstracta `Protocol` de Python) para cumplir con el **Principio de Inversión de Dependencias (DIP)** de SOLID.
4. **Capa de Modelos (`app/models/`):** Modelos SQLAlchemy 2.0 que definen la estructura de tablas de la base de datos relacional.

---

## Consecuencias

### Positivas (+)
* **Testabilidad Extrema:** Se pueden ejecutar pruebas unitarias puras en la capa de servicios usando simuladores (`MagicMock` o `FakeRepository`) sin tocar la base de datos real (demostrado con un 95.06% de cobertura de código).
* **Independencia del Motor de BD:** La migración de SQLite a PostgreSQL en Render se realiza modificando únicamente la cadena de conexión en la capa de infraestructura, manteniendo intacta la lógica de negocio.
* **Mantenibilidad y Módulos Claros:** Cada capa tiene una sola responsabilidad (SRP), facilitando las revisiones de código (*Code Review*) y la auditoría con linters (`ruff`, `mypy`).

### Negativas (-)
* **Mayor Ceremonia y Archivos:** Un requerimiento simple (*feature*) requiere modificar esquemas Pydantic, métodos del servicio, firmas del repositorio y la implementación en SQL.
* **Curva de Aprendizaje:** Requiere entender patrones de diseño orientados a objetos (`Protocols`, Inyección de Dependencias) en lugar de escribir scripts lineales.