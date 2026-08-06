from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


# --- ESQUEMAS PARA SENSORES ---
class SensorBase(BaseModel):
    type: str = Field(..., description="Tipo de sensor (ej. temperature, humidity)")
    name: str = Field(..., description="Nombre del sensor")


class SensorCreate(SensorBase):
    id: str = Field(..., description="ID único (ej. TEMP-01)")


class SensorOut(SensorBase):
    id: str
    model_config = ConfigDict(from_attributes=True)


# --- ESQUEMAS PARA LECTURAS ---


# EXTRAEMOS LAS REGLAS FÍSICAS A LA CLASE BASE
class ReadingBase(BaseModel):
    value: float | None = None
    unit: str | None = None

    @model_validator(mode="after")
    def check_physics(self) -> "ReadingBase":
        # Si alguno falta, no podemos validar la combinación, lo dejamos pasar
        # (Esto es útil para PATCH donde pueden enviar solo el 'value' sin 'unit')
        if self.unit is None or self.value is None:
            return self

        unit_upper = self.unit.upper()

        # Filtros físicos
        if unit_upper in ["C", "F", "K"]:
            if unit_upper == "C" and self.value < -273.15:
                raise ValueError("Física inválida: Temperatura C bajo el cero absoluto")
            elif unit_upper == "F" and self.value < -459.67:
                raise ValueError("Física inválida: Temperatura F bajo el cero absoluto")
            elif unit_upper == "K" and self.value < 0:
                raise ValueError("Física inválida: Temperatura K bajo cero")
        elif unit_upper == "%":
            if self.value < 0 or self.value > 100:
                raise ValueError(
                    "Física inválida: La humedad debe estar entre 0% y 100%"
                )
        else:
            raise ValueError(f"Física inválida: Unidad desconocida '{self.unit}'")

        self.unit = unit_upper  # Normaliza a mayúscula
        return self


class ReadingCreate(ReadingBase):
    # En creación, forzamos que vengan los dos campos obligatoriamente
    value: float
    unit: str


class ReadingUpdate(ReadingBase):
    # En actualización, ambos siguen siendo opcionales (ya heredan de la base)
    pass


class ReadingOut(ReadingBase):
    # En salida, forzamos que existan
    value: float
    unit: str
    id: int
    sensor_id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
