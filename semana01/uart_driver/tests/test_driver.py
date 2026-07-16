import pytest
import json
from dataclasses import FrozenInstanceError
from semana01.uart_driver.config import UartConfig
from semana01.uart_driver.parsers import ModbusParser, NMEAParser, CANParser
from semana01.uart_driver.device import UartDevice
from semana01.uart_driver.recorder import DataRecorder

# ==========================================
# TESTS PARA UartConfig (Inmutabilidad y SRP)
# ==========================================
def test_config_invalid_baudrate():
    """Falla rápido si se inyecta un baudrate no estándar."""
    with pytest.raises(ValueError, match="Baudrate inválido"):
        UartConfig(baudrate=9601, parity="N", stop_bits=1, timeout=1.0)

def test_config_invalid_parity():
    """Falla rápido si la paridad no es N, E, o O."""
    with pytest.raises(ValueError, match="La paridad debe ser"):
        UartConfig(baudrate=9600, parity="X", stop_bits=1, timeout=1.0)

def test_config_immutability():
    """Garantiza que la configuración de hardware no se altere en tiempo de ejecución."""
    config = UartConfig(baudrate=9600, parity="N", stop_bits=1, timeout=1.0)
    with pytest.raises(FrozenInstanceError):
        config.baudrate = 115200  # type: ignore

# ==========================================
# TESTS PARA Parsers (OCP, LSP)
# ==========================================
def test_parser_modbus_valid():
    """Verifica el parseo correcto de una trama Modbus RTU."""
    parser = ModbusParser()
    data = b"\x01\x03\x04\x00\x00"
    assert parser.can_parse(data) is True
    assert parser.parse(data)["protocol"] == "MODBUS"

def test_parser_nmea_invalid():
    """Asegura que el parser NMEA rechace tramas corruptas."""
    parser = NMEAParser()
    bad_data = b"$GPXXX,corrupt"
    assert parser.can_parse(bad_data) is False
    with pytest.raises(ValueError):
        parser.parse(bad_data)

def test_parser_can_extension_valid():
    """Verifica la extensión del protocolo CAN (Distinción)."""
    parser = CANParser()
    data = b"CAN:RPM:3200"
    assert parser.can_parse(data) is True
    assert parser.parse(data)["engine_rpm"] == 3200.0

# ==========================================
# TESTS PARA UartDevice (DIP y Concurrencia)
# ==========================================
@pytest.fixture
def device_setup():
    """Fixture de Pytest para preparar el dispositivo (Patrón Arrange)."""
    config = UartConfig(115200, "N", 1, 1.0)
    parsers = [ModbusParser(), NMEAParser(), CANParser()]
    return UartDevice(config, parsers)

def test_device_rx_disconnected(device_setup: UartDevice):
    """Evita lectura de buffer si el puerto está cerrado."""
    with pytest.raises(RuntimeError, match="Dispositivo desconectado"):
        device_setup.receive_raw(b"data")

def test_device_read_disconnected(device_setup: UartDevice):
    """Evita parseo si el puerto está cerrado."""
    with pytest.raises(RuntimeError, match="Dispositivo desconectado"):
        device_setup.read_and_parse()

def test_device_full_flow(device_setup: UartDevice):
    """Prueba de integración: Conexión -> RX -> Parseo."""
    device_setup.connect()
    device_setup.receive_raw(b"CAN:123")
    result = device_setup.read_and_parse()
    assert result["protocol"] == "CAN"

# ==========================================
# TESTS PARA DataRecorder (Persistencia)
# ==========================================
def test_recorder_ignores_empty(tmp_path):
    """Ignora diccionarios vacíos sin escribir en disco."""
    file = tmp_path / "test_log.jsonl"
    recorder = DataRecorder(str(file))
    recorder.record({})
    assert not file.exists()

def test_recorder_writes_valid_json(tmp_path):
    """Verifica formato JSON-lines en disco."""
    file = tmp_path / "test_log.jsonl"
    recorder = DataRecorder(str(file))
    recorder.record({"sensor": "TMP", "val": 25.5})
    
    with open(file, "r") as f:
        line = f.readline()
        data = json.loads(line)
        assert data["sensor"] == "TMP"

def test_recorder_appends_data(tmp_path):
    """Verifica que no sobrescriba datos previos (modo append)."""
    file = tmp_path / "test_log.jsonl"
    recorder = DataRecorder(str(file))
    recorder.record({"id": 1})
    recorder.record({"id": 2})
    
    with open(file, "r") as f:
        lines = f.readlines()
        assert len(lines) == 2