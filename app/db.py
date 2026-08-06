# Configuración del motor (Engine)
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


def get_database_url() -> str:
    # Leemos la variable de entorno. Si no existe, usamos SQLite por defecto.
    url = os.getenv("DATABASE_URL", "sqlite:///sensorhub.db")

    # Normalizamos la URL para asegurar que use el driver psycopg
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://") and "+psycopg" not in url:
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


SQLALCHEMY_DATABASE_URL = get_database_url()

# El "puerto serial" hacia nuestra memoria no volátil
# Evaluamos dinámicamente si estamos en SQLite o PostgreSQL
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL no necesita ni soporta check_same_thread
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# La fábrica de "transacciones" (Start bit / Stop bit)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# La placa base de donde heredarán todos los modelos
class Base(DeclarativeBase):
    pass
