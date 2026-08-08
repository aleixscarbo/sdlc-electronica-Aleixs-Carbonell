import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# --- INYECCIÓN DE RUTAS E IMPORTACIÓN DE MODELOS ---
# Esto permite que Alembic (que corre en la carpeta migrations/)
# encuentre la carpeta 'app/' que está un nivel arriba.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db import Base

# IMPORTACIÓN CORREGIDA: Traemos los modelos desde el __init__.py
from app.models import ReadingModel, SensorModel  # noqa: F401

# ---------------------------------------------------

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# Imprimimos las tablas para debuggear la detección de Alembic
print(">>> DEBUG ALEMBIC: Tablas detectadas en Python:", Base.metadata.tables.keys())
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # 1. Leemos la configuración base del alembic.ini
    configuration = config.get_section(config.config_ini_section, {})
    
    # 2. INTERRUPTOR CLOUD: Si existe DATABASE_URL en el entorno (ej. en Render o Docker
    # Compose),sobrescribimos la URL del .ini para usar la de producción/entorno virtual
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        # Forzamos el uso del driver moderno (psycopg 3) reemplazando cualquier prefijo 
        # genérico
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)
        elif db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)
            
        configuration["sqlalchemy.url"] = db_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()