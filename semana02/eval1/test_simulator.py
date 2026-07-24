import random
from detector import SensorReading
from simulator import SensorSimulator

def test_simulator_generates_gaussian_distribution() -> None:
    # Arrange: Semilla fija para que el test sea determinista y reproducible
    random.seed(42)  
    
    # Inicializamos con Media (mu)=22.0°C y Desviación (sigma)=2.0°C
    simulator = SensorSimulator(
        sensor_id="SIM-01",
        mu_temp=22.0, sigma_temp=2.0,
        mu_hum=50.0, sigma_hum=5.0
    )
    
    # Act: Generamos 1000 lecturas de golpe
    readings = [simulator.generate_reading() for _ in range(1000)]
    
    # Assert 1: Tipos de datos correctos
    assert isinstance(readings[0], SensorReading)
    assert readings[0].sensor_id == "SIM-01"
    
    # Assert 2: Regla empírica (95% dentro de +/- 2 sigma, es decir, de 18°C a 26°C)
    within_2_sigma = [
        r for r in readings 
        if 18.0 <= r.temperature <= 26.0
    ]
    
    # El 95% de 1000 es 950. Damos un margen por la naturaleza estocástica (900 a 1000)
    assert 900 <= len(within_2_sigma) <= 1000