from semana01.solid_isp_dip import (
    SimpleTempSensor, SmartThermostat, 
    DataProcessor, InMemoryRepository, SensorReading
)

# --- PRUEBAS ISP ---
def test_isp_simple_sensor():
    # Arrange
    sensor = SimpleTempSensor()
    # Act
    val = sensor.read()
    # Assert: El sensor funciona sin verse obligado a implementar calibrate()
    assert val == 22.5

def test_isp_smart_thermostat():
    # Arrange
    thermostat = SmartThermostat()
    # Act
    thermostat.write(30.0)
    thermostat.calibrate()
    # Assert: Implementa limpiamente interfaces múltiples
    assert thermostat.read() == 0.0

# --- PRUEBAS DIP ---
def test_dip_processor_with_in_memory_repo():
    # Arrange
    # ¡Inyectamos la dependencia falsa! El procesador no sabe que es en memoria RAM.
    test_repo = InMemoryRepository()
    processor = DataProcessor(test_repo)
    reading = SensorReading("SNS-100", 45.5)
    
    # Act
    processor.process_and_save(reading)
    retrieved = processor.retrieve_last("SNS-100")
    
    # Assert
    assert retrieved is not None
    assert retrieved.value == 45.5
    assert retrieved.sensor_id == "SNS-100"