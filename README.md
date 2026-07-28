# 🛠️ Reto EDSIA: De Electrónica a Desarrollo de Software con IA
**Estudiante:** Aleixs Carbonell Montaño  
**Perfil:** Ingeniería en Instrumentación Electrónica (Universidad Veracruzana) ➡️ Desarrollo Backend Moderno

---

## 📖 Descripción del Proyecto

Este repositorio documenta mi transición técnica desde la programación de sistemas embebidos (firmware y hardware) hacia la ingeniería de software backend profesional utilizando Python y metodologías modernas (TDD, control de versiones, entornos virtuales).

### 🏎️ Proyecto Destacado: El Driver UART Modernizado (Semana01)
El proyecto principal de la Semana 1 es la refactorización de un **Driver UART**. Se migró de un enfoque procedural en C (basado en buffers globales) a un diseño orientado a objetos en Python, incorporando decodificadores polimórficos (Modbus, NMEA, CAN), concurrencia segura (`threading.Lock`) y persistencia en JSON-lines.

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

## 🧪 Cómo correr los tests

El proyecto fue construido bajo la filosofía de Desarrollo Guiado por Pruebas (TDD). Para ejecutar la suite de **12 pruebas unitarias** que validan la resiliencia del hardware emulado y verificar el tipado/estilo, utiliza:

```cmd
pytest semana01/uart_driver/tests/ -v
mypy semana01/
ruff check semana01/
```

---

## 🧠 Reflexión SOLID

La adopción de los principios SOLID fue fundamental para crear un software de grado industrial:
1. **SRP:** El controlador de hardware (`UartDevice`) se separó del guardado de datos (`DataRecorder`).
2. **OCP:** El sistema procesa abstracciones (`MessageParser`), lo que me permitió agregar el protocolo **CAN Bus** sin modificar la lógica existente.
3. **LSP:** Todos los decodificadores respetan estrictamente los tipos de retorno de la clase base, evitando excepciones inesperadas.
4. **ISP:** Se dividieron interfaces gigantes en micro-contratos lógicos (`Readable`, `Writable`).
5. **DIP:** Gracias a la inyección de dependencias (`Protocol`), se desacopló el hardware real, permitiendo inyectar repositorios en memoria (RAM) para correr pruebas en milisegundos.