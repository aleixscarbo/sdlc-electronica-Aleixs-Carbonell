# Arquitectura del Sistema - Diagrama C4 (Nivel 2: Contenedores)

El siguiente diagrama ilustra la arquitectura de la solución de monitoreo IoT desarrollada durante la Evaluación 1, destacando la separación de responsabilidades entre la ingesta de datos, el motor de reglas y las estrategias de persistencia.

```mermaid
C4Container
    title Diagrama de Contenedores - Sistema de Monitoreo IoT (Bodega)

    Person(operador, "Operador de Planta", "Supervisa las alertas físicas en consola.")
    Person(qa, "Auditor QA", "Revisa el registro inmutable de anomalías.")

    System_Boundary(iot_system, "SensorHub (Núcleo IoT)") {
        Container(simulator, "Sensor Simulator", "Python", "Genera telemetría estocástica (Gaussiana) simulando ruido térmico y de humedad ambiental.")
        Container(registry, "Sensor Registry", "Python", "Almacena en memoria de forma temporal el estado y telemetría de los 10 sensores activos.")
        Container(detector, "Anomaly Detector", "Python", "Motor de evaluación (T > 35°C, H > 80%). Clasifica lecturas y dispara eventos de anomalía.")
        Container(alert_manager, "Alert Manager", "Python (Patrón Strategy)", "Recibe eventos críticos y despacha alertas a múltiples interfaces de salida.")
    }

    SystemExt(file_system, "File System (OS)", "Almacenamiento local del servidor.")

    Rel(simulator, registry, "Ingesta de lecturas (SensorReading)", "Llamada a método")
    Rel(registry, detector, "Envía telemetría para validación", "Llamada a método")
    Rel(detector, alert_manager, "Dispara eventos (HIGH_TEMP / HIGH_HUM)", "Llamada a método")
    
    Rel(alert_manager, operador, "Notifica alerta visual", "Stdout (Console)")
    Rel(alert_manager, file_system, "Persiste bitácora en 'alerts.log'", "Escritura (Append)")
    Rel(qa, file_system, "Audita historial de métricas", "Lectura OS")