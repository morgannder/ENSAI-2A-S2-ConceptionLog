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


class TestMatchTeamDAOCreation:
    """Tests pour la création d'équipes de match"""

    def test_create_match_team_success(
        self, match_team_dao, sample_match_team, mock_cursor
    ):
        """Test la création réussie d'une équipe de match"""
        # Simule qu'aucune équipe n'existe avec cet ID
        mock_cursor.fetchone.return_value = None

        result = match_team_dao.create_match_team(sample_match_team)

        assert result is True
        assert mock_cursor.execute.call_count == 2

        # Vérifie la requête SELECT
        first_call = mock_cursor.execute.call_args_list[0]
        assert "SELECT 1" in first_call[0][0]
        assert "FROM match_teams" in first_call[0][0]
        assert "WHERE id = ?" in first_call[0][0]
        assert first_call[0][1] == (sample_match_team.id,)

        # Vérifie la requête INSERT
        second_call = mock_cursor.execute.call_args_list[1]
        assert "INSERT INTO match_teams" in second_call[0][0]
        assert second_call[0][1] == (
            sample_match_team.id,
            sample_match_team.match_id,
            sample_match_team.color,
            sample_match_team.score,
            sample_match_team.possession_time,
            sample_match_team.time_in_side,
        )

    def test_create_match_team_already_exists(
        self, match_team_dao, sample_match_team, mock_cursor
    ):
        """Test la création d'une équipe qui existe déjà"""
        # Simule qu'une équipe existe déjà avec cet ID
        mock_cursor.fetchone.return_value = (1,)

        result = match_team_dao.create_match_team(sample_match_team)

        assert result is False
        # Vérifie qu'INSERT n'a pas été appelé (seulement SELECT)
        assert mock_cursor.execute.call_count == 1


class TestMatchTeamDAORetrieval:
    """Tests pour la récupération d'équipes de match"""

    def test_get_match_teams_by_parameter_found_single(
        self, match_team_dao, sample_match_team, mock_cursor
    ):
        """Test la récupération d'une équipe par paramètre (un seul résultat)"""
        mock_cursor.fetchall.return_value = [
            {
                "id": sample_match_team.id,
                "match_id": sample_match_team.match_id,
                "color": sample_match_team.color,
                "score": sample_match_team.score,
                "possession_time": sample_match_team.possession_time,
                "time_in_side": sample_match_team.time_in_side,
            }
        ]

        result = match_team_dao.get_match_teams_by_parameter("id", sample_match_team.id)

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], MatchTeam)

        # Vérifie la requête SQL
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "FROM match_teams" in call_args[0]
        assert "WHERE id= ?" in call_args[0]
        assert call_args[1] == (sample_match_team.id,)

    def test_get_match_teams_by_parameter_found_multiple(
        self, match_team_dao, mock_cursor
    ):
        """Test la récupération de plusieurs équipes par paramètre"""
        # Simule plusieurs équipes du même match
        mock_cursor.fetchall.return_value = [
            {
                "id": "team1",
                "match_id": "match123",
                "color": "blue",
                "score": 3,
                "possession_time": 145.5,
                "time_in_side": 150.0,
            },
            {
                "id": "team2",
                "match_id": "match123",
                "color": "orange",
                "score": 2,
                "possession_time": 154.5,
                "time_in_side": 150.0,
            },
        ]

        result = match_team_dao.get_match_teams_by_parameter("match_id", "match123")

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 2
        for team in result:
            assert isinstance(team, MatchTeam)

    def test_get_match_teams_by_parameter_not_found(self, match_team_dao, mock_cursor):
        """Test la récupération d'une équipe inexistante"""
        mock_cursor.fetchall.return_value = []

        result = match_team_dao.get_match_teams_by_parameter("id", "nonexistent")

        assert result is None

    def test_get_match_teams_by_parameter_invalid_column(self, match_team_dao):
        """Test avec un nom de colonne invalide"""
        with pytest.raises(ValueError, match="Invalid column name"):
            match_team_dao.get_match_teams_by_parameter("invalid_column", "value")

    def test_get_match_teams_by_parameter_all_allowed_columns(
        self, match_team_dao, mock_cursor
    ):
        """Test avec toutes les colonnes autorisées"""
        allowed_columns = [
            "id",
            "match_id",
            "score",
            "color",
            "time_in_side",
            "possession_time",
        ]

        for column in allowed_columns:
            # Reset et reconfigure le mock pour chaque itération
            mock_cursor.reset_mock()
            mock_cursor.fetchall.return_value = [
                {
                    "id": "test_id",
                    "match_id": "test_match",
                    "color": "blue",
                    "score": 3,
                    "possession_time": 145.5,
                    "time_in_side": 150.0,
                }
            ]

            result = match_team_dao.get_match_teams_by_parameter(column, "test_value")

            assert result is not None
            assert isinstance(result, list)
            assert len(result) == 1
            call_args = mock_cursor.execute.call_args[0]
            assert f"WHERE {column}= ?" in call_args[0]

    def test_get_match_teams_by_parameter_by_color(self, match_team_dao, mock_cursor):
        """Test la récupération des équipes par couleur"""
        mock_cursor.fetchall.return_value = [
            {
                "id": "team1",
                "match_id": "match1",
                "color": "blue",
                "score": 3,
                "possession_time": 145.5,
                "time_in_side": 150.0,
            },
            {
                "id": "team2",
                "match_id": "match2",
                "color": "blue",
                "score": 5,
                "possession_time": 160.0,
                "time_in_side": 140.0,
            },
        ]

        result = match_team_dao.get_match_teams_by_parameter("color", "blue")

        assert result is not None
        assert len(result) == 2
        call_args = mock_cursor.execute.call_args[0]
        assert call_args[1] == ("blue",)


