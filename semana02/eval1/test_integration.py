from pathlib import Path

from main import run_simulation


def test_full_system_integration(tmp_path: Path) -> None:
    """Valida que los 4 componentes del sistema interactúen sin fallos bajo carga."""
    # Arrange: Archivo temporal para no ensuciar el disco duro durante el test
    log_file = tmp_path / "integration_alerts.log"
    
    # Act: Ejecutamos el motor orquestador (10 sensores, 60 iteraciones)
    total_readings = run_simulation(
        num_sensors=10, 
        cycles=60, 
        log_path=str(log_file)
    )
    
    # Assert 1: Se debieron procesar exactamente 600 lecturas
    assert total_readings == 600
    
    # Assert 2: El archivo de log debe existir y contener alertas generadas por el simulador
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "ALERTA" in content