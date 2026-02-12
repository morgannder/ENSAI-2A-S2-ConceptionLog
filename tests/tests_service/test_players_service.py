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


# create_player


def test_create_player_ok():
    service = PlayerService()
    service.player_dao.create_player = MagicMock(return_value=True)
    service.get_player_by_name = MagicMock(return_value=PLAYER)

    result = service.create_player("PC", "abc123", "PlayerOne")

    assert result == PLAYER
    service.player_dao.create_player.assert_called_once()
    service.get_player_by_name.assert_called_once_with("PlayerOne")


def test_create_player_fail():
    service = PlayerService()
    service.player_dao.create_player = MagicMock(return_value=False)

    result = service.create_player("PC", "abc123", "PlayerOne")

    assert result is None


def test_create_player_invalid_name():
    service = PlayerService()

    with pytest.raises(ValueError):
        service.create_player("PC", "abc123", "")


def test_create_player_missing_platform_ids():
    service = PlayerService()

    with pytest.raises(ValueError):
        service.create_player(None, None, "PlayerOne")


# get_player_by_id


def test_get_player_by_id_ok():
    service = PlayerService()
    service.player_dao.get_player_by_parameter = MagicMock(return_value=PLAYER)

    result = service.get_player_by_id(1)

    assert result == PLAYER
    service.player_dao.get_player_by_parameter.assert_called_once_with("id", 1)


def test_get_player_by_id_invalid():
    service = PlayerService()

    with pytest.raises(ValueError):
        service.get_player_by_id(-1)


# get_player_by_


def test_get_player_by_name_ok():
    service = PlayerService()
    service.player_dao.get_player_by_parameter = MagicMock(return_value=PLAYER)

    result = service.get_player_by_("PlayerOne")

    assert result == PLAYER
    service.player_dao.get_player_by_parameter.assert_called_once_with(
        "name", "PlayerOne"
    )


def test_get_player_by_name_invalid():
    service = PlayerService()

    with pytest.raises(ValueError):
        service.get_player_by_("   ")


# delete_player


def test_delete_player_ok():
    service = PlayerService()
    service.player_dao.delete_player = MagicMock()

    result = service.delete_player(PLAYER)

    assert result is True
    service.player_dao.delete_player.assert_called_once_with(PLAYER)


def test_delete_player_none():
    service = PlayerService()

    with pytest.raises(ValueError):
        service.delete_player(None)


# delete_player_by_name


def test_delete_player_by_name_ok():
    service = PlayerService()
    service.get_player_by_name = MagicMock(return_value=PLAYER)
    service.delete_player = MagicMock(return_value=True)

    result = service.delete_player_by_name("PlayerOne")

    assert result is True


def test_delete_player_by_name_not_found():
    service = PlayerService()
    service.get_player_by_name = MagicMock(return_value=None)

    result = service.delete_player_by_name("Unknown")

    assert result is False


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


def test_player_exists_by_id_true():
    service = PlayerService()
    service.get_player_by_id = MagicMock(return_value=PLAYER)

    assert service.player_exists_by_id(1) is True


def test_player_exists_by_id_false():
    service = PlayerService()
    service.get_player_by_id = MagicMock(return_value=None)

    assert service.player_exists_by_id(1) is False


def test_player_exists_by_id_invalid():
    service = PlayerService()

    assert service.player_exists_by_id(-1) is False


# get_or_create_player


def test_get_or_create_existing():
    service = PlayerService()
    service.get_player_by_name = MagicMock(return_value=PLAYER)

    result = service.get_or_create_player("PC", "abc123", "PlayerOne")

    assert result == PLAYER


def test_get_or_create_new():
    service = PlayerService()
    service.get_player_by_name = MagicMock(side_effect=[None, PLAYER])
    service.create_player = MagicMock(return_value=PLAYER)

    result = service.get_or_create_player("PC", "abc123", "PlayerOne")

    assert result == PLAYER


def test_get_or_create_fail():
    service = PlayerService()
    service.get_player_by_name = MagicMock(return_value=None)
    service.create_player = MagicMock(return_value=None)

    with pytest.raises(RuntimeError):
        service.get_or_create_player("PC", "abc123", "PlayerOne")


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
