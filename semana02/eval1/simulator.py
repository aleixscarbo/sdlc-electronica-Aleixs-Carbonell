import random

from detector import SensorReading


class SensorSimulator:
    """Generador de telemetría sintética usando distribución gaussiana."""
    
    def __init__(
        self, 
        sensor_id: str, 
        mu_temp: float = 22.0, 
        sigma_temp: float = 2.0,
        mu_hum: float = 50.0, 
        sigma_hum: float = 5.0
    ) -> None:
        self.sensor_id = sensor_id
        self.mu_temp = mu_temp
        self.sigma_temp = sigma_temp
        self.mu_hum = mu_hum
        self.sigma_hum = sigma_hum

    def generate_reading(self) -> SensorReading:
        """Genera una nueva lectura simulada limitando la humedad de 0 a 100%."""
        temp = random.gauss(self.mu_temp, self.sigma_temp)
        hum = random.gauss(self.mu_hum, self.sigma_hum)
        
        # Lógica de negocio: La humedad no puede salir del rango 0-100
        hum = max(0.0, min(100.0, hum))
        
        return SensorReading(
            sensor_id=self.sensor_id,
            temperature=round(temp, 2),
            humidity=round(hum, 2)
        )