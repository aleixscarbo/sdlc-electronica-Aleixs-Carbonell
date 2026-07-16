import json
import logging
from typing import Dict, Union

# EXTENSIÓN: Configuración de Logging estructurado en consola
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)

class DataRecorder:
    """(SRP) Única responsabilidad: Persistir datos de telemetría parseados."""
    
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def record(self, data: Dict[str, Union[str, float]]) -> None:
        """Guarda los datos en formato JSON-lines (una línea por registro)."""
        if not data:
            return
        
        # Serializamos el diccionario a un string JSON
        json_line = json.dumps(data)
        
        # Escribimos en el archivo en modo "append" (añadir al final)
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(json_line + "\n")
        
        # Log estructurado para auditoría en tiempo real
        logging.info(f"Telemetría persistida: {json_line}")