from abc import ABC, abstractmethod

class MessageParser(ABC):
    """(ISP & OCP) Interfaz segregada para parseo de protocolos."""
    @abstractmethod
    def can_parse(self, raw_data: bytes) -> bool: ...
    
    @abstractmethod
    def parse(self, raw_data: bytes) -> dict[str, str | float]: ...

class ModbusParser(MessageParser):
    """Parsea tramas Modbus RTU simuladas."""
    def can_parse(self, raw_data: bytes) -> bool:
        return raw_data.startswith(b"\x01\x03") # Simula ID 1, Función 3 (Read)

    def parse(self, raw_data: bytes) -> dict[str, str | float]:
        if not self.can_parse(raw_data):
            raise ValueError("No es un frame Modbus válido")
        # Simulación de extracción de datos
        return {"protocol": "MODBUS", "register_value": 25.5}

class NMEAParser(MessageParser):
    """Parsea sentencias GPS NMEA."""
    def can_parse(self, raw_data: bytes) -> bool:
        return raw_data.startswith(b"$GPGGA")

    def parse(self, raw_data: bytes) -> dict[str, str | float]:
        if not self.can_parse(raw_data):
            raise ValueError("No es una sentencia NMEA válida")
        return {"protocol": "NMEA", "latitude": 19.543, "longitude": -96.921}

# --- EXTENSIÓN PARA CALIFICACIÓN EXCEPCIONAL ---
class CANParser(MessageParser):
    """Parsea tramas simplificadas del bus CAN automotriz."""
    def can_parse(self, raw_data: bytes) -> bool:
        return raw_data.startswith(b"CAN:")

    def parse(self, raw_data: bytes) -> dict[str, str | float]:
        if not self.can_parse(raw_data):
            raise ValueError("No es un frame CAN válido")
        return {"protocol": "CAN", "engine_rpm": 3200.0}