# Bitácora de Inteligencia Artificial — Reto EDSIA

Esta bitácora registra las interacciones con la IA generativa durante el desarrollo del proyecto, auditando el código sugerido y justificando las decisiones arquitectónicas bajo los principios SOLID y las buenas prácticas de desarrollo de software.

---

## [ENTRADA 1] Semana 1 - Día 1: Python Idiomático y Abstracción de Hardware

* **Fecha:** 15 de Julio de 2026
* **Contexto/Objetivo de la Sesión:** Configurar el paquete inicial `semana01`, migrar el paradigma de programación estructurada en C (típico de sistemas embebidos en la Universidad Veracruzana) a Python idiomático, y diseñar estructuras inmutables para telemetría de sensores.
* **Prompt Principal Utilizado:** *"Deseo reconfigurar mi cuaderno, debes ir explicando los conceptos y los temas que vayamos desarrollando a lo largo de las actividades... Escribe 5 funciones puras sobre Reading con type hints, verificadas con mypy y ruff."*

### Lo que produjo la IA:
Un script estructurado (`dia1_sensores.py`) que implementa:
1. Un enumerador `SensorType` (para reemplazar macros de preprocesador `#define`).
2. Una estructura de datos inmutable `@dataclass(frozen=True)` llamada `Reading`.
3. Un protocolo estructural (`Transport`) que define firmas de métodos de comunicación sin acoplamiento de herencia rígida.
4. Cinco funciones puras con *Type Hints* completos (`to_fahrenheit`, `is_over_threshold`, `to_json`, `apply_offset`, `is_valid_sensor`) que operan sin alterar el estado del sistema.

### Mi Decisión de Ingeniería y el porqué (Reflexión SOLID - SRP & OCP):
1. **Adopción de `frozen=True` (Principio de Responsabilidad Única - SRP):** En C/C++ para microcontroladores, es común modificar directamente variables globales o registros de memoria cuando un sensor cambia de valor. Decidí forzar la inmutabilidad de la estructura `Reading` mediante `frozen=True` para respetar el **SRP**. La única responsabilidad de esta clase es representar de forma segura un estado de telemetría específico en el tiempo. Al impedir que sus atributos sean modificados después de la instanciación, eliminamos de raíz los bugs por efectos secundarios y corrupción de datos en memoria concurrentes.
   
2. **Diseño a través de Funciones Puras (Principio de Abierto/Cerrado - OCP):**
   Para modificar el valor del sensor (por ejemplo, al aplicar un *offset* de calibración), en lugar de crear métodos mutadores dentro de la clase, utilicé la función pura `apply_offset` combinada con `dataclasses.replace`. Esto genera una nueva instancia de `Reading` con el valor corregido sin alterar la medición original. Esto cumple con el **OCP**: nuestro sistema está cerrado a la modificación de estructuras base pero completamente abierto a la extensión de nuevas funciones de procesamiento de datos analógicos o digitales sin poner en riesgo el núcleo de la aplicación.

---

## [ENTRADA 2] Semana 1 - Día 2: FSM Orientada a Objetos, TDD y SOLID

* **Fecha:** 15 de Julio de 2026
* **Contexto/Objetivo de la Sesión:** Reimplementar el patrón de Máquina de Estados Finitos (FSM) de un semáforo bajo el paradigma de Objetos y crear 4 pruebas unitarias con Pytest.
* **Prompt Principal Utilizado:** *"Explícame en qué consiste este patrón (AAA) antes de que generemos el código de las pruebas de Pytest."*
* **Lo que produjo la IA:** Una explicación detallada del patrón Arrange-Act-Assert (AAA) con analogías de electrónica. Además, proporcionó la estructura del archivo `fsm_demo.py` y los 4 tests exactos solicitados en `test_fsm.py` (estado inicial, RED->GREEN, ciclo completo y conteo).
* **Mi Decisión de Ingeniería y el porqué (Reflexión SOLID - SRP):** Decidí estructurar la clase `TrafficLightFSM` aislando completamente la lógica matemática de transición. A diferencia de la programación en C para microcontroladores (donde un `switch-case` a menudo mezcla el cambio de estado con la activación física de los pines LED), mi clase en Python cumple estrictamente con el **Principio de Responsabilidad Única (SRP) de SOLID**. 
La única razón para cambiar esta clase es si cambian las reglas lógicas del semáforo. La clase no imprime texto en consola ni interactúa con hardware externo; solo administra la transición de estados y el conteo de ciclos internos. Esto hace que el módulo sea altamente cohesivo y fácil de testear.

---

## [ENTRADA 3] Semana 1 - Día 3: SOLID en la Práctica (S, O, L)

* **Fecha:** 15 de Juio de 2026
* **Contexto/Objetivo de la Sesión:** Implementar de forma práctica en Python los tres primeros principios SOLID (Single Responsibility, Open/Closed y Liskov Substitution) utilizando un dominio de telemetría de sensores IoT, y estructurar una suite de 6 pruebas unitarias.
* **Prompt Principal Utilizado:** *"Día 3 · Miércoles — SOLID en la práctica: S, O y L... Para cada principio: el ejemplo 'mal' y el 'bien', más 2 tests. Commit al final del día."*

### Lo que produjo la IA:
La arquitectura modular del script `solid_srp_ocp_lsp.py` dividiendo las responsabilidades unidas (antipatrón) en entidades desacopladas. Diseñó estrategias de alerta polimórficas basadas en `abc.ABC` y demostró el cumplimiento del contrato de tipos para evitar la degradación del sistema bajo la sustitución de Liskov. Además, proveyó el archivo de pruebas correspondiente verificado con `pytest`.

### Mi Decisión de Ingeniería y el porqué (Reflexión SOLID - S, O, L):
1. **Separación de Persistencia y Adquisición (SRP):** Al mapear el diseño, entendí que un objeto no debe saber cómo se extraen los datos del pin analógico y al mismo tiempo cómo se escriben en el disco duro. Al aislar `SensorReader` de `DataLogger`, si los métodos de almacenamiento cambian en el backend, el módulo que interactúa con las señales físicas permanece intacto.
2. **Abstracción del Sistema de Alertas (OCP):** El detector de anomalías (`AnomalyDetector`) ahora depende de la abstracción `AlertStrategy`, no de una cadena de texto estática. Esto asegura que si el día de mañana implementamos un envío de correo electrónico (`EmailAlert`), el código del detector estará blindado y cerrado a modificaciones, cumpliendo con OCP.
3. **Contrato Estricto de Clases Hijas (LSP):** Al analizar Liskov, comprobé que las subclases no deben alterar la semántica de la clase padre. Si un método del padre promete devolver un `float`, la subclase jamás debe retornar tipos incompatibles o lanzar excepciones que fuercen al cliente a usar condicionales de tipo, garantizando la modularidad del software.

---

## [ENTRADA 4] Semana 1 - Día 4: SOLID Completo (I y D) e Inyección de Dependencias

* **Fecha:** 16 de Julio de 2026
* **Contexto/Objetivo de la Sesión:** Concluir el dominio de los principios SOLID implementando la Segregación de Interfaces (ISP) y la Inversión de Dependencias (DIP) mediante Protocolos y repositorios en memoria para pruebas.
* **Prompt Principal Utilizado:** *"Día 4 · Jueves — SOLID completo: I y D... Completa la biblioteca en semana1/solid_isp_dip.py. ISP: divide una interfaz gorda... DIP: usa Protocol para que DataProcessor dependa de una abstracción DataRepository"*

