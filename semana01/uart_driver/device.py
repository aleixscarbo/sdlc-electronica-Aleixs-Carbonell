import threading
from collections import deque
from typing import List, Dict, Union
from .config import UartConfig
from .parsers import MessageParser

class UartDevice:
    """
    (DIP) Depende de abstracciones (MessageParser), no de implementaciones concretas.
    """
    def __init__(self, config: UartConfig, parsers: List[MessageParser]) -> None:
        self.config = config
        self.parsers = parsers
        self._connected = False
        
        # EXTENSIÓN: Buffer circular thread-safe usando deque y Lock
        self._buffer: deque[bytes] = deque(maxlen=1024)
        self._lock = threading.Lock()

    def connect(self) -> None:
        """Simula la apertura segura del puerto de hardware."""
        self._connected = True
        
    def disconnect(self) -> None:
        """Cierra el puerto de hardware."""
        self._connected = False

    def receive_raw(self, data: bytes) -> None:
        """Simula la interrupción de hardware (RX). Segura para concurrencia."""
        if not self._connected:
            raise RuntimeError("Dispositivo desconectado: no se puede recibir datos.")
        
        # Adquirimos el candado antes de tocar la memoria compartida
        with self._lock:
            self._buffer.append(data)

    def read_and_parse(self) -> Dict[str, Union[str, float]]:
        """Extrae el mensaje del buffer y lo delega al parser adecuado."""
        if not self._connected:
            raise RuntimeError("Dispositivo desconectado: no se puede leer.")
        
        # Extracción segura del buffer
        with self._lock:
            if not self._buffer:
                return {}
            raw_data = self._buffer.popleft()

        # (OCP/LSP) Iteramos sobre las abstracciones, sin importar cuántos protocolos existan
        for parser in self.parsers:
            if parser.can_parse(raw_data):
                return parser.parse(raw_data)
        
        raise ValueError(f"Trama desconocida o corrupta: {raw_data!r}")