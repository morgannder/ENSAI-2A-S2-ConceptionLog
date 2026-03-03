from unittest.mock import MagicMock, patch

import pytest

from src.dto.stats_movement_dto import StatsMovementAggregatedDTO
from src.models.matches import Match
from src.models.players import Player
from src.models.ranks import Ranks
from src.models.stats_movement import StatsMovement
from src.service.stats_movement_service import StatMovementService


# ──────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────


@pytest.fixture
def service():
    with patch("src.service.stats_movement_service.StatMovementDAO") as mockdao:
        svc = StatMovementService()
        svc.stats_movement_dao = mockdao.return_value
        yield svc


@pytest.fixture
def valid_player():
    player = MagicMock(spec=Player)
    player.id = "player-123"
    return player


@pytest.fixture
def valid_match():
    match = MagicMock(spec=Match)
    match.id = "match-abc"
    return match


@pytest.fixture
def valid_rank():
    rank = MagicMock(spec=Ranks)
    rank.name = "Champion"
    return rank


@pytest.fixture
def aggregated_dto():
    return MagicMock(spec=StatsMovementAggregatedDTO)


@pytest.fixture
def movement_bo():
    return MagicMock(spec=StatsMovement)


# ──────────────────────────────────────────────
# get_average_stats_movement_by_rank
# ──────────────────────────────────────────────


class TestGetAverageStatsMovementByRank:
    def test_retourne_dto_quand_donnees_trouvees(
        self, service, valid_rank, aggregated_dto
    ):
        service.stats_movement_dao.get_average_stats_movement_per_rank.return_value = (
            aggregated_dto
        )

        result = service.get_average_stats_movement_by_rank(valid_rank)

        assert result == aggregated_dto
        service.stats_movement_dao.get_average_stats_movement_per_rank.assert_called_once_with(
            valid_rank, None
        )

    def test_retourne_none_quand_aucune_donnee(self, service, valid_rank):
        service.stats_movement_dao.get_average_stats_movement_per_rank.return_value = (
            None
        )

        result = service.get_average_stats_movement_by_rank(valid_rank)

        assert result is None

    def test_transmet_game_mode(self, service, valid_rank, aggregated_dto):
        service.stats_movement_dao.get_average_stats_movement_per_rank.return_value = (
            aggregated_dto
        )

        service.get_average_stats_movement_by_rank(
            valid_rank, game_mode="ranked-standard"
        )

        service.stats_movement_dao.get_average_stats_movement_per_rank.assert_called_once_with(
            valid_rank, "ranked-standard"
        )


# ──────────────────────────────────────────────
# get_player_match_movement_stats
# ──────────────────────────────────────────────


class TestGetPlayerMatchMovementStats:
    def test_retourne_bo_quand_donnees_trouvees(
        self, service, valid_player, valid_match, movement_bo
    ):
        service.stats_movement_dao.get_player_match_stats_movement.return_value = (
            movement_bo
        )

        result = service.get_player_match_movement_stats(valid_player, valid_match)

        assert result == movement_bo
        service.stats_movement_dao.get_player_match_stats_movement.assert_called_once_with(
            valid_player, valid_match, None
        )

    def test_retourne_none_quand_aucune_donnee(
        self, service, valid_player, valid_match
    ):
        service.stats_movement_dao.get_player_match_stats_movement.return_value = None

        result = service.get_player_match_movement_stats(valid_player, valid_match)

        assert result is None

    def test_transmet_game_mode(self, service, valid_player, valid_match, movement_bo):
        service.stats_movement_dao.get_player_match_stats_movement.return_value = (
            movement_bo
        )

        service.get_player_match_movement_stats(
            valid_player, valid_match, game_mode="ranked-doubles"
        )

        service.stats_movement_dao.get_player_match_stats_movement.assert_called_once_with(
            valid_player, valid_match, "ranked-doubles"
        )

    def test_leve_valeur_erreur_si_player_none(self, service, valid_match):
        with pytest.raises(ValueError, match="joueur"):
            service.get_player_match_movement_stats(None, valid_match)

    def test_leve_valeur_erreur_si_player_sans_id(self, service, valid_match):
        player_sans_id = MagicMock(spec=Player)
        player_sans_id.id = None

        with pytest.raises(ValueError, match="joueur"):
            service.get_player_match_movement_stats(player_sans_id, valid_match)

    def test_leve_valeur_erreur_si_match_none(self, service, valid_player):
        with pytest.raises(ValueError, match="match"):
            service.get_player_match_movement_stats(valid_player, None)

    def test_leve_valeur_erreur_si_match_sans_id(self, service, valid_player):
        match_sans_id = MagicMock(spec=Match)
        match_sans_id.id = None

        with pytest.raises(ValueError, match="match"):
            service.get_player_match_movement_stats(valid_player, match_sans_id)


# ──────────────────────────────────────────────
# get_player_average_movement_stats
# ──────────────────────────────────────────────


class TestGetPlayerAverageMovementStats:
    def test_retourne_dto_quand_donnees_trouvees(
        self, service, valid_player, aggregated_dto
    ):
        service.stats_movement_dao.get_player_average_stats_movement.return_value = (
            aggregated_dto
        )

        result = service.get_player_average_movement_stats(valid_player)

        assert result == aggregated_dto
        service.stats_movement_dao.get_player_average_stats_movement.assert_called_once_with(
            valid_player, None
        )

    def test_retourne_none_quand_aucune_donnee(self, service, valid_player):
        service.stats_movement_dao.get_player_average_stats_movement.return_value = None

        result = service.get_player_average_movement_stats(valid_player)

        assert result is None

    def test_transmet_game_mode(self, service, valid_player, aggregated_dto):
        service.stats_movement_dao.get_player_average_stats_movement.return_value = (
            aggregated_dto
        )

        service.get_player_average_movement_stats(valid_player, game_mode="ranked-solo")

        service.stats_movement_dao.get_player_average_stats_movement.assert_called_once_with(
            valid_player, "ranked-solo"
        )

    def test_leve_valeur_erreur_si_player_none(self, service):
        with pytest.raises(ValueError, match="joueur"):
            service.get_player_average_movement_stats(None)

    def test_leve_valeur_erreur_si_player_sans_id(self, service):
        player_sans_id = MagicMock(spec=Player)
        player_sans_id.id = None

        with pytest.raises(ValueError, match="joueur"):
            service.get_player_average_movement_stats(player_sans_id)
