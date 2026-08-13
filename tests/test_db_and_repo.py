"""
Pruebas unitarias para persistencia y configuración de base de datos.
Patrón: Arrange-Act-Assert (AAA) con mocks de SQLAlchemy.
"""
import os
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from app.db import get_database_url, get_db
from app.models import ReadingModel
from app.repositories.sql import SQLSensorHubRepository

# ==========================================
# TESTS PARA app/db.py
# ==========================================

def test_get_database_url_replaces_postgres_scheme() -> None:
    # Arrange: Simulamos que Render inyecta la URL antigua
    with patch.dict(os.environ, {"DATABASE_URL": "postgres://user:pass@host/db"}):
        # Act
        url = get_database_url()
        # Assert: Verificamos que añade +psycopg
        assert url == "postgresql+psycopg://user:pass@host/db"

def test_get_database_url_replaces_postgresql_scheme() -> None:
    # Arrange: Simulamos otra variante de URL
    with patch.dict(os.environ, {"DATABASE_URL": "postgresql://user:pass@host/db"}):
        # Act
        url = get_database_url()
        # Assert
        assert url == "postgresql+psycopg://user:pass@host/db"

def test_get_db_yields_session_and_closes() -> None:
    # Arrange: Mockeamos el creador de sesiones
    with patch("app.db.SessionLocal") as mock_session_local:
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        
        # Act: Iniciamos el generador
        gen = get_db()
        db = next(gen)
        
        # Assert: Verifica que retorna la sesión correcta
        assert db == mock_session
        
        # Act: Forzamos el cierre del generador (simulando fin de petición en FastAPI)
        with pytest.raises(StopIteration):
            next(gen)
        
        # Assert: Garantizamos que no hay fugas de memoria
        mock_session.close.assert_called_once()

# ==========================================
# TESTS PARA app/repositories/sql.py
# ==========================================

def test_delete_sensor_not_found() -> None:
    # Arrange: Simulamos que la BD devuelve None
    mock_session = MagicMock()
    mock_session.get.return_value = None
    repo = SQLSensorHubRepository(session=mock_session)
    
    # Act
    result = repo.delete_sensor("fake_id")
    
    # Assert
    assert result is False
    mock_session.delete.assert_not_called()

def test_update_reading_not_found() -> None:
    # Arrange
    mock_session = MagicMock()
    mock_session.get.return_value = None
    repo = SQLSensorHubRepository(session=mock_session)
    
    # Act
    result = repo.update_reading(reading_id=999, data={"value": 10.0})
    
    # Assert
    assert result is None
    mock_session.commit.assert_not_called()

def test_delete_reading_success() -> None:
    # Arrange: Simulamos que sí encontró el registro
    mock_session = MagicMock()
    mock_reading = ReadingModel(id=1, sensor_id="S1", value=20.0, unit="C")
    mock_session.get.return_value = mock_reading
    repo = SQLSensorHubRepository(session=mock_session)
    
    # Act
    result = repo.delete_reading(reading_id=1)
    
    # Assert
    assert result is True
    mock_session.delete.assert_called_once_with(mock_reading)
    mock_session.commit.assert_called_once()

def test_delete_reading_not_found() -> None:
    # Arrange
    mock_session = MagicMock()
    mock_session.get.return_value = None
    repo = SQLSensorHubRepository(session=mock_session)
    
    # Act
    result = repo.delete_reading(reading_id=999)
    
    # Assert
    assert result is False
    mock_session.delete.assert_not_called()

def test_list_readings_with_date_filters() -> None:
    # Arrange: Aislamos la capa de consultas (scalars)
    mock_session = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = []
    mock_session.scalars.return_value = mock_scalars
    
    repo = SQLSensorHubRepository(session=mock_session)
    d1 = datetime(2026, 8, 1)
    d2 = datetime(2026, 8, 2)
    
    # Act: Disparamos todos los 'if' de fecha
    result = repo.list_readings("sensor_1", from_date=d1, to_date=d2)
    
    # Assert
    assert result == []
    mock_session.scalars.assert_called_once()