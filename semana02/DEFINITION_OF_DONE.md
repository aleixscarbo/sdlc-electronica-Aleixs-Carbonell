# Definition of Done (DoD) - Proyecto IoT

Para que una Historia de Usuario (Feature) sea considerada "Terminada" (Done) y pueda fusionarse a la rama principal, debe cumplir estrictamente con los siguientes criterios:

- [ ] **1. Criterios Gherkin Implementados:** Todos los escenarios definidos en la Historia de Usuario han sido traducidos a tests automatizados.
- [ ] **2. TDD Estricto:** Existe evidencia en el historial de Git de que las pruebas fueron escritas y fallaron (RED) antes de implementar el código funcional (GREEN).
- [ ] **3. Cobertura de Pruebas (Coverage):** La ejecución de `pytest` arroja una cobertura de código igual o superior al 80% (`--cov-fail-under=80`).
- [ ] **4. Análisis Estático (Mypy):** El código pasa la revisión de `mypy` sin errores, garantizando que no hay funciones sin tipado estático (`disallow_untyped_defs = true`).
- [ ] **5. Calidad de Código (Ruff):** El código cumple con las reglas de estilo (E, F, I, UP, B) analizadas mediante `ruff check`, sin advertencias ni "code smells".
- [ ] **6. Revisión Humana (Pull Request):** El código fue sometido mediante un PR, revisado línea por línea en el diff por el autor antes del merge.
- [ ] **7. Documentación y Bitácora:** Los *docstrings* están actualizados y se ha registrado el uso de herramientas de IA en `AI_LOG.md`.