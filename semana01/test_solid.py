import pytest
from semana01.solid_srp_ocp_lsp import (
    SensorReader, DataLogger, SensorReading,
    ConsoleAlert, FileAlert, AnomalyDetector,
    TemperatureSensor, HumiditySensor, ViolacionLSP, process_sensor
)

# --- PRUEBAS SRP ---
def test_srp_reader_responsibility():
    # Arrange
    reader = SensorReader("SNS-01")
    # Act
    reading = reader.get_reading()
    # Assert
    assert reading.sensor_id == "SNS-01"
    assert reading.value == 25.0

def test_srp_logger_responsibility():
    # Arrange
    logger = DataLogger()
    reading = SensorReading("SNS-01", 30.0)
    # Act
    result = logger.save(reading)
    # Assert
    assert "Persistido con éxito" in result


# --- PRUEBAS OCP ---
def test_ocp_console_alert_strategy():
    # Arrange
    detector = AnomalyDetector(ConsoleAlert(), threshold=40.0)
    reading = SensorReading("SNS-TEMP", 45.0)
    # Act
    result = detector.check(reading)
    # Assert
    assert result == "Console: Anomalia en SNS-TEMP"

def test_ocp_file_alert_strategy():
    # Arrange
    detector = AnomalyDetector(FileAlert(), threshold=40.0)
    reading = SensorReading("SNS-HUM", 50.0)
    # Act
    result = detector.check(reading)
    # Assert
    assert result == "File Log: Anomalia en SNS-HUM"


# --- PRUEBAS LSP ---
def test_lsp_interchangeable_sensors():
    # Arrange
    t_sensor = TemperatureSensor()
    h_sensor = HumiditySensor()
    # Act & Assert (Ambos funcionan idénticamente en la función cliente)
    assert process_sensor(t_sensor) == 36.5
    assert process_sensor(h_sensor) == 60.2

def test_lsp_breakage_demonstration():
    # Arrange
    broken_sensor = ViolacionLSP()
    # Act & Assert: Demuestra cómo la violación rompe la ejecución genérica
    with pytest.raises(RuntimeError):
        process_sensor(broken_sensor)