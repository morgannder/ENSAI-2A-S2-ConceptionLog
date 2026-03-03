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


# Rang actuel d'un joueur par son platform_id


def test_get_player_rank_by_platform_id_ok():
    service = RanksService()
    service.player_dao.get_player_by_parameter = MagicMock(return_value=PLAYER)
    service.ranks_dao.get_player_rank = MagicMock(return_value=RANK_GOLD_I_DIV_2)

    result = service.get_player_rank_by_platform_id("player_123")

    assert result == {
        "tier": RANK_GOLD_I_DIV_2.tier,
        "division": RANK_GOLD_I_DIV_2.division,
        "name": RANK_GOLD_I_DIV_2.display_name,
        "full_name": RANK_GOLD_I_DIV_2.name,
    }
    service.player_dao.get_player_by_parameter.assert_called_once_with(
        "platform_user_id", "player_123"
    )
    service.ranks_dao.get_player_rank.assert_called_once_with(PLAYER)


def test_get_player_rank_by_platform_id_none():
    service = RanksService()

    with pytest.raises(ValueError, match="Veuillez insérer un identifiant."):
        service.get_player_rank_by_platform_id(None)
