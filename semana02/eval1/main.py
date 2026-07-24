from alerts import AlertManager, FileAlertStrategy
from detector import AnomalyDetector
from registry import SensorRegistry
from simulator import SensorSimulator


def run_simulation(
    num_sensors: int = 10, 
    cycles: int = 60, 
    log_path: str = "system_alerts.log"
) -> int:
    """Orquesta el ciclo de vida completo de la telemetría IoT."""
    
    # 1. Inicializar infraestructura y reglas de negocio
    registry = SensorRegistry()
    detector = AnomalyDetector(temp_threshold=35.0, humidity_threshold=80.0)
    alert_manager = AlertManager(FileAlertStrategy(filepath=log_path))
    
    # 2. Inicializar el hardware simulado (10 sensores)
    # Les damos medias térmicas progresivas para asegurar que algunos generen anomalías
    simulators = [
        SensorSimulator(
            sensor_id=f"SENSOR-{i:02d}", 
            mu_temp=25.0 + i,   # SENSOR-10 tendrá media de 35°C (generará alertas)
            mu_hum=50.0 + i
        )
        for i in range(1, num_sensors + 1)
    ]
    
    readings_processed = 0
    
    # 3. Motor de ejecución continuo (Bucle principal)
    for _ in range(cycles):
        for sim in simulators:
            # Fase A: Ingesta
            reading = sim.generate_reading()
            registry.add_reading(reading)
            
            # Fase B: Evaluación
            result = detector.evaluate(reading)
            
            # Fase C: Despacho de Alertas
            if result["is_anomaly"]:
                alert_manager.process_anomaly(reading.sensor_id, result["type"])
                
            readings_processed += 1
            
    return readings_processed


if __name__ == "__main__":
    print("Iniciando motor de monitoreo IoT...")
    total = run_simulation()
    print(f"Simulación completada con éxito. Lecturas procesadas: {total}")