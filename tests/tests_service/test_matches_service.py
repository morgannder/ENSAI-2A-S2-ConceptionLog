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


# Tests pour create_match
def test_create_match_ok(mock_match):
    """La DAO crée le match avec succès -> le service retourne True."""
    # GIVEN
    MatchDAO().create_match = MagicMock(return_value=True)
    # WHEN
    result = MatchService().create_match(mock_match)
    # THEN
    assert result is True
    MatchDAO().create_match.assert_called_once_with(mock_match)


def test_create_match_already_exists(mock_match):
    """La DAO indique que le match existe déjà -> le service retourne False."""
    # GIVEN
    MatchDAO().create_match = MagicMock(return_value=False)
    # WHEN
    result = MatchService().create_match(mock_match)
    # THEN
    assert result is False
    MatchDAO().create_match.assert_called_once_with(mock_match)


def test_create_match_no_id():
    """Le match n'a pas d'ID -> le service lève une ValueError."""
    # GIVEN
    match_sans_id = Match(None, 13, 5, 300, False, "2024-01-15 14:30:00")
    # WHEN / THEN
    with pytest.raises(ValueError, match="L'ID du match est requis"):
        MatchService().create_match(match_sans_id)


def test_create_match_no_playlist_id():
    """Le match n'a pas de playlist_id -> le service lève une ValueError."""
    # GIVEN
    match_sans_playlist = Match(
        id="match_123",
        playlist_id=None,  # ← Créez directement avec None
        season=5,
        duration=300,
        overtime=False,
        date_upload="2024-01-15 14:30:00",
    )
    # WHEN / THEN
    with pytest.raises(ValueError, match="Le playlist_id est requis"):
        MatchService().create_match(match_sans_playlist)


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


# Tests pour get_matches_by_season
def test_get_matches_by_season_ok(mock_match_list):
    """La DAO renvoie une liste de matchs -> le service la relaie telle quelle."""
    # GIVEN
    MatchDAO().get_match_by_parameter = MagicMock(return_value=mock_match_list)
    # WHEN
    result = MatchService().get_matches_by_season(5)
    # THEN
    assert result == mock_match_list
    MatchDAO().get_match_by_parameter.assert_called_once_with("season", 5)


def test_get_matches_by_season_empty():
    """La DAO renvoie None -> le service retourne None."""
    # GIVEN
    MatchDAO().get_match_by_parameter = MagicMock(return_value=None)
    # WHEN
    result = MatchService().get_matches_by_season(999)
    # THEN
    assert result is None


# Tests pour get_matches_by_playlist
def test_get_matches_by_playlist_ok(mock_match_list):
    """La DAO renvoie une liste de matchs -> le service la relaie telle quelle."""
    # GIVEN
    MatchDAO().get_match_by_parameter = MagicMock(return_value=mock_match_list)
    # WHEN
    result = MatchService().get_matches_by_playlist(13)
    # THEN
    assert result == mock_match_list
    MatchDAO().get_match_by_parameter.assert_called_once_with("playlist_id", 13)


# Tests pour get_overtime_matches
def test_get_overtime_matches_true(mock_match_list):
    """La DAO renvoie des matchs en overtime -> le service les retourne."""
    # GIVEN
    MatchDAO().get_match_by_parameter = MagicMock(return_value=mock_match_list)
    # WHEN
    result = MatchService().get_overtime_matches(overtime=True)
    # THEN
    assert result == mock_match_list
    MatchDAO().get_match_by_parameter.assert_called_once_with("overtime", 1)


def test_get_overtime_matches_false(mock_match_list):
    """La DAO renvoie des matchs sans overtime -> le service les retourne."""
    # GIVEN
    MatchDAO().get_match_by_parameter = MagicMock(return_value=mock_match_list)
    # WHEN
    result = MatchService().get_overtime_matches(overtime=False)
    # THEN
    assert result == mock_match_list
    MatchDAO().get_match_by_parameter.assert_called_once_with("overtime", 0)


# Tests pour get_recent_matches
def test_get_recent_matches_ok(mock_match_list):
    """La DAO renvoie les matchs récents -> le service les retourne."""
    # GIVEN
    MatchDAO().get_20_recent_matches = MagicMock(return_value=mock_match_list)
    # WHEN
    result = MatchService().get_recent_matches(20)
    # THEN
    assert result == mock_match_list
    MatchDAO().get_20_recent_matches.assert_called_once_with(20)


