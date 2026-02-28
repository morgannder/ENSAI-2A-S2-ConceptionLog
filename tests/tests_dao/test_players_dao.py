from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

import pytest

from src.dao.players_dao import PlayerDAO
from src.models.match_teams import MatchTeam
from src.models.matches import Match

# Ajustez ces imports selon votre structure de projet
from src.models.players import Player
from src.models.ranks import Ranks


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


class TestPlayerDAOCreation:
    """Tests pour la création de joueurs"""

    def test_create_player_success(self, player_dao, sample_player, mock_cursor):
        """Test la création réussie d'un joueur"""
        # Simule qu'aucun joueur n'existe avec ce nom
        mock_cursor.fetchone.return_value = None

        result = player_dao.create_player(sample_player)

        assert result is True
        assert mock_cursor.execute.call_count == 2

        # Vérifie la requête SELECT
        first_call = mock_cursor.execute.call_args_list[0]
        assert "SELECT 1" in first_call[0][0]
        assert first_call[0][1] == (sample_player.name,)

        # Vérifie la requête INSERT
        second_call = mock_cursor.execute.call_args_list[1]
        assert "INSERT INTO players" in second_call[0][0]
        assert second_call[0][1] == (
            sample_player.id,
            sample_player.platform_id,
            sample_player.platform_user_id,
            sample_player.name,
        )

    def test_create_player_already_exists(self, player_dao, sample_player, mock_cursor):
        """Test la création d'un joueur qui existe déjà"""
        # Simule qu'un joueur existe déjà avec ce nom
        mock_cursor.fetchone.return_value = (1,)

        result = player_dao.create_player(sample_player)

        assert result is False
        # Vérifie qu'INSERT n'a pas été appelé (seulement SELECT)
        assert mock_cursor.execute.call_count == 1


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


class TestFindPlayersByPartialName:
    """Tests pour la recherche de joueurs par nom partiel"""

    def test_find_players_by_partial_name_found(self, player_dao, mock_cursor):
        """Test la recherche avec des résultats"""
        # Mock les résultats comme des dictionnaires
        mock_cursor.fetchall.return_value = [
            {"name": "TestPlayer1", "platform_name": "PC", "platform_user_id": "user1"},
            {
                "name": "TestPlayer2",
                "platform_name": "PS5",
                "platform_user_id": "user2",
            },
        ]

        results = player_dao.find_players_by_partial_name("Test")

        assert len(results) == 2
        assert results[0] == ("TestPlayer1", "PC", "user1")
        assert results[1] == ("TestPlayer2", "PS5", "user2")

        # Vérifie la requête SQL
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "WHERE p.name LIKE ?" in call_args[0]
        assert call_args[1] == ("%Test%",)

    def test_find_players_by_partial_name_not_found(self, player_dao, mock_cursor):
        """Test la recherche sans résultats"""
        mock_cursor.fetchall.return_value = []

        results = player_dao.find_players_by_partial_name("NonExistent")

        assert results == []


class TestPlayerDAODeletion:
    """Tests pour la suppression de joueurs"""

    def test_delete_player(self, player_dao, sample_player, mock_cursor):
        """Test la suppression d'un joueur"""
        player_dao.delete_player(sample_player)

        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "DELETE FROM players" in call_args[0]
        assert "WHERE name = ?" in call_args[0]
        assert call_args[1] == (sample_player.name,)


class TestGetMatchesCount:
    """Tests pour le comptage de matchs"""

    def test_get_matches_count_with_matches(
        self, player_dao, sample_player, mock_cursor
    ):
        """Test le comptage avec des matchs"""
        # Mock le résultat comme un tuple
        mock_cursor.fetchone.return_value = (5,)

        count = player_dao.get_matches_count(sample_player)

        # Le code retourne directement fetchone() qui est (5,)
        assert count == (5,)
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "COUNT(DISTINCT mp.id)" in call_args[0]
        assert call_args[1] == (sample_player.id,)

    def test_get_matches_count_no_matches(self, player_dao, sample_player, mock_cursor):
        """Test le comptage sans matchs"""
        mock_cursor.fetchone.return_value = None

        count = player_dao.get_matches_count(sample_player)

        assert count == 0


