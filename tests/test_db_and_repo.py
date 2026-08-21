"""
Pruebas unitarias para persistencia y configuración de base de datos.
Patrón: Arrange-Act-Assert (AAA) con mocks de SQLAlchemy.
"""

import os
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.db import get_database_url
from app.models import ReadingModel, SensorModel
from app.repositories.sql import SQLSensorHubRepository

# ==========================================
# TESTS PARA app/db.py
# ==========================================


def test_get_database_url_replaces_postgres_scheme() -> None:
    """Simula el comportamiento en Render donde postgres:// debe cambiar a postgresql+psycopg://"""
    with patch.dict(os.environ, {"DATABASE_URL": "postgres://user:pass@host/db"}):
        url = get_database_url()
        assert url == "postgresql+psycopg://user:pass@host/db"


def test_get_database_url_replaces_postgresql_scheme() -> None:
    with patch.dict(os.environ, {"DATABASE_URL": "postgresql://user:pass@host/db"}):
        url = get_database_url()
        assert url == "postgresql+psycopg://user:pass@host/db"


# ==========================================
# TESTS PARA REPOSITORIO: SENSORES
# ==========================================


def test_add_sensor_success() -> None:
    mock_session = MagicMock()
    repo = SQLSensorHubRepository(session=mock_session)

    result = repo.add_sensor(
        sensor_id="S1", type="temp", name="Prueba", location="Bodega 1", threshold=30.0
    )

    assert result.id == "S1"
    assert result.location == "Bodega 1"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


def test_add_sensor_rollback_on_error() -> None:
    mock_session = MagicMock()
    mock_session.commit.side_effect = SQLAlchemyError("Error DB")
    repo = SQLSensorHubRepository(session=mock_session)

    with pytest.raises(SQLAlchemyError):
        repo.add_sensor("S1", "temp", "Prueba", "Bodega 1")
    mock_session.rollback.assert_called_once()


def test_get_sensor() -> None:
    mock_session = MagicMock()
    # Inyectamos location e is_active al mock
    mock_sensor = SensorModel(
        id="S1", type="temp", name="Prueba", location="Bodega 1", is_active=True
    )
    mock_session.get.return_value = mock_sensor
    repo = SQLSensorHubRepository(session=mock_session)

    result = repo.get_sensor("S1")
    assert result is mock_sensor
    mock_session.get.assert_called_once_with(SensorModel, "S1")


def test_list_sensors_filters_active() -> None:
    mock_session = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = [
        SensorModel(id="S1", location="Bodega 1", is_active=True)
    ]
    mock_session.scalars.return_value = mock_scalars
    repo = SQLSensorHubRepository(session=mock_session)

    result = repo.list_sensors()
    assert len(result) == 1
    assert result[0].id == "S1"


# --- SOFT DELETE TESTS ---
def test_delete_sensor_success() -> None:
    """Verifica que el repositorio hace un Soft Delete en lugar de un DELETE físico"""
    mock_session = MagicMock()
    mock_sensor = SensorModel(
        id="S1", type="temp", name="Sensor", location="Bodega 1", is_active=True
    )
    mock_session.get.return_value = mock_sensor
    repo = SQLSensorHubRepository(session=mock_session)

    result = repo.delete_sensor("S1")

    assert result is True
    assert mock_sensor.is_active is False  # ASERCIÓN CLAVE: comprobamos el soft delete
    mock_session.delete.assert_not_called()  # NUNCA debe borrarse físicamente
    mock_session.commit.assert_called_once()


def test_delete_sensor_already_inactive_or_not_found() -> None:
    mock_session = MagicMock()
    mock_sensor = SensorModel(id="S1", location="Bodega 1", is_active=False)
    mock_session.get.return_value = mock_sensor
    repo = SQLSensorHubRepository(session=mock_session)

    result = repo.delete_sensor("S1")

    assert result is False  # Porque ya estaba inactivo o no existía
    mock_session.commit.assert_not_called()


def test_delete_sensor_rollback_on_error() -> None:
    mock_session = MagicMock()
    mock_sensor = SensorModel(id="S1", location="Bodega 1", is_active=True)
    mock_session.get.return_value = mock_sensor
    mock_session.commit.side_effect = SQLAlchemyError("Error DB")
    repo = SQLSensorHubRepository(session=mock_session)

    with pytest.raises(SQLAlchemyError):
        repo.delete_sensor("S1")
    mock_session.rollback.assert_called_once()


# ==========================================
# TESTS PARA REPOSITORIO: LECTURAS
# ==========================================


def test_add_reading_success() -> None:
    mock_session = MagicMock()
    repo = SQLSensorHubRepository(session=mock_session)

    result = repo.add_reading(sensor_id="S1", value=25.5, unit="C")

    assert result.sensor_id == "S1"
    assert result.value == 25.5
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_delete_reading_success() -> None:
    mock_session = MagicMock()
    mock_reading = ReadingModel(id=1, sensor_id="S1", value=20.0, unit="C")
    mock_session.get.return_value = mock_reading
    repo = SQLSensorHubRepository(session=mock_session)

    result = repo.delete_reading(reading_id=1)

    assert result is True
    mock_session.delete.assert_called_once_with(mock_reading)
    mock_session.commit.assert_called_once()


def test_delete_reading_not_found() -> None:
    mock_session = MagicMock()
    mock_session.get.return_value = None
    repo = SQLSensorHubRepository(session=mock_session)

    result = repo.delete_reading(reading_id=999)

    assert result is False
    mock_session.delete.assert_not_called()


def test_update_reading_success() -> None:
    mock_session = MagicMock()
    mock_reading = ReadingModel(id=1, sensor_id="S1", value=20.0, unit="C")
    mock_session.get.return_value = mock_reading
    repo = SQLSensorHubRepository(session=mock_session)

    result = repo.update_reading(1, {"value": 30.0})

    assert result is not None
    assert result.value == 30.0
    mock_session.commit.assert_called_once()


def test_list_readings_with_date_filters() -> None:
    mock_session = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = []
    mock_session.scalars.return_value = mock_scalars

    repo = SQLSensorHubRepository(session=mock_session)
    result = repo.list_readings("S1", from_date=datetime.now(), to_date=datetime.now())

    assert isinstance(result, list)


# ==========================================
# TESTS PARA REPOSITORIO: ALERTAS
# ==========================================


def test_add_alert_success() -> None:
    mock_session = MagicMock()
    repo = SQLSensorHubRepository(session=mock_session)

    result = repo.add_alert(sensor_id="S1", value=40.0, threshold=30.0)

    assert result.sensor_id == "S1"
    assert result.value == 40.0
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