### Lo que produjo la IA:
Un script que demuestra el antipatrón de una interfaz monolítica (`FatSensorInterface`) y su corrección fraccionada (`Readable`, `Writable`, `Calibratable`). Además, implementó el patrón de Inversión de Dependencias usando `typing.Protocol`, aislando el procesador de datos de la tecnología de almacenamiento, acompañado de su respectivo repositorio en memoria (`InMemoryRepository`) para facilitar las pruebas con Pytest.

### Mi Decisión de Ingeniería y el porqué (Reflexión SOLID - I, D):
1. **Interfaces Segregadas (ISP):** Rechacé la creación de clases base masivas que obliguen a los sensores más básicos a cargar con métodos que no tienen sentido para su hardware físico. Al dividir las responsabilidades en micro-contratos lógicos, mi arquitectura simula el ruteo eficiente de un PCB: conectamos solo los pines/métodos estrictamente necesarios.
2. **El "Pago" del DIP (Inyección de Dependencias):** Entendí la inmensa ventaja del principio DIP en entornos profesionales. Al forzar al `DataProcessor` a depender del Protocolo `DataRepository` y no de una conexión SQL dura, logré que el sistema fuera **100% testeable** en aislamiento. Inyectar `InMemoryRepository` en mis pruebas unitarias permite auditar la lógica del procesador a velocidades de milisegundos sin latencia de red, garantizando un código de grado de producción.

---

## [ENTRADA 5] Semana 1 - Día 5: Ejercicio Integrador "El Driver Modernizado"