class TestGetPlayersInRank:
    """Tests pour récupérer les joueurs d'un rang"""

    def test_get_players_in_rank_found(self, player_dao, mock_cursor):
        """Test la récupération de joueurs dans un rang"""
        # Créer un mock de Ranks avec tous les paramètres nécessaires
        rank = Mock(spec=Ranks)
        rank.id = "rank_123"

        # Mock les résultats avec dictionnaires
        mock_cursor.fetchall.return_value = [
            {
                "id": "player1",
                "platform_id": "plat1",
                "platform_user_id": "user1",
                "name": "Player1",
            },
            {
                "id": "player2",
                "platform_id": "plat2",
                "platform_user_id": "user2",
                "name": "Player2",
            },
        ]

        results = player_dao.get_players_in_rank(rank)

        assert results is not None
        assert len(results) == 2
        assert all(isinstance(p, Player) for p in results)
        assert results[0].name == "Player1"
        assert results[1].name == "Player2"

        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "WHERE r.id = ?" in call_args[0]
        assert call_args[1] == (rank.id,)

    def test_get_players_in_rank_not_found(self, player_dao, mock_cursor):
        """Test sans joueurs dans le rang"""
        mock_cursor.fetchall.return_value = None

        rank = Mock(spec=Ranks)
        rank.id = "rank_123"

        results = player_dao.get_players_in_rank(rank)

        assert results is None

    def test_get_players_in_rank_empty_list(self, player_dao, mock_cursor):
        """Test avec liste vide de joueurs"""
        mock_cursor.fetchall.return_value = []

        rank = Mock(spec=Ranks)
        rank.id = "rank_123"

        results = player_dao.get_players_in_rank(rank)

        # Le code vérifie "if not res" donc [] retourne aussi None
        assert results is None


class TestGetPlayersInTeam:
    """Tests pour récupérer les joueurs d'une équipe"""

    def test_get_players_in_team_found(self, player_dao, mock_cursor):
        """Test la récupération de joueurs dans une équipe"""
        # Créer un mock de MatchTeam
        match_team = Mock(spec=MatchTeam)
        match_team.id = "team_123"

        mock_cursor.fetchall.return_value = [
            {
                "id": "player1",
                "platform_id": "plat1",
                "platform_user_id": "user1",
                "name": "Player1",
            }
        ]

        results = player_dao.get_players_in_team(match_team)

        assert results is not None
        assert len(results) == 1
        assert isinstance(results[0], Player)

        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "WHERE mt.id = ?" in call_args[0]
        assert call_args[1] == (match_team.id,)

    def test_get_players_in_team_not_found(self, player_dao, mock_cursor):
        """Test sans joueurs dans l'équipe"""
        mock_cursor.fetchall.return_value = None

        match_team = Mock(spec=MatchTeam)
        match_team.id = "team_123"

        results = player_dao.get_players_in_team(match_team)

        assert results is None

    def test_get_players_in_team_empty_list(self, player_dao, mock_cursor):
        """Test avec liste vide de joueurs"""
        mock_cursor.fetchall.return_value = []

        match_team = Mock(spec=MatchTeam)
        match_team.id = "team_123"

        results = player_dao.get_players_in_team(match_team)

        assert results is None


class TestGetPlayersInMatch:
    """Tests pour récupérer les joueurs d'un match"""

    def test_get_players_in_match_found(self, player_dao, mock_cursor):
        """Test la récupération de joueurs dans un match"""
        # Créer un mock de Match
        match = Mock(spec=Match)
        match.id = "match_123"

        mock_cursor.fetchall.return_value = [
            {
                "id": "player1",
                "platform_id": "plat1",
                "platform_user_id": "user1",
                "name": "Player1",
            },
            {
                "id": "player2",
                "platform_id": "plat2",
                "platform_user_id": "user2",
                "name": "Player2",
            },
        ]

        results = player_dao.get_players_in_match(match)

        assert results is not None
        assert len(results) == 2
        assert all(isinstance(p, Player) for p in results)

        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "WHERE m.id = ?" in call_args[0]
        assert call_args[1] == (match.id,)

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


class TestUpdatePlayer:
    """Tests pour la méthode update_player"""

    def test_update_player_not_implemented(self, player_dao, sample_player):
        """Test que update_player ne fait rien (pass)"""
        # Cette méthode n'est pas implémentée, elle ne devrait rien faire
        result = player_dao.update_player(sample_player)
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
