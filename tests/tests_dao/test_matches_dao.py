from unittest.mock import MagicMock, Mock, PropertyMock, patch
from uuid import uuid4

import pytest

from src.dao.matches_dao import MatchDAO

# Ajustez ces imports selon votre structure de projet
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
    connection.__enter__ = MagicMock(return_value=connection)
    connection.__exit__ = MagicMock(return_value=None)
    return connection


@pytest.fixture
def match_dao(mock_connection):
    """Fixture pour créer une instance de MatchDAO avec mock"""
    with patch("src.dao.matches_dao.DBConnection") as mock_db_conn:
        # Mock de la classe DBConnection elle-même (pas d'instance)
        type(mock_db_conn).connection = PropertyMock(return_value=mock_connection)

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


class TestMatchDAOCreation:
    """Tests pour la création de matchs"""

    def test_create_match_success(self, match_dao, sample_match, mock_cursor):
        """Test la création réussie d'un match"""
        # Simule qu'aucun match n'existe avec cet ID
        mock_cursor.fetchone.return_value = None

        result = match_dao.create_match(sample_match)

        assert result is True
        assert mock_cursor.execute.call_count == 2

        # Vérifie la requête SELECT
        first_call = mock_cursor.execute.call_args_list[0]
        assert "SELECT 1" in first_call[0][0]
        assert "FROM matches" in first_call[0][0]
        assert "WHERE id = ?" in first_call[0][0]
        assert first_call[0][1] == (sample_match.id,)

        # Vérifie la requête INSERT
        second_call = mock_cursor.execute.call_args_list[1]
        assert "INSERT INTO matches" in second_call[0][0]
        assert second_call[0][1] == (
            sample_match.id,
            sample_match.playlist_id,
            sample_match.season,
            sample_match.duration,
            sample_match.overtime,
            sample_match.date_upload,
        )

    def test_create_match_already_exists(self, match_dao, sample_match, mock_cursor):
        """Test la création d'un match qui existe déjà"""
        # Simule qu'un match existe déjà avec cet ID
        mock_cursor.fetchone.return_value = (1,)

        result = match_dao.create_match(sample_match)

        assert result is False
        # Vérifie qu'INSERT n'a pas été appelé (seulement SELECT)
        assert mock_cursor.execute.call_count == 1


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


class TestMatchDAODeletion:
    """Tests pour la suppression de matchs"""

    def test_delete_match(self, match_dao, sample_match, mock_cursor):
        """Test la suppression d'un match"""
        match_dao.delete_match(sample_match)

        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "DELETE FROM matches" in call_args[0]
        assert "WHERE id = ?" in call_args[0]
        assert call_args[1] == (sample_match.id,)


class TestGet20RecentMatches:
    """Tests pour la récupération des matchs récents"""

    def test_get_20_recent_matches_default(self, match_dao, mock_cursor):
        """Test la récupération des 20 matchs les plus récents (défaut)"""
        # Simule 20 matchs
        matches_data = [
            {
                "id": f"match_{i}",
                "playlist_id": "ranked-doubles",
                "season": "Season 15",
                "duration": 300 + i * 10,
                "overtime": i % 2 == 0,
                "date_upload": f"2024-02-{11 + i // 10} 14:{i % 60:02d}:00",
            }
            for i in range(20)
        ]
        mock_cursor.fetchall.return_value = matches_data

        result = match_dao.get_20_recent_matches()

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 20
        for match in result:
            assert isinstance(match, Match)

        # Vérifie la requête SQL
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "ORDER BY date_upload DESC" in call_args[0]
        assert "LIMIT ?" in call_args[0]
        assert call_args[1] == (20,)

    def test_get_20_recent_matches_custom_number(self, match_dao, mock_cursor):
        """Test la récupération d'un nombre personnalisé de matchs récents"""
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

        result = match_dao.get_20_recent_matches(nb_match=10)

        assert result is not None
        assert len(result) == 10

        call_args = mock_cursor.execute.call_args[0]
        assert call_args[1] == (10,)

    def test_get_20_recent_matches_no_matches(self, match_dao, mock_cursor):
        """Test quand il n'y a aucun match"""
        mock_cursor.fetchall.return_value = []

        result = match_dao.get_20_recent_matches()

        assert result is None

    def test_get_20_recent_matches_less_than_requested(self, match_dao, mock_cursor):
        """Test quand il y a moins de matchs que demandé"""
        matches_data = [
            {
                "id": f"match_{i}",
                "playlist_id": "ranked-doubles",
                "season": "Season 15",
                "duration": 300,
                "overtime": False,
                "date_upload": f"2024-02-11 14:{i:02d}:00",
            }
            for i in range(5)
        ]
        mock_cursor.fetchall.return_value = matches_data

        result = match_dao.get_20_recent_matches(nb_match=20)

        assert result is not None
        assert len(result) == 5