def test_get_recent_matches_custom_limit(mock_match_list):
    """Le service accepte une limite personnalisée."""
    # GIVEN
    MatchDAO().get_20_recent_matches = MagicMock(return_value=mock_match_list)
    # WHEN
    result = MatchService().get_recent_matches(5)
    # THEN
    assert result == mock_match_list
    MatchDAO().get_20_recent_matches.assert_called_once_with(5)


def test_get_recent_matches_invalid_limit():
    """Une limite <= 0 -> le service lève une ValueError."""
    # WHEN / THEN
    with pytest.raises(ValueError, match="strictement supérieur à 0"):
        MatchService().get_recent_matches(0)

    with pytest.raises(ValueError, match="strictement supérieur à 0"):
        MatchService().get_recent_matches(-5)


# Tests pour get_player_matches
def test_get_player_matches_ok(mock_player, mock_match_list):
    """La DAO renvoie les matchs du joueur -> le service les retourne."""
    # GIVEN
    MatchDAO().get_player_last_matches = MagicMock(return_value=mock_match_list)
    # WHEN
    result = MatchService().get_player_matches(mock_player, 20)
    # THEN
    assert result == mock_match_list
    MatchDAO().get_player_last_matches.assert_called_once_with(mock_player, 20)


def test_get_player_matches_custom_limit(mock_player, mock_match_list):
    """Le service accepte une limite personnalisée pour les matchs du joueur."""
    # GIVEN
    MatchDAO().get_player_last_matches = MagicMock(return_value=mock_match_list)
    # WHEN
    result = MatchService().get_player_matches(mock_player, 10)
    # THEN
    assert result == mock_match_list
    MatchDAO().get_player_last_matches.assert_called_once_with(mock_player, 10)


def test_get_player_matches_no_player():
    """Aucun joueur fourni -> le service lève une ValueError."""
    # WHEN / THEN
    with pytest.raises(ValueError, match="ID valide"):
        MatchService().get_player_matches(None, 20)


def test_get_player_matches_player_no_id():
    """Le joueur n'a pas d'ID -> le service lève une ValueError."""
    # GIVEN
    player_sans_id = Player(None, "steam_789", "Steam", "TestPlayer")
    # WHEN / THEN
    with pytest.raises(ValueError, match="ID valide"):
        MatchService().get_player_matches(player_sans_id, 20)


def test_get_player_matches_invalid_limit(mock_player):
    """Une limite <= 0 -> le service lève une ValueError."""
    # WHEN / THEN
    with pytest.raises(ValueError, match="supérieur à 0"):
        MatchService().get_player_matches(mock_player, 0)


# Tests pour delete_match
def test_delete_match_ok(mock_match):
    """La DAO supprime le match -> le service appelle la DAO."""
    # GIVEN
    MatchDAO().delete_match = MagicMock()
    # WHEN
    MatchService().delete_match(mock_match)
    # THEN
    MatchDAO().delete_match.assert_called_once_with(mock_match)


def test_delete_match_no_match():
    """Aucun match fourni -> le service lève une ValueError."""
    # WHEN / THEN
    with pytest.raises(ValueError, match="ID valide"):
        MatchService().delete_match(None)


def test_delete_match_no_id():
    """Le match n'a pas d'ID -> le service lève une ValueError."""
    # GIVEN
    match_sans_id = Match(None, "13", 5, 300, False, "2024-01-15 14:30:00")
    # WHEN / THEN
    with pytest.raises(ValueError, match="ID valide"):
        MatchService().delete_match(match_sans_id)


# Tests pour get_match_statistics
def test_get_match_statistics_ok(mock_match):
    """La DAO renvoie un match -> le service retourne ses statistiques."""
    # GIVEN
    MatchDAO().get_match_by_parameter = MagicMock(return_value=[mock_match])
    # WHEN
    result = MatchService().get_match_statistics("match_123")
    # THEN
    assert result == {
        "id": "1",
        "playlist_id": "13",
        "season": 5,
        "duration": 300,
        "overtime": False,
        "date_upload": "2024-01-15 14:30:00",
    }


def test_get_match_statistics_not_found():
    """La DAO renvoie None -> le service retourne None."""
    # GIVEN
    MatchDAO().get_match_by_parameter = MagicMock(return_value=None)
    # WHEN
    result = MatchService().get_match_statistics("match_inexistant")
    # THEN
    assert result is None
