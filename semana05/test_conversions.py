import pytest

from semana05.conversions import celsius_to_fahrenheit


def test_celsius_to_fahrenheit_known_values() -> None:
    assert celsius_to_fahrenheit(0) == 32.0
    assert celsius_to_fahrenheit(100) == 212.0


def test_celsius_to_fahrenheit_absolute_zero() -> None:
    with pytest.raises(ValueError, match="cero absoluto"):
        celsius_to_fahrenheit(-274.0)
