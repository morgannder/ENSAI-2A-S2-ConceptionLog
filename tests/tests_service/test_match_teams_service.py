from unittest.mock import MagicMock

import pytest

from src.dao.match_teams_dao import MatchTeamDAO
from src.models.match_teams import MatchTeam
from src.models.players import Player
from src.service.match_teams_service import MatchTeamService


# Fixtures pour les données de test
@pytest.fixture
def mock_match_team():
    """Crée une équipe de match de test."""
    return MatchTeam(
        id=1,
        match_id="match_456",
        color="blue",
        score=3,
        possession_time=180,
        time_in_side=150,
    )


@pytest.fixture
def mock_player():
    """Crée un joueur de test."""
    return Player(
        id=1,
        platform_id=2,
        platform_user_id="Steam_2",
        name="TestPlayer",
    )


@pytest.fixture
def mock_team_list():
    """Crée une liste d'équipes de test."""
    return [
        MatchTeam("team_1", "match_1", "blue", 3, 180, 150),
        MatchTeam("team_2", "match_1", "orange", 2, 120, 150),
        MatchTeam("team_3", "match_2", "blue", 5, 200, 170),
    ]


# Tests pour get_match_team_by_id
def test_get_match_team_by_id_ok(mock_match_team):
    """La DAO renvoie une liste avec une équipe -> le service retourne cette équipe."""
    # GIVEN
    MatchTeamDAO().get_match_teams_by_parameter = MagicMock(
        return_value=[mock_match_team]
    )
    # WHEN
    result = MatchTeamService().get_match_team_by_id("team_123")
    # THEN
    assert result == mock_match_team
    MatchTeamDAO().get_match_teams_by_parameter.assert_called_once_with(
        "id", "team_123"
    )


def test_get_match_team_by_id_not_found():
    """La DAO renvoie None -> le service retourne None."""
    # GIVEN
    MatchTeamDAO().get_match_teams_by_parameter = MagicMock(return_value=None)
    # WHEN
    result = MatchTeamService().get_match_team_by_id("team_inexistant")
    # THEN
    assert result is None


# Tests pour get_teams_by_match
def test_get_teams_by_match_ok(mock_team_list):
    """La DAO renvoie une liste d'équipes -> le service la relaie telle quelle."""
    # GIVEN
    MatchTeamDAO().get_match_teams_by_parameter = MagicMock(return_value=mock_team_list)
    # WHEN
    result = MatchTeamService().get_teams_by_match("match_1")
    # THEN
    assert result == mock_team_list
    MatchTeamDAO().get_match_teams_by_parameter.assert_called_once_with(
        "match_id", "match_1"
    )


def test_get_teams_by_match_empty():
    """La DAO renvoie None -> le service retourne None."""
    # GIVEN
    MatchTeamDAO().get_match_teams_by_parameter = MagicMock(return_value=None)
    # WHEN
    result = MatchTeamService().get_teams_by_match("match_999")
    # THEN
    assert result is None


# Tests pour get_teams_by_color
def test_get_teams_by_color_ok(mock_team_list):
    """La DAO renvoie des équipes bleues -> le service les retourne."""
    # GIVEN
    MatchTeamDAO().get_match_teams_by_parameter = MagicMock(return_value=mock_team_list)
    # WHEN
    result = MatchTeamService().get_teams_by_color("blue")
    # THEN
    assert result == mock_team_list
    MatchTeamDAO().get_match_teams_by_parameter.assert_called_once_with("color", "blue")


def test_get_teams_by_color_invalid():
    """Une couleur invalide -> le service lève une ValueError."""
    # WHEN / THEN
    with pytest.raises(ValueError, match="La couleur doit être 'blue' ou 'orange'"):
        MatchTeamService().get_teams_by_color("red")
