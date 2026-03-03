from unittest.mock import MagicMock, patch

import pytest

from src.dao.platforms_dao import PlatformDAO
from src.models.platforms import Platform


# ──────────────────────────────────────────────
# Reset Singleton
# ──────────────────────────────────────────────


@pytest.fixture(autouse=True)
def reset_singleton():
    PlatformDAO._instances = {}
    yield
    PlatformDAO._instances = {}


# ──────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────


@pytest.fixture
def mock_cursor():
    return MagicMock()


@pytest.fixture
def mock_connection(mock_cursor):
    connection = MagicMock()
    connection.cursor.return_value = mock_cursor
    connection.__enter__ = MagicMock(return_value=connection)
    connection.__exit__ = MagicMock(return_value=None)
    return connection


@pytest.fixture
def platform_dao(mock_connection):
    with patch("src.dao.platforms_dao.DBConnection") as mock_db_conn:
        mock_db_instance = MagicMock()
        mock_db_instance.connection = mock_connection
        mock_db_conn.return_value = mock_db_instance
        dao = PlatformDAO()
        yield dao


@pytest.fixture
def platform_row():
    return {
        "id": 1,
        "namebigint": "Steam",
    }


# ──────────────────────────────────────────────
# get_platform_by_id
# ──────────────────────────────────────────────


class TestGetPlatformById:
    def test_retourne_platform_quand_trouve(
        self, platform_dao, mock_cursor, platform_row
    ):
        mock_cursor.fetchone.return_value = platform_row

        result = platform_dao.get_platform_by_id(1)

        assert result is not None
        assert isinstance(result, Platform)

    def test_retourne_none_si_non_trouve(self, platform_dao, mock_cursor):
        mock_cursor.fetchone.return_value = None

        result = platform_dao.get_platform_by_id(99)

        assert result is None

    def test_requete_contient_bon_id(self, platform_dao, mock_cursor, platform_row):
        mock_cursor.fetchone.return_value = platform_row

        platform_dao.get_platform_by_id(1)

        mock_cursor.execute.assert_called_once()
        params = mock_cursor.execute.call_args[0][1]
        assert params == (1,)

    def test_requete_cible_table_platforms(
        self, platform_dao, mock_cursor, platform_row
    ):
        mock_cursor.fetchone.return_value = platform_row

        platform_dao.get_platform_by_id(1)

        query = mock_cursor.execute.call_args[0][0]
        assert "platforms" in query
        assert "WHERE id = ?" in query


# ──────────────────────────────────────────────
# Singleton
# ──────────────────────────────────────────────


class TestPlatformDAOSingleton:
    def test_singleton_pattern(self):
        with patch("src.dao.platforms_dao.DBConnection"):
            instance1 = PlatformDAO()
            instance2 = PlatformDAO()
            assert instance1 is instance2