class TestGetPlayerLastMatches:
    """Tests pour la récupération des derniers matchs d'un joueur"""

    def test_get_player_last_matches_default(
        self, match_dao, sample_player, mock_cursor
    ):
        """Test la récupération des 20 derniers matchs d'un joueur (défaut)"""
        matches_data = [
            {
                "id": f"match_{i}",
                "playlist_id": "ranked-doubles",
                "season": "Season 15",
                "duration": 300,
                "overtime": False,
                "date_upload": f"2024-02-11 14:{i:02d}:00",
            }
            for i in range(20)
        ]
        mock_cursor.fetchall.return_value = matches_data

        result = match_dao.get_player_last_matches(sample_player)

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 20
        for match in result:
            assert isinstance(match, Match)

        # Vérifie la requête SQL
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]

        # Vérifie la structure de la requête
        assert "SELECT m.*" in call_args[0]
        assert "FROM matches m" in call_args[0]
        assert "JOIN match_teams mt ON mt.match_id = m.id" in call_args[0]
        assert "JOIN match_participation mp ON mp.match_team_id = mt.id" in call_args[0]
        assert "JOIN players p ON p.id = mp.player_id" in call_args[0]
        assert "WHERE p.id = ?" in call_args[0]
        assert "ORDER BY m.date_upload DESC" in call_args[0]
        assert "LIMIT ?" in call_args[0]
        assert call_args[1] == (sample_player.id, 20)

    def test_get_player_last_matches_custom_number(
        self, match_dao, sample_player, mock_cursor
    ):
        """Test la récupération d'un nombre personnalisé de matchs d'un joueur"""
        matches_data = [
            {
                "id": f"match_{i}",
                "playlist_id": "ranked-doubles",
                "season": "Season 15",
                "duration": 300,
                "overtime": False,
                "date_upload": f"2024-02-11 14:{i:02d}:00",
            }
            for i in range(5)
        ]
        mock_cursor.fetchall.return_value = matches_data

        result = match_dao.get_player_last_matches(sample_player, nb_match=5)

        assert result is not None
        assert len(result) == 5

        call_args = mock_cursor.execute.call_args[0]
        assert call_args[1] == (sample_player.id, 5)

    def test_get_player_last_matches_no_matches(
        self, match_dao, sample_player, mock_cursor
    ):
        """Test quand un joueur n'a aucun match"""
        mock_cursor.fetchall.return_value = []

        result = match_dao.get_player_last_matches(sample_player)

        assert result is None

    def test_get_player_last_matches_verifies_order(
        self, match_dao, sample_player, mock_cursor
    ):
        """Test que les matchs sont bien triés par date décroissante"""
        matches_data = [
            {
                "id": "match_recent",
                "playlist_id": "ranked-doubles",
                "season": "Season 15",
                "duration": 300,
                "overtime": False,
                "date_upload": "2024-02-11 15:00:00",
            }
        ]
        mock_cursor.fetchall.return_value = matches_data

        result = match_dao.get_player_last_matches(sample_player)

        assert result is not None

        call_args = mock_cursor.execute.call_args[0]
        assert "ORDER BY m.date_upload DESC" in call_args[0]


