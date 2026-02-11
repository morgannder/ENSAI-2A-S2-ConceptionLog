from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

import pytest

from src.dao.match_participation_dao import MatchParticipationDAO

# Ajustez ces imports selon votre structure de projet
from src.models.match_participation import MatchParticipation
from src.models.players import Player


# Reset du singleton avant chaque test
@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset le singleton MatchParticipationDAO avant chaque test"""
    MatchParticipationDAO._instances = {}
    yield
    MatchParticipationDAO._instances = {}


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
def match_participation_dao(mock_connection):
    """Fixture pour créer une instance de MatchParticipationDAO avec mock"""
    with patch("src.dao.match_participation_dao.DBConnection") as mock_db_conn:
        mock_instance = MagicMock()
        mock_instance.connection = mock_connection
        mock_db_conn.return_value = mock_instance

        dao = MatchParticipationDAO()
        yield dao


@pytest.fixture
def sample_match_participation():
    """Fixture pour créer une participation de match exemple"""
    match_participation = Mock(spec=MatchParticipation)
    match_participation.id = str(uuid4())
    match_participation.match_team_id = str(uuid4())
    match_participation.player_id = str(uuid4())
    match_participation.rank_id = str(uuid4())
    match_participation.car_id = str(uuid4())
    match_participation.car_name = "Octane"
    match_participation.mvp = True
    match_participation.start_time = 0.0
    match_participation.end_time = 300.0
    return match_participation


@pytest.fixture
def sample_player():
    """Fixture pour créer un joueur exemple"""
    player = Mock(spec=Player)
    player.id = str(uuid4())
    player.platform_id = "platform_123"
    player.platform_user_id = "user_456"
    player.name = "TestPlayer"
    return player


class TestMatchParticipationDAOCreation:
    """Tests pour la création de participations de match"""

    def test_create_match_participation_success(
        self, match_participation_dao, sample_match_participation, mock_cursor
    ):
        """Test la création réussie d'une participation de match"""
        # Simule qu'aucune participation n'existe avec cet ID
        mock_cursor.fetchone.return_value = None

        result = match_participation_dao.create_match_participation(
            sample_match_participation
        )

        assert result is True
        assert mock_cursor.execute.call_count == 2

        # Vérifie la requête SELECT
        first_call = mock_cursor.execute.call_args_list[0]
        assert "SELECT 1" in first_call[0][0]
        assert "FROM match_participation" in first_call[0][0]
        assert "WHERE id = ?" in first_call[0][0]
        assert first_call[0][1] == (sample_match_participation.id,)

        # Vérifie la requête INSERT
        second_call = mock_cursor.execute.call_args_list[1]
        assert "INSERT INTO match_participation" in second_call[0][0]
        assert "start_time" in second_call[0][0]
        assert second_call[0][1] == (
            sample_match_participation.id,
            sample_match_participation.match_team_id,
            sample_match_participation.player_id,
            sample_match_participation.rank_id,
            sample_match_participation.car_id,
            sample_match_participation.car_name,
            sample_match_participation.mvp,
            sample_match_participation.start_time,
            sample_match_participation.end_time,
        )

    def test_create_match_participation_already_exists(
        self, match_participation_dao, sample_match_participation, mock_cursor
    ):
        """Test la création d'une participation qui existe déjà"""
        # Simule qu'une participation existe déjà avec cet ID
        mock_cursor.fetchone.return_value = (1,)

        result = match_participation_dao.create_match_participation(
            sample_match_participation
        )

        assert result is False
        # Vérifie qu'INSERT n'a pas été appelé (seulement SELECT)
        assert mock_cursor.execute.call_count == 1

    def test_create_match_participation_not_mvp(
        self, match_participation_dao, mock_cursor
    ):
        """Test la création d'une participation sans MVP"""
        match_participation = Mock(spec=MatchParticipation)
        match_participation.id = str(uuid4())
        match_participation.match_team_id = str(uuid4())
        match_participation.player_id = str(uuid4())
        match_participation.rank_id = str(uuid4())
        match_participation.car_id = str(uuid4())
        match_participation.car_name = "Fennec"
        match_participation.mvp = False
        match_participation.start_time = 0.0
        match_participation.end_time = 300.0

        mock_cursor.fetchone.return_value = None

        result = match_participation_dao.create_match_participation(match_participation)

        assert result is True
        second_call = mock_cursor.execute.call_args_list[1]
        assert second_call[0][1][6] is False  # mvp est False


