from dataclasses import dataclass

@dataclass(frozen=True)
class UartConfig:
    baudrate: int
    parity: str
    stop_bits: int
    timeout: float

    def __post_init__(self) -> None:
        """Validación estricta post-creación (Falla rápido si hay error)."""
        valid_baudrates = {9600, 19200, 38400, 115200}
        if self.baudrate not in valid_baudrates:
            raise ValueError(f"Baudrate inválido: {self.baudrate}")
        if self.parity not in {"N", "E", "O"}:
            raise ValueError("La paridad debe ser 'N', 'E' u 'O'")
        if self.stop_bits not in {1, 2}:
            raise ValueError("Stop bits deben ser 1 o 2")