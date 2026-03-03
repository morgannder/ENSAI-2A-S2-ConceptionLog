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


# Tests pour get_teams_by_score
def test_get_teams_by_score_ok(mock_team_list):
    """La DAO renvoie des équipes avec le score donné -> le service les retourne."""
    # GIVEN
    MatchTeamDAO().get_match_teams_by_parameter = MagicMock(return_value=mock_team_list)
    # WHEN
    result = MatchTeamService().get_teams_by_score(3)
    # THEN
    assert result == mock_team_list
    MatchTeamDAO().get_match_teams_by_parameter.assert_called_once_with("score", 3)


def test_get_teams_by_score_negative():
    """Un score négatif -> le service lève une ValueError."""
    # WHEN / THEN
    with pytest.raises(ValueError, match="Le score ne peut pas être négatif"):
        MatchTeamService().get_teams_by_score(-1)


# Tests pour get_player_teams
def test_get_player_teams_ok(mock_player, mock_team_list):
    """La DAO renvoie les équipes du joueur -> le service les retourne."""
    # GIVEN
    MatchTeamDAO().get_player_last_match_teams = MagicMock(return_value=mock_team_list)
    # WHEN
    result = MatchTeamService().get_player_teams(mock_player, 20)
    # THEN
    assert result == mock_team_list
    MatchTeamDAO().get_player_last_match_teams.assert_called_once_with(mock_player, 20)


def test_get_player_teams_custom_limit(mock_player, mock_team_list):
    """Le service accepte une limite personnalisée."""
    # GIVEN
    MatchTeamDAO().get_player_last_match_teams = MagicMock(return_value=mock_team_list)
    # WHEN
    result = MatchTeamService().get_player_teams(mock_player, 10)
    # THEN
    assert result == mock_team_list
    MatchTeamDAO().get_player_last_match_teams.assert_called_once_with(mock_player, 10)


def test_get_player_teams_no_player():
    """Aucun joueur fourni -> le service lève une ValueError."""
    # WHEN / THEN
    with pytest.raises(ValueError, match="ID valide"):
        MatchTeamService().get_player_teams(None, 20)


def test_get_player_teams_player_no_id():
    """Le joueur n'a pas d'ID -> le service lève une ValueError."""
    # GIVEN
    player_sans_id = Player(None, 2, "Steam_2", "TestPlayer")
    # WHEN / THEN
    with pytest.raises(ValueError, match="ID valide"):
        MatchTeamService().get_player_teams(player_sans_id, 20)


def test_get_player_teams_invalid_limit(mock_player):
    """Une limite <= 0 -> le service lève une ValueError."""
    # WHEN / THEN
    with pytest.raises(ValueError, match="supérieur à 0"):
        MatchTeamService().get_player_teams(mock_player, 0)


# Tests pour get_match_winner
def test_get_match_winner_ok():
    """Deux équipes avec des scores différents -> le service retourne le gagnant."""
    # GIVEN
    team_blue = MatchTeam("team_1", "match_1", "blue", 5, 180, 150)
    team_orange = MatchTeam("team_2", "match_1", "orange", 3, 120, 150)
    MatchTeamDAO().get_match_teams_by_parameter = MagicMock(
        return_value=[team_blue, team_orange]
    )
    # WHEN
    result = MatchTeamService().get_match_winner("match_1")
    # THEN
    assert result == team_blue
    assert result.score == 5


def test_get_match_winner_draw():
    """Deux équipes avec le même score -> le service retourne None (match nul)."""
    # GIVEN
    team_blue = MatchTeam("team_1", "match_1", "blue", 3, 180, 150)
    team_orange = MatchTeam("team_2", "match_1", "orange", 3, 120, 150)
    MatchTeamDAO().get_match_teams_by_parameter = MagicMock(
        return_value=[team_blue, team_orange]
    )
    # WHEN
    result = MatchTeamService().get_match_winner("match_1")
    # THEN
    assert result is None


def test_get_match_winner_not_found():
    """La DAO ne trouve pas d'équipes -> le service retourne None."""
    # GIVEN
    MatchTeamDAO().get_match_teams_by_parameter = MagicMock(return_value=None)
    # WHEN
    result = MatchTeamService().get_match_winner("match_inexistant")
    # THEN
    assert result is None


def test_get_match_winner_incomplete_teams():
    """Moins de 2 équipes trouvées -> le service retourne None."""
    # GIVEN
    team_blue = MatchTeam("team_1", "match_1", "blue", 5, 180, 150)
    MatchTeamDAO().get_match_teams_by_parameter = MagicMock(return_value=[team_blue])
    # WHEN
    result = MatchTeamService().get_match_winner("match_1")
    # THEN
    assert result is None


# Tests pour get_team_statistics
def test_get_team_statistics_ok(mock_match_team):
    """La DAO renvoie une équipe -> le service retourne ses statistiques."""
    # GIVEN
    MatchTeamDAO().get_match_teams_by_parameter = MagicMock(
        return_value=[mock_match_team]
    )
    # WHEN
    result = MatchTeamService().get_team_statistics("team_123")
    # THEN
    assert result == {
        "id": 1,
        "match_id": "match_456",
        "color": "blue",
        "score": 3,
        "possession_time": 180,
        "time_in_side": 150,
        "possession_percentage": 60.0,  # 180/300 * 100
    }


def test_get_team_statistics_not_found():
    """La DAO renvoie None -> le service retourne None."""
    # GIVEN
    MatchTeamDAO().get_match_teams_by_parameter = MagicMock(return_value=None)
    # WHEN
    result = MatchTeamService().get_team_statistics("team_inexistant")
    # THEN
    assert result is None


def test_get_team_statistics_no_possession():
    """Une équipe sans possession_time -> le pourcentage est None."""
    # GIVEN
    team_sans_possession = MatchTeam("team_1", "match_1", "blue", 3, 0, 150)
    MatchTeamDAO().get_match_teams_by_parameter = MagicMock(
        return_value=[team_sans_possession]
    )
    # WHEN
    result = MatchTeamService().get_team_statistics("team_1")
    # THEN
    assert result["possession_percentage"] is None
