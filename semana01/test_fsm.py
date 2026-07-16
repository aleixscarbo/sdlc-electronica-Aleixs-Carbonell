from semana01.fsm_demo import TrafficLightFSM, TrafficLightState

def test_initial_state():
    # Arrange: Preparamos la FSM
    fsm = TrafficLightFSM()
    
    # Act: Consultamos el estado inicial (no hay transición aún)
    current_state = fsm.state
    
    # Assert: Comprobamos que arranque en ROJO
    assert current_state == TrafficLightState.RED

def test_transition_red_to_green():
    # Arrange
    fsm = TrafficLightFSM()
    
    # Act: Forzamos un pulso de reloj / una transición
    new_state = fsm.transition()
    
    # Assert: Validamos que pasó de ROJO a VERDE
    assert new_state == TrafficLightState.GREEN
    assert fsm.state == TrafficLightState.GREEN

def test_full_cycle_returns_to_red():
    # Arrange
    fsm = TrafficLightFSM()
    
    # Act: Ejecutamos 3 transiciones (Rojo -> Verde -> Amarillo -> Rojo)
    fsm.transition() 
    fsm.transition() 
    fsm.transition() 
    
    # Assert: Comprobamos que el ciclo se cerró correctamente
    assert fsm.state == TrafficLightState.RED

def test_cycle_count():
    # Arrange
    fsm = TrafficLightFSM()
    
    # Act: Ejecutamos 3 transiciones
    fsm.transition()
    fsm.transition()
    fsm.transition()
    
    # Assert: Comprobamos que el contador interno registró las 3 transiciones
    assert fsm.cycle_count == 3