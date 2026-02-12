from unittest.mock import MagicMock

import pytest

from src.models.players import Player
from src.models.ranks import Ranks
from src.service.ranks_service import RanksService


RANK_GOLD_I_DIV_2 = Ranks(id=1, tier=7, division=2, name="Gold I division 2")

RANK_PLATINUM_II_DIV_1 = Ranks(id=2, tier=11, division=1, name="Platinum II division 1")

RANK_SILVER_I_DIV_3 = Ranks(id=3, tier=4, division=3, name="Silver I division 3")

PLAYER = Player(
    id="1",
    platform_id="2",
    platform_user_id="Steam_2",
    name="TestPlayer",
)

# Tests de création


def test_create_rank_ok():
    service = RanksService()
    service.ranks_dao.create_rank = MagicMock(return_value=True)
    service.ranks_dao.get_rank_by_parameter = MagicMock(return_value=RANK_GOLD_I_DIV_2)

    result = service.create_rank(7, 2, "Gold I division 2")

    assert result == RANK_GOLD_I_DIV_2
    service.ranks_dao.create_rank.assert_called_once()
    service.ranks_dao.get_rank_by_parameter.assert_called_once_with(
        "name", "Gold I division 2"
    )


def test_create_rank_failed():
    service = RanksService()
    service.ranks_dao.create_rank = MagicMock(return_value=False)

    result = service.create_rank(7, 2, "Gold I division 2")

    assert result is None
    service.ranks_dao.create_rank.assert_called_once()


# Récupération par ID


def test_get_rank_by_id_ok():
    service = RanksService()
    service.ranks_dao.get_rank_by_parameter = MagicMock(return_value=RANK_GOLD_I_DIV_2)

    result = service.get_rank_by_id(1)

    assert result == RANK_GOLD_I_DIV_2
    service.ranks_dao.get_rank_by_parameter.assert_called_once_with("id", 1)


def test_get_rank_by_id_not_found():
    service = RanksService()
    service.ranks_dao.get_rank_by_parameter = MagicMock(return_value=None)

    result = service.get_rank_by_id(999)

    assert result is None
    service.ranks_dao.get_rank_by_parameter.assert_called_once_with("id", 999)


# Récupération par nom


def test_get_rank_by_name_ok():
    service = RanksService()
    service.ranks_dao.get_rank_by_parameter = MagicMock(return_value=RANK_GOLD_I_DIV_2)

    result = service.get_rank_by_name("Gold I division 2")

    assert result == RANK_GOLD_I_DIV_2
    service.ranks_dao.get_rank_by_parameter.assert_called_once_with(
        "name", "Gold I division 2"
    )


def test_get_rank_by_name_not_found():
    service = RanksService()
    service.ranks_dao.get_rank_by_parameter = MagicMock(return_value=None)

    result = service.get_rank_by_name("Unknown Rank")

    assert result is None
    service.ranks_dao.get_rank_by_parameter.assert_called_once_with(
        "name", "Unknown Rank"
    )


# Rang actuel d'un joueur


def test_get_current_rank_for_player_ok():
    service = RanksService()
    service.ranks_dao.get_rank_by_player = MagicMock(return_value=RANK_GOLD_I_DIV_2)

    result = service.get_current_rank_for_player(PLAYER)

    assert result == RANK_GOLD_I_DIV_2
    service.ranks_dao.get_rank_by_player.assert_called_once_with(PLAYER)


def test_get_current_rank_for_player_none():
    service = RanksService()

    with pytest.raises(ValueError, match="Le joueur ne peut pas être None"):
        service.get_current_rank_for_player(None)


def test_get_current_rank_for_player_not_found():
    service = RanksService()
    service.ranks_dao.get_rank_by_player = MagicMock(return_value=None)

    result = service.get_current_rank_for_player(PLAYER)

    assert result is None
    service.ranks_dao.get_rank_by_player.assert_called_once_with(PLAYER)


# Suppression


def test_delete_rank_ok():
    service = RanksService()
    service.ranks_dao.delete_rank = MagicMock()

    result = service.delete_rank(RANK_GOLD_I_DIV_2)

    assert result is True
    service.ranks_dao.delete_rank.assert_called_once_with(RANK_GOLD_I_DIV_2)


def test_delete_rank_none():
    service = RanksService()

    with pytest.raises(ValueError, match="Le rang ne peut pas être None"):
        service.delete_rank(None)


# Vérification d'existence


def test_rank_exists_true():
    service = RanksService()
    service.ranks_dao.get_rank_by_parameter = MagicMock(return_value=RANK_GOLD_I_DIV_2)

    result = service.rank_exists("Gold I division 2")

    assert result is True
    service.ranks_dao.get_rank_by_parameter.assert_called_once_with(
        "name", "Gold I division 2"
    )


def test_rank_exists_false():
    service = RanksService()
    service.ranks_dao.get_rank_by_parameter = MagicMock(return_value=None)

    result = service.rank_exists("Unknown Rank")

    assert result is False
    service.ranks_dao.get_rank_by_parameter.assert_called_once_with(
        "name", "Unknown Rank"
    )


# Display name


def test_get_rank_display_name_ok():
    service = RanksService()

    result = service.get_rank_display_name(RANK_GOLD_I_DIV_2)

    assert result == "Gold I division 2"


def test_get_rank_display_name_none():
    service = RanksService()

    result = service.get_rank_display_name(None)

    assert result == "Non classé"


# Comparaison de rangs


def test_compare_ranks_same():
    service = RanksService()

    rank1 = Ranks(id=1, tier=7, division=2, name="Gold I Division 2")
    rank2 = Ranks(id=2, tier=7, division=2, name="Gold I Division 2")

    assert service.compare_ranks(rank1, rank2) == 0


def test_compare_ranks_higher_tier():
    """Platinum (11) > Gold (7)"""
    service = RanksService()

    assert service.compare_ranks(RANK_PLATINUM_II_DIV_1, RANK_GOLD_I_DIV_2) == 1


def test_compare_ranks_lower_tier():
    """Silver (4) < Gold (7)"""
    service = RanksService()

    assert service.compare_ranks(RANK_SILVER_I_DIV_3, RANK_GOLD_I_DIV_2) == -1


def test_compare_ranks_same_tier_higher_division():
    service = RanksService()

    rank1 = Ranks(id=1, tier=7, division=4, name="Gold I division 4")
    rank2 = Ranks(id=2, tier=7, division=2, name="Gold I division 2")

    assert service.compare_ranks(rank1, rank2) == 1


def test_compare_ranks_same_tier_lower_division():
    service = RanksService()

    rank1 = Ranks(id=1, tier=7, division=1, name="Gold I division 1")
    rank2 = Ranks(id=2, tier=7, division=3, name="Gold I division 3")

    assert service.compare_ranks(rank1, rank2) == -1


def test_compare_ranks_unknown_tier():
    service = RanksService()

    rank1 = Ranks(id=1, tier=0, division=1, name="Unknown")
    rank2 = Ranks(id=2, tier=2, division=1, name="Bronze I")

    assert service.compare_ranks(rank1, rank2) == -1


def test_compare_ranks_unknown_division():
    service = RanksService()

    rank1 = Ranks(id=1, tier=7, division=0, name="Gold Unknown")
    rank2 = Ranks(id=2, tier=7, division=3, name="Gold I division 3")

    assert service.compare_ranks(rank1, rank2) == -1
