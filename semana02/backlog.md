# Product Backlog - Sistema de Monitoreo IoT (Bodega Industrial)

## US-01: Ingesta de Lectura de Sensor
Como operador de planta,
quiero que el sistema registre la lectura de temperatura y humedad de un sensor con su timestamp,
para tener un historial de las condiciones ambientales de la bodega.

**Prioridad:** Must Have
**Estimación:** 3 Story Points

**Criterios de Aceptación:**
` ` `gherkin
Scenario: Registrar una lectura válida dentro de rangos operativos
  Given un sistema de monitoreo inicializado
  When recibo una lectura del sensor "SENSOR-01" con temperatura 25.0 °C y humedad 50%
  Then la lectura se almacena correctamente
  And se le asigna el timestamp actual
  And el estado de la lectura se marca como "NORMAL"

Scenario: Rechazar una lectura con formato de datos incorrecto
  Given un sistema de monitoreo inicializado
  When recibo una lectura del sensor "SENSOR-01" con temperatura "Veinticinco" y humedad 50%
  Then el sistema rechaza la lectura
  And genera un error de validación de tipo (TypeError)
` ` `

---

## US-02: Detección de Anomalía por Alta Temperatura
Como supervisor de calidad,
quiero que el sistema evalúe si la temperatura supera los 35 °C,
para identificar condiciones que puedan degradar la materia prima.

**Prioridad:** Must Have
**Estimación:** 5 Story Points

**Criterios de Aceptación:**
` ` `gherkin
Scenario: Detectar temperatura en el umbral crítico
  Given el motor de detección configurado con un umbral máximo de temperatura de 35.0 °C
  When se procesa una lectura con temperatura de 35.1 °C y humedad de 40%
  Then el detector clasifica la lectura como "ANOMALY"
  And especifica el tipo de anomalía como "HIGH_TEMPERATURE"

Scenario: Validar temperatura justo en el límite permitido
  Given el motor de detección configurado con un umbral máximo de temperatura de 35.0 °C
  When se procesa una lectura con temperatura de 35.0 °C y humedad de 40%
  Then el detector clasifica la lectura como "NORMAL"
` ` `

---

## US-03: Detección de Anomalía por Alta Humedad
Como supervisor de calidad,
quiero que el sistema evalúe si la humedad relativa supera el 80%,
para prevenir la proliferación de moho en los empaques.

**Prioridad:** Must Have
**Estimación:** 3 Story Points

**Criterios de Aceptación:**
` ` `gherkin
Scenario: Detectar humedad superior al límite
  Given el motor de detección configurado con un umbral máximo de humedad de 80.0%
  When se procesa una lectura con temperatura de 22.0 °C y humedad de 81.5%
  Then el detector clasifica la lectura como "ANOMALY"
  And especifica el tipo de anomalía como "HIGH_HUMIDITY"
` ` `

---

## US-04: Gestión y Emisión de Alertas
Como equipo de mantenimiento,
quiero recibir notificaciones inmediatas cuando se detecte una anomalía,
para poder intervenir físicamente en la zona afectada de la bodega.

**Prioridad:** Must Have
**Estimación:** 5 Story Points

**Criterios de Aceptación:**
` ` `gherkin
Scenario: Emitir alerta a la consola por alta temperatura
  Given el gestor de alertas configurado con la estrategia de salida por consola
  When el detector de anomalías emite un evento de tipo "HIGH_TEMPERATURE" para el "SENSOR-05"
  Then el sistema imprime "[CRITICAL] SENSOR-05: Temperatura excedió el límite (35 °C)"
` ` `