class TestUpdateMatch:
    """Tests pour la méthode update_match"""

    def test_update_match_not_implemented(self, match_dao, sample_match):
        """Test que update_match ne fait rien (pass)"""
        result = match_dao.update_match(sample_match)
        assert result is None


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

    def test_create_match_with_overtime(self, match_dao, mock_cursor):
        """Test la création d'un match avec overtime"""
        match = Mock(spec=Match)
        match.id = str(uuid4())
        match.playlist_id = "ranked-doubles"
        match.season = "Season 15"
        match.duration = 420  # 7 minutes avec overtime
        match.overtime = True
        match.date_upload = "2024-02-11 14:30:00"

        mock_cursor.fetchone.return_value = None

        result = match_dao.create_match(match)

        assert result is True
        second_call = mock_cursor.execute.call_args_list[1]
        assert second_call[0][1] == (
            match.id,
            match.playlist_id,
            match.season,
            match.duration,
            match.overtime,
            match.date_upload,
        )

    def test_get_match_by_parameter_empty_result(self, match_dao, mock_cursor):
        """Test avec un résultat vide"""
        mock_cursor.fetchall.return_value = []

        result = match_dao.get_match_by_parameter("season", "NonExistent Season")

        assert result is None

    def test_delete_match_twice(self, match_dao, sample_match, mock_cursor):
        """Test la suppression d'un match deux fois"""
        # Première suppression
        match_dao.delete_match(sample_match)
        assert mock_cursor.execute.call_count == 1

        # Deuxième suppression
        match_dao.delete_match(sample_match)
        assert mock_cursor.execute.call_count == 2

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


class TestMatchDAOIntegration:
    """Tests d'intégration simulant des scénarios réels"""

    def test_create_and_retrieve_match(self, match_dao, sample_match, mock_cursor):
        """Test la création puis la récupération d'un match"""
        # Création
        mock_cursor.fetchone.return_value = None
        create_result = match_dao.create_match(sample_match)
        assert create_result is True

        # Récupération
        mock_cursor.reset_mock()
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

        retrieved_matches = match_dao.get_match_by_parameter("id", sample_match.id)
        assert retrieved_matches is not None
        assert len(retrieved_matches) == 1
        assert isinstance(retrieved_matches[0], Match)

    def test_player_match_history_workflow(self, match_dao, sample_player, mock_cursor):
        """Test le workflow complet de récupération de l'historique d'un joueur"""
        # Simule 15 matchs pour un joueur
        matches_data = [
            {
                "id": f"match_{i}",
                "playlist_id": "ranked-doubles" if i % 2 == 0 else "ranked-standard",
                "season": "Season 15",
                "duration": 300 + i * 20,
                "overtime": i > 10,
                "date_upload": f"2024-02-11 {14 + i // 60}:{i % 60:02d}:00",
            }
            for i in range(15)
        ]
        mock_cursor.fetchall.return_value = matches_data

        # Récupération des matchs du joueur
        player_matches = match_dao.get_player_last_matches(sample_player, nb_match=15)

        assert player_matches is not None
        assert len(player_matches) == 15
        assert all(isinstance(m, Match) for m in player_matches)

    def test_recent_matches_then_player_matches(
        self, match_dao, sample_player, mock_cursor
    ):
        """Test récupération des matchs récents puis des matchs d'un joueur spécifique"""
        # Premier appel: matchs récents
        recent_matches_data = [
            {
                "id": f"match_{i}",
                "playlist_id": "ranked-doubles",
                "season": "Season 15",
                "duration": 300,
                "overtime": False,
                "date_upload": f"2024-02-11 14:{i:02d}:00",
            }
            for i in range(20)
        ]
        mock_cursor.fetchall.return_value = recent_matches_data

        recent = match_dao.get_20_recent_matches()
        assert recent is not None
        assert len(recent) == 20

        # Deuxième appel: matchs du joueur
        mock_cursor.reset_mock()
        player_matches_data = [
            {
                "id": f"player_match_{i}",
                "playlist_id": "ranked-doubles",
                "season": "Season 15",
                "duration": 300,
                "overtime": False,
                "date_upload": f"2024-02-11 14:{i:02d}:00",
            }
            for i in range(10)
        ]
        mock_cursor.fetchall.return_value = player_matches_data

        player_matches = match_dao.get_player_last_matches(sample_player, nb_match=10)
        assert player_matches is not None
        assert len(player_matches) == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
