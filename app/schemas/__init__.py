from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


# --- ESQUEMAS PARA SENSORES ---
class SensorBase(BaseModel):
    type: str = Field(..., description="Tipo de sensor (ej. temperature, humidity)")
    name: str = Field(..., description="Nombre del sensor")
    location: str = Field(..., description="Ubicación física del sensor")  # <- ¡NUEVO!
    threshold: float | None = Field(
        default=None, description="Umbral para alerta de anomalías", allow_inf_nan=False
    )


class SensorCreate(SensorBase):
    id: str = Field(..., description="ID único (ej. TEMP-01)")


class SensorOut(SensorBase):
    id: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


# --- ESQUEMAS PARA LECTURAS ---
class ReadingBase(BaseModel):
    value: float | None = Field(default=None, allow_inf_nan=False)
    unit: str | None = None

    @model_validator(mode="after")
    def check_physics(self) -> "ReadingBase":
        if self.unit is None or self.value is None:
            return self

        unit_upper = self.unit.upper()
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

        self.unit = unit_upper
        return self


class ReadingCreate(ReadingBase):
    value: float = Field(..., allow_inf_nan=False)
    unit: str


class ReadingUpdate(ReadingBase):
    pass


class ReadingOut(ReadingBase):
    id: int
    sensor_id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# --- ESQUEMAS PARA ALERTAS ---
class AlertBase(BaseModel):
    status: str = Field(
        ..., description="Estado de la alerta: open, acknowledged, resolved"
    )


class AlertUpdate(AlertBase):
    pass


class AlertOut(AlertBase):
    id: int
    sensor_id: str
    value: float
    threshold: float
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- ESQUEMAS PARA ESTADÍSTICAS (RF-6) ---
class SensorStats(BaseModel):
    min: float = Field(..., description="Valor mínimo registrado")
    max: float = Field(..., description="Valor máximo registrado")
    avg: float = Field(..., description="Valor promedio registrado")