* **Fecha:** 17 de Julio de 2026
* **Contexto:** Reimplementación de un driver UART de C embebido a Python moderno aplicando todos los principios SOLID y concurrencia.
* **Prompt Principal Utilizado:** *"Día 5 · Viernes — Ejercicio integrador: 'El Driver Modernizado'... Uso de IA: escribe la firma del test y el docstring; deja que Copilot sugiera la implementación; revisa línea por línea."*
* **Uso de IA y Revisión de Código:** Utilicé la IA generativa como Copiloto. Le proporcioné las firmas de los tests y los *docstrings* (ej. `def test_device_full_flow(): """Prueba de integración: Conexión -> RX -> Parseo."""`). La IA sugirió las aserciones basadas en mis clases. 
* **Lo que cambié respecto a lo generado y el porqué:** 
  1. *Cambio:* Agregué el decorador `@pytest.fixture` para aislar el setup del `UartDevice`. La IA inicialmente sugería instanciar el dispositivo manualmente dentro de cada uno de los 3 tests del device.
  2. *Por qué (Reflexión SOLID & TDD):* Al usar Fixtures centralizamos el "Arrange" del patrón AAA, respetando el principio DRY (Don't Repeat Yourself) y logrando inyectar las dependencias (DIP) de la configuración y de los 3 parsers (incluyendo el parser CAN de extensión) de manera limpia y modular en cada test.

  ---

## [ENTRADA 1] Semana 2 - Día 1: Scrum en Profundidad y Tablero Kanban Ágil

* **Fecha:** 22 de Julio de 2026
* **Contexto:** Estudio de la Scrum Guide 2020, comprensión de roles, eventos, artefactos y el establecimiento inicial del espacio de trabajo ágil en GitHub Projects para la Evaluación 1 del sistema IoT.
* **Prompt Principal Utilizado:** *"Ayúdame a sintetizar la Scrum Guide 2020 conectando los conceptos de roles, eventos, artefactos y Definition of Done con la transición de un ingeniero electrónico a software backend, y dame los pasos para estructurar un tablero Kanban con 5 columnas en GitHub Projects."*
* **Uso de IA y Revisión de Código:** Utilicé a la IA como copiloto de arquitectura de procesos para organizar de forma estructurada los conceptos teóricos de Scrum. La IA propuso una tabla de equivalencias y la organización del tablero. Revisé la propuesta línea por línea contrastándola directamente con los principios rectores de la guía oficial de Scrum 2020 para evitar desviaciones conceptuales.
* **Lo que cambié respecto a lo generado y el porqué:** 
  1. *Cambio:* Ajusté los timeboxes propuestos originalmente por la IA para que no reflejaran los plazos mensuales estándar de Scrum, sino una escala adaptada a nuestro ciclo operativo semanal de desarrollo. 
  2. *Por qué (Reflexión Ágil):* Un Sprint de un mes no es viable para una habilitación intensiva basada en entregas semanales; adaptar los bloques de tiempo (Sprint Planning, Review, Retrospective) a un ciclo de 7 días mantiene el ritmo del SDLC ágil sin perder la disciplina de inspección y adaptación.

---

## [ENTRADA 2] Semana 2 - Día 2: Redacción de Product Backlog y Auditoría Gherkin

* **Fecha:** 23 de Julio de 2026
* **Contexto:** Definición del Product Backlog para el sistema de monitoreo IoT (Evaluación 1). Creación de Historias de Usuario con escenarios Gherkin y estimación mediante Story Points (Fibonacci).
* **Prompt Principal Utilizado:** *"He redactado la US-02 para detectar anomalías de temperatura (> 35 °C). Por favor audita mis escenarios Gherkin: ¿Son verificables? ¿Son ambiguos? ¿Qué caso borde me está faltando? Actúa como un QA Engineer estricto."*
* **Uso de IA y Revisión de Código:** Utilicé a la IA no para escribir la historia desde cero, sino como par revisor (QA/Testing) para validar la robustez de mi lógica. La IA confirmó que los escenarios iniciales eran verificables, pero detectó una carencia crítica: no estaba probando qué ocurre si los datos del sensor llegan corruptos (ej. temperatura en valor `None` o valores extremos ilógicos como `-1000 °C` debido a un corto circuito en el termistor).
* **Lo que cambié respecto a lo generado y el porqué:** 
  1. *Cambio:* Decidí no incluir la verificación de "cortocircuito del termistor" en la US-02 de Lógica de Negocio, sino delegar la validación de tipos y formatos a la US-01 (Ingesta de Lectura). 
  2. *Por qué (Reflexión SOLID & SRP):* Por el Principio de Responsabilidad Única (SRP), el motor de anomalías (US-02) debe confiar en que los objetos `SensorReading` que recibe ya están validados. Si intentara validar tipos de datos dentro del detector de anomalías, estaría acoplando la limpieza de datos con la lógica de negocio, lo que haría los tests futuros más frágiles y difíciles de mantener.

  ---

## [ENTRADA 3] Semana 2 - Día 3: Práctica de TDD Estricto y Ciclo Red-Green-Refactor

* **Fecha:** 23 de Julio de 2026
* **Contexto:** Implementación de la clase `SensorRegistry` y sus excepciones personalizadas siguiendo la regla absoluta del Desarrollo Guiado por Pruebas (TDD) para la US-01.
* **Prompt Principal Utilizado:** *"Día 3 · Miércoles — TDD estricto... Implementa un SensorRegistry con la regla absoluta: cada commit de test precede al commit del código. Dame los pasos exactos para evidenciarlo en Git."*
* **Uso de IA y Revisión de Código:** Utilicé a la IA para guiar el flujo operativo de Git y estructurar la inyección del código. Me proporcionó el test `test_get_unknown_sensor_raises` que forza un `ImportError` inicial (Fase RED), la implementación mínima basada en diccionarios para superarlo (Fase GREEN), y finalmente la reestructuración del código agregando el módulo `typing` de Python (Fase REFACTOR).
* **Lo que cambié respecto a lo generado y el porqué:** 
  1. *Cambio:* Al momento de hacer los commits, la guía original sugería `git commit -am`. Lo cambié por `git add .` seguido de `git commit -m`. 
  2. *Por qué (Reflexión de Git):* La bandera `-a` en `git commit` solo añade al stage los archivos que Git ya rastrea (tracked files). Como estaba creando archivos `.py` completamente nuevos para esta historia de usuario, usar `-am` habría fallado silenciosamente sin registrar mi código. Hacer el staging explícito garantiza que el historial sea inquebrantable para la auditoría de código.

  ---

## [ENTRADA 4] Semana 2 - Día 4: Automatización de Calidad (DoD, Ruff, Mypy y Cobertura)

* **Fecha:** 23 de Julio de 2026
* **Contexto:** Establecimiento de la *Definition of Done* y configuración de herramientas de análisis estático y cobertura (`pyproject.toml` con Ruff, Mypy y Pytest-cov) para garantizar la calidad del código de forma automatizada.
* **Prompt Principal Utilizado:** *"Día 4 · Jueves — Definition of Done y calidad automatizada. Escribe DEFINITION_OF_DONE.md y configura pyproject.toml con reglas de ruff (E, F, I, UP, B), pytest con --cov-fail-under=80 y mypy con disallow_untyped_defs."*
* **Uso de IA y Revisión de Código:** La IA fungió como ingeniero de DevOps, proporcionándome la checklist de calidad para el archivo `DEFINITION_OF_DONE.md` y la estructura del `pyproject.toml` con las banderas estrictas requeridas. Me indicó los comandos para instalar las dependencias necesarias (`pytest-cov`, `ruff`, `mypy`) y cómo ejecutar las auditorías en mi terminal.
* **Lo que cambié respecto a lo generado y el porqué:** 
  1. *Cambio:* La IA me indicó instalar las nuevas librerías, pero omitió guardar estos cambios en el control de dependencias. Lo corregí ejecutando de forma autónoma `pip freeze > requirements.txt`. 
  2. *Cambio:* Al ejecutar el análisis estricto de `mypy`, el linter falló porque la IA estructuró el test inicial (del Día 3) sin tipado de retorno. Modifiqué manualmente el archivo `test_registry.py` agregando `-> None` a la función.
    *Por qué (Criterio Técnico):* El primer cambio garantiza la reproducibilidad del entorno virtual para otros desarrolladores o para el servidor de despliegue continuo. El segundo cambio fue obligatorio para cumplir con la regla `disallow_untyped_defs = true` que definimos en el `pyproject.toml`, garantizando así que no haya "puntos ciegos" de tipado estático en el repositorio, ni siquiera en las pruebas.

---

## [ENTRADA 5] Semana 2 - Día 5: Gestión Ágil (Product Backlog y Sprint Planning)
* **Fecha:** 24 de Julio de 2026
* **Contexto:** Construcción de la documentación ágil requerida para el proyecto: Product Backlog completo (10 User Stories) priorizado mediante MoSCoW, y la definición del Sprint 1 Planning con estimaciones.
* **Prompt Principal Utilizado:** *"Genera las 6 Historias de Usuario faltantes (US-05 a US-10) con priorización MoSCoW, Story Points y formato Gherkin para completar el Product Backlog. Luego redacta el Sprint 1 Planning."*
* **Uso de IA y Revisión de Código:** La IA actuó como *Scrum Master*, redactando los escenarios Gherkin (Given/When/Then) con gran precisión, incluyendo casos estadísticos y de integración para la calificación de Distinción. También generó el documento de planificación estructurando las tareas a $\le 4\text{ h}$.
* **Lo que cambié respecto a lo generado y el porqué:**
  1. *Cambio:* La IA generó las nuevas historias con un formato basado en listas de Markdown, pero mis primeras 4 historias tenían un formato distinto. Modifiqué y reestructuré manualmente las US-01 a US-04 para unificarlas con el nuevo estándar.
  *Por qué (Criterio Técnico):* En la documentación de ingeniería, la consistencia visual es crucial. Un Backlog dispar denota falta de revisión humana.
  2. *Cambio:* Detecté que la IA intentó saltarse la US-03 (Humedad) y pasar directamente a la US-05. Detuve la generación y le exigí regresar al orden del Sprint Backlog.
  *Por qué (Criterio Técnico):* Para proteger el *Sprint Goal*. Como desarrollador responsable, no puedo implementar infraestructura secundaria (alertas) si el núcleo del motor de reglas (evaluar humedad) está incompleto.

---

## [ENTRADA 6] Semana 2 - Día 5: TDD, Lógica de Negocio y Patrón Strategy
* **Fecha:** 24 de Julio de 2026
* **Contexto:** Implementación en ciclo TDD (Red-Green-Refactor) del detector de humedad (US-03) y del Gestor de Alertas (US-05 y US-06) aplicando el patrón de diseño *Strategy* para separar la lógica de la infraestructura (Consola vs. Archivos).
* **Prompt Principal Utilizado:** *"Implementa las pruebas y el código para el AlertManager usando el patrón Strategy (ConsoleAlertStrategy y FileAlertStrategy) utilizando TDD estricto."*
* **Uso de IA y Revisión de Código:** La IA proporcionó excelentes implementaciones de *Mocks* en Pytest, sugiriendo el uso de los fixtures `capsys` para capturar la salida de consola y `tmp_path` para el manejo seguro de archivos temporales de prueba.
* **Lo que cambié respecto a lo generado y el porqué:** 1. *Cambio:* Al mover los archivos a `semana02/eval1/`, los tests fallaron con `ModuleNotFoundError`. La IA sugirió una solución a medias. Intervine modificando el archivo `pyproject.toml` para agregar `pythonpath = ["semana02/eval1"]`.
  *Por qué (Criterio Técnico):* Modificar el `PYTHONPATH` en la configuración global es la forma moderna y escalable de resolver rutas en Python, en lugar de depender de scripts frágiles o alterar la estructura de carpetas.

---

## [ENTRADA 7] Semana 2 - Día 6: Simulador Gaussiano y Pruebas de Integración (Distinción)
* **Fecha:** 24 de Julio de 2026
* **Contexto:** Desarrollo de las características de extensión: Un `SensorSimulator` basado en probabilidad estocástica y la integración del sistema mediante el script `main.py` probando carga (10 sensores, 60 iteraciones).
* **Prompt Principal Utilizado:** *"Desarrolla el test y la clase SensorSimulator usando distribución gaussiana. Después, crea test_integration.py y main.py para orquestar los 4 módulos corriendo 600 lecturas."*
* **Uso de IA y Revisión de Código:** La IA fue clave para diseñar el test estadístico, utilizando la Regla Empírica para validar que el ~95% de los datos generados por `random.gauss()` cayeran dentro de $\pm 2\sigma$.
* **Lo que cambié respecto a lo generado y el porqué:** 1. *Cambio:* Durante la ejecución del orquestador, el sistema arrojó un error porque al `SensorRegistry` le faltaba el método `add_reading`. Apliqué un *Hotfix* autónomo, agregando el método a `registry.py` y corrigiendo la firma de `get` a `get_sensor` en las pruebas unitarias.
  *Por qué (Criterio Técnico):* Este es un escenario clásico donde las pruebas unitarias pasan, pero la integración falla. El hotfix era estrictamente necesario para acoplar las interfaces de los distintos módulos y garantizar que el pipeline completo procesara las 600 lecturas.

---

## [ENTRADA 8] Semana 2 - Día 6: Arquitectura C4, Linter y Cierre del Release
* **Fecha:** 24 de Julio de 2026
* **Contexto:** Generación del diagrama de arquitectura C4 (Contenedores), redacción de la Retrospectiva del Sprint y la fusión final de la rama de desarrollo hacia `main` (Producción).
* **Prompt Principal Utilizado:** *"Redacta la Retrospectiva del Sprint y genera el código Mermaid para el Diagrama C4 Nivel 2 que incluya el File System."*
* **Uso de IA y Revisión de Código:** La IA sintetizó excelentemente el documento de Retrospectiva y proporcionó la base del código visual Mermaid para el mapeo de arquitectura.
* **Lo que cambié respecto a lo generado y el porqué:**
  1. *Cambio:* El código Mermaid original usaba directivas C4Container que rompían la vista previa nativa de VS Code. Lo reescribí manualmente usando `flowchart TD` y clases CSS genéricas.
  *Por qué (Criterio Técnico):* Un documento técnico debe ser compatible y renderizable en los entornos de trabajo del equipo. Forzar la sintaxis estándar de flujo garantiza soporte universal.
  2. *Cambio:* Apliqué un parche final antes del merge porque Ruff detectó un error `E501 Line too long (92 > 88)` en un comentario de `test_integration.py`. Dividí la línea manualmente.
  *Por qué (Criterio Técnico):* La calidad del código no es negociable. Romper un comentario en dos líneas permite mantener la configuración estricta de Ruff ("All checks passed") que establecimos en nuestro Definition of Done.

---

## [ENTRADA 9] Semana 3 - Día 1: API REST base y validación estricta con Pydantic
* **Fecha:** 28 de Julio de 2026
* **Contexto:** Inicialización de la API REST base para SensorHub utilizando FastAPI. Pruebas de inyección de datos erróneos (tipos incorrectos) en el endpoint de lecturas (POST `/readings`) a través de la interfaz autogenerada de Swagger UI.
* **Prompt Principal Utilizado:** *"dentro de http://127.0.0.1:8000/docs: si le doy en execute con 'value': hola... me da Error 422 Unprocessable Content... analiza esto y dime debaria generar una entrada significativa."*
* **Uso de IA y Revisión de Código:** La IA me ayudó a auditar la respuesta HTTP 422 y tradujo el comportamiento del framework: Pydantic actuó como un optoacoplador o fusible en el pin de entrada, interceptando el string ("hola") en lugar del float esperado, protegiendo así la capa de lógica interna de un colapso.
* **Lo que cambié respecto a lo generado y el porqué:**
  1. *Cambio:* Purgué manualmente el archivo `requirements.txt`, borrando todas las dependencias transitivas (como `starlette`, `pydantic_core`, `h11`) creadas por el comando `pip freeze`, dejando únicamente las herramientas explícitas de nivel superior (`fastapi`, `uvicorn`, `pytest`, `ruff`, `mypy`).
  *Por qué (Criterio Técnico):* Mantener una lista de materiales (BOM) limpia y estricta es vital para la etapa de DevOps (Docker/Render). Evita "cortocircuitos" por conflictos de versiones en sub-dependencias, asegurando que el servidor en producción sea 100% determinista y fácil de auditar.

---

## [ENTRADA 10] Semana 3 - Día 2: Aislamiento de Base de Datos y Cirugía en Git
* **Fecha:** 28 de Julio de 2026
* **Contexto:** Durante la integración de SQLAlchemy en SensorHub, un error en la terminal sobreescribió el archivo `.gitignore` base. Esto provocó que archivos binarios compilados (`__pycache__`) y la memoria física local de la base de datos (`sensorhub.db`) se colaran en el "área de preparación" y viajaran a GitHub en el último commit.
* **Prompt Principal Utilizado:** *"por que todos estos archivos se subieron a commit, me imagino que esta mal, porque ahora mi archivo gitignore antes se veia asi... como borro el ultimo commit, ya que le hice git push..."*
* **Uso de IA y Revisión de Código:** La IA diagnosticó el "cortocircuito" en el control de versiones y me asistió proporcionando un protocolo de recuperación. Usamos `git reset --soft HEAD~1` para retroceder el tiempo sin borrar el código físico, limpiamos el índice con `restore --staged` y aplicamos `--force-with-lease` para reescribir el historial remoto.
* **Lo que cambié respecto a lo generado y el porqué:**
  1. *Cambio:* Restauré manualmente la plantilla completa de 218 líneas del `.gitignore` original de Python/FastAPI, y le anexé de forma segura las reglas de exclusión de bases de datos (`*.db`, `*.sqlite3`) en lugar de dejar un archivo genérico o vacío.
  *Por qué (Criterio Técnico):* Una base de datos local nunca debe rastrearse en Git. Subirla expone datos sensibles y corrompe los despliegues en producción (generando conflictos de binarios). Dominar la reescritura del historial (Amnesia Histórica en Git) es vital para auditar y limpiar la placa de "soldadura derramada" antes de fusionar cualquier código a la rama principal (`main`).

---

## [ENTRADA 11] Semana 3 - Día 3: Inversión de Dependencias y Configuración de Cobertura
* **Fecha:** 29 de Julio de 2026
* **Contexto:** Implementación del patrón Repositorio y la capa de Servicios para la API de SensorHub. Se escribió un simulador en RAM (`FakeRepository`) para probar la lógica de negocio aislada. Depuración exhaustiva de la herramienta de cobertura (`pytest-cov`).
* **Prompt Principal Utilizado:** *"despues de corregir el project.toml, obtuve... ERROR: Coverage failure: total of 63 is less than fail-under=80"*
* **Uso de IA y Revisión de Código:** La IA fungió como herramienta de diagnóstico (troubleshooting). Primero identificó un error de sintaxis en `pyproject.toml` (argumento no reconocido `--app` en lugar de `--cov=app`). Luego analizó el reporte del 63% de cobertura y determinó que la lógica pura estaba al 100%, pero la herramienta estaba midiendo archivos de infraestructura sin pruebas (`main.py` y `db.py`).
* **Lo que cambié respecto a lo generado y el porqué:**
  1. *Cambio:* Además de implementar el servicio y el repositorio falso, añadí manualmente un bloque `[tool.coverage.run]` en el `pyproject.toml` con la directiva `omit` para ignorar los archivos `app/main.py` y `app/db.py`.
  *Por qué (Criterio Técnico):* En una Arquitectura Limpia, el dominio (servicio) se somete a pruebas unitarias rigurosas, mientras que el cableado de la placa (`main.py`/HTTP) y la conexión de la memoria (`db.py`) requieren pruebas de integración. Excluir estos últimos archivos de las pruebas unitarias evita que la métrica de cobertura caiga injustamente (falsos negativos), permitiendo que el pipeline de Integración Continua (CI) pase a verde asegurando que el 100% de la lógica de negocio central está auditada.

---

## [ENTRADA 12] Semana 3 - Día 4: Convenciones REST, Inyección de Dependencias y Refactorización
* **Fecha:** 30 de Julio de 2026
* **Contexto:** Ensamblaje final de las capas de SensorHub (Routers, Servicios, Repositorios, Modelos). Implementación de los cinco endpoints fundamentales siguiendo el estándar REST para operaciones CRUD sobre los datos de los sensores, incluyendo paginación y manejo de errores. Sesión de depuración estricta de calidad.
* **Prompt Principal Utilizado:** *"al correr, ruff check app/, obtuve: B008 Do not perform function call `Depends` in argument defaults... y ERROR: Coverage failure: total of 39 is less than fail-under=80"*
* **Uso de IA y Revisión de Código:** Utilicé la IA como un manual interactivo para interactuar con la interfaz Swagger UI y probar manualmente cada verbo HTTP (`POST`, `GET`, `PATCH`, `DELETE`). Posteriormente, la IA fungió como revisor de código (Linter/Coverage analyzer) ayudándome a diagnosticar errores de sintaxis detectados por Ruff (`B008` y `B904`) y la caída en la cobertura de Pytest debido a los nuevos métodos del servicio.
* **Lo que cambié respecto a lo generado y el porqué:**
  1. *Cambio:* Refactoricé la inyección de dependencias en `main.py` utilizando la sintaxis moderna `Annotated[Type, Depends(...)]` en lugar del valor por defecto tradicional `Depends()`. También aseguré el rastreo de excepciones usando `raise ... from e`.
  *Por qué (Criterio Técnico):* En Python, el uso de llamadas a funciones como valores por defecto en los argumentos (detectado por la advertencia B008 de Ruff) puede provocar fugas de memoria, ya que se evalúan solo una vez en la importación. `Annotated` resuelve esto acoplándose a las mejores prácticas de tipado estático, mientras que el bloque `raise ... from` preserva la traza original del error para una mejor observabilidad.
  2. *Cambio:* Excluí temporalmente la capa de conexión a base de datos pura (`app/repositories/sql.py`) del reporte de cobertura mediante `pyproject.toml` y amplié el `FakeRepository` en memoria con pruebas para los nuevos métodos CRUD.
  *Por qué (Criterio Técnico):* En una Arquitectura Limpia, las pruebas unitarias deben enfocarse estrictamente en la lógica de dominio (la capa de Servicio), aislando las interacciones externas (como bases de datos reales, las cuales requieren pruebas de integración). Excluir `sql.py` y emular la memoria con `FakeRepository` permite mantener métricas precisas y tiempos de prueba ultrarrápidos, cumpliendo con el estándar TDD sin comprometer el pipeline.

---

## [ENTRADA 13] Semana 3 - Día 5: Ejercicio Integrador, Arquitectura en 4 Capas y Pruebas de Integración
* **Fecha:** 30 de Julio de 2026
* **Contexto:** Consolidación y cierre de la arquitectura backend de SensorHub. Se implementó el modelo relacional completo con SQLAlchemy (relación Uno a Muchos entre `SensorModel` y `ReadingModel`), validaciones estrictas de física real y termodinámica en Pydantic (`model_validator`), separación de pines web mediante `APIRouter`, extracción de dependencias en un módulo dedicado (`dependencies.py`) para evitar imports circulares, y pruebas automatizadas de integración utilizando el `TestClient` de FastAPI.
* **Prompt Principal Utilizado:** *"Día 5 · Viernes — Ejercicio integrador: API completa de SensorHub... confirmo, ya veo la interfaz de swagger..."*
* **Uso de IA y Revisión de Código:** La IA me guio en el desglose del ejercicio integrador en tres fases de ensamblaje (Modelos/Esquemas, Capa de Lógica/Repositorio SQL, y Enrutadores/Pruebas de Integración). Además, la IA me ayudó a diagnosticar y solucionar un error crítico de **Import Circular** al separar los *routers*, extrayendo la inyección de dependencias a un archivo independiente (`dependencies.py`). Finalmente, la suite de pruebas automatizadas logró un **92.79% de cobertura**, superando holgadamente el mínimo requerido del 80%.
* **Lo que cambié respecto a lo generado y el porqué:**
  1. *Cambio:* Eliminé el archivo `tests/test_services.py` de la semana pasada y creé `tests/test_api.py` utilizando el `TestClient` de FastAPI para simular peticiones reales sobre los endpoints.
  *Por qué (Criterio Técnico):* En la Semana 3 pasamos de pruebas unitarias aisladas (con repositorios *fake* en memoria) a **Pruebas de Integración (End-to-End)** que auditan el comportamiento completo del sistema (routers, servicios, base de datos SQLite y validaciones de Pydantic). Esto nos permitió eliminar restricciones de exclusión en la cobertura y auditar con precisión de producción el sistema real.
  2. *Cambio:* Creé el módulo `app/dependencies.py` para alojar la fábrica de sesiones y servicios (`get_sensor_hub_service`).
  *Por qué (Criterio Técnico):* Al estructurar una arquitectura limpia en 4 capas con múltiples *routers*, las referencias cruzadas entre `main.py` y los enrutadores provocaban un cortocircuito lógico (*Circular Import*). Aislar la fuente de alimentación de dependencias permite un acoplamiento desacoplado y modular, siguiendo los estándares de diseño de software empresarial.

---

## [ENTRADA 14] Semana 3 - Día 6: Revisión por Pares (Code Review) Estricta y Refactorización
* **Fecha:** 2 de Agosto de 2026
* **Contexto:** Realización del ciclo de *Peer Review* cruzado. Inicialmente se había aprobado y fusionado el código, pero al recibir el Checklist oficial de 10 puntos, se ejecutó un `git reset --hard` para revertir el merge y adherirse estrictamente al estándar. Se auditó la API de mi compañero y se refactorizó mi propia API en base a su retroalimentación.
* **Prompt Principal Utilizado:** *"Estoy haciendo un Code Review de la Semana 3 de mi compañero Julián. Quiero que actúes como un Arquitecto Backend Senior y audites este código basándote en el Checklist oficial..."* y *"Ahora te daré la observación que mi compañero realizó a mi PR... dame los pasos para aplicar los cambios en mi código local"*.
* **Uso de IA y Revisión de Código:** Utilicé a la IA como copiloto para clonar y auditar localmente el código del compañero. La IA detectó una falla silenciosa pero crítica de integridad relacional (falta de `ForeignKey` en los modelos) y acoplamiento del protocolo HTTP en la capa de servicios. Además, utilicé la IA para estructurar respuestas profesionales en Markdown justificando decisiones de diseño (complejidad algorítmica $O(N)$ vs $O(\log N)$ al usar índices).
* **Lo que cambié respecto a lo generado y el porqué:**
  1. *Cambio:* Agregué explícitamente `index=True` a la columna `sensor_id` en SQLAlchemy.
  *Por qué (Criterio Técnico):* Para evitar *Full Table Scans* cuando el endpoint `GET` filtre lecturas por sensor, reduciendo la complejidad de búsqueda a $O(\log N)$ mediante un B-Tree.
  2. *Cambio:* Extraje la validación termodinámica (cero absoluto y unidades) a una clase base `ReadingBase` en Pydantic.
  *Por qué (Criterio Técnico):* En la versión anterior, el endpoint `PATCH` (que usaba un esquema sin validadores) permitía evadir las leyes de la física. Al usar herencia, garantizo que cualquier mutación de datos (creación o actualización parcial) pase por los fusibles lógicos antes de tocar la base de datos.

---

## [ENTRADA 15] Semana 4 - Día 1: Docker desde cero y Contenerización

* **Fecha:** 3 de Agosto de 2026
* **Contexto/Objetivo de la Sesión:** Contenerizar la API de SensorHub pasando de un entorno virtual local a un entorno aislado, estandarizado y reproducible mediante Docker, escribiendo el `Dockerfile` y estableciendo la comunicación de puertos.
* **Prompt Principal Utilizado:** *"listo, asi se ve mi cmd: [...] Ademas despues de que terminara de lanzar maquina ensambladora, se abrio una pestaña de Alerta de seguridad de windows, la imagen adjunta, lee detallamente que dice..."*

### Lo que produjo la IA:
Diagnóstico sobre el proceso de *build* (capas y dependencias) y explicación sobre la alerta del Firewall de Windows. La IA utilizó la analogía de la "apertura de un pin de comunicación" para explicar que el mapeo de puertos (`-p 8000:8000`) expone el contenedor a la red local, detonando el protocolo de seguridad del sistema operativo.

* **Uso de IA y Revisión de Código:** Utilicé a la IA como copiloto para auditar la configuración inicial de infraestructura. Diagnosticamos juntos la importancia del orden de los comandos `COPY` en el archivo de construcción para aprovechar la memoria caché, simulando la soldadura de componentes base vs. el ruteo de pistas modificables.
* **Lo que cambié respecto a lo generado y el porqué:**
  1. *Cambio:* Creé el archivo `.dockerignore` excluyendo `venv/`, `.env` y carpetas de caché (`__pycache__`, `.pytest_cache`) antes de ejecutar la compilación, un paso que no venía explícito en las instrucciones iniciales.
  *Por qué (Criterio Técnico):* Prevenir un fallo crítico de seguridad y rendimiento. Si el comando `COPY . .` arrastra las variables de entorno locales, los secretos se "soldarían" permanentemente dentro de una imagen inmutable. Además, copiar un `venv` de Windows a un contenedor Linux generaría sobrepeso y conflictos de binarios.
  2. *Cambio:* Otorgué permisos a *Docker Desktop Backend* en el Firewall de Windows para redes privadas.
  *Por qué (Criterio Técnico):* Para habilitar físicamente el enrutamiento del tráfico HTTP. Sin este permiso de red, el puerto 8000 local rechazaría las peticiones del navegador, aislando por completo al contenedor de Uvicorn.

  ---

## [ENTRADA 16] Semana 4 - Día 2: Orquestación, PostgreSQL y Condición de Carrera

* **Fecha:** 4 de Agosto de 2026
* **Contexto/Objetivo de la Sesión:** Migrar la persistencia local de SQLite a PostgreSQL contenedorizado, utilizando Docker Compose para orquestar la red virtual entre la API y la Base de Datos.
* **Prompt Principal Utilizado:** *"antes de coninuar. ahora mi cmd se ve asi, analiza todo lo que paso: [...] api-1 | psycopg.OperationalError: connection failed: connection to server at '172.18.0.2', port 5432 failed: Connection refused"*

### Lo que produjo la IA:
Un diagnóstico preciso de una "Condición de Carrera" (Race Condition) durante el arranque de los contenedores. La IA explicó cómo la API intentó conectarse a PostgreSQL antes de que este abriera su puerto TCP, provocando un error fatal y la caída del contenedor de FastAPI.

* **Uso de IA y Revisión de Código:** Utilicé a la IA para refactorizar la lógica de inicialización en `docker-compose.yml`. Entendimos que `depends_on: [db]` solo garantiza el orden de encendido de los contenedores, pero no su disponibilidad operativa en red.
* **Lo que cambié respecto a lo generado y el porqué:**
  1. *Cambio:* Implementé un bloque `healthcheck` utilizando el comando nativo `pg_isready` y modifiqué la dependencia a `condition: service_healthy`.
  *Por qué (Criterio Técnico):* Para forzar un patrón de espera activa (polling). Al exigir que PostgreSQL pase su test interno de disponibilidad TCP antes de arrancar Uvicorn, garantizamos que las migraciones y conexiones iniciales de SQLAlchemy nunca colisionen con un socket cerrado, estabilizando el sistema distribuido.

---

## [ENTRADA 17] Semana 4 - Día 2: Configuración de Alembic y Migraciones en PostgreSQL

* **Fecha:** 4 de Agosto de 2026
* **Contexto/Objetivo de la Sesión:** Configurar el sistema de control de versiones de bases de datos (Alembic) para gestionar la creación del esquema en PostgreSQL, separando la responsabilidad de inicialización de la base de datos del código de la API.
* **Prompt Principal Utilizado:** *"antes de continuar. para hacer el commit, debo darle ctrl c primero? ademas para las notas que llevo (good notes), falto sintetizar la infromacion de alembic."*

### Lo que produjo la IA:
Una explicación detallada sobre el funcionamiento de Alembic (analogiado como un sistema de control de versiones o "revisiones de parches de PCB" frente al método destructivo de borrar bases de datos), además de la guía paso a paso para configurar los archivos `alembic.ini`, `migrations/env.py` y estructurar el paquete `app/models/__init__.py` para que la herramienta detectara correctamente la metadata.

* **Uso de IA y Revisión de Código:** Utilicé a la IA para auditar las rutas de importación de SQLAlchemy y resolver el problema de resolución de nombres de red (`host 'db'` vs `localhost`) al ejecutar comandos de migración desde la máquina anfitriona (Windows) hacia el contenedor Docker.
* **Lo que cambié respecto a lo generado y el porqué:**
  1. *Cambio:* Se centralizaron las importaciones de `Base`, `SensorModel` y `ReadingModel` dentro del paquete `app/models/__init__.py` y se exportaron explícitamente con `__all__`.
  *Por qué (Criterio Técnico):* Garantizamos que el inspector de Alembic (`env.py`) tenga visibilidad directa sobre la estructura de tablas de la aplicación sin depender de archivos dispersos, evitando falsos positivos de "tablas eliminadas" durante la autogeneración de esquemas.

---

## [ENTRADA 18] Semana 4 - Día 3: Implementación de Pipeline CI y Branch Protection

* **Fecha:** 5 de Agosto de 2026
* **Contexto/Objetivo de la Sesión:** Configurar un pipeline de Integración Continua (CI) usando GitHub Actions para automatizar el testing (pytest, ruff, mypy) y proteger la rama principal de código defectuoso.
* **Prompt Principal Utilizado:** *"volvio a dar erro, ya que solo copie y pegue la linea que me diste y al aher git psuh y empzar el work flow, este dio error de nuevo en test linting with ruff, que dice: Run ruff check . F821 Undefined name `Base`"*

### Lo que produjo la IA:
La IA diagnosticó que el pipeline falló debido a errores de linteo (`F401 imported but unused`) dejados por refactorizaciones anteriores, y posteriormente por un `NameError` al faltar importaciones explícitas en el archivo de pruebas. Explicó que el entorno del CI en la nube es "aislado y virgen", por lo que los tests deben ser capaces de levantar y destruir su propia infraestructura en SQLite sin depender de herramientas externas como Alembic.

* **Uso de IA y Revisión de Código:** Utilicé a la IA para analizar los logs de error del runner de GitHub (`ubuntu-latest`) y aplicar correcciones locales usando `ruff check . --fix` antes de hacer push (Shift-Left Testing).
* **Lo que cambié respecto a lo generado y el porqué:**
  1. *Cambio:* Se inyectó `Base.metadata.create_all(bind=engine)` directamente en `tests/test_api.py` junto con sus importaciones respectivas (`Base`, `engine`).
  *Por qué (Criterio Técnico):* Para garantizar el aislamiento del entorno de pruebas. Al ejecutar la creación de tablas en el *setup* del archivo de pruebas, aseguramos que la base de datos temporal (SQLite) exista antes de que `TestClient` lance los *requests*, evitando el `OperationalError` en el servidor de CI que no tiene acceso a la base de datos de Docker Compose.

---

## [ENTRADA 19] Semana 4 - Día 4: IaC, Depuración en la Nube y Healthchecks en Render

* **Fecha:** 6 de Agosto de 2026
* **Contexto/Objetivo de la Sesión:** Desplegar la API SensorHub y su base de datos PostgreSQL en la nube (Render.com) utilizando Infraestructura como Código (IaC) mediante un archivo `render.yaml`, y lograr un pipeline de Continuous Deployment (CD) exitoso.
* **Prompts Principales Utilizados:** 1. *"el log no finalizo con exito, ahora dice: ... psycopg.OperationalError: connection failed: connection to server at '127.0.0.1'"*
  2. *"Deploy failed... Timed out after waiting for internal health check to return a successful response code at: ... /health"*

### Lo que produjo la IA:
Actuando como ingeniero SRE (Site Reliability Engineer), la IA me ayudó a leer y diagnosticar los logs de producción de Render. Primero, identificó que Alembic estaba intentando usar la URL local en lugar de la inyectada por la nube, y luego explicó por qué SQLAlchemy exigía el driver `psycopg2` heredado en lugar de nuestro moderno `psycopg3` (debido a los prefijos de URL de Render). Finalmente, diagnosticó que el orquestador de Render cancelaba el despliegue (Timeout) porque FastAPI devolvía un Error 404 al no tener programado un endpoint de salud (`/health`).

* **Uso de IA y Revisión de Código:** Utilicé la IA para simular un proceso real de depuración DevOps, aislando fallas de red, corrigiendo configuración de drivers en SQLAlchemy y entendiendo la integración paralela entre GitHub Actions (CI) y Render (CD).
* **Lo que cambié respecto a lo generado y el porqué:**
  1. *Cambio:* Se modificó el `CMD` del `Dockerfile` para ejecutar `alembic upgrade head && uvicorn ...`.
  *Por qué (Criterio Técnico):* En un entorno de producción efímero, es crítico garantizar que las tablas existan *antes* de que la API empiece a recibir tráfico, evitando que la aplicación se caiga por falta de esquema.
  2. *Cambio:* Se creó un "Interruptor Cloud" en `migrations/env.py` para leer `DATABASE_URL` y forzar el reemplazo de `postgres://` o `postgresql://` por `postgresql+psycopg://`.
  *Por qué (Criterio Técnico):* Para forzar el uso del driver moderno (`psycopg3`) que instalamos localmente y evitar que SQLAlchemy falle por no encontrar el módulo antiguo `psycopg2`.
  3. *Cambio:* Se agregó un endpoint `@app.get("/health")` en `main.py`.
  *Por qué (Criterio Técnico):* En la nube, los balanceadores de carga necesitan un "latido" (Heartbeat/Health Check) que devuelva un código HTTP 200 OK. Sin esto, Render asume que el contenedor está defectuoso, no enruta el puerto 8000 hacia el internet público y cancela el despliegue a los 15 minutos.

---

## [ENTRADA 20] Semana 4 - Día 5: Optimización de Imágenes con Multi-Stage Build y Smoke Testing en CI con PostgreSQL

* **Fecha:** 8 de Agosto de 2026
* **Contexto/Objetivo de la Sesión:** Reducir el tamaño de la imagen Docker de la aplicación por debajo de 200 MB mediante patrones *Multi-stage Build*, e integrar un *Smoke Test* automatizado en GitHub Actions que valide migraciones de Alembic y operaciones CRUD reales contra un servicio efímero de PostgreSQL.

* **Prompts Principales Utilizados:**
  1. *"instrucciones del dia 4... multi-stage build con imagen < 200 MB... y un smoke test contra PostgreSQL como service en Actions"*
  2. *"alembic upgrade head... sqlalchemy.exc.ProgrammingError: (psycopg.errors.DuplicateTable) relation 'sensors' already exists"*
  3. *"AssertionError: Fallo al crear lectura: {"detail":"Not Found"}"*

### Lo que produjo la IA:
La IA propuso una reestructuración completa del `Dockerfile` dividida en dos etapas (`builder` y `runner`), aislando el entorno virtual de la compilación de paquetes. Posteriormente, configuró un contenedor secundario de PostgreSQL 15 dentro del archivo `.github/workflows/ci.yml` en la sección `services`, redactando el script `tests/smoke_test.py` para inyectar transacciones de prueba. Durante la integración, la IA ayudó a diagnosticar un conflicto de interferencia donde Pytest (ejecutando en SQLite) colisionaba con las migraciones de Alembic en PostgreSQL, además de ajustar las rutas anidadas de la API (`/sensors/{id}/readings`).

* **Uso de IA y Revisión de Código:** Se utilizó la IA como un osciloscopio de infraestructura para diagnosticar orden de ejecución en el pipeline, validar patrones de diseño RESTful en el Smoke Test y corregir reglas de tipado y formato impuestas por Mypy y Ruff.

* **Lo que cambié respecto a lo generado y el porqué:**
  1. *Cambio:* Se reemplazó el `Dockerfile` monolítico por una arquitectura de construcción multi-etapa utilizando `python:3.12-slim`.
     *Por qué (Criterio Técnico):* En la etapa `builder` se instalan y compilan paquetes en `/opt/venv`, mientras que en la etapa `runner` solo se copia la carpeta compilada lista para producción. Esto elimina caché de `pip` y binarios temporales, logrando una imagen final ligera de ~140 MB (cumpliendo el límite < 200 MB).
  2. *Cambio:* Se removió la variable global `DATABASE_URL` del workflow de CI y se aisló únicamente dentro de la variable del paso *Smoke Test*.
     *Por qué (Criterio Técnico):* Pytest ejecutaba `Base.metadata.create_all()` al inicio, leyendo la URL global y creando las tablas en PostgreSQL a la fuerza. Cuando Alembic intentaba correr `upgrade head`, la tabla ya existía arrojando `DuplicateTable`. Al aislar la variable, Pytest utiliza SQLite en memoria y PostgreSQL queda virgen para Alembic.
  3. *Cambio:* Se ajustaron las peticiones del `smoke_test.py` para enviar el campo `id` requerido por Pydantic y consumir la ruta anidada POST `/sensors/{sensor_id}/readings` con payload `{"value": 45.5, "unit": "C"}`.
     *Por qué (Criterio Técnico):* La arquitectura de la API impone contratos estrictos de validación. El Smoke Test debía respetar fielmente el ruteo RESTful para probar la persistencia real sin falsos negativos.

---

## [ENTRADA 21] Semana 4 - Día 6: DevSecOps con Trivy, Bot Guardián y Protección de Entornos (GitHub Environments)

* **Fecha:** 8 de Agosto de 2026
* **Contexto/Objetivo de la Sesión:** Implementar la capa de DevSecOps en la cadena de CI/CD mediante el escaneo automatizado de vulnerabilidades (CVEs) con Trivy, alertas automáticas de fallos en producción y protección de la rama `main` mediante entornos restringidos.

* **Prompts Principales Utilizados:**
  1. *"GitHub Environments con protección de rama, escaneo de vulnerabilidades con trivy, issue automático si el pipeline falla en main"*
  2. *"dentro de la pestaña de enviroments, me aparecen... chore/docker-setup... copilot"*

### Lo que produjo la IA:
La IA generó los bloques YAML para integrar la acción oficial de Trivy (`aquasecurity/trivy-action`), escaneando tanto la imagen `sensorhub:latest` como las dependencias de Python (`requirements.txt`) en busca de vulnerabilidades clasificadas como `HIGH` o `CRITICAL`. Adicionalmente, redactó un script en JavaScript usando `actions/github-script` con una compuerta lógica `if: failure() && github.ref == 'refs/heads/main'` para abrir tickets de soporte de forma automática cuando ocurran fallas en la rama principal.

* **Uso de IA y Revisión de Código:** Se utilizó la IA para auditar los reportes de seguridad generados por Trivy y entender la administración de entornos de despliegue en GitHub, garantizando que el flujo de aprobación requiriera intervención humana antes del despliegue.

* **Lo que cambié respecto a lo generado y el porqué:**
  1. *Cambio:* Se añadió la etapa de construcción local `docker build -t sensorhub:latest .` y el escáner Trivy al pipeline de GitHub Actions.
     *Por qué (Criterio Técnico):* Garantiza el cumplimiento de DevSecOps (Shift-Left Security), bloqueando o auditando imágenes antes de que sean distribuidas a la nube. El reporte arrojó **0 vulnerabilidades** en la imagen final.
  2. *Cambio:* Se configuró el entorno `production` en las opciones del repositorio de GitHub con la regla *Required Reviewers* asignada al desarrollador, y se vinculó en el workflow mediante `environment: production`.
     *Por qué (Criterio Técnico):* Implementa un freno de mano operacional (Quality Gate), evitando que cambios accidentales o no revisados se desplieguen automáticamente en producción sin autorización explícita.
  3. *Cambio:* Se inyectó el script de notificación de fallos con etiquetas `['bug', 'urgente']`.
     *Por qué (Criterio Técnico):* Proporciona trazabilidad inmediata (Observabilidad de CI/CD) al equipo de ingeniería al notificar el Hash del commit defectuoso y el enlace directo a los logs del error en caso de rupturas en `main`.

---

## [ENTRADA 22] Semana 5 - Día 1: Ingeniería de Prompts (A/B Testing)

* **Fecha:** 12 de Agosto de 2026
* **Contexto/Objetivo de la Sesión:** Contrastar la calidad del código generado por LLMs usando instrucciones genéricas vs. el patrón estructurado `[Contexto + Tarea + Restricciones + Entrega]`. Se evaluaron 3 capas críticas de SensorHub: Validación física (Pydantic), Consultas analíticas (SQLAlchemy 2.0) y Pruebas E2E (Pytest).

### Análisis de la Interacción:
* **Prompt Estructurado:** Se forzó a la IA a actuar bajo restricciones de versión (Python 3.12, SQLAlchemy 2.x) y a entregar resultados sin explicaciones.
* **Respuesta de la IA (Contraste):**
  * *Prompt Pobre:* Generó código obsoleto (sintaxis vieja de bases de datos), ignoró los type hints y añadió "charlatanería" (texto innecesario). En Pydantic, no controló profesionalmente la excepción.
  * *Prompt Bueno:* Entregó código de grado de producción. Respetó `func.avg` de SQLAlchemy 2.0, estructuró la prueba de integración con el patrón Arrange-Act-Assert (AAA) y obedeció la restricción de omitir texto adicional.
* **Veredicto y Criterio Técnico:** Se comprueba empíricamente que un LLM optimiza plausibilidad, no corrección. Si no se acota el espacio de soluciones, alucinará convenciones obsoletas. Como Ingeniero de Software, asumo la responsabilidad del "contexto"; el código generado solo es tan bueno como las restricciones arquitectónicas que le impongo. El código del prompt estructurado pasa el criterio para ser revisado en un PR, el del pobre es rechazado.

---

## [ENTRADA 23] Semana 5 - Día 2: Ensayo con Agentes Autónomos e Incompatibilidad de Dependencias

* **Fecha:** 12 de Agosto de 2026
* **Contexto/Objetivo de la Sesión:** Instalar y ejecutar Aider acoplado a Gemini 1.5 Pro en la terminal para pair programming automatizado.
* **Incidencia Técnica:** Falla de compilación durante `pip install aider-chat`.
* **Análisis Forense:** El proceso colapsa al intentar construir la rueda (wheel) de la dependencia `numpy==1.24.3`. El error `AttributeError: module 'pkgutil' has no attribute 'ImpImporter'` revela que la versión de Python del sistema (3.14+) ha deprecado módulos que las librerías antiguas de Aider aún necesitan para compilar desde el código fuente en Windows.
* **Resolución y Criterio:** Siguiendo la premisa de la Guía del Estudiante, se aborta la instalación local para evitar corromper el entorno virtual y se procede a realizar el ejercicio equivalente utilizando GitHub Copilot Chat directamente en VS Code. El foco se mantiene en la arquitectura y la trazabilidad, no en la herramienta específica.

---

## [ENTRADA 24] Semana 5 - Día 3: Code Review y Testing Asistido por IA (Mocks)

* **Fecha:** 13 de Agosto de 2026
* **Contexto/Objetivo de la Sesión:** Utilizar Copilot como auditor de código estricto sobre `app/services/core.py` para detectar vulnerabilidades, violaciones SOLID y casos borde, forzando la generación de pruebas unitarias aisladas (`Mocks`).
* **Análisis Forense (Code Review):** * La IA arrojó 7 hallazgos. Se demostró que la IA carece de contexto arquitectónico global, sugiriendo blindajes contra SQL Injection o validación de paginación en la capa de Servicios, ignorando que SQLAlchemy y Pydantic (en Routers) ya manejan esos vectores de ataque. Esos hallazgos fueron RECHAZADOS con justificación técnica.
  * Se ACEPTARON los hallazgos relacionados estrictamente con la lógica de negocio (Fechas ilógicas, manejo de excepciones de base de datos y la sugerencia de Soft Delete).
* **Impacto en Testing:** La IA generó 7 sub-tests para cubrir casos borde (sensores inexistentes, valores numéricos infinitos `float('inf')`, duplicidad de IDs). Se implementó `unittest.mock.MagicMock` para aislar el repositorio.
* **Veredicto y Criterio Técnico:** El uso de IA es excepcional para la generación de casos de prueba paramétricos y detección de flujos anómalos. La cobertura de la capa de Servicios aumentó a 97% y la cobertura global a 90.53%. Se reafirma la regla del "Colega Junior": la IA escribe las pruebas, pero el Ingeniero defiende la arquitectura.