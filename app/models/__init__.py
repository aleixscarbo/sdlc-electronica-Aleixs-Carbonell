#Creamos el modelo de lectura, tal como lo indican las instrucciones

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

class ReadingModel(Base):
    __tablename__ = "readings"

    # id es nuestra llave principal (primary key)
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # sensor_id tiene un index=True (nuestra Lookup Table para búsquedas rápidas)
    sensor_id: Mapped[str] = mapped_column(index=True)
    value: Mapped[float]
    unit: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)