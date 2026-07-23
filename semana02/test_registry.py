import pytest

# Intentamos importar algo que aún no existe
from registry import SensorNotFoundError, SensorRegistry


def test_get_unknown_sensor_raises() -> None:
    registry = SensorRegistry()
    with pytest.raises(SensorNotFoundError):
        registry.get("GHOST-99")