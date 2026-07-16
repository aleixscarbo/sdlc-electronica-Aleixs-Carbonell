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
* **Lo que cambié respecto a lo generado y el porqué:** 1. *Cambio:* Agregué el decorador `@pytest.fixture` para aislar el setup del `UartDevice`. La IA inicialmente sugería instanciar el dispositivo manualmente dentro de cada uno de los 3 tests del device.
  2. *Por qué (Reflexión SOLID & TDD):* Al usar Fixtures centralizamos el "Arrange" del patrón AAA, respetando el principio DRY (Don't Repeat Yourself) y logrando inyectar las dependencias (DIP) de la configuración y de los 3 parsers (incluyendo el parser CAN de extensión) de manera limpia y modular en cada test.