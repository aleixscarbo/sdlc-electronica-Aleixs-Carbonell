import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


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

# Evaluamos dinamicamente si estamos en SQLite o PostgreSQL
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL no necesita check_same_thread
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Fabrica de sesiones
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# Clase base para los modelos SQLAlchemy
class Base(DeclarativeBase):
    pass


# Generador de sesiones para inyeccion de dependencias en FastAPI
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
