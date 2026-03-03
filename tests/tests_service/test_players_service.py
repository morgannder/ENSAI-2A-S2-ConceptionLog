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


def test_search_players_retourne_liste_joueurs():
    service = PlayerService()
    service.player_dao.search_players_by_name = MagicMock(
        return_value=[
            {"platform_user_id": "uid_1", "name": "User", "platform_name": "Steam"},
            {"platform_user_id": "uid_2", "name": "UserRL", "platform_name": "Epic"},
        ]
    )

    result = service.search_players("User")

    assert len(result) == 2
    assert result[0] == {
        "platform_user_id": "uid_1",
        "name": "User",
        "platform": "Steam",
    }
    assert result[1] == {
        "platform_user_id": "uid_2",
        "name": "UserRL",
        "platform": "Epic",
    }
    service.player_dao.search_players_by_name.assert_called_once_with(
        "User", None, 30, 0
    )


def test_search_players_retourne_liste_vide_si_aucun_resultat():
    service = PlayerService()
    service.player_dao.search_players_by_name = MagicMock(return_value=[])

    result = service.search_players("Inconnu")

    assert result == []


def test_search_players_retourne_liste_vide_si_dao_retourne_none():
    service = PlayerService()
    service.player_dao.search_players_by_name = MagicMock(return_value=None)

    result = service.search_players("Inconnu")

    assert result == []


def test_search_players_leve_erreur_si_limite_nulle():
    service = PlayerService()

    with pytest.raises(ValueError, match="La limite doit être supérieure à 0"):
        service.search_players("User", limit=0)


def test_search_players_leve_erreur_si_limite_negative():
    service = PlayerService()

    with pytest.raises(ValueError, match="La limite doit être supérieure à 0"):
        service.search_players("User", limit=-5)


def test_search_players_transmet_platform_et_pagination():
    service = PlayerService()
    service.player_dao.search_players_by_name = MagicMock(return_value=[])

    service.search_players("User", platform="Steam", limit=10, offset=20)

    service.player_dao.search_players_by_name.assert_called_once_with(
        "User", "Steam", 10, 20
    )


def test_search_players_structure_dict_correcte():
    service = PlayerService()
    service.player_dao.search_players_by_name = MagicMock(
        return_value=[
            {"platform_user_id": "uid_1", "name": "User", "platform_name": "Steam"},
        ]
    )

    result = service.search_players("User")

    assert "platform_user_id" in result[0]
    assert "name" in result[0]
    assert "platform" in result[0]
    assert "platform_name" not in result[0]
