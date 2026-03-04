from unittest.mock import MagicMock, Mock, PropertyMock, patch
from uuid import uuid4

import pytest

from src.dao.match_teams_dao import MatchTeamDAO

# Ajustez ces imports selon votre structure de projet
from src.models.match_teams import MatchTeam
from src.models.players import Player


# Reset du singleton avant chaque test
@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset le singleton MatchTeamDAO avant chaque test"""
    MatchTeamDAO._instances = {}
    yield
    MatchTeamDAO._instances = {}


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
    connection.__enter__ = MagicMock(return_value=connection)
    connection.__exit__ = MagicMock(return_value=None)
    return connection


@pytest.fixture
def match_team_dao(mock_connection):
    """Fixture pour créer une instance de MatchTeamDAO avec mock"""
    with patch("src.dao.match_teams_dao.DBConnection") as mock_db_conn:
        # Mock de la classe DBConnection elle-même
        type(mock_db_conn).connection = PropertyMock(return_value=mock_connection)

        dao = MatchTeamDAO()
        yield dao


@pytest.fixture
def sample_match_team():
    """Fixture pour créer une équipe de match exemple"""
    match_team = Mock(spec=MatchTeam)
    match_team.id = str(uuid4())
    match_team.match_id = str(uuid4())
    match_team.color = "blue"
    match_team.score = 3
    match_team.possession_time = 145.5
    match_team.time_in_side = 150.0
    return match_team


@pytest.fixture
def sample_player():
    """Fixture pour créer un joueur exemple"""
    player = Mock(spec=Player)
    player.id = str(uuid4())
    player.platform_id = "platform_123"
    player.platform_user_id = "user_456"
    player.name = "TestPlayer"
    return player


class TestMatchTeamDAORetrieval:
    """Tests pour la récupération d'équipes de match"""

    def test_get_match_teams_by_parameter_invalid_column(self, match_team_dao):
        """Test avec un nom de colonne invalide"""
        with pytest.raises(ValueError, match="Invalid column name"):
            match_team_dao.get_match_teams_by_parameter("invalid_column", "value")


class TestMatchTeamDAOSingleton:
    """Tests pour vérifier le pattern Singleton"""

    def test_singleton_pattern(self):
        """Test que MatchTeamDAO est bien un singleton"""
        with patch("src.dao.match_teams_dao.DBConnection"):
            instance1 = MatchTeamDAO()
            instance2 = MatchTeamDAO()

            assert instance1 is instance2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
