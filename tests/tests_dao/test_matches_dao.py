from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

import pytest

from src.dao.matches_dao import MatchDAO
from src.models.matches import Match
from src.models.players import Player


# Reset du singleton avant chaque test
@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset le singleton MatchDAO avant chaque test"""
    MatchDAO._instances = {}
    yield
    MatchDAO._instances = {}


@pytest.fixture
def mock_cursor():
    """Fixture pour créer un curseur mocké"""
    cursor = MagicMock()
    cursor.fetchone = MagicMock(return_value=None)
    cursor.fetchall = MagicMock(return_value=[])
    cursor.execute = MagicMock()
    return cursor


@pytest.fixture
def mock_connection(mock_cursor):
    """Fixture pour créer une connexion mockée"""
    connection = MagicMock()
    connection.cursor.return_value = mock_cursor
    return connection


@pytest.fixture
def match_dao(mock_connection):
    """Fixture pour créer une instance de MatchDAO avec mock"""
    with patch("src.dao.matches_dao.DBConnection") as mock_db_conn:
        # Mock l'instance retournée par DBConnection()
        mock_instance = MagicMock()
        mock_instance.connection = mock_connection
        mock_db_conn.return_value = mock_instance

        dao = MatchDAO()
        yield dao


@pytest.fixture
def sample_match():
    """Fixture pour créer un match exemple"""
    match = Mock(spec=Match)
    match.id = str(uuid4())
    match.playlist_id = "ranked-doubles"
    match.season = "Season 15"
    match.duration = 300
    match.overtime = False
    match.date_upload = "2024-02-11 14:30:00"
    return match


@pytest.fixture
def sample_player():
    """Fixture pour créer un joueur exemple"""
    player = Mock(spec=Player)
    player.id = str(uuid4())
    player.platform_id = "platform_123"
    player.platform_user_id = "user_456"
    player.name = "TestPlayer"
    return player


class TestMatchDAORetrieval:
    """Tests pour la récupération de matchs"""

    def test_get_match_by_parameter_found_single(
        self, match_dao, sample_match, mock_cursor
    ):
        """Test la récupération d'un match par paramètre (un seul résultat)"""
        mock_cursor.fetchall.return_value = [
            {
                "id": sample_match.id,
                "playlist_id": sample_match.playlist_id,
                "season": sample_match.season,
                "duration": sample_match.duration,
                "overtime": sample_match.overtime,
                "date_upload": sample_match.date_upload,
            }
        ]

        result = match_dao.get_match_by_parameter("id", sample_match.id)

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Match)

        # Vérifie la requête SQL
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "WHERE id= ?" in call_args[0]
        assert call_args[1] == (sample_match.id,)

    def test_get_match_by_parameter_found_multiple(self, match_dao, mock_cursor):
        """Test la récupération de plusieurs matchs par paramètre"""
        # Simule plusieurs matchs de la même saison
        mock_cursor.fetchall.return_value = [
            {
                "id": "match1",
                "playlist_id": "ranked-doubles",
                "season": "Season 15",
                "duration": 300,
                "overtime": False,
                "date_upload": "2024-02-11 14:00:00",
            },
            {
                "id": "match2",
                "playlist_id": "ranked-standard",
                "season": "Season 15",
                "duration": 350,
                "overtime": True,
                "date_upload": "2024-02-11 15:00:00",
            },
        ]

        result = match_dao.get_match_by_parameter("season", "Season 15")

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 2
        for match in result:
            assert isinstance(match, Match)

    def test_get_match_by_parameter_not_found(self, match_dao, mock_cursor):
        """Test la récupération d'un match inexistant"""
        mock_cursor.fetchall.return_value = []

        result = match_dao.get_match_by_parameter("id", "nonexistent")

        assert result is None

    def test_get_match_by_parameter_invalid_column(self, match_dao):
        """Test avec un nom de colonne invalide"""
        with pytest.raises(ValueError, match="Invalid column name"):
            match_dao.get_match_by_parameter("invalid_column", "value")

    def test_get_match_by_parameter_all_allowed_columns(self, match_dao, mock_cursor):
        """Test avec toutes les colonnes autorisées"""
        allowed_columns = [
            "id",
            "playlist_id",
            "season",
            "date_upload",
            "overtime",
            "duration",
        ]

        for column in allowed_columns:
            # Reset et reconfigure le mock pour chaque itération
            mock_cursor.reset_mock()
            mock_cursor.fetchall.return_value = [
                {
                    "id": "test_id",
                    "playlist_id": "test_playlist",
                    "season": "test_season",
                    "duration": 300,
                    "overtime": False,
                    "date_upload": "2024-02-11 14:00:00",
                }
            ]

            result = match_dao.get_match_by_parameter(column, "test_value")

            assert result is not None
            assert isinstance(result, list)
            assert len(result) == 1
            call_args = mock_cursor.execute.call_args[0]
            assert f"WHERE {column}= ?" in call_args[0]

    def test_get_match_by_parameter_overtime_filter(self, match_dao, mock_cursor):
        """Test la récupération des matchs en overtime"""
        mock_cursor.fetchall.return_value = [
            {
                "id": "ot_match1",
                "playlist_id": "ranked-doubles",
                "season": "Season 15",
                "duration": 400,
                "overtime": True,
                "date_upload": "2024-02-11 14:00:00",
            }
        ]

        result = match_dao.get_match_by_parameter("overtime", True)

        assert result is not None
        assert len(result) == 1
        call_args = mock_cursor.execute.call_args[0]
        assert call_args[1] == (True,)


class TestMatchDAOSingleton:
    """Tests pour vérifier le pattern Singleton"""

    def test_singleton_pattern(self):
        """Test que MatchDAO est bien un singleton"""
        with patch("src.dao.matches_dao.DBConnection"):
            instance1 = MatchDAO()
            instance2 = MatchDAO()

            assert instance1 is instance2


class TestMatchDAOEdgeCases:
    """Tests pour les cas limites"""

    def test_get_match_by_parameter_empty_result(self, match_dao, mock_cursor):
        """Test avec un résultat vide"""
        mock_cursor.fetchall.return_value = []

        result = match_dao.get_match_by_parameter("season", "NonExistent Season")

        assert result is None

    def test_get_match_by_parameter_by_playlist(self, match_dao, mock_cursor):
        """Test la récupération de tous les matchs d'une playlist"""
        matches_data = [
            {
                "id": f"match_{i}",
                "playlist_id": "ranked-doubles",
                "season": "Season 15",
                "duration": 300,
                "overtime": False,
                "date_upload": f"2024-02-11 14:{i:02d}:00",
            }
            for i in range(10)
        ]
        mock_cursor.fetchall.return_value = matches_data

        result = match_dao.get_match_by_parameter("playlist_id", "ranked-doubles")

        assert result is not None
        assert len(result) == 10
        assert all(isinstance(m, Match) for m in result)
