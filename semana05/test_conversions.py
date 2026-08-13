
from conversions import celsius_to_fahrenheit


def test_celsius_to_fahrenheit_known_values() -> None:
    assert celsius_to_fahrenheit(0) == 32.0
    assert celsius_to_fahrenheit(100) == 212.0
