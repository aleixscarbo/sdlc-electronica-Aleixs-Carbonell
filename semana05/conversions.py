def celsius_to_fahrenheit(c: float) -> float:
    """Convert a temperature in degrees Celsius to degrees Fahrenheit.

    Args:
        c: Temperature in Celsius.

    Returns:
        The equivalent temperature in Fahrenheit rounded to 2 decimal places.

    Example:
        >>> celsius_to_fahrenheit(0)
        32.0
    """
    if c < -273.15:
        raise ValueError("Temperatura por debajo del cero absoluto (-273.15 C)")
    return round((c * 9 / 5) + 32, 2)
