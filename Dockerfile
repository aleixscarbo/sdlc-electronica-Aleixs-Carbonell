# ==============================================================================
# ETAPA 1: Banco de Ensamble y Carga de Componentes (Builder)
# En esta etapa temporal instalamos pip, compilamos librerías y preparamos el venv.
# Ninguno de los residuos de instalación se heredará a la placa final.
# ==============================================================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Evitar que Python escriba archivos .pyc y forzar salida de logs inmediata
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear entorno virtual de producción aislado
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instalar dependencias (BOM) en el entorno virtual
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ==============================================================================
# ETAPA 2: Placa Final de Producción (Runner)
# Sustrato ultra ligero (< 200 MB) que solo contiene el binario/venv ya construido
# y el firmware/código fuente de la aplicación.
# ==============================================================================
FROM python:3.12-slim AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

# Copiar el entorno virtual ya compilado y listo desde la etapa "builder"
COPY --from=builder /opt/venv /opt/venv

# Copiar el ruteo de pistas (código fuente) a la placa de producción
COPY . .

# Pin de salida para tráfico de red
EXPOSE 8000

# Comando de arranque atómico (Correr migraciones Alembic + Servidor Uvicorn)
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]