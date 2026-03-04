from unittest.mock import MagicMock, Mock, PropertyMock, patch
from uuid import uuid4

import pytest

from src.dao.ranks_dao import RanksDAO

# Ajustez ces imports selon votre structure de projet
from src.models.players import Player
from src.models.ranks import Ranks


# Reset du singleton avant chaque test
@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset le singleton RanksDAO avant chaque test"""
    RanksDAO._instances = {}
    yield
    RanksDAO._instances = {}


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
def ranks_dao(mock_connection):
    """Fixture pour créer une instance de RanksDAO avec mock"""
    with patch("src.dao.ranks_dao.DBConnection") as mock_db_conn:
        mock_db_instance = MagicMock()
        type(mock_db_instance).connection = PropertyMock(return_value=mock_connection)
        mock_db_conn.return_value = mock_db_instance

        dao = RanksDAO()
        yield dao


@pytest.fixture
def sample_rank():
    """Fixture pour créer un rang exemple"""
    rank = Mock(spec=Ranks)
    rank.id = str(uuid4())
    rank.tier = 3
    rank.division = 2
    rank.name = "Gold III"
    return rank


@pytest.fixture
def sample_player():
    """Fixture pour créer un joueur exemple"""
    player = Mock(spec=Player)
    player.id = str(uuid4())
    player.platform_id = "platform_123"
    player.platform_user_id = "user_456"
    player.name = "TestPlayer"
    return player


class TestRanksDAORetrieval:
    """Tests pour la récupération de rangs"""

    def test_get_rank_by_parameter_found_single(
        self, ranks_dao, sample_rank, mock_cursor
    ):
        """Test la récupération d'un rang par paramètre (un seul résultat)"""
        # Simule un résultat de base de données
        mock_cursor.fetchall.return_value = [
            {
                "id": sample_rank.id,
                "tier": sample_rank.tier,
                "division": sample_rank.division,
                "name": sample_rank.name,
            }
        ]

        result = ranks_dao.get_rank_by_parameter("name", "Gold III")

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Ranks)

        # Vérifie la requête SQL
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "WHERE name = ?" in call_args[0]
        assert call_args[1] == ("Gold III",)

    def test_get_rank_by_parameter_found_multiple(self, ranks_dao, mock_cursor):
        """Test la récupération de plusieurs rangs par paramètre (ex: même tier)"""
        # Simule plusieurs résultats avec le même tier
        mock_cursor.fetchall.return_value = [
            {"id": "id1", "tier": 3, "division": 1, "name": "Gold I"},
            {"id": "id2", "tier": 3, "division": 2, "name": "Gold II"},
            {"id": "id3", "tier": 3, "division": 3, "name": "Gold III"},
        ]

        result = ranks_dao.get_rank_by_parameter("tier", 3)

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 3
        for rank in result:
            assert isinstance(rank, Ranks)

    def test_get_rank_by_parameter_not_found(self, ranks_dao, mock_cursor):
        """Test la récupération d'un rang inexistant"""
        # Explicitement définir fetchall pour retourner une liste vide
        mock_cursor.fetchall.return_value = []

        result = ranks_dao.get_rank_by_parameter("name", "NonExistent")

        assert result is None

    def test_get_rank_by_parameter_invalid_column(self, ranks_dao):
        """Test avec un nom de colonne invalide"""
        with pytest.raises(ValueError, match="Invalid column name"):
            ranks_dao.get_rank_by_parameter("invalid_column", "value")

    def test_get_rank_by_parameter_all_allowed_columns(self, ranks_dao, mock_cursor):
        """Test avec toutes les colonnes autorisées"""
        allowed_columns = ["id", "name", "tier", "division"]

        for column in allowed_columns:
            # Reset et reconfigure le mock pour chaque itération
            mock_cursor.reset_mock()
            mock_cursor.fetchall.return_value = [
                {
                    "id": "test_id",
                    "tier": 2,
                    "division": 1,
                    "name": "test_name",
                }
            ]

            result = ranks_dao.get_rank_by_parameter(column, "test_value")

            assert result is not None
            assert isinstance(result, list)
            assert len(result) == 1
            call_args = mock_cursor.execute.call_args[0]
            assert f"WHERE {column} = ?" in call_args[0]

    def test_get_rank_by_parameter_by_id(self, ranks_dao, sample_rank, mock_cursor):
        """Test la récupération d'un rang par ID"""
        mock_cursor.fetchall.return_value = [
            {
                "id": sample_rank.id,
                "tier": sample_rank.tier,
                "division": sample_rank.division,
                "name": sample_rank.name,
            }
        ]

        result = ranks_dao.get_rank_by_parameter("id", sample_rank.id)

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Ranks)

        call_args = mock_cursor.execute.call_args[0]
        assert "WHERE id = ?" in call_args[0]
        assert call_args[1] == (sample_rank.id,)


