import json
import logging
import os
import sys


class JSONFormatter(logging.Formatter):
    """Formateador personalizado que genera logs en formato JSON estructurado."""

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def setup_logger(name: str = "sensorhub") -> logging.Logger:
    """Configura el logger estructurado basado en la variable de entorno."""
    _logger = logging.getLogger(name)

    # RNF-5: Configuración exclusiva por variable de entorno (por defecto INFO)
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    _logger.setLevel(log_level)

    # Evitar duplicar handlers en recargas (reloader de uvicorn)
    if not _logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        _logger.addHandler(handler)

    return _logger


# Instancia global lista para ser importada en toda la app
logger = setup_logger()
