from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

import pytest

from src.dao.players_dao import PlayerDAO
from src.models.matches import Match

# Ajustez ces imports selon votre structure de projet
from src.models.players import Player


# Reset du singleton avant chaque test
@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset le singleton PlayerDAO avant chaque test"""
    PlayerDAO._instances = {}
    yield
    PlayerDAO._instances = {}


@pytest.fixture
def mock_cursor():
    """Fixture pour créer un curseur mocké"""
    cursor = MagicMock()
    return cursor


@pytest.fixture
def mock_connection(mock_cursor):
    """Fixture pour créer une connexion mockée"""
    connection = MagicMock()
    connection.cursor.return_value = mock_cursor
    connection.__enter__ = MagicMock(return_value=connection)
    connection.__exit__ = MagicMock(return_value=None)
    return connection


@pytest.fixture
def player_dao(mock_connection):
    """Fixture pour créer une instance de PlayerDAO avec mock"""
    with patch("src.dao.players_dao.DBConnection") as mock_db_conn:
        mock_db_instance = MagicMock()
        mock_db_instance.connection = mock_connection
        mock_db_conn.return_value = mock_db_instance

        dao = PlayerDAO()
        yield dao


@pytest.fixture
def sample_player():
    """Fixture pour créer un joueur exemple"""
    player = Mock(spec=Player)
    player.id = str(uuid4())
    player.platform_id = "platform_123"
    player.platform_user_id = "user_456"
    player.name = "TestPlayer"
    return player


class TestPlayerDAORetrieval:
    """Tests pour la récupération de joueurs"""

    def test_get_player_by_parameter_found(
        self, player_dao, sample_player, mock_cursor
    ):
        """Test la récupération d'un joueur par paramètre"""
        # Simule un résultat de base de données
        mock_cursor.fetchone.return_value = {
            "id": sample_player.id,
            "platform_id": sample_player.platform_id,
            "platform_user_id": sample_player.platform_user_id,
            "name": sample_player.name,
        }

        result = player_dao.get_player_by_parameter("name", "TestPlayer")

        assert result is not None
        assert isinstance(result, Player)
        assert result.name == sample_player.name
        assert result.id == sample_player.id

        # Vérifie la requête SQL
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "WHERE name= ?" in call_args[0]
        assert call_args[1] == ("TestPlayer",)

    def test_get_player_by_parameter_not_found(self, player_dao, mock_cursor):
        """Test la récupération d'un joueur inexistant"""
        mock_cursor.fetchone.return_value = None

        result = player_dao.get_player_by_parameter("name", "NonExistent")

        assert result is None

    def test_get_player_by_parameter_invalid_column(self, player_dao):
        """Test avec un nom de colonne invalide"""
        with pytest.raises(ValueError, match="Invalid column name"):
            player_dao.get_player_by_parameter("invalid_column", "value")

    def test_get_player_by_parameter_all_allowed_columns(self, player_dao, mock_cursor):
        """Test avec toutes les colonnes autorisées"""
        # Mock pour retourner un résultat valide
        mock_cursor.fetchone.return_value = {
            "id": "test_id",
            "platform_id": "test_platform",
            "platform_user_id": "test_user",
            "name": "test_name",
        }

        allowed_columns = ["id", "name", "platform_id", "platform_user_id"]

        for column in allowed_columns:
            mock_cursor.reset_mock()  # Reset les appels précédents
            player_dao.get_player_by_parameter(column, "test_value")
            call_args = mock_cursor.execute.call_args[0]
            assert f"WHERE {column}= ?" in call_args[0]

    def test_get_players_in_match_not_found(self, player_dao, mock_cursor):
        """Test sans joueurs dans le match"""
        mock_cursor.fetchall.return_value = None

        match = Mock(spec=Match)
        match.id = "match_123"

        results = player_dao.get_players_in_match(match)

        assert results is None

    def test_get_players_in_match_empty_list(self, player_dao, mock_cursor):
        """Test avec liste vide de joueurs"""
        mock_cursor.fetchall.return_value = []

        match = Mock(spec=Match)
        match.id = "match_123"

        results = player_dao.get_players_in_match(match)

        assert results is None


class TestPlayerDAOSingleton:
    """Tests pour vérifier le pattern Singleton"""

    def test_singleton_pattern(self):
        """Test que PlayerDAO est bien un singleton"""
        with patch("src.dao.players_dao.DBConnection"):
            instance1 = PlayerDAO()
            instance2 = PlayerDAO()

            assert instance1 is instance2
