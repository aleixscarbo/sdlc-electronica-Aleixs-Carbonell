# Product Backlog - Sistema de Monitoreo IoT (Bodega Industrial)

### US-01: Ingesta de Lectura de Sensor
* **Prioridad (MoSCoW):** Must Have
* **Story Points:** 3
* **Como** operador de planta,
* **Quiero** que el sistema registre la lectura de temperatura y humedad de un sensor con su timestamp,
* **Para** tener un historial de las condiciones ambientales de la bodega.

**Criterios de Aceptación (Gherkin):**
* **Scenario:** Registrar una lectura válida dentro de rangos operativos
  * **Given** un sistema de monitoreo inicializado
  * **When** recibo una lectura del sensor "SENSOR-01" con temperatura 25.0 °C y humedad 50%
  * **Then** la lectura se almacena correctamente
  * **And** se le asigna el timestamp actual
  * **And** el estado de la lectura se marca como "NORMAL"
* **Scenario:** Rechazar una lectura con formato de datos incorrecto
  * **Given** un sistema de monitoreo inicializado
  * **When** recibo una lectura del sensor "SENSOR-01" con temperatura "Veinticinco" y humedad 50%
  * **Then** el sistema rechaza la lectura
  * **And** genera un error de validación de tipo (TypeError)

---

### US-02: Detección de Anomalía por Alta Temperatura
* **Prioridad (MoSCoW):** Must Have
* **Story Points:** 5
* **Como** supervisor de calidad,
* **Quiero** que el sistema evalúe si la temperatura supera los 35 °C,
* **Para** identificar condiciones que puedan degradar la materia prima.

**Criterios de Aceptación (Gherkin):**
* **Scenario:** Detectar temperatura en el umbral crítico
  * **Given** el motor de detección configurado con un umbral máximo de temperatura de 35.0 °C
  * **When** se procesa una lectura con temperatura de 35.1 °C y humedad de 40%
  * **Then** el detector clasifica la lectura como "ANOMALY"
  * **And** especifica el tipo de anomalía como "HIGH_TEMPERATURE"
* **Scenario:** Validar temperatura justo en el límite permitido
  * **Given** el motor de detección configurado con un umbral máximo de temperatura de 35.0 °C
  * **When** se procesa una lectura con temperatura de 35.0 °C y humedad de 40%
  * **Then** el detector clasifica la lectura como "NORMAL"

---

### US-03: Detección de Anomalía por Alta Humedad
* **Prioridad (MoSCoW):** Must Have
* **Story Points:** 3
* **Como** supervisor de calidad,
* **Quiero** que el sistema evalúe si la humedad relativa supera el 80%,
* **Para** prevenir la proliferación de moho en los empaques.

**Criterios de Aceptación (Gherkin):**
* **Scenario:** Detectar humedad superior al límite
  * **Given** el motor de detección configurado con un umbral máximo de humedad de 80.0%
  * **When** se procesa una lectura con temperatura de 22.0 °C y humedad de 81.5%
  * **Then** el detector clasifica la lectura como "ANOMALY"
  * **And** especifica el tipo de anomalía como "HIGH_HUMIDITY"

---

### US-04: Gestión y Emisión de Alertas
* **Prioridad (MoSCoW):** Must Have
* **Story Points:** 5
* **Como** equipo de mantenimiento,
* **Quiero** recibir notificaciones inmediatas cuando se detecte una anomalía,
* **Para** poder intervenir físicamente en la zona afectada de la bodega.

**Criterios de Aceptación (Gherkin):**
* **Scenario:** Emitir alerta a la consola por alta temperatura
  * **Given** el gestor de alertas configurado con la estrategia de salida por consola
  * **When** el detector de anomalías emite un evento de tipo "HIGH_TEMPERATURE" para el "SENSOR-05"
  * **Then** el sistema imprime "[CRITICAL] SENSOR-05: Temperatura excedió el límite (35 °C)"

---

### US-05: Gestor de Alertas (AlertManager) por Consola
* **Prioridad (MoSCoW):** Must Have
* **Story Points:** 3
* **Como** operador de la bodega industrial,
* **Quiero** que el sistema emita notificaciones inmediatas en la pantalla,
* **Para** poder reaccionar físicamente cuando un sensor detecte fuego o inundación.

**Criterios de Aceptación (Gherkin):**
* **Scenario:** Despacho exitoso de alerta térmica.
  * **Given** un `AlertManager` configurado con la estrategia `ConsoleAlertStrategy`
  * **And** un evento de anomalía con `type="HIGH_TEMPERATURE"` del `SENSOR-05`
  * **When** el manager procesa el evento
  * **Then** imprime un mensaje en mayúsculas en la salida estándar indicando el sensor y el tipo de emergencia.

