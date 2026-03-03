from unittest.mock import MagicMock, patch

import pytest

from src.dao.stats_positioning_dao import StatPositioningDAO
from src.dto.stats_positioning_dto import StatsPositioningAggregatedDTO
from src.models.matches import Match
from src.models.players import Player
from src.models.ranks import Ranks
from src.models.stats_positioning import StatsPositioning


# ──────────────────────────────────────────────
# Reset Singleton
# ──────────────────────────────────────────────


@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset le singleton StatPositioningDAO avant chaque test"""
    StatPositioningDAO._instances = {}
    yield
    StatPositioningDAO._instances = {}


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
def positioning_dao(mock_connection):
    with patch("src.dao.stats_positioning_dao.DBConnection") as mock_db_conn:
        mock_db_instance = MagicMock()
        mock_db_instance.connection = mock_connection
        mock_db_conn.return_value = mock_db_instance
        dao = StatPositioningDAO()
        yield dao


@pytest.fixture
def sample_rank():
    rank = MagicMock(spec=Ranks)
    rank.name = "Platinum"
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
def positioning_row():
    """Ligne de résultat SQL simulée pour un match individuel"""
    return {
        "participation_id": 42,
        "average_distance_to_ball": 2800,
        "average_distance_to_ball_possession": 2500,
        "average_distance_to_ball_no_possession": 3100,
        "average_distance_to_mates": 1800,
        "time_defensive_third": 90.5,
        "time_neutral_third": 75.3,
        "time_offensive_third": 60.2,
        "time_defensive_half": 145.8,
        "time_offensive_half": 80.2,
        "time_behind_ball": 130.4,
        "time_infront_ball": 95.6,
        "time_most_back": 45.2,
        "time_most_forward": 38.7,
        "goals_against_while_last_defender": 1,
        "time_closest_to_ball": 55.3,
        "time_farthest_to_ball": 40.1,
        "percent_defensive_third": 35.8,
        "percent_neutral_third": 29.7,
        "percent_offensive_third": 23.8,
        "percent_defensive_half": 57.6,
        "percent_offensive_half": 31.7,
        "percent_behind_ball": 51.5,
        "percent_infront_ball": 37.8,
        "percent_most_back": 17.9,
        "percent_most_forward": 15.3,
        "percent_closest_to_ball": 21.8,
        "percent_farthest_from_ball": 15.9,
    }


@pytest.fixture
def aggregated_row():
    """Ligne de résultat SQL simulée pour les statistiques agrégées"""
    return {
        "avg_average_distance_to_ball": 2750.5,
        "avg_average_distance_to_ball_possession": 2450.3,
        "avg_average_distance_to_ball_no_possession": 3050.7,
        "avg_average_distance_to_mates": 1750.2,
        "avg_time_defensive_third": 88.3,
        "avg_time_neutral_third": 73.1,
        "avg_time_offensive_third": 58.6,
        "avg_time_defensive_half": 142.4,
        "avg_time_offensive_half": 78.6,
        "avg_time_behind_ball": 127.9,
        "avg_time_infront_ball": 93.1,
        "avg_time_most_back": 43.8,
        "avg_time_most_forward": 37.2,
        "avg_goals_against_while_last_defender": 0.8,
        "avg_time_closest_to_ball": 53.7,
        "avg_time_farthest_to_ball": 38.9,
        "avg_percent_defensive_third": 34.9,
        "avg_percent_neutral_third": 28.8,
        "avg_percent_offensive_third": 22.7,
        "avg_percent_defensive_half": 56.3,
        "avg_percent_offensive_half": 30.9,
        "avg_percent_behind_ball": 50.4,
        "avg_percent_infront_ball": 36.9,
        "avg_percent_most_back": 17.2,
        "avg_percent_most_forward": 14.7,
        "avg_percent_closest_to_ball": 21.2,
        "avg_percent_farthest_from_ball": 15.3,
    }


# ──────────────────────────────────────────────
# get_average_stats_positioning_per_rank
# ──────────────────────────────────────────────


class TestGetAverageStatsPositioningPerRank:
    def test_retourne_dto_quand_donnees_trouvees(
        self, positioning_dao, mock_cursor, sample_rank, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        result = positioning_dao.get_average_stats_positioning_per_rank(sample_rank)

        assert result is not None
        assert isinstance(result, StatsPositioningAggregatedDTO)
        assert (
            result.average_distance_to_ball
            == aggregated_row["avg_average_distance_to_ball"]
        )
        assert (
            result.percent_defensive_third
            == aggregated_row["avg_percent_defensive_third"]
        )

    def test_retourne_none_quand_aucune_donnee(
        self, positioning_dao, mock_cursor, sample_rank
    ):
        mock_cursor.fetchone.return_value = None

        result = positioning_dao.get_average_stats_positioning_per_rank(sample_rank)

        assert result is None

    def test_retourne_none_quand_champ_principal_null(
        self, positioning_dao, mock_cursor, sample_rank, aggregated_row
    ):
        aggregated_row["avg_average_distance_to_ball"] = None
        mock_cursor.fetchone.return_value = aggregated_row

        result = positioning_dao.get_average_stats_positioning_per_rank(sample_rank)

        assert result is None

    def test_requete_contient_rank_name(
        self, positioning_dao, mock_cursor, sample_rank, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        positioning_dao.get_average_stats_positioning_per_rank(sample_rank)

        mock_cursor.execute.assert_called_once()
        params = mock_cursor.execute.call_args[0][1]
        assert sample_rank.name in params

    def test_transmet_game_mode_dans_params(
        self, positioning_dao, mock_cursor, sample_rank, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        positioning_dao.get_average_stats_positioning_per_rank(
            sample_rank, game_mode="ranked-standard"
        )

        params = mock_cursor.execute.call_args[0][1]
        assert "ranked-standard" in params

    def test_sans_game_mode_params_contient_seulement_rank(
        self, positioning_dao, mock_cursor, sample_rank, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        positioning_dao.get_average_stats_positioning_per_rank(
            sample_rank, game_mode=None
        )

        params = mock_cursor.execute.call_args[0][1]
        assert params == (sample_rank.name,)


# ──────────────────────────────────────────────
# get_player_match_stats_positioning
# ──────────────────────────────────────────────


class TestGetPlayerMatchStatsPositioning:
    def test_retourne_bo_quand_donnees_trouvees(
        self, positioning_dao, mock_cursor, sample_player, sample_match, positioning_row
    ):
        mock_cursor.fetchone.return_value = positioning_row

        result = positioning_dao.get_player_match_stats_positioning(
            sample_player, sample_match
        )

        assert result is not None
        assert isinstance(result, StatsPositioning)
        assert result.participation_id == positioning_row["participation_id"]
        assert (
            result.average_distance_to_ball
            == positioning_row["average_distance_to_ball"]
        )

    def test_retourne_none_quand_aucune_donnee(
        self, positioning_dao, mock_cursor, sample_player, sample_match
    ):
        mock_cursor.fetchone.return_value = None

        result = positioning_dao.get_player_match_stats_positioning(
            sample_player, sample_match
        )

        assert result is None

    def test_requete_contient_match_id_et_player_id(
        self, positioning_dao, mock_cursor, sample_player, sample_match, positioning_row
    ):
        mock_cursor.fetchone.return_value = positioning_row

        positioning_dao.get_player_match_stats_positioning(sample_player, sample_match)

        params = mock_cursor.execute.call_args[0][1]
        assert sample_match.id in params
        assert sample_player.id in params

    def test_transmet_game_mode_dans_params(
        self, positioning_dao, mock_cursor, sample_player, sample_match, positioning_row
    ):
        mock_cursor.fetchone.return_value = positioning_row

        positioning_dao.get_player_match_stats_positioning(
            sample_player, sample_match, game_mode="ranked-doubles"
        )

        params = mock_cursor.execute.call_args[0][1]
        assert "ranked-doubles" in params

    def test_sans_game_mode_params_contient_match_et_player(
        self, positioning_dao, mock_cursor, sample_player, sample_match, positioning_row
    ):
        mock_cursor.fetchone.return_value = positioning_row

        positioning_dao.get_player_match_stats_positioning(
            sample_player, sample_match, game_mode=None
        )

        params = mock_cursor.execute.call_args[0][1]
        assert params == (sample_match.id, sample_player.id)


# ──────────────────────────────────────────────
# get_player_average_stats_positioning
# ──────────────────────────────────────────────


class TestGetPlayerAverageStatsPositioning:
    def test_retourne_dto_quand_donnees_trouvees(
        self, positioning_dao, mock_cursor, sample_player, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        result = positioning_dao.get_player_average_stats_positioning(sample_player)

        assert result is not None
        assert isinstance(result, StatsPositioningAggregatedDTO)
        assert (
            result.average_distance_to_ball
            == aggregated_row["avg_average_distance_to_ball"]
        )
        assert (
            result.percent_farthest_from_ball
            == aggregated_row["avg_percent_farthest_from_ball"]
        )

    def test_retourne_none_quand_aucune_donnee(
        self, positioning_dao, mock_cursor, sample_player
    ):
        mock_cursor.fetchone.return_value = None

        result = positioning_dao.get_player_average_stats_positioning(sample_player)

        assert result is None

    def test_retourne_none_quand_champ_principal_null(
        self, positioning_dao, mock_cursor, sample_player, aggregated_row
    ):
        aggregated_row["avg_average_distance_to_ball"] = None
        mock_cursor.fetchone.return_value = aggregated_row

        result = positioning_dao.get_player_average_stats_positioning(sample_player)

        assert result is None

    def test_requete_contient_player_id(
        self, positioning_dao, mock_cursor, sample_player, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        positioning_dao.get_player_average_stats_positioning(sample_player)

        params = mock_cursor.execute.call_args[0][1]
        assert sample_player.id in params

    def test_transmet_game_mode_dans_params(
        self, positioning_dao, mock_cursor, sample_player, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        positioning_dao.get_player_average_stats_positioning(
            sample_player, game_mode="ranked-solo"
        )

        params = mock_cursor.execute.call_args[0][1]
        assert "ranked-solo" in params

    def test_sans_game_mode_params_contient_seulement_player(
        self, positioning_dao, mock_cursor, sample_player, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        positioning_dao.get_player_average_stats_positioning(
            sample_player, game_mode=None
        )

        params = mock_cursor.execute.call_args[0][1]
        assert params == (sample_player.id,)


# ──────────────────────────────────────────────
# Singleton
# ──────────────────────────────────────────────


class TestStatPositioningDAOSingleton:
    def test_singleton_pattern(self):
        with patch("src.dao.stats_positioning_dao.DBConnection"):
            instance1 = StatPositioningDAO()
            instance2 = StatPositioningDAO()
            assert instance1 is instance2