class TestMatchParticipationDAORetrieval:
    """Tests pour la récupération de participations de match"""

    def test_get_matches_by_parameter_found_single(
        self, match_participation_dao, sample_match_participation, mock_cursor
    ):
        """Test la récupération d'une participation par paramètre (un seul résultat)"""
        mock_cursor.fetchall.return_value = [
            {
                "id": sample_match_participation.id,
                "match_team_id": sample_match_participation.match_team_id,
                "player_id": sample_match_participation.player_id,
                "rank_id": sample_match_participation.rank_id,
                "car_id": sample_match_participation.car_id,
                "car_name": sample_match_participation.car_name,
                "mvp": sample_match_participation.mvp,
                "start_time": sample_match_participation.start_time,
                "end_time": sample_match_participation.end_time,
            }
        ]

        result = match_participation_dao.get_matches_by_parameter(
            "id", sample_match_participation.id
        )

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], MatchParticipation)

        # Vérifie la requête SQL
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "FROM match_participation" in call_args[0]
        assert "WHERE id= ?" in call_args[0]
        assert call_args[1] == (sample_match_participation.id,)

    def test_get_matches_by_parameter_found_multiple(
        self, match_participation_dao, mock_cursor
    ):
        """Test la récupération de plusieurs participations par paramètre"""
        mock_cursor.fetchall.return_value = [
            {
                "id": "part1",
                "match_team_id": "team1",
                "player_id": "player1",
                "rank_id": "rank1",
                "car_id": "car1",
                "car_name": "Octane",
                "mvp": True,
                "start_time": 0.0,
                "end_time": 300.0,
            },
            {
                "id": "part2",
                "match_team_id": "team1",
                "player_id": "player2",
                "rank_id": "rank2",
                "car_id": "car2",
                "car_name": "Fennec",
                "mvp": False,
                "start_time": 0.0,
                "end_time": 300.0,
            },
        ]

        result = match_participation_dao.get_matches_by_parameter(
            "match_team_id", "team1"
        )

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 2
        for participation in result:
            assert isinstance(participation, MatchParticipation)

    def test_get_matches_by_parameter_not_found(
        self, match_participation_dao, mock_cursor
    ):
        """Test la récupération d'une participation inexistante"""
        mock_cursor.fetchall.return_value = []

        result = match_participation_dao.get_matches_by_parameter("id", "nonexistent")

        assert result is None

    def test_get_matches_by_parameter_invalid_column(self, match_participation_dao):
        """Test avec un nom de colonne invalide"""
        with pytest.raises(ValueError, match="Invalid column name"):
            match_participation_dao.get_matches_by_parameter("invalid_column", "value")

    def test_get_matches_by_parameter_all_allowed_columns(
        self, match_participation_dao, mock_cursor
    ):
        """Test avec toutes les colonnes autorisées"""
        allowed_columns = [
            "id",
            "match_team_id",
            "player_id",
            "rank_id",
            "car_id",
            "car_name",
            "mvp",
            "start_time",
            "end_time",
        ]

        for column in allowed_columns:
            # Reset et reconfigure le mock pour chaque itération
            mock_cursor.reset_mock()
            mock_cursor.fetchall.return_value = [
                {
                    "id": "test_id",
                    "match_team_id": "test_team",
                    "player_id": "test_player",
                    "rank_id": "test_rank",
                    "car_id": "test_car",
                    "car_name": "Octane",
                    "mvp": True,
                    "start_time": 0.0,
                    "end_time": 300.0,
                }
            ]

            result = match_participation_dao.get_matches_by_parameter(
                column, "test_value"
            )

            assert result is not None
            assert isinstance(result, list)
            assert len(result) == 1
            call_args = mock_cursor.execute.call_args[0]
            assert f"WHERE {column}= ?" in call_args[0]

    def test_get_matches_by_mvp_status(self, match_participation_dao, mock_cursor):
        """Test la récupération des participations MVP"""
        mock_cursor.fetchall.return_value = [
            {
                "id": "part1",
                "match_team_id": "team1",
                "player_id": "player1",
                "rank_id": "rank1",
                "car_id": "car1",
                "car_name": "Octane",
                "mvp": True,
                "start_time": 0.0,
                "end_time": 300.0,
            },
            {
                "id": "part2",
                "match_team_id": "team2",
                "player_id": "player2",
                "rank_id": "rank2",
                "car_id": "car2",
                "car_name": "Dominus",
                "mvp": True,
                "start_time": 0.0,
                "end_time": 300.0,
            },
        ]

        result = match_participation_dao.get_matches_by_parameter("mvp", True)

        assert result is not None
        assert len(result) == 2
        for participation in result:
            assert participation.mvp is True


