#Configuración del motor (Engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# El "puerto serial" hacia nuestra memoria no volátil
# (Usamos SQLite que guarda todo en un archivo local por ahora)
engine = create_engine("sqlite:///sensorhub.db", connect_args={"check_same_thread": False})

# La fábrica de "transacciones" (Start bit / Stop bit)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# La placa base de donde heredarán todos los modelos
class Base(DeclarativeBase):
    pass