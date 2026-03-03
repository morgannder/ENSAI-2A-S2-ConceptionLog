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


def test_get_player_rank_by_platform_id_ok():
    service = RanksService()
    service.player_dao.get_player_by_parameter = MagicMock(return_value=PLAYER)
    service.ranks_dao.get_player_rank = MagicMock(return_value=RANK_GOLD_I_DIV_2)

    result = service.get_player_rank_by_platform_id("player_123")

    assert result == RANK_GOLD_I_DIV_2
    service.player_dao.get_player_by_parameter.assert_called_once_with(
        "platform_user_id", "player_123"
    )
    service.ranks_dao.get_player_rank.assert_called_once_with(PLAYER)


def test_get_player_rank_by_platform_id_none():
    service = RanksService()

    with pytest.raises(ValueError, match="Veuillez insérer un identifiant."):
        service.get_player_rank_by_platform_id(None)


def test_get_player_rank_by_id_not_found():
    service = RanksService()
    service.player_dao.get_player_by_parameter = MagicMock(return_value=PLAYER)
    service.ranks_dao.get_player_rank = MagicMock(return_value=None)

    with pytest.raises(AttributeError):
        service.get_player_rank_by_id("player_123")


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
