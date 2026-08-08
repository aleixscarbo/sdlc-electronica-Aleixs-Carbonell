# 🛠️ Reto EDSIA: De Electrónica a Desarrollo de Software con IA

[![CI](https://github.com/aleixscarbo/sdlc-electronica-Aleixs-Carbonell/actions/workflows/ci.yml/badge.svg)](https://github.com/aleixscarbo/sdlc-electronica-Aleixs-Carbonell/actions/workflows/ci.yml)

**Estudiante:** Aleixs Carbonell Montaño  
**Perfil:** Ingeniería en Instrumentación Electrónica (Universidad Veracruzana) ➡️ Desarrollo Backend Moderno & DevOps

---

## 📖 Descripción del Proyecto

Este repositorio documenta mi transición técnica desde la programación de sistemas embebidos (firmware y hardware) hacia la ingeniería de software backend profesional utilizando Python, FastAPI, SQLAlchemy, Docker, GitHub Actions y despliegue continuo en la nube.

### 🌐 Producción (API Desplegada en Vivo)

La aplicación **SensorHub API** se encuentra desplegada en la nube utilizando infraestructura contenerizada (Docker) y base de datos PostgreSQL orquestada mediante Render:

* **Swagger UI (Documentación Interactiva):** [https://sensorhub-api-bi65.onrender.com/docs](https://sensorhub-api-bi65.onrender.com/docs)
* **Endpoint de Salud (Healthcheck):** [https://sensorhub-api-bi65.onrender.com/health](https://sensorhub-api-bi65.onrender.com/docs#/default/health_check_health_get)

---

## 🏗️ Arquitectura y Tecnologías

* **Backend Framework:** FastAPI (Python 3.12)
* **Persistencia & ORM:** SQLAlchemy 2.x + PostgreSQL (Producción) / SQLite (Pruebas aisladas)
* **Migraciones de Base de Datos:** Alembic
* **Contenerización & Orquestación:** Docker, Docker Compose
* **CI/CD:** GitHub Actions (Ruff, Mypy, Pytest con Cobertura ≥ 80%)
* **Infraestructura como Código (IaC):** `render.yaml` (Blueprints)

---

## 🚀 Guía de Instalación y Ejecución Local

### Opción 1: Entorno de Producción Local (Docker Compose)
Para levantar la API junto con la base de datos PostgreSQL orquestados mediante un solo comando:

```bash
docker compose up --build
```
La API estará disponible en http://localhost:8000/docs.

### Opción 2: Entorno Virtual Local (Desarrollo)

```bash
git clone [https://github.com/aleixscarbo/sdlc-electronica-Aleixs-Carbonell.git](https://github.com/aleixscarbo/sdlc-electronica-Aleixs-Carbonell.git)
cd sdlc-electronica-Aleixs-Carbonell
python -m venv venv

# En Windows:
call venv\Scripts\activate
# En Linux/Mac:
# source venv/bin/activate

pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Pruebas Automatizadas y Calidad de Código
El proyecto incluye un pipeline estricto de Integración Continua (CI) que valida la calidad en cada push:

```bash
# Ejecutar suite de pruebas con cobertura
pytest --cov=app --cov-fail-under=80

# Verificación de tipos estáticos
mypy app --ignore-missing-imports

# Linter y formateador
ruff check .
```

## Reflexión SOLID y DevOps
1. Inversión de Dependencias (DIP) & 12-Factor App: La configuración de la base de datos lee dinámicamente DATABASE_URL desde el entorno (os.getenv), aislando credenciales y adaptando los drivers según el entorno (SQLite para pruebas, PostgreSQL para Docker/Render).

2. Infraestructura Reproducible: La migración de base de datos se desacopló del código principal de la API mediante Alembic, ejecutándose como un paso previo atómico durante el arranque del contenedor.

3. Shift-Left Testing & Observabilidad: Se implementó un endpoint dedicado /health para pruebas de salud del orquestador en producción, garantizando cero downtime y despliegues seguros.