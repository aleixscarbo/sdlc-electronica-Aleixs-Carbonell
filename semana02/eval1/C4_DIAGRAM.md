# Arquitectura del Sistema - Diagrama C4 (Nivel 2: Contenedores)

El siguiente diagrama ilustra la arquitectura de la solución de monitoreo IoT desarrollada durante la Evaluación 1, destacando la separación de responsabilidades entre la ingesta de datos, el motor de reglas y las estrategias de persistencia.

```mermaid
flowchart TD
    %% Estilos de Nivel C4
    classDef person fill:#08427b,stroke:#052e52,color:#ffffff,stroke-width:2px;
    classDef container fill:#1168bd,stroke:#0b4880,color:#ffffff,stroke-width:2px;
    classDef external fill:#999999,stroke:#666666,color:#ffffff,stroke-width:2px;

    %% Actores
    operador["👤 Operador de Planta<br/><i>[Persona]</i><br/>Supervisa las alertas físicas en consola."]:::person
    qa["👤 Auditor QA<br/><i>[Persona]</i><br/>Revisa el registro inmutable de anomalías."]:::person

    %% Límite del Sistema
    subgraph iot_system ["📦 SensorHub - Núcleo IoT (Sistema)"]
        simulator["⚡ Sensor Simulator<br/><i>[Contenedor: Python]</i><br/>Genera telemetría estocástica (Gaussiana)."]:::container
        registry["🗃️ Sensor Registry<br/><i>[Contenedor: Python]</i><br/>Almacena en memoria el historial de 10 sensores."]:::container
        detector["🔍 Anomaly Detector<br/><i>[Contenedor: Python]</i><br/>Motor de reglas (T > 35°C, H > 80%)."]:::container
        alert_manager["🔔 Alert Manager<br/><i>[Contenedor: Python - Patrón Strategy]</i><br/>Despacha eventos a múltiples salidas."]:::container
    end

    %% Sistema Externo
    file_system["📄 File System (OS)<br/><i>[Sistema Externo]</i><br/>Almacenamiento de logs de auditoría."]:::external

    %% Relaciones y Flujo de Datos
    simulator -->|"Ingesta de lecturas (SensorReading)"| registry
    registry -->|"Envía telemetría para validación"| detector
    detector -->|"Dispara eventos (HIGH_TEMP / HIGH_HUM)"| alert_manager
    alert_manager -->|"Notifica alerta visual (Console)"| operador
    alert_manager -->|"Persiste bitácora ('alerts.log')"| file_system
    qa -->|"Audita historial de métricas"| file_system