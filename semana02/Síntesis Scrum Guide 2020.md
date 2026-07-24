# Síntesis de la Scrum Guide 2020

## 1. Los 3 Roles (El Scrum Team)
En Scrum no existen jerarquías tradicionales ni cargos como "jefe de proyecto"; existe un equipo multidisciplinario enfocado en entregar valor:
* **Developers (Desarrolladores):** Las personas del equipo comprometidas a crear cualquier aspecto de un Incremento utilizable en cada Sprint. (En la Evaluación 1, tú ejecutas este rol al construir el código Python y los tests).
* **Product Owner (PO):** Maximiza el valor del producto y gestiona de forma transparente el Product Backlog.
* **Scrum Master (SM):** Líder que vela por la efectividad del equipo y la adopción correcta del marco Scrum.

## 2. Los 5 Eventos y sus Timeboxes (Límites de Tiempo)
Todos los eventos son bloques de tiempo acotados (timeboxed). Los límites oficiales de la guía son para Sprints de 1 mes; al lado se incluye la equivalencia adaptada para nuestro desarrollo semanal:

| Evento Scrum | Propósito Técnico | Timebox Oficial (Sprint 1 mes) | Adaptación a Sprint Semanal |
| :--- | :--- | :--- | :--- |
| **The Sprint** | Contenedor de todos los demás eventos donde se crea valor. | ≤ 1 mes | 1 semana |
| **Sprint Planning** | Define qué se hará en el Sprint y cómo se construirá. | Máx. 8 h | ~ 1.5 - 2 h |
| **Daily Scrum** | Sincronización diaria e inspección del progreso hacia el Sprint Goal. | 15 min (estricto) | 15 min |
| **Sprint Review** | Inspección del Incremento terminado con los interesados (stakeholders). | Máx. 4 h | ~ 45 - 60 min |
| **Sprint Retrospective**| Inspección del equipo sobre sí mismo: proceso, herramientas y relaciones. | Máx. 3 h | ~ 30 - 45 min |

## 3. Los 3 Artefactos y sus Compromisos Obligatorios
Cada artefacto contiene un compromiso (commitment) que garantiza la transparencia y la medición del progreso:

```text
┌─────────────────────────┐       Contiene       ┌─────────────────────────┐
│     PRODUCT BACKLOG     │ ───────────────────> │      PRODUCT GOAL       │
└─────────────────────────┘                      └─────────────────────────┘

┌─────────────────────────┐       Contiene       ┌─────────────────────────┐
│     SPRINT BACKLOG      │ ───────────────────> │       SPRINT GOAL       │
└─────────────────────────┘                      └─────────────────────────┘

┌─────────────────────────┐       Contiene       ┌─────────────────────────┐
│        INCREMENT        │ ───────────────────> │   DEFINITION OF DONE    │
└─────────────────────────┘                      └─────────────────────────┘
```

* **Product Backlog:** Lista ordenada y viva de todo lo que se necesita en el producto.
  * *Compromiso:* Product Goal (Objetivo del Producto a largo plazo).
* **Sprint Backlog:** El conjunto de elementos seleccionados para el Sprint + el plan para entregarlos.
  * *Compromiso:* Sprint Goal (Objetivo único del Sprint actual).
* **Increment (Incremento):** La suma de todos los elementos del Product Backlog completados durante el Sprint.
  * *Compromiso:* Definition of Done (Criterio global de calidad que debe cumplirse al 100%).

## 4. Los 5 Valores de Scrum
Son la base actitudinal de la ingeniería ágil:
* **Compromiso (Commitment):** Con alcanzar las metas del equipo.
* **Foco (Focus):** En el trabajo del Sprint y el Sprint Goal.
* **Franqueza / Apertura (Openness):** Sobre el trabajo y los desafíos encontrados.
* **Respeto (Respect):** Hacia las capacidades e independencia de los miembros del equipo.
* **Coraje (Courage):** Para hacer lo correcto y trabajar en problemas difíciles.

## 5. Diferencia Clave: Definition of Done vs. Criterios de Aceptación

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        CRITERIO DE ACEPTACIÓN                          │
├────────────────────────────────────────────────────────────────────────┤
│ • Nivel: Especifico de UNA User Story.                                 │
│ • Formato: Gherkin (Given / When / Then).                              │
│ • Ejemplo: "Given lectura T = 36 °C, Then marca_anomalia = True."      │
└────────────────────────────────────────────────────────────────────────┘

                                   VS

┌────────────────────────────────────────────────────────────────────────┐
│                           DEFINITION OF DONE                           │
├────────────────────────────────────────────────────────────────────────┤
│ • Nivel: Global e inquebrantable para TODO el repositorio.              │
│ • Formato: Checklist de calidad industrial.                            │
│ • Ejemplo: Pruebas unitarias en verde (pytest), Cobertura >= 80%,      │
│   Type Hints validados, PR revisado y AI Log registrado.               │
└────────────────────────────────────────────────────────────────────────┘
```