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