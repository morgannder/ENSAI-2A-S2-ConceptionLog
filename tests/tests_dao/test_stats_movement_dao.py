from unittest.mock import MagicMock, patch

import pytest

from src.dao.stats_movement_dao import StatMovementDAO
from src.dto.stats_movement_dto import StatsMovementAggregatedDTO
from src.models.matches import Match
from src.models.players import Player
from src.models.ranks import Ranks
from src.models.stats_movement import StatsMovement


# ──────────────────────────────────────────────
# Reset Singleton
# ──────────────────────────────────────────────


@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset le singleton StatMovementDAO avant chaque test"""
    StatMovementDAO._instances = {}
    yield
    StatMovementDAO._instances = {}


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
def movement_dao(mock_connection):
    with patch("src.dao.stats_movement_dao.DBConnection") as mock_db_conn:
        mock_db_instance = MagicMock()
        mock_db_instance.connection = mock_connection
        mock_db_conn.return_value = mock_db_instance
        dao = StatMovementDAO()
        yield dao


@pytest.fixture
def sample_rank():
    rank = MagicMock(spec=Ranks)
    rank.name = "Champion"
    return rank


@pytest.fixture
def sample_player():
    player = MagicMock(spec=Player)
    player.id = "player-123"
    return player


@pytest.fixture
def sample_match():
    match = MagicMock(spec=Match)
    match.id = "match-abc"
    return match


@pytest.fixture
def movement_row():
    """Ligne de résultat SQL simulée pour un match individuel"""
    return {
        "participation_id": 42,
        "avg_speed": 1450.5,
        "total_distance": 85000.0,
        "time_supersonic_speed": 45.3,
        "time_boost_speed": 120.7,
        "time_slow_speed": 80.2,
        "time_ground": 200.5,
        "time_low_air": 40.3,
        "time_high_air": 15.1,
        "time_powerslide": 12.4,
        "count_powerslide": 25,
        "avg_powerslide_duration": 0.5,
        "avg_speed_percentage": 62.3,
        "percent_slow_speed": 31.5,
        "percent_boost_speed": 47.2,
        "percent_supersonic_speed": 17.8,
        "percent_ground": 78.6,
        "percent_low_air": 15.8,
        "percent_high_air": 5.9,
    }


@pytest.fixture
def aggregated_row():
    """Ligne de résultat SQL simulée pour les statistiques agrégées"""
    return {
        "avg_avg_speed": 1420.3,
        "avg_total_distance": 82000.0,
        "avg_time_supersonic_speed": 42.1,
        "avg_time_boost_speed": 115.4,
        "avg_time_slow_speed": 78.9,
        "avg_time_ground": 195.2,
        "avg_time_low_air": 38.7,
        "avg_time_high_air": 14.3,
        "avg_time_powerslide": 11.8,
        "avg_count_powerslide": 23.5,
        "avg_average_powerslide_duration": 0.48,
        "avg_average_speed_percentage": 60.1,
        "avg_percent_slow_speed": 30.2,
        "avg_percent_boost_speed": 45.8,
        "avg_percent_supersonic_speed": 16.5,
        "avg_percent_ground": 76.9,
        "avg_percent_low_air": 16.4,
        "avg_percent_high_air": 6.1,
    }


# ──────────────────────────────────────────────
# get_average_stats_movement_per_rank
# ──────────────────────────────────────────────


class TestGetAverageStatsMovementPerRank:
    def test_retourne_dto_quand_donnees_trouvees(
        self, movement_dao, mock_cursor, sample_rank, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        result = movement_dao.get_average_stats_movement_per_rank(sample_rank)

        assert result is not None
        assert isinstance(result, StatsMovementAggregatedDTO)
        assert result.avg_speed == aggregated_row["avg_avg_speed"]
        assert result.total_distance == aggregated_row["avg_total_distance"]

    def test_retourne_none_quand_aucune_donnee(
        self, movement_dao, mock_cursor, sample_rank
    ):
        mock_cursor.fetchone.return_value = None

        result = movement_dao.get_average_stats_movement_per_rank(sample_rank)

        assert result is None

    def test_retourne_none_quand_champ_principal_null(
        self, movement_dao, mock_cursor, sample_rank, aggregated_row
    ):
        aggregated_row["avg_avg_speed"] = None
        mock_cursor.fetchone.return_value = aggregated_row

        result = movement_dao.get_average_stats_movement_per_rank(sample_rank)

        assert result is None

    def test_requete_contient_rank_name(
        self, movement_dao, mock_cursor, sample_rank, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        movement_dao.get_average_stats_movement_per_rank(sample_rank)

        mock_cursor.execute.assert_called_once()
        params = mock_cursor.execute.call_args[0][1]
        assert sample_rank.name in params

    def test_transmet_game_mode_dans_params(
        self, movement_dao, mock_cursor, sample_rank, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        movement_dao.get_average_stats_movement_per_rank(
            sample_rank, game_mode="ranked-standard"
        )

        params = mock_cursor.execute.call_args[0][1]
        assert "ranked-standard" in params

    def test_sans_game_mode_params_contient_seulement_rank(
        self, movement_dao, mock_cursor, sample_rank, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        movement_dao.get_average_stats_movement_per_rank(sample_rank, game_mode=None)

        params = mock_cursor.execute.call_args[0][1]
        assert params == (sample_rank.name,)


# ──────────────────────────────────────────────
# get_player_match_stats_movement
# ──────────────────────────────────────────────


class TestGetPlayerMatchStatsMovement:
    def test_retourne_bo_quand_donnees_trouvees(
        self, movement_dao, mock_cursor, sample_player, sample_match, movement_row
    ):
        mock_cursor.fetchone.return_value = movement_row

        result = movement_dao.get_player_match_stats_movement(
            sample_player, sample_match
        )

        assert result is not None
        assert isinstance(result, StatsMovement)
        assert result.participation_id == movement_row["participation_id"]
        assert result.avg_speed == movement_row["avg_speed"]
        assert result.total_distance == movement_row["total_distance"]

    def test_retourne_none_quand_aucune_donnee(
        self, movement_dao, mock_cursor, sample_player, sample_match
    ):
        mock_cursor.fetchone.return_value = None

        result = movement_dao.get_player_match_stats_movement(
            sample_player, sample_match
        )

        assert result is None

    def test_requete_contient_match_id_et_player_id(
        self, movement_dao, mock_cursor, sample_player, sample_match, movement_row
    ):
        mock_cursor.fetchone.return_value = movement_row

        movement_dao.get_player_match_stats_movement(sample_player, sample_match)

        params = mock_cursor.execute.call_args[0][1]
        assert sample_match.id in params
        assert sample_player.id in params

    def test_transmet_game_mode_dans_params(
        self, movement_dao, mock_cursor, sample_player, sample_match, movement_row
    ):
        mock_cursor.fetchone.return_value = movement_row

        movement_dao.get_player_match_stats_movement(
            sample_player, sample_match, game_mode="ranked-doubles"
        )

        params = mock_cursor.execute.call_args[0][1]
        assert "ranked-doubles" in params

    def test_sans_game_mode_params_contient_match_et_player(
        self, movement_dao, mock_cursor, sample_player, sample_match, movement_row
    ):
        mock_cursor.fetchone.return_value = movement_row

        movement_dao.get_player_match_stats_movement(
            sample_player, sample_match, game_mode=None
        )

        params = mock_cursor.execute.call_args[0][1]
        assert params == (sample_match.id, sample_player.id)


# ──────────────────────────────────────────────
# get_player_average_stats_movement
# ──────────────────────────────────────────────


class TestGetPlayerAverageStatsMovement:
    def test_retourne_dto_quand_donnees_trouvees(
        self, movement_dao, mock_cursor, sample_player, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        result = movement_dao.get_player_average_stats_movement(sample_player)

        assert result is not None
        assert isinstance(result, StatsMovementAggregatedDTO)
        assert result.avg_speed == aggregated_row["avg_avg_speed"]
        assert (
            result.percent_supersonic_speed
            == aggregated_row["avg_percent_supersonic_speed"]
        )

    def test_retourne_none_quand_aucune_donnee(
        self, movement_dao, mock_cursor, sample_player
    ):
        mock_cursor.fetchone.return_value = None

        result = movement_dao.get_player_average_stats_movement(sample_player)

        assert result is None

    def test_retourne_none_quand_champ_principal_null(
        self, movement_dao, mock_cursor, sample_player, aggregated_row
    ):
        aggregated_row["avg_avg_speed"] = None
        mock_cursor.fetchone.return_value = aggregated_row

        result = movement_dao.get_player_average_stats_movement(sample_player)

        assert result is None

    def test_requete_contient_player_id(
        self, movement_dao, mock_cursor, sample_player, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        movement_dao.get_player_average_stats_movement(sample_player)

        params = mock_cursor.execute.call_args[0][1]
        assert sample_player.id in params

    def test_transmet_game_mode_dans_params(
        self, movement_dao, mock_cursor, sample_player, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        movement_dao.get_player_average_stats_movement(
            sample_player, game_mode="ranked-solo"
        )

        params = mock_cursor.execute.call_args[0][1]
        assert "ranked-solo" in params

    def test_sans_game_mode_params_contient_seulement_player(
        self, movement_dao, mock_cursor, sample_player, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        movement_dao.get_player_average_stats_movement(sample_player, game_mode=None)

        params = mock_cursor.execute.call_args[0][1]
        assert params == (sample_player.id,)


# ──────────────────────────────────────────────
# Singleton
# ──────────────────────────────────────────────


class TestStatMovementDAOSingleton:
    def test_singleton_pattern(self):
        with patch("src.dao.stats_movement_dao.DBConnection"):
            instance1 = StatMovementDAO()
            instance2 = StatMovementDAO()
            assert instance1 is instance2
