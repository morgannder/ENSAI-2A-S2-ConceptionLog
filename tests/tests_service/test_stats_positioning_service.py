from unittest.mock import MagicMock, patch

import pytest

from src.dto.stats_positioning_dto import StatsPositioningAggregatedDTO
from src.models.matches import Match
from src.models.players import Player
from src.models.ranks import Ranks
from src.models.stats_positioning import StatsPositioning
from src.service.stats_positioning_service import StatPositionningService


# ──────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────


@pytest.fixture
def service():
    with patch("src.service.stats_positioning_service.StatPositioningDAO") as mockdao:
        svc = StatPositionningService()
        svc.stats_positioning_dao = mockdao.return_value
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
    rank.name = "Platinum"
    return rank


@pytest.fixture
def aggregated_dto():
    return MagicMock(spec=StatsPositioningAggregatedDTO)


@pytest.fixture
def positioning_bo():
    return MagicMock(spec=StatsPositioning)


# ──────────────────────────────────────────────
# get_average_stats_positioning_by_rank
# ──────────────────────────────────────────────


class TestGetAverageStatsPositioningByRank:
    def test_retourne_dto_quand_donnees_trouvees(
        self, service, valid_rank, aggregated_dto
    ):
        service.stats_positioning_dao.get_average_stats_positioning_per_rank.return_value = aggregated_dto

        result = service.get_average_stats_positioning_by_rank(valid_rank)

        assert result == aggregated_dto
        service.stats_positioning_dao.get_average_stats_positioning_per_rank.assert_called_once_with(
            valid_rank, None
        )

    def test_retourne_none_quand_aucune_donnee(self, service, valid_rank):
        service.stats_positioning_dao.get_average_stats_positioning_per_rank.return_value = None

        result = service.get_average_stats_positioning_by_rank(valid_rank)

        assert result is None

    def test_transmet_game_mode(self, service, valid_rank, aggregated_dto):
        service.stats_positioning_dao.get_average_stats_positioning_per_rank.return_value = aggregated_dto

        service.get_average_stats_positioning_by_rank(
            valid_rank, game_mode="ranked-standard"
        )

        service.stats_positioning_dao.get_average_stats_positioning_per_rank.assert_called_once_with(
            valid_rank, "ranked-standard"
        )


# ──────────────────────────────────────────────
# get_player_match_positioning_stats
# ──────────────────────────────────────────────


class TestGetPlayerMatchPositioningStats:
    def test_retourne_bo_quand_donnees_trouvees(
        self, service, valid_player, valid_match, positioning_bo
    ):
        service.stats_positioning_dao.get_player_match_stats_positioning.return_value = positioning_bo

        result = service.get_player_match_positioning_stats(valid_player, valid_match)

        assert result == positioning_bo
        service.stats_positioning_dao.get_player_match_stats_positioning.assert_called_once_with(
            valid_player, valid_match, None
        )

    def test_retourne_none_quand_aucune_donnee(
        self, service, valid_player, valid_match
    ):
        service.stats_positioning_dao.get_player_match_stats_positioning.return_value = None

        result = service.get_player_match_positioning_stats(valid_player, valid_match)

        assert result is None

    def test_transmet_game_mode(
        self, service, valid_player, valid_match, positioning_bo
    ):
        service.stats_positioning_dao.get_player_match_stats_positioning.return_value = positioning_bo

        service.get_player_match_positioning_stats(
            valid_player, valid_match, game_mode="ranked-doubles"
        )

        service.stats_positioning_dao.get_player_match_stats_positioning.assert_called_once_with(
            valid_player, valid_match, "ranked-doubles"
        )

    def test_leve_valeur_erreur_si_player_none(self, service, valid_match):
        with pytest.raises(ValueError, match="joueur"):
            service.get_player_match_positioning_stats(None, valid_match)

    def test_leve_valeur_erreur_si_player_sans_id(self, service, valid_match):
        player_sans_id = MagicMock(spec=Player)
        player_sans_id.id = None

        with pytest.raises(ValueError, match="joueur"):
            service.get_player_match_positioning_stats(player_sans_id, valid_match)

    def test_leve_valeur_erreur_si_match_none(self, service, valid_player):
        with pytest.raises(ValueError, match="match"):
            service.get_player_match_positioning_stats(valid_player, None)

    def test_leve_valeur_erreur_si_match_sans_id(self, service, valid_player):
        match_sans_id = MagicMock(spec=Match)
        match_sans_id.id = None

        with pytest.raises(ValueError, match="match"):
            service.get_player_match_positioning_stats(valid_player, match_sans_id)


# ──────────────────────────────────────────────
# get_player_average_positioning_stats
# ──────────────────────────────────────────────


class TestGetPlayerAveragePositioningStats:
    def test_retourne_dto_quand_donnees_trouvees(
        self, service, valid_player, aggregated_dto
    ):
        service.stats_positioning_dao.get_player_average_stats_positioning.return_value = aggregated_dto

        result = service.get_player_average_positioning_stats(valid_player)

        assert result == aggregated_dto
        service.stats_positioning_dao.get_player_average_stats_positioning.assert_called_once_with(
            valid_player, None
        )

    def test_retourne_none_quand_aucune_donnee(self, service, valid_player):
        service.stats_positioning_dao.get_player_average_stats_positioning.return_value = None

        result = service.get_player_average_positioning_stats(valid_player)

        assert result is None

    def test_transmet_game_mode(self, service, valid_player, aggregated_dto):
        service.stats_positioning_dao.get_player_average_stats_positioning.return_value = aggregated_dto

        service.get_player_average_positioning_stats(
            valid_player, game_mode="ranked-solo"
        )

        service.stats_positioning_dao.get_player_average_stats_positioning.assert_called_once_with(
            valid_player, "ranked-solo"
        )

    def test_leve_valeur_erreur_si_player_none(self, service):
        with pytest.raises(ValueError, match="joueur"):
            service.get_player_average_positioning_stats(None)

    def test_leve_valeur_erreur_si_player_sans_id(self, service):
        player_sans_id = MagicMock(spec=Player)
        player_sans_id.id = None

        with pytest.raises(ValueError, match="joueur"):
            service.get_player_average_positioning_stats(player_sans_id)