class TestMatchTeamDAODeletion:
    """Tests pour la suppression d'équipes de match"""

    def test_delete_match_teams(self, match_team_dao, sample_match_team, mock_cursor):
        """Test la suppression d'une équipe de match"""
        match_team_dao.delete_match_teams(sample_match_team)

        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "DELETE FROM match_teams" in call_args[0]
        assert "WHERE id = ?" in call_args[0]
        assert call_args[1] == (sample_match_team.id,)


class TestGetPlayerLastMatchTeams:
    """Tests pour la récupération des dernières équipes d'un joueur"""

    def test_get_player_last_match_teams_default(
        self, match_team_dao, sample_player, mock_cursor
    ):
        """Test la récupération des 20 dernières équipes d'un joueur (défaut)"""
        teams_data = [
            {
                "id": f"team_{i}",
                "match_id": f"match_{i}",
                "color": "blue" if i % 2 == 0 else "orange",
                "score": 3,
                "possession_time": 145.5,
                "time_in_side": 150.0,
            }
            for i in range(20)
        ]
        mock_cursor.fetchall.return_value = teams_data

        result = match_team_dao.get_player_last_match_teams(sample_player)

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 20
        for team in result:
            assert isinstance(team, MatchTeam)

        # Vérifie la requête SQL
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]

        # Vérifie la structure de la requête
        assert "SELECT mt.*" in call_args[0]
        assert "FROM matches m" in call_args[0]
        assert "JOIN match_teams mt ON mt.match_id = m.id" in call_args[0]
        assert "JOIN match_participation mp ON mp.match_team_id = mt.id" in call_args[0]
        assert "JOIN players p ON p.id = mp.player_id" in call_args[0]
        assert "WHERE p.id = ?" in call_args[0]
        assert "ORDER BY m.date_upload DESC" in call_args[0]
        assert "LIMIT ?" in call_args[0]
        assert call_args[1] == (sample_player.id, 20)

    def test_get_player_last_match_teams_custom_number(
        self, match_team_dao, sample_player, mock_cursor
    ):
        """Test la récupération d'un nombre personnalisé d'équipes d'un joueur"""
        teams_data = [
            {
                "id": f"team_{i}",
                "match_id": f"match_{i}",
                "color": "blue",
                "score": 3,
                "possession_time": 145.5,
                "time_in_side": 150.0,
            }
            for i in range(5)
        ]
        mock_cursor.fetchall.return_value = teams_data

        result = match_team_dao.get_player_last_match_teams(sample_player, nb_match=5)

        assert result is not None
        assert len(result) == 5

        call_args = mock_cursor.execute.call_args[0]
        assert call_args[1] == (sample_player.id, 5)

    def test_get_player_last_match_teams_no_teams(
        self, match_team_dao, sample_player, mock_cursor
    ):
        """Test quand un joueur n'a aucune équipe"""
        mock_cursor.fetchall.return_value = []

        result = match_team_dao.get_player_last_match_teams(sample_player)

        assert result is None

    def test_get_player_last_match_teams_verifies_order(
        self, match_team_dao, sample_player, mock_cursor
    ):
        """Test que les équipes sont bien triées par date décroissante"""
        teams_data = [
            {
                "id": "team_recent",
                "match_id": "match_123",
                "color": "blue",
                "score": 3,
                "possession_time": 145.5,
                "time_in_side": 150.0,
            }
        ]
        mock_cursor.fetchall.return_value = teams_data

        result = match_team_dao.get_player_last_match_teams(sample_player)

        assert result is not None

        call_args = mock_cursor.execute.call_args[0]
        assert "ORDER BY m.date_upload DESC" in call_args[0]


