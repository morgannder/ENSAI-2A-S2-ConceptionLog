from unittest.mock import MagicMock, patch

import pytest

from src.dao.stats_core_dao import StatsCoreDAO
from src.dto.stats_core_dto import StatsCoreAggregatedDTO
from src.models.matches import Match
from src.models.players import Player
from src.models.ranks import Ranks
from src.models.stats_core import StatsCore


# ──────────────────────────────────────────────
# Reset Singleton
# ──────────────────────────────────────────────


@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset le singleton StatsCoreDAO avant chaque test"""
    StatsCoreDAO._instances = {}
    yield
    StatsCoreDAO._instances = {}


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
def core_dao(mock_connection):
    with patch("src.dao.stats_core_dao.DBConnection") as mock_db_conn:
        mock_db_instance = MagicMock()
        mock_db_instance.connection = mock_connection
        mock_db_conn.return_value = mock_db_instance
        dao = StatsCoreDAO()
        yield dao


@pytest.fixture
def sample_rank():
    rank = MagicMock(spec=Ranks)
    rank.name = "Diamond"
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
def core_row():
    """Ligne de résultat SQL simulée pour un match individuel"""
    return {
        "participation_id": 42,
        "shots": 5,
        "goals": 2,
        "saves": 3,
        "assists": 1,
        "score": 450,
        "shooting_percentage": 40.0,
        "demo_inflicted": 1,
        "demo_taken": 0,
    }


@pytest.fixture
def aggregated_row():
    """Ligne de résultat SQL simulée pour les statistiques agrégées"""
    return {
        "avg_shots": 4.5,
        "avg_goals": 1.8,
        "avg_saves": 2.3,
        "avg_assists": 0.9,
        "avg_score": 380.0,
        "avg_shooting_percentage": 38.5,
        "avg_demo_inflicted": 0.7,
        "avg_demo_taken": 0.5,
    }


# ──────────────────────────────────────────────
# get_average_stats_core_per_rank
# ──────────────────────────────────────────────


class TestGetAverageStatsCorePerRank:
    def test_retourne_dto_quand_donnees_trouvees(
        self, core_dao, mock_cursor, sample_rank, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        result = core_dao.get_average_stats_core_per_rank(sample_rank)

        assert result is not None
        assert isinstance(result, StatsCoreAggregatedDTO)
        assert result.goals == aggregated_row["avg_goals"]
        assert result.shots == aggregated_row["avg_shots"]
        assert result.score == aggregated_row["avg_score"]

    def test_retourne_none_quand_aucune_donnee(
        self, core_dao, mock_cursor, sample_rank
    ):
        mock_cursor.fetchone.return_value = None

        result = core_dao.get_average_stats_core_per_rank(sample_rank)

        assert result is None

    def test_retourne_none_quand_champ_principal_null(
        self, core_dao, mock_cursor, sample_rank, aggregated_row
    ):
        aggregated_row["avg_goals"] = None
        mock_cursor.fetchone.return_value = aggregated_row

        result = core_dao.get_average_stats_core_per_rank(sample_rank)

        assert result is None

    def test_requete_contient_rank_name(
        self, core_dao, mock_cursor, sample_rank, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        core_dao.get_average_stats_core_per_rank(sample_rank)

        mock_cursor.execute.assert_called_once()
        params = mock_cursor.execute.call_args[0][1]
        assert sample_rank.name in params

    def test_transmet_game_mode_dans_params(
        self, core_dao, mock_cursor, sample_rank, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        core_dao.get_average_stats_core_per_rank(
            sample_rank, game_mode="ranked-standard"
        )

        params = mock_cursor.execute.call_args[0][1]
        assert "ranked-standard" in params

    def test_sans_game_mode_params_contient_seulement_rank(
        self, core_dao, mock_cursor, sample_rank, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        core_dao.get_average_stats_core_per_rank(sample_rank, game_mode=None)

        params = mock_cursor.execute.call_args[0][1]
        assert params == (sample_rank.name,)


# ──────────────────────────────────────────────
# get_player_match_stats_core
# ──────────────────────────────────────────────


class TestGetPlayerMatchStatsCore:
    def test_retourne_bo_quand_donnees_trouvees(
        self, core_dao, mock_cursor, sample_player, sample_match, core_row
    ):
        mock_cursor.fetchone.return_value = core_row

        result = core_dao.get_player_match_stats_core(sample_player, sample_match)

        assert result is not None
        assert isinstance(result, StatsCore)
        assert result.participation_id == core_row["participation_id"]
        assert result.goals == core_row["goals"]
        assert result.shots == core_row["shots"]

    def test_retourne_none_quand_aucune_donnee(
        self, core_dao, mock_cursor, sample_player, sample_match
    ):
        mock_cursor.fetchone.return_value = None

        result = core_dao.get_player_match_stats_core(sample_player, sample_match)

        assert result is None

    def test_requete_contient_match_id_et_player_id(
        self, core_dao, mock_cursor, sample_player, sample_match, core_row
    ):
        mock_cursor.fetchone.return_value = core_row

        core_dao.get_player_match_stats_core(sample_player, sample_match)

        params = mock_cursor.execute.call_args[0][1]
        assert sample_match.id in params
        assert sample_player.id in params

    def test_transmet_game_mode_dans_params(
        self, core_dao, mock_cursor, sample_player, sample_match, core_row
    ):
        mock_cursor.fetchone.return_value = core_row

        core_dao.get_player_match_stats_core(
            sample_player, sample_match, game_mode="ranked-doubles"
        )

        params = mock_cursor.execute.call_args[0][1]
        assert "ranked-doubles" in params

    def test_sans_game_mode_params_contient_match_et_player(
        self, core_dao, mock_cursor, sample_player, sample_match, core_row
    ):
        mock_cursor.fetchone.return_value = core_row

        core_dao.get_player_match_stats_core(
            sample_player, sample_match, game_mode=None
        )

        params = mock_cursor.execute.call_args[0][1]
        assert params == (sample_match.id, sample_player.id)


# ──────────────────────────────────────────────
# get_player_average_stats_core
# ──────────────────────────────────────────────


class TestGetPlayerAverageStatsCore:
    def test_retourne_dto_quand_donnees_trouvees(
        self, core_dao, mock_cursor, sample_player, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        result = core_dao.get_player_average_stats_core(sample_player)

        assert result is not None
        assert isinstance(result, StatsCoreAggregatedDTO)
        assert result.goals == aggregated_row["avg_goals"]
        assert result.shooting_percentage == aggregated_row["avg_shooting_percentage"]

    def test_retourne_none_quand_aucune_donnee(
        self, core_dao, mock_cursor, sample_player
    ):
        mock_cursor.fetchone.return_value = None

        result = core_dao.get_player_average_stats_core(sample_player)

        assert result is None

    def test_retourne_none_quand_champ_principal_null(
        self, core_dao, mock_cursor, sample_player, aggregated_row
    ):
        aggregated_row["avg_goals"] = None
        mock_cursor.fetchone.return_value = aggregated_row

        result = core_dao.get_player_average_stats_core(sample_player)

        assert result is None

    def test_requete_contient_player_id(
        self, core_dao, mock_cursor, sample_player, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        core_dao.get_player_average_stats_core(sample_player)

        params = mock_cursor.execute.call_args[0][1]
        assert sample_player.id in params

    def test_transmet_game_mode_dans_params(
        self, core_dao, mock_cursor, sample_player, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        core_dao.get_player_average_stats_core(sample_player, game_mode="ranked-solo")

        params = mock_cursor.execute.call_args[0][1]
        assert "ranked-solo" in params

    def test_sans_game_mode_params_contient_seulement_player(
        self, core_dao, mock_cursor, sample_player, aggregated_row
    ):
        mock_cursor.fetchone.return_value = aggregated_row

        core_dao.get_player_average_stats_core(sample_player, game_mode=None)

        params = mock_cursor.execute.call_args[0][1]
        assert params == (sample_player.id,)


# ──────────────────────────────────────────────
# Singleton
# ──────────────────────────────────────────────


class TestStatsCoreDAOSingleton:
    def test_singleton_pattern(self):
        with patch("src.dao.stats_core_dao.DBConnection"):
            instance1 = StatsCoreDAO()
            instance2 = StatsCoreDAO()
            assert instance1 is instance2
