from unittest.mock import MagicMock

import pytest

from src.models.players import Player
from src.service.players_service import PlayerService


# Fixtures

PLAYER = Player(
    id=1,
    platform_id=1,
    platform_user_id="abc123",
    name="PlayerOne",
)


# get_player_by_platform_id


def test_get_player_by_platform_id_ok():
    service = PlayerService()
    service.player_dao.get_player_by_parameter = MagicMock(return_value=PLAYER)

    result = service.get_player_by_platform_id(123)

    assert result == PLAYER
    service.player_dao.get_player_by_parameter.assert_called_once_with(
        "platform_user_id", 123
    )


def test_get_player_by_platform_id_invalid():
    service = PlayerService()

    with pytest.raises(ValueError, match="Le platform_id du joueur doit être non vide"):
        service.get_player_by_platform_id(None)


# get_player_by_


def test_get_player_by_name_ok():
    service = PlayerService()
    service.player_dao.get_player_by_parameter = MagicMock(return_value=PLAYER)

    result = service.get_player_by_name("PlayerOne")

    assert result == PLAYER
    service.player_dao.get_player_by_parameter.assert_called_once_with(
        "name", "PlayerOne"
    )


def test_get_player_by_name_invalid():
    service = PlayerService()

    with pytest.raises(ValueError):
        service.get_player_by_name("   ")


# player_exists


def test_player_exists_true():
    service = PlayerService()
    service.get_player_by_name = MagicMock(return_value=PLAYER)

    assert service.player_exists("PlayerOne") is True


def test_player_exists_false():
    service = PlayerService()
    service.get_player_by_name = MagicMock(return_value=None)

    assert service.player_exists("Unknown") is False


# player_exists_by_id


def test_player_exists_by_platform_id_true():
    service = PlayerService()
    service.get_player_by_platform_id = MagicMock(return_value=PLAYER)

    assert service.player_exists_by_platform_id(1) is True


def test_player_exists_by_platform_id_false():
    service = PlayerService()
    service.get_player_by_platform_id = MagicMock(return_value=None)

    assert service.player_exists_by_platform_id(1) is False


def test_player_exists_by_platform_id_invalid():
    service = PlayerService()
    service.player_dao.get_player_by_parameter = MagicMock(
        side_effect=ValueError("Le platform_id du joueur doit être non vide")
    )

    assert service.player_exists_by_platform_id("abc123") is False


# validate_player_name


def test_validate_player_name_ok():
    service = PlayerService()

    valid, msg = service.validate_player_name("PlayerOne")

    assert valid is True
    assert msg == ""


def test_validate_player_name_too_short():
    service = PlayerService()

    valid, msg = service.validate_player_name("ab")

    assert valid is False


def test_validate_player_name_too_long():
    service = PlayerService()

    valid, msg = service.validate_player_name("a" * 51)

    assert valid is False


def test_validate_player_name_empty():
    service = PlayerService()

    valid, msg = service.validate_player_name("")

    assert valid is False


# get_player_display_info


def test_get_player_display_info_ok():
    service = PlayerService()

    result = service.get_player_display_info(PLAYER)

    assert "PlayerOne" in result
    assert "ID: 1" in result


def test_get_player_display_info_none():
    service = PlayerService()

    assert service.get_player_display_info(None) == "Joueur inconnu"


# search_players_by_name_partial


def test_search_players_not_implemented():
    service = PlayerService()

    with pytest.raises(NotImplementedError):
        service.search_players_by_name_partial("Play")