class TestUpdate:
    """Tests pour la méthode update"""

    def test_update_not_implemented(self, match_team_dao, sample_match_team):
        """Test que update ne fait rien (pass)"""
        result = match_team_dao.update(sample_match_team)
        assert result is None


class TestMatchTeamDAOSingleton:
    """Tests pour vérifier le pattern Singleton"""

    def test_singleton_pattern(self):
        """Test que MatchTeamDAO est bien un singleton"""
        with patch("src.dao.match_teams_dao.DBConnection"):
            instance1 = MatchTeamDAO()
            instance2 = MatchTeamDAO()

            assert instance1 is instance2


class TestMatchTeamDAOEdgeCases:
    """Tests pour les cas limites"""

    def test_create_match_team_with_high_score(self, match_team_dao, mock_cursor):
        """Test la création d'une équipe avec un score élevé"""
        team = Mock(spec=MatchTeam)
        team.id = str(uuid4())
        team.match_id = str(uuid4())
        team.color = "orange"
        team.score = 15
        team.possession_time = 200.0
        team.time_in_side = 100.0

        mock_cursor.fetchone.return_value = None

        result = match_team_dao.create_match_team(team)

        assert result is True
        second_call = mock_cursor.execute.call_args_list[1]
        assert second_call[0][1] == (
            team.id,
            team.match_id,
            team.color,
            team.score,
            team.possession_time,
            team.time_in_side,
        )

    def test_get_match_teams_by_parameter_empty_result(
        self, match_team_dao, mock_cursor
    ):
        """Test avec un résultat vide"""
        mock_cursor.fetchall.return_value = []

        result = match_team_dao.get_match_teams_by_parameter("score", 10)

        assert result is None

    def test_delete_match_teams_twice(
        self, match_team_dao, sample_match_team, mock_cursor
    ):
        """Test la suppression d'une équipe deux fois"""
        # Première suppression
        match_team_dao.delete_match_teams(sample_match_team)
        assert mock_cursor.execute.call_count == 1

        # Deuxième suppression
        match_team_dao.delete_match_teams(sample_match_team)
        assert mock_cursor.execute.call_count == 2

    def test_get_match_teams_by_score(self, match_team_dao, mock_cursor):
        """Test la récupération des équipes par score"""
        teams_data = [
            {
                "id": f"team_{i}",
                "match_id": f"match_{i}",
                "color": "blue" if i % 2 == 0 else "orange",
                "score": 5,
                "possession_time": 145.5,
                "time_in_side": 150.0,
            }
            for i in range(3)
        ]
        mock_cursor.fetchall.return_value = teams_data

        result = match_team_dao.get_match_teams_by_parameter("score", 5)

        assert result is not None
        assert len(result) == 3
        assert all(isinstance(t, MatchTeam) for t in result)


class TestMatchTeamDAOIntegration:
    """Tests d'intégration simulant des scénarios réels"""

    def test_create_and_retrieve_match_team(
        self, match_team_dao, sample_match_team, mock_cursor
    ):
        """Test la création puis la récupération d'une équipe"""
        # Création
        mock_cursor.fetchone.return_value = None
        create_result = match_team_dao.create_match_team(sample_match_team)
        assert create_result is True

        # Récupération
        mock_cursor.reset_mock()
        mock_cursor.fetchall.return_value = [
            {
                "id": sample_match_team.id,
                "match_id": sample_match_team.match_id,
                "color": sample_match_team.color,
                "score": sample_match_team.score,
                "possession_time": sample_match_team.possession_time,
                "time_in_side": sample_match_team.time_in_side,
            }
        ]

        retrieved_teams = match_team_dao.get_match_teams_by_parameter(
            "id", sample_match_team.id
        )
        assert retrieved_teams is not None
        assert len(retrieved_teams) == 1
        assert isinstance(retrieved_teams[0], MatchTeam)

    def test_get_both_teams_from_match(self, match_team_dao, mock_cursor):
        """Test la récupération des deux équipes d'un match"""
        match_id = str(uuid4())
        teams_data = [
            {
                "id": "blue_team",
                "match_id": match_id,
                "color": "blue",
                "score": 3,
                "possession_time": 145.5,
                "time_in_side": 150.0,
            },
            {
                "id": "orange_team",
                "match_id": match_id,
                "color": "orange",
                "score": 2,
                "possession_time": 154.5,
                "time_in_side": 150.0,
            },
        ]
        mock_cursor.fetchall.return_value = teams_data

        result = match_team_dao.get_match_teams_by_parameter("match_id", match_id)

        assert result is not None
        assert len(result) == 2
        # Vérifie qu'on a bien une équipe bleue et une orange
        colors = [team.color for team in result]
        assert "blue" in colors
        assert "orange" in colors


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
