from pathlib import Path
from typing import Any

from alerts import AlertManager, ConsoleAlertStrategy, FileAlertStrategy


def test_console_alert_strategy_prints_to_stdout(capsys: Any) -> None:
    # Arrange
    strategy = ConsoleAlertStrategy()
    manager = AlertManager(strategy)
    
    # Act
    manager.process_anomaly("SENSOR-05", "HIGH_TEMPERATURE")
    
    # Assert
    captured = capsys.readouterr()
    assert "[CRITICAL]" in captured.out
    assert "SENSOR-05" in captured.out
    assert "HIGH_TEMPERATURE" in captured.out


def test_file_alert_strategy_writes_to_log(tmp_path: Path) -> None:
    # Arrange
    log_file = tmp_path / "test_alerts.log"
    strategy = FileAlertStrategy(filepath=str(log_file))
    manager = AlertManager(strategy)
    
    # Act
    manager.process_anomaly("SENSOR-09", "HIGH_HUMIDITY")
    
    # Assert
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "ALERTA" in content
    assert "SENSOR-09" in content
    assert "HIGH_HUMIDITY" in content