class TestMatchParticipationDAODeletion:
    """Tests pour la suppression de participations de match"""

    def test_delete_match_participation(
        self, match_participation_dao, sample_match_participation, mock_cursor
    ):
        """Test la suppression d'une participation de match"""
        match_participation_dao.delete_match_participation(sample_match_participation)

        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "DELETE FROM match_participation" in call_args[0]
        assert "WHERE id = ?" in call_args[0]
        assert call_args[1] == (sample_match_participation.id,)


class TestGetPlayerLastMatchParticipation:
    """Tests pour la récupération des dernières participations d'un joueur"""

    def test_get_player_last_match_participation_default(
        self, match_participation_dao, sample_player, mock_cursor
    ):
        """Test la récupération des 20 dernières participations d'un joueur (défaut)"""
        participations_data = [
            {
                "id": f"part_{i}",
                "match_team_id": f"team_{i}",
                "player_id": sample_player.id,
                "rank_id": f"rank_{i}",
                "car_id": f"car_{i}",
                "car_name": "Octane",
                "mvp": i % 3 == 0,
                "start_time": 0.0,
                "end_time": 300.0,
            }
            for i in range(20)
        ]
        mock_cursor.fetchall.return_value = participations_data

        result = match_participation_dao.get_player_last_match_participation(
            sample_player
        )

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 20
        for participation in result:
            assert isinstance(participation, MatchParticipation)

        # Vérifie la requête SQL
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]

        assert "SELECT mp.*" in call_args[0]
        assert "FROM matches m" in call_args[0]
        assert "JOIN match_teams mt ON mt.match_id = m.id" in call_args[0]
        assert "JOIN match_participation mp ON mp.match_team_id = mt.id" in call_args[0]
        assert "JOIN players p ON p.id = mp.player_id" in call_args[0]
        assert "WHERE p.id = ?" in call_args[0]
        assert "ORDER BY m.date_upload DESC" in call_args[0]
        assert "LIMIT ?" in call_args[0]
        assert call_args[1] == (sample_player.id, 20)

    def test_get_player_last_match_participation_custom_number(
        self, match_participation_dao, sample_player, mock_cursor
    ):
        """Test la récupération d'un nombre personnalisé de participations"""
        participations_data = [
            {
                "id": f"part_{i}",
                "match_team_id": f"team_{i}",
                "player_id": sample_player.id,
                "rank_id": f"rank_{i}",
                "car_id": f"car_{i}",
                "car_name": "Fennec",
                "mvp": False,
                "start_time": 0.0,
                "end_time": 300.0,
            }
            for i in range(5)
        ]
        mock_cursor.fetchall.return_value = participations_data

        result = match_participation_dao.get_player_last_match_participation(
            sample_player, nb_match=5
        )

        assert result is not None
        assert len(result) == 5

        call_args = mock_cursor.execute.call_args[0]
        assert call_args[1] == (sample_player.id, 5)

    def test_get_player_last_match_participation_no_participations(
        self, match_participation_dao, sample_player, mock_cursor
    ):
        """Test quand un joueur n'a aucune participation"""
        mock_cursor.fetchall.return_value = []

        result = match_participation_dao.get_player_last_match_participation(
            sample_player
        )

        assert result is None

    def test_get_player_last_match_participation_verifies_order(
        self, match_participation_dao, sample_player, mock_cursor
    ):
        """Test que les participations sont bien triées par date décroissante"""
        participations_data = [
            {
                "id": "part_recent",
                "match_team_id": "team_123",
                "player_id": sample_player.id,
                "rank_id": "rank_1",
                "car_id": "car_1",
                "car_name": "Octane",
                "mvp": True,
                "start_time": 0.0,
                "end_time": 300.0,
            }
        ]
        mock_cursor.fetchall.return_value = participations_data

        result = match_participation_dao.get_player_last_match_participation(
            sample_player
        )

        assert result is not None

        call_args = mock_cursor.execute.call_args[0]
        assert "ORDER BY m.date_upload DESC" in call_args[0]


