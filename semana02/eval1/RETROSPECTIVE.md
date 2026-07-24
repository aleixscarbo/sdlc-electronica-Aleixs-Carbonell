# Sprint 1 Retrospective - Sistema de Monitoreo IoT

**Fecha:** 24/07/26
**Participantes:** Aleixs Carbonell (Solo Developer)

### 🟢 ¿Qué salió bien? (What went well)
1. **Disciplina TDD:** Logré mantener de forma inquebrantable el ciclo Red -> Green -> Refactor. Las pruebas estadísticas del simulador gaussiano y el uso de *Mocks/Fixtures* para la consola fueron un éxito total.
2. **Arquitectura SOLID:** La implementación del `AlertManager` mediante el Patrón *Strategy* aisló perfectamente la lógica de negocio de los detalles de infraestructura (Consola vs. Archivo), facilitando las pruebas.
3. **Calidad Automatizada:** La configuración del `pyproject.toml` funcionó como un escudo perfecto. Las advertencias de Mypy y Ruff me forzaron a escribir código estrictamente tipado desde el día 1.

### 🔴 ¿Qué se puede mejorar? (What to improve)
1. **Planificación de Historias:** Durante la implementación del motor de reglas, estuve a punto de saltarme la US-03 (Humedad) para pasar directo a las Alertas. Me faltó revisar el *Sprint Backlog* de forma estructurada antes de iniciar la siguiente *Feature Branch*.
2. **Gestión de Rutas en Python (PYTHONPATH):** Al reorganizar los módulos dentro de la carpeta `eval1/`, rompí momentáneamente las pruebas porque Pytest no encontraba los archivos. 

### 🎯 Acción Concreta para el Próximo Sprint (Action Item)
**Checklist de Transición de Tarea:** Antes de ejecutar el comando `git checkout -b` para crear una nueva rama, abriré obligatoriamente el archivo `backlog.md` para verificar exactamente qué ID de historia sigue en prioridad (MoSCoW) y no dejar características del núcleo a medias.