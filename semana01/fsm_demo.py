from enum import Enum, auto

class TrafficLightState(Enum):
    RED = auto()
    YELLOW = auto()
    GREEN = auto()

class TrafficLightFSM:
    """El estado vive dentro del objeto, no en una variable global."""
    
    def __init__(self) -> None:
        # Variables privadas (Encapsulamiento)
        self._state = TrafficLightState.RED
        self._cycle_count = 0

    @property
    def state(self) -> TrafficLightState:
        """Pin de solo lectura para ver el estado actual."""
        return self._state
        
    @property
    def cycle_count(self) -> int:
        """Pin de solo lectura para ver cuántas transiciones han ocurrido."""
        return self._cycle_count

    def transition(self) -> TrafficLightState:
        """Ejecuta la transición basada en un diccionario de estados."""
        transitions = {
            TrafficLightState.RED: TrafficLightState.GREEN,
            TrafficLightState.GREEN: TrafficLightState.YELLOW,
            TrafficLightState.YELLOW: TrafficLightState.RED,
        }
        # Actualizamos el estado interno
        self._state = transitions[self._state]
        self._cycle_count += 1
        return self._state