---

### US-06: Estrategia de Persistencia de Alertas en Archivo Log
* **Prioridad (MoSCoW):** Must Have
* **Story Points:** 2
* **Como** auditor de calidad (QA),
* **Quiero** que todas las alertas se guarden en un archivo de texto inmutable,
* **Para** tener un historial auditable de las emergencias pasadas en la bodega.

**Criterios de Aceptación (Gherkin):**
* **Scenario:** Registro en archivo de anomalía de humedad.
  * **Given** un `AlertManager` configurado con `FileAlertStrategy(filepath="alerts.log")`
  * **When** el sistema despacha una anomalía de alta humedad (ej. 85%)
  * **Then** se anexa una nueva línea en `alerts.log` con el formato `[TIMESTAMP] - ALERTA - SENSOR_ID - HUMEDAD_ALTA`.
* **Scenario:** Creación automática del archivo.
  * **Given** que el archivo `alerts.log` no existe en el sistema
  * **When** se intenta escribir la primera alerta
  * **Then** el archivo es creado automáticamente sin lanzar excepciones de sistema de archivos (`FileNotFoundError`).

---

### US-07: Simulador de Telemetría (Distribución Gaussiana)
* **Prioridad (MoSCoW):** Should Have *(Extensión para Distinción)*
* **Story Points:** 5
* **Como** desarrollador de software,
* **Quiero** un generador de lecturas sintéticas basado en probabilidad gaussiana,
* **Para** simular el comportamiento realista del entorno físico sin necesitar hardware conectado.

**Criterios de Aceptación (Gherkin):**
* **Scenario:** Variación realista de temperatura.
  * **Given** un `SensorSimulator` inicializado con una temperatura media (mu) de 22.0 °C y desviación estándar (sigma) de 2.0 °C
  * **When** el simulador genera 100 lecturas consecutivas
  * **Then** estadísticamente el ~95% de los valores generados caen en el rango de 18.0 °C a 26.0 °C (±2 sigma).

---

### US-08: Orquestación de Motor de Integración (10x60)
* **Prioridad (MoSCoW):** Should Have *(Extensión para Distinción)*
* **Story Points:** 5
* **Como** Tech Lead del proyecto,
* **Quiero** un script de integración que ensamble todos los módulos (Registry, Simulator, Detector, AlertManager),
* **Para** validar el sistema a carga real durante el equivalente a 30 minutos de operación.

**Criterios de Aceptación (Gherkin):**
* **Scenario:** Ejecución ininterrumpida de ciclo de vida IoT.
  * **Given** 10 instancias de `SensorSimulator` registradas en el `SensorRegistry`
  * **And** un intervalo de tiempo simulado de 30 segundos
  * **When** el motor de orquestación se ejecuta por 60 iteraciones (ciclos)
  * **Then** el sistema procesa exactamente 600 lecturas totales
  * **And** despacha correctamente las alertas a la consola y al log sin detener la ejecución por excepciones.

---

### US-09: Documentación de Arquitectura (Diagrama C4 - Nivel 2)
* **Prioridad (MoSCoW):** Could Have *(Extensión para Distinción)*
* **Story Points:** 2
* **Como** arquitecto de software,
* **Quiero** un diagrama C4 de Contenedores documentado en el repositorio,
* **Para** que cualquier nuevo desarrollador entienda cómo interactúa el simulador con el motor de reglas y la persistencia de logs.

**Criterios de Aceptación (Gherkin):**
* **Scenario:** Entrega de diagrama en repositorio.
  * **Given** el código fuente finalizado en la rama `semana02`
  * **When** se evalúen los entregables
  * **Then** existe un archivo visual (imagen o código Mermaid) que muestra explícitamente los límites del sistema, el contenedor de aplicación Python y el contenedor del File System.

---

### US-10: Dashboard Web en Tiempo Real para Monitoreo
* **Prioridad (MoSCoW):** Won't Have *(Diferido para futuros Sprints)*
* **Story Points:** 8
* **Como** gerente de la planta,
* **Quiero** una interfaz gráfica web accesible por navegador,
* **Para** visualizar gráficas de las últimas 24 horas y los picos de anomalías sin usar la terminal.

**Criterios de Aceptación (Gherkin):**
* **Scenario:** Visualización de métricas en navegador.
  * **Given** el motor de monitoreo en ejecución
  * **When** un cliente GET hace una petición a la ruta `/dashboard`
  * **Then** el servidor retorna una gráfica generada con las lecturas recientes en formato HTML.
*(Nota: Esta historia queda explícitamente fuera del alcance del Sprint 1 para proteger el límite de tiempo).*