class TestGetPlayerMatchMVP:
    """Tests pour la récupération des participations MVP d'un joueur"""

    def test_get_player_match_mvp_with_mvps(
        self, match_participation_dao, sample_player, mock_cursor
    ):
        """Test la récupération des participations MVP d'un joueur qui a des MVPs"""
        mvp_data = [
            {
                "id": f"mvp_{i}",
                "match_team_id": f"team_{i}",
                "player_id": sample_player.id,
                "rank_id": f"rank_{i}",
                "car_id": f"car_{i}",
                "car_name": "Octane",
                "mvp": True,
                "start_time": 0.0,
                "end_time": 300.0,
            }
            for i in range(5)
        ]
        mock_cursor.fetchall.return_value = mvp_data

        result = match_participation_dao.get_player_match_mvp(sample_player)

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 5
        for participation in result:
            assert isinstance(participation, MatchParticipation)
            assert participation.mvp is True

        # Vérifie la requête SQL
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "SELECT mp.*" in call_args[0]
        assert "FROM match_participation mp" in call_args[0]
        assert "WHERE mp.player_id = ? and mvp = TRUE" in call_args[0]
        assert call_args[1] == (sample_player.id,)

    def test_get_player_match_mvp_no_mvps(
        self, match_participation_dao, sample_player, mock_cursor
    ):
        """Test quand un joueur n'a aucun MVP"""
        mock_cursor.fetchall.return_value = []

        result = match_participation_dao.get_player_match_mvp(sample_player)

        assert result is None


class TestGetPlayerNbMVP:
    """Tests pour le comptage des MVPs d'un joueur"""

    def test_get_player_nb_mvp_with_mvps(
        self, match_participation_dao, sample_player, mock_cursor
    ):
        """Test le comptage des MVPs d'un joueur qui a des MVPs"""
        mock_cursor.fetchone.return_value = (15,)

        result = match_participation_dao.get_player_nb_mvp(sample_player)

        assert result == (15,)

        # Vérifie la requête SQL
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "SELECT COUNT(id)" in call_args[0]
        assert "FROM match_participation" in call_args[0]
        assert "WHERE player_id = ? and mvp = TRUE" in call_args[0]
        assert call_args[1] == (sample_player.id,)

    def test_get_player_nb_mvp_no_mvps(
        self, match_participation_dao, sample_player, mock_cursor
    ):
        """Test le comptage quand un joueur n'a aucun MVP"""
        mock_cursor.fetchone.return_value = None

        result = match_participation_dao.get_player_nb_mvp(sample_player)

        assert result == 0

    def test_get_player_nb_mvp_zero_count(
        self, match_participation_dao, sample_player, mock_cursor
    ):
        """Test le comptage quand un joueur a 0 MVP"""
        mock_cursor.fetchone.return_value = (0,)

        result = match_participation_dao.get_player_nb_mvp(sample_player)

        assert result == (0,)


class TestUpdate:
    """Tests pour la méthode update"""

    def test_update_not_implemented(self, match_participation_dao):
        """Test que update_match_participation ne fait rien (pass)"""
        result = match_participation_dao.update_match_participation()
        assert result is None


class TestMatchParticipationDAOSingleton:
    """Tests pour vérifier le pattern Singleton"""

    def test_singleton_pattern(self):
        """Test que MatchParticipationDAO est bien un singleton"""
        with patch("src.dao.match_participation_dao.DBConnection"):
            instance1 = MatchParticipationDAO()
            instance2 = MatchParticipationDAO()

            assert instance1 is instance2