class TestGetPlayerRank:
    """Tests pour récupérer le rang d'un joueur"""

    def test_get_player_rank_found(self, ranks_dao, sample_player, mock_cursor):
        """Test la récupération du rang d'un joueur"""
        # Mock le résultat du rang le plus récent
        mock_cursor.fetchone.return_value = {
            "id": "rank_123",
            "tier": 3,
            "division": 2,
            "name": "Gold II",
        }

        result = ranks_dao.get_player_rank(sample_player)

        assert result is not None
        assert isinstance(result, Ranks)

        # Vérifie la requête SQL
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]

        # Vérifie les éléments clés de la requête
        assert "SELECT r.id, r.tier, r.division, r.name" in call_args[0]
        assert "FROM ranks r" in call_args[0]
        assert "JOIN match_participation mp ON mp.rank_id=r.id" in call_args[0]
        assert "JOIN match_teams mt ON mt.id=mp.match_team_id" in call_args[0]
        assert "JOIN matches m ON m.id=mt.match_id" in call_args[0]
        assert "JOIN players p ON p.id=mp.player_id" in call_args[0]
        assert "WHERE p.id = ?" in call_args[0]
        assert "ORDER BY m.date_upload DESC" in call_args[0]
        assert "LIMIT 1" in call_args[0]
        assert call_args[1] == (sample_player.id,)

    def test_get_player_rank_not_found(self, ranks_dao, sample_player, mock_cursor):
        """Test quand un joueur n'a pas de rang (aucun match)"""
        mock_cursor.fetchone.return_value = None

        result = ranks_dao.get_player_rank(sample_player)

        assert result is None

    def test_get_player_rank_verifies_most_recent(
        self, ranks_dao, sample_player, mock_cursor
    ):
        """Test que la méthode retourne bien le rang le plus récent"""
        # Mock un rang spécifique
        mock_cursor.fetchone.return_value = {
            "id": "rank_latest",
            "tier": 5,
            "division": 1,
            "name": "Diamond I",
        }

        result = ranks_dao.get_player_rank(sample_player)

        assert result is not None
        assert isinstance(result, Ranks)

        # Vérifie que ORDER BY et LIMIT 1 sont présents
        call_args = mock_cursor.execute.call_args[0]
        assert "ORDER BY m.date_upload DESC" in call_args[0]
        assert "LIMIT 1" in call_args[0]


class TestRanksDAOSingleton:
    """Tests pour vérifier le pattern Singleton"""

    def test_singleton_pattern(self):
        """Test que RanksDAO est bien un singleton"""
        with patch("src.dao.ranks_dao.DBConnection"):
            instance1 = RanksDAO()
            instance2 = RanksDAO()

            assert instance1 is instance2


class TestRanksDAOEdgeCases:
    """Tests pour les cas limites"""

    def test_get_rank_by_parameter_empty_result(self, ranks_dao, mock_cursor):
        """Test avec un résultat vide"""
        mock_cursor.fetchall.return_value = []

        result = ranks_dao.get_rank_by_parameter("name", "test")

        assert result is None

    def test_get_rank_by_parameter_with_tier_returns_all_divisions(
        self, ranks_dao, mock_cursor
    ):
        """Test que la recherche par tier retourne toutes les divisions"""
        # Simule 3 divisions du tier Gold (tier 3)
        mock_cursor.fetchall.return_value = [
            {"id": "g1", "tier": 3, "division": 1, "name": "Gold I"},
            {"id": "g2", "tier": 3, "division": 2, "name": "Gold II"},
            {"id": "g3", "tier": 3, "division": 3, "name": "Gold III"},
        ]

        result = ranks_dao.get_rank_by_parameter("tier", 3)

        assert result is not None
        assert len(result) == 3
        assert all(isinstance(r, Ranks) for r in result)


class TestRanksDAOIntegration:
    """Tests d'intégration simulant des scénarios réels"""

    def test_player_rank_progression(self, ranks_dao, sample_player, mock_cursor):
        """Test la progression de rang d'un joueur"""
        # Simule différents rangs au fil du temps
        # Le plus récent devrait être Platinum II (grâce à ORDER BY DESC LIMIT 1)
        mock_cursor.fetchone.return_value = {
            "id": "r3",
            "tier": 4,
            "division": 2,
            "name": "Platinum II",
        }

        current_rank = ranks_dao.get_player_rank(sample_player)

        assert current_rank is not None
        assert isinstance(current_rank, Ranks)

        # Deuxième appel: get_player_rank
        mock_cursor.reset_mock()
        mock_cursor.fetchone.return_value = {
            "id": "diamond2_id",
            "tier": 5,
            "division": 2,
            "name": "Diamond II",
        }

        player_rank = ranks_dao.get_player_rank(sample_player)
        assert player_rank is not None
        assert isinstance(player_rank, Ranks)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
