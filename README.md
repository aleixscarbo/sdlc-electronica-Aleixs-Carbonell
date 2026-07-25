# 🛠️ Reto EDSIA: De Electrónica a Desarrollo de Software con IA
**Estudiante:** Aleixs Carbonell Montaño  
**Perfil:** Ingeniería en Instrumentación Electrónica (Universidad Veracruzana) ➡️ Desarrollo Backend Moderno

---

## 📖 Descripción del Proyecto

Este repositorio documenta mi transición técnica desde la programación de sistemas embebidos (firmware y hardware) hacia la ingeniería de software backend profesional utilizando Python y metodologías modernas (TDD, Scrum, control de versiones, entornos virtuales, IA como copiloto).

---

## 🏆 Proyectos Destacados

### 🏭 1. Sistema de Monitoreo IoT Industrial (Semana 02 - Evaluación 1)
Desarrollo del núcleo lógico para una bodega industrial aplicando **Scrum** y **TDD (Test-Driven Development) estricto**. El sistema procesa telemetría, detecta anomalías térmicas y de humedad, y orquesta respuestas del sistema.
* **Patrón de Diseño Strategy:** Implementado en el `AlertManager` para desacoplar la lógica de negocio de las salidas de infraestructura (Consola vs. Archivo Log), respetando el principio Open/Closed.
* **Simulación Estocástica:** Creación de un generador de telemetría gaussiana (`random.gauss`) para estresar el sistema sin depender de hardware físico.
* **Orquestación y Carga:** Integración de componentes bajo carga real (10 sensores emulados procesando 600 iteraciones ininterrumpidas).
* **Gestión Ágil:** Elaboración de Product Backlog con 10 historias de usuario (formato **Gherkin** y priorización **MoSCoW**), Sprint Planning, Retrospectiva y un robusto `DEFINITION_OF_DONE.md`.
* **Arquitectura:** Documentación del sistema mediante un **Diagrama C4 (Contenedores)** usando Mermaid.

### 🏎️ 2. El Driver UART Modernizado (Semana 01)
Refactorización de un Driver UART clásico. Se migró de un enfoque procedural en C (basado en buffers globales) a un diseño orientado a objetos en Python.
* **Polimorfismo:** Incorporación de decodificadores dinámicos (Modbus, NMEA, CAN).
* **Concurrencia:** Hilos seguros mediante `threading.Lock`.
* **Persistencia:** Almacenamiento ágil en JSON-lines.

---

## 🚀 Instalación

Para configurar el entorno de desarrollo de forma aislada, ejecuta en tu terminal:

```cmd
git clone [https://github.com/aleixscarbo/sdlc-electronica-Aleixs-Carbonell.git](https://github.com/aleixscarbo/sdlc-electronica-Aleixs-Carbonell.git)
cd sdlc-electronica-Aleixs-Carbonell
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🧪 Pruebas y Aseguramiento de Calidad (QA)

El proyecto está construido bajo la filosofía de Desarrollo Guiado por Pruebas (TDD) y cumple con barreras de calidad automatizadas estrictas.

**Ejecutar pruebas del Sistema IoT (Semana 2) con métricas de cobertura:**
```cmd
pytest semana02/eval1/ --cov=semana02/eval1 --cov-fail-under=80 -v
```

**Ejecutar pruebas del Driver UART (Semana 1):**
```cmd
pytest semana01/uart_driver/tests/ -v
```

**Auditoría de Código y Tipado Estático Global:**
Garantiza que el código no tenga "code smells" y que las firmas de funciones estén estrictamente tipadas.
```cmd
mypy semana01/ semana02/
ruff check semana01/ semana02/
```

---

## 🧠 Reflexión Teórica y Buenas Prácticas

### Principios SOLID Aplicados
1. **SRP:** El controlador de hardware (`UartDevice`) se separó del guardado de datos (`DataRecorder`).
2. **OCP:** El sistema procesa abstracciones (`MessageParser` / `AlertStrategy`), lo que permite agregar nuevos protocolos (CAN Bus) o salidas de alerta (Archivos) sin modificar la lógica existente.
3. **LSP:** Todos los decodificadores y estrategias de alertas respetan estrictamente los tipos de retorno de la clase base, evitando excepciones inesperadas.
4. **ISP:** Se dividieron interfaces gigantes en micro-contratos lógicos (`Readable`, `Writable`).
5. **DIP:** Gracias a la inyección de dependencias (`Protocol` / `AlertStrategy`), se desacopló el hardware real y la infraestructura, permitiendo inyectar fakes/mocks en memoria para correr pruebas en milisegundos.

### Bitácora de Inteligencia Artificial
El proyecto incorpora el uso avanzado de LLMs (Modelos de Lenguaje Grande) como copiloto de ingeniería, documentando prompts, decisiones arquitectónicas y refactorizaciones en el archivo `AI_LOG.md`.