class TestMatchParticipationDAOEdgeCases:
    """Tests pour les cas limites"""

    def test_create_match_participation_with_different_cars(
        self, match_participation_dao, mock_cursor
    ):
        """Test la création de participations avec différentes voitures"""
        cars = ["Octane", "Fennec", "Dominus", "Batmobile"]

        for car in enumerate(cars):
            mock_cursor.reset_mock()
            mock_cursor.fetchone.return_value = None

            participation = Mock(spec=MatchParticipation)
            participation.id = str(uuid4())
            participation.match_team_id = str(uuid4())
            participation.player_id = str(uuid4())
            participation.rank_id = str(uuid4())
            participation.car_id = str(uuid4())
            participation.car_name = car
            participation.mvp = False
            participation.start_time = 0.0
            participation.end_time = 300.0

            result = match_participation_dao.create_match_participation(participation)

            assert result is True
            second_call = mock_cursor.execute.call_args_list[1]
            assert second_call[0][1][5] == car

    def test_get_matches_by_parameter_empty_result(
        self, match_participation_dao, mock_cursor
    ):
        """Test avec un résultat vide"""
        mock_cursor.fetchall.return_value = []

        result = match_participation_dao.get_matches_by_parameter("car_name", "Unknown")

        assert result is None

    def test_delete_match_participation_twice(
        self, match_participation_dao, sample_match_participation, mock_cursor
    ):
        """Test la suppression d'une participation deux fois"""
        # Première suppression
        match_participation_dao.delete_match_participation(sample_match_participation)
        assert mock_cursor.execute.call_count == 1

        # Deuxième suppression
        match_participation_dao.delete_match_participation(sample_match_participation)
        assert mock_cursor.execute.call_count == 2


class TestMatchParticipationDAOIntegration:
    """Tests d'intégration simulant des scénarios réels"""

    def test_create_and_retrieve_match_participation(
        self, match_participation_dao, sample_match_participation, mock_cursor
    ):
        """Test la création puis la récupération d'une participation"""
        # Création
        mock_cursor.fetchone.return_value = None
        create_result = match_participation_dao.create_match_participation(
            sample_match_participation
        )
        assert create_result is True

        # Récupération
        mock_cursor.reset_mock()
        mock_cursor.fetchall.return_value = [
            {
                "id": sample_match_participation.id,
                "match_team_id": sample_match_participation.match_team_id,
                "player_id": sample_match_participation.player_id,
                "rank_id": sample_match_participation.rank_id,
                "car_id": sample_match_participation.car_id,
                "car_name": sample_match_participation.car_name,
                "mvp": sample_match_participation.mvp,
                "start_time": sample_match_participation.start_time,
                "end_time": sample_match_participation.end_time,
            }
        ]

        retrieved_participations = match_participation_dao.get_matches_by_parameter(
            "id", sample_match_participation.id
        )
        assert retrieved_participations is not None
        assert len(retrieved_participations) == 1
        assert isinstance(retrieved_participations[0], MatchParticipation)

    def test_get_all_participations_from_team(
        self, match_participation_dao, mock_cursor
    ):
        """Test la récupération de toutes les participations d'une équipe"""
        team_id = str(uuid4())
        participations_data = [
            {
                "id": f"part_{i}",
                "match_team_id": team_id,
                "player_id": f"player_{i}",
                "rank_id": f"rank_{i}",
                "car_id": f"car_{i}",
                "car_name": "Octane" if i % 2 == 0 else "Fennec",
                "mvp": i == 0,
                "start_time": 0.0,
                "end_time": 300.0,
            }
            for i in range(3)
        ]
        mock_cursor.fetchall.return_value = participations_data

        result = match_participation_dao.get_matches_by_parameter(
            "match_team_id", team_id
        )

        assert result is not None
        assert len(result) == 3
        # Vérifie qu'une seule participation a le MVP
        mvp_count = sum(1 for p in result if p.mvp)
        assert mvp_count == 1

    def test_player_with_multiple_mvps_workflow(
        self, match_participation_dao, sample_player, mock_cursor
    ):
        """Test un workflow complet avec un joueur ayant plusieurs MVPs"""
        # Récupère les MVPs
        mvp_data = [
            {
                "id": f"mvp_{i}",
                "match_team_id": f"team_{i}",
                "player_id": sample_player.id,
                "rank_id": f"rank_{i}",
                "car_id": f"car_{i}",
                "car_name": "Octane",
                "mvp": True,
                "start_time": 0.0,
                "end_time": 300.0,
            }
            for i in range(7)
        ]
        mock_cursor.fetchall.return_value = mvp_data

        mvp_participations = match_participation_dao.get_player_match_mvp(sample_player)
        assert mvp_participations is not None
        assert len(mvp_participations) == 7

        # Compte les MVPs
        mock_cursor.reset_mock()
        mock_cursor.fetchone.return_value = (7,)

        mvp_count = match_participation_dao.get_player_nb_mvp(sample_player)
        assert mvp_count == (7,)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
