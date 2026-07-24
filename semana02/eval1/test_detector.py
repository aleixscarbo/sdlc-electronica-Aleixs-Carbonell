from detector import AnomalyDetector, SensorReading


def test_detects_high_temperature_anomaly() -> None:
    # Arrange: Inicializamos el detector con un límite de 35.0 °C
    detector = AnomalyDetector(temp_threshold=35.0, humidity_threshold=80.0)
    # Arrange: Simulamos una lectura de 36.5 °C
    reading = SensorReading(sensor_id="SENSOR-01", temperature=36.5, humidity=50.0)
    
    # Act
    result = detector.evaluate(reading)
    
    # Assert
    assert result["is_anomaly"] is True
    assert result["type"] == "HIGH_TEMPERATURE"