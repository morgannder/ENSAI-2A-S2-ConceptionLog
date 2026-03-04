from unittest.mock import MagicMock, patch

import pytest

from src.dao.stats_boost_dao import StatBoostDAO
from src.dto.stats_boost_dto import StatsBoostAggregatedDTO
from src.models.matches import Match
from src.models.players import Player
from src.models.ranks import Ranks
from src.models.stats_boost import StatsBoost


# ──────────────────────────────────────────────
# Reset Singleton
# ──────────────────────────────────────────────


@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset le singleton StatBoostDAO avant chaque test"""
    StatBoostDAO._instances = {}
    yield
    StatBoostDAO._instances = {}


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
def boost_dao(mock_connection):
    with patch("src.dao.stats_boost_dao.DBConnection") as mock_db_conn:
        mock_db_instance = MagicMock()
        mock_db_instance.connection = mock_connection
        mock_db_conn.return_value = mock_db_instance
        dao = StatBoostDAO()
        yield dao


@pytest.fixture
def sample_rank():
    rank = MagicMock(spec=Ranks)
    rank.name = "Gold"
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
def boost_row():
    """Ligne de résultat SQL simulée pour un match individuel"""
    return {
        "participation_id": 42,
        "boost_per_minute": 10.5,
        "boost_consumed_per_minute": 8.2,
        "average_amount": 45.3,
        "amount_collected": 3000,
        "amount_stolen": 200,
        "amount_collected_big": 1500,
        "amount_stolen_big": 100,
        "amount_collected_small": 1500,
        "amount_stolen_small": 100,
        "count_collected_big": 10,
        "count_stolen_big": 2,
        "count_collected_small": 20,
        "count_stolen_small": 3,
        "amount_overfill": 50,
        "amount_overfill_stolen": 10,
        "amount_used_while_supersonic": 300,
        "time_zero_boost": 12.5,
        "percent_zero_boost": 5.2,
        "time_full_boost": 30.0,
        "percent_full_boost": 12.5,
        "time_boost_0_25": 20.0,
        "time_boost_25_50": 30.0,
        "time_boost_50_75": 40.0,
        "time_boost_75_100": 50.0,
        "percent_boost_0_25": 8.0,
        "percent_boost_25_50": 12.0,
        "percent_boost_50_75": 16.0,
        "percent_boost_75_100": 20.0,
    }


@pytest.fixture
def aggregated_row():
    """Ligne de résultat SQL simulée pour les statistiques agrégées"""
    return {
        "avg_boost_per_minute": 10.5,
        "avg_boost_consumed_per_minute": 8.2,
        "avg_average_amount": 45.3,
        "avg_amount_collected": 3000.0,
        "avg_amount_stolen": 200.0,
        "avg_amount_collected_big": 1500.0,
        "avg_amount_stolen_big": 100.0,
        "avg_amount_collected_small": 1500.0,
        "avg_amount_stolen_small": 100.0,
        "avg_count_collected_big": 10.0,
        "avg_count_stolen_big": 2.0,
        "avg_count_collected_small": 20.0,
        "avg_count_stolen_small": 3.0,
        "avg_amount_overfill": 50.0,
        "avg_amount_overfill_stolen": 10.0,
        "avg_amount_used_while_supersonic": 300.0,
        "avg_time_zero_boost": 12.5,
        "avg_percent_zero_boost": 5.2,
        "avg_time_full_boost": 30.0,
        "avg_percent_full_boost": 12.5,
        "avg_time_boost_0_25": 20.0,
        "avg_time_boost_25_50": 30.0,
        "avg_time_boost_50_75": 40.0,
        "avg_time_boost_75_100": 50.0,
        "avg_percent_boost_0_25": 8.0,
        "avg_percent_boost_25_50": 12.0,
        "avg_percent_boost_50_75": 16.0,
        "avg_percent_boost_75_100": 20.0,
    }


# ──────────────────────────────────────────────
# get_average_stats_boost_per_rank
# ──────────────────────────────────────────────


class TestGetAverageStatsBoostPerRank:
    def test_retourne_dto_quand_donnees_trouvees(
        self, boost_dao, mock_cursor, sample_rank, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        result = boost_dao.get_average_stats_boost_per_rank(sample_rank)

        assert result is not None
        assert isinstance(result, StatsBoostAggregatedDTO)
        assert result.boost_per_minute == aggregated_row["avg_boost_per_minute"]
        assert result.average_amount == aggregated_row["avg_average_amount"]

    def test_retourne_none_quand_aucune_donnee(
        self, boost_dao, mock_cursor, sample_rank
    ):
        mock_cursor.fetchone.return_value = None

        result = boost_dao.get_average_stats_boost_per_rank(sample_rank)

        assert result is None

    def test_retourne_none_quand_champ_principal_null(
        self, boost_dao, mock_cursor, sample_rank, aggregated_row
    ):
        aggregated_row["avg_boost_per_minute"] = None
        mock_cursor.fetchone.return_value = aggregated_row

        result = boost_dao.get_average_stats_boost_per_rank(sample_rank)

        assert result is None

    def test_requete_contient_rank_name(
        self, boost_dao, mock_cursor, sample_rank, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        boost_dao.get_average_stats_boost_per_rank(sample_rank)

        mock_cursor.execute.assert_called_once()
        params = mock_cursor.execute.call_args[0][1]
        assert sample_rank.name in params

    def test_transmet_game_mode_dans_params(
        self, boost_dao, mock_cursor, sample_rank, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        boost_dao.get_average_stats_boost_per_rank(
            sample_rank, game_mode="ranked-standard"
        )

        params = mock_cursor.execute.call_args[0][1]
        assert "ranked-standard" in params

    def test_sans_game_mode_params_contient_seulement_rank(
        self, boost_dao, mock_cursor, sample_rank, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        boost_dao.get_average_stats_boost_per_rank(sample_rank, game_mode=None)

        params = mock_cursor.execute.call_args[0][1]
        assert params == (sample_rank.name,)


# ──────────────────────────────────────────────
# get_player_match_stats_boost
# ──────────────────────────────────────────────


class TestGetPlayerMatchStatsBoost:
    def test_retourne_bo_quand_donnees_trouvees(
        self, boost_dao, mock_cursor, sample_player, sample_match, boost_row
    ):
        mock_cursor.fetchone.return_value = boost_row

        result = boost_dao.get_player_match_stats_boost(sample_player, sample_match)

        assert result is not None
        assert isinstance(result, StatsBoost)
        assert result.participation_id == boost_row["participation_id"]
        assert result.boost_per_minute == boost_row["boost_per_minute"]

    def test_retourne_none_quand_aucune_donnee(
        self, boost_dao, mock_cursor, sample_player, sample_match
    ):
        mock_cursor.fetchone.return_value = None

        result = boost_dao.get_player_match_stats_boost(sample_player, sample_match)

        assert result is None

    def test_requete_contient_match_id_et_player_id(
        self, boost_dao, mock_cursor, sample_player, sample_match, boost_row
    ):
        mock_cursor.fetchone.return_value = boost_row

        boost_dao.get_player_match_stats_boost(sample_player, sample_match)

        mock_cursor.execute.assert_called_once()
        params = mock_cursor.execute.call_args[0][1]
        assert sample_match.id in params
        assert sample_player.id in params

    def test_transmet_game_mode_dans_params(
        self, boost_dao, mock_cursor, sample_player, sample_match, boost_row
    ):
        mock_cursor.fetchone.return_value = boost_row

        boost_dao.get_player_match_stats_boost(
            sample_player, sample_match, game_mode="ranked-doubles"
        )

        params = mock_cursor.execute.call_args[0][1]
        assert "ranked-doubles" in params

    def test_sans_game_mode_params_contient_match_et_player(
        self, boost_dao, mock_cursor, sample_player, sample_match, boost_row
    ):
        mock_cursor.fetchone.return_value = boost_row

        boost_dao.get_player_match_stats_boost(
            sample_player, sample_match, game_mode=None
        )

        params = mock_cursor.execute.call_args[0][1]
        assert params == (sample_match.id, sample_player.id)


# ──────────────────────────────────────────────
# get_player_average_stats_boost
# ──────────────────────────────────────────────


class TestGetPlayerAverageStatsBoost:
    def test_retourne_dto_quand_donnees_trouvees(
        self, boost_dao, mock_cursor, sample_player, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        result = boost_dao.get_player_average_stats_boost(sample_player)

        assert result is not None
        assert isinstance(result, StatsBoostAggregatedDTO)
        assert result.boost_per_minute == aggregated_row["avg_boost_per_minute"]
        assert result.percent_full_boost == aggregated_row["avg_percent_full_boost"]

    def test_retourne_none_quand_aucune_donnee(
        self, boost_dao, mock_cursor, sample_player
    ):
        mock_cursor.fetchone.return_value = None

        result = boost_dao.get_player_average_stats_boost(sample_player)

        assert result is None

    def test_retourne_none_quand_champ_principal_null(
        self, boost_dao, mock_cursor, sample_player, aggregated_row
    ):
        aggregated_row["avg_boost_per_minute"] = None
        mock_cursor.fetchone.return_value = aggregated_row

        result = boost_dao.get_player_average_stats_boost(sample_player)

        assert result is None

    def test_requete_contient_player_id(
        self, boost_dao, mock_cursor, sample_player, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        boost_dao.get_player_average_stats_boost(sample_player)

        params = mock_cursor.execute.call_args[0][1]
        assert sample_player.id in params

    def test_transmet_game_mode_dans_params(
        self, boost_dao, mock_cursor, sample_player, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        boost_dao.get_player_average_stats_boost(sample_player, game_mode="ranked-solo")

        params = mock_cursor.execute.call_args[0][1]
        assert "ranked-solo" in params

    def test_sans_game_mode_params_contient_seulement_player(
        self, boost_dao, mock_cursor, sample_player, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        boost_dao.get_player_average_stats_boost(sample_player, game_mode=None)

        params = mock_cursor.execute.call_args[0][1]
        assert params == (sample_player.id,)


# ──────────────────────────────────────────────
# Singleton
# ──────────────────────────────────────────────


class TestStatBoostDAOSingleton:
    def test_singleton_pattern(self):
        with patch("src.dao.stats_boost_dao.DBConnection"):
            instance1 = StatBoostDAO()
            instance2 = StatBoostDAO()
            assert instance1 is instance2
