from unittest.mock import MagicMock

import pytest

from src.dao.matches_dao import MatchDAO
from src.models.matches import Match
from src.models.players import Player
from src.service.matches_service import MatchService


# Fixtures pour les données de test
@pytest.fixture
def mock_match():
    """Crée un match de test."""
    return Match(
        id="1",
        playlist_id="13",
        season=5,
        duration=300,
        overtime=False,
        date_upload="2024-01-15 14:30:00",
    )


@pytest.fixture
def mock_player():
    """Crée un joueur de test."""
    return Player(
        id=2,
        platform_id=2,
        platform_user_id="Steam_2",
        name="TestPlayer",
    )


@pytest.fixture
def mock_match_list():
    """Crée une liste de matchs de test."""
    return [
        Match("match_1", "13", 5, 300, False, "2024-01-15 14:30:00"),
        Match("match_2", "13", 5, 350, True, "2024-01-15 15:00:00"),
        Match("match_3", "10", 4, 280, False, "2024-01-14 18:00:00"),
    ]


# Tests pour get_match_by_id
def test_get_match_by_id_ok(mock_match):
    """La DAO renvoie une liste avec un match -> le service retourne ce match."""
    # GIVEN
    MatchDAO().get_match_by_parameter = MagicMock(return_value=[mock_match])
    # WHEN
    result = MatchService().get_match_by_id("match_123")
    # THEN
    assert result == mock_match
    MatchDAO().get_match_by_parameter.assert_called_once_with("id", "match_123")


def test_get_match_by_id_not_found():
    """La DAO renvoie None -> le service retourne None."""
    # GIVEN
    MatchDAO().get_match_by_parameter = MagicMock(return_value=None)
    # WHEN
    result = MatchService().get_match_by_id("match_inexistant")
    # THEN
    assert result is None
    MatchDAO().get_match_by_parameter.assert_called_once_with("id", "match_inexistant")


def test_get_match_by_match_team_id_retourne_match():
    service = MatchService()
    match = MagicMock(spec=Match)
    service.match_dao.get_match_by_match_team_id = MagicMock(return_value=match)

    result = service.get_match_by_match_team_id(42)

    assert result == match
    service.match_dao.get_match_by_match_team_id.assert_called_once_with(42)


def test_get_match_by_match_team_id_retourne_none_si_non_trouve():
    service = MatchService()
    service.match_dao.get_match_by_match_team_id = MagicMock(return_value=None)

    result = service.get_match_by_match_team_id(99)

    assert result is None


def test_get_match_by_match_team_id_retourne_none_si_dao_retourne_falsy():
    service = MatchService()
    service.match_dao.get_match_by_match_team_id = MagicMock(return_value=False)

    result = service.get_match_by_match_team_id(1)

    assert result is None
