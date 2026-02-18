from unittest.mock import MagicMock

import pytest

from src.models.match_participation import MatchParticipation
from src.models.players import Player
from src.service.match_participation_service import MatchParticipationService


# Fixtures de données de test
PARTICIPATION_1 = MatchParticipation(
    id=1,
    match_team_id=1,
    player_id=1,
    rank_id=1,
    car_id=10,
    car_name="Octane",
    mvp=True,
    start_time=0,
    end_time=300,
)

PARTICIPATION_2 = MatchParticipation(
    id=1,
    match_team_id=1,
    player_id=2,
    rank_id=2,
    car_id=11,
    car_name="Fennec",
    mvp=False,
    start_time=0,
    end_time=250,
)

PARTICIPATION_LIST = [PARTICIPATION_1, PARTICIPATION_2]

PLAYER = Player(
    id=1,
    platform_id=2,
    platform_user_id="Steam_2",
    name="TestPlayer",
)


# Tests de création de participation


def test_create_ok():
    """La DAO crée la participation -> le service relaie True."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.create_match_participation = MagicMock(
        return_value=True
    )
    # WHEN
    result = service.create_match_participation(PARTICIPATION_1)
    # THEN
    assert result is True
    service.match_participation_dao.create_match_participation.assert_called_once_with(
        PARTICIPATION_1
    )


def test_create_already_exists():
    """La DAO indique que la participation existe déjà -> le service relaie False."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.create_match_participation = MagicMock(
        return_value=False
    )
    # WHEN
    result = service.create_match_participation(PARTICIPATION_1)
    # THEN
    assert result is False
    service.match_participation_dao.create_match_participation.assert_called_once_with(
        PARTICIPATION_1
    )


def test_create_no_id():
    """Participation sans ID -> ValueError."""
    # GIVEN
    participation = MatchParticipation(
        id=None,
        match_team_id=1,
        player_id=1,
        rank_id=1,
        car_id=10,
        car_name="Octane",
        mvp=True,
        start_time=0,
        end_time=300,
    )
    service = MatchParticipationService()
    # WHEN / THEN
    with pytest.raises(ValueError, match="L'ID de la participation est requis"):
        service.create_match_participation(participation)


def test_create_no_match_team_id():
    """Participation sans match_team_id -> ValueError."""
    # GIVEN
    participation = MatchParticipation(
        id=1,
        match_team_id=None,
        player_id=1,
        rank_id=1,
        car_id=10,
        car_name="Octane",
        mvp=True,
        start_time=0,
        end_time=300,
    )
    service = MatchParticipationService()
    # WHEN / THEN
    with pytest.raises(ValueError, match="Le match_team_id est requis"):
        service.create_match_participation(participation)


def test_create_no_player_id():
    """Participation sans player_id -> ValueError."""
    # GIVEN
    participation = participation = MatchParticipation(
        id=1,
        match_team_id=1,
        player_id=None,
        rank_id=1,
        car_id=10,
        car_name="Octane",
        mvp=True,
        start_time=0,
        end_time=300,
    )
    service = MatchParticipationService()
    # WHEN / THEN
    with pytest.raises(ValueError, match="Le player_id est requis"):
        service.create_match_participation(participation)


def test_create_invalid_times():
    """Temps de début après temps de fin -> ValueError."""
    # GIVEN
    participation = participation = MatchParticipation(
        id=1,
        match_team_id=1,
        player_id=1,
        rank_id=1,
        car_id=10,
        car_name="Octane",
        mvp=True,
        start_time=300,
        end_time=-2,
    )
    service = MatchParticipationService()
    # WHEN / THEN
    with pytest.raises(
        ValueError, match="Les temps de début et de fin ne conviennent pas"
    ):
        service.create_match_participation(participation)


# Tests de récupération par ID


def test_get_by_id_ok():
    """La DAO renvoie une participation -> le service la relaie."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.get_matches_by_parameter = MagicMock(
        return_value=[PARTICIPATION_1]
    )
    # WHEN
    result = service.get_participation_by_id("part1")
    # THEN
    assert result == PARTICIPATION_1
    service.match_participation_dao.get_matches_by_parameter.assert_called_once_with(
        "id", "part1"
    )


def test_get_by_id_not_found():
    """La DAO ne trouve pas la participation -> le service renvoie None."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.get_matches_by_parameter = MagicMock(
        return_value=[]
    )
    # WHEN
    result = service.get_participation_by_id("part999")
    # THEN
    assert result is None
    service.match_participation_dao.get_matches_by_parameter.assert_called_once_with(
        "id", "part999"
    )


# Tests de récupération par équipe


def test_get_by_team_ok():
    """La DAO renvoie une liste de participations -> le service la relaie."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.get_matches_by_parameter = MagicMock(
        return_value=PARTICIPATION_LIST
    )
    # WHEN
    result = service.get_participations_by_team("team1")
    # THEN
    assert result == PARTICIPATION_LIST
    service.match_participation_dao.get_matches_by_parameter.assert_called_once_with(
        "match_team_id", "team1"
    )


# Tests de récupération par joueur


def test_get_by_player_ok():
    """La DAO renvoie une liste de participations -> le service la relaie."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.get_matches_by_parameter = MagicMock(
        return_value=PARTICIPATION_LIST
    )
    # WHEN
    result = service.get_participations_by_player("player1")
    # THEN
    assert result == PARTICIPATION_LIST
    service.match_participation_dao.get_matches_by_parameter.assert_called_once_with(
        "player_id", "player1"
    )


# Tests de récupération par rang


def test_get_by_rank_ok():
    """La DAO renvoie une liste de participations -> le service la relaie."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.get_matches_by_parameter = MagicMock(
        return_value=[PARTICIPATION_1]
    )
    # WHEN
    result = service.get_participations_by_rank(1)
    # THEN
    assert result == [PARTICIPATION_1]
    service.match_participation_dao.get_matches_by_parameter.assert_called_once_with(
        "rank_id", 1
    )


# Tests de récupération par voiture


def test_get_by_car_ok():
    """La DAO renvoie une liste de participations -> le service la relaie."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.get_matches_by_parameter = MagicMock(
        return_value=[PARTICIPATION_1]
    )
    # WHEN
    result = service.get_participations_by_car(10)
    # THEN
    assert result == [PARTICIPATION_1]
    service.match_participation_dao.get_matches_by_parameter.assert_called_once_with(
        "car_id", 10
    )


# Tests de récupération des participations récentes


def test_get_recent_ok():
    """La DAO renvoie une liste de participations récentes -> le service la relaie."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.get_player_last_match_participation = MagicMock(
        return_value=PARTICIPATION_LIST
    )
    # WHEN
    result = service.get_player_recent_participations(PLAYER, 20)
    # THEN
    assert result == PARTICIPATION_LIST
    service.match_participation_dao.get_player_last_match_participation.assert_called_once_with(
        PLAYER, 20
    )


def test_get_recent_custom_limit():
    """La DAO renvoie une liste limitée -> le service la relaie."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.get_player_last_match_participation = MagicMock(
        return_value=[PARTICIPATION_1]
    )
    # WHEN
    result = service.get_player_recent_participations(PLAYER, 5)
    # THEN
    assert result == [PARTICIPATION_1]
    service.match_participation_dao.get_player_last_match_participation.assert_called_once_with(
        PLAYER, 5
    )


def test_get_recent_no_player_id():
    """Joueur sans ID -> ValueError."""
    # GIVEN
    player = Player(
        id=None,
        platform_id=2,
        platform_user_id="Steam_2",
        name="TestPlayer",
    )
    service = MatchParticipationService()
    # WHEN / THEN
    with pytest.raises(ValueError, match="Le joueur doit avoir un ID valide"):
        service.get_player_recent_participations(player)


def test_get_recent_invalid_limit():
    """Limite invalide -> ValueError."""
    # GIVEN
    service = MatchParticipationService()
    # WHEN / THEN
    with pytest.raises(
        ValueError, match="Le nombre de participations doit être supérieur à 0"
    ):
        service.get_player_recent_participations(PLAYER, 0)


# Tests de récupération des participations MVP


def test_get_mvp_ok():
    """La DAO renvoie une liste de participations MVP -> le service la relaie."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.get_player_match_mvp = MagicMock(
        return_value=[PARTICIPATION_1]
    )
    # WHEN
    result = service.get_player_mvp_participations(PLAYER)
    # THEN
    assert result == [PARTICIPATION_1]
    service.match_participation_dao.get_player_match_mvp.assert_called_once_with(PLAYER)


def test_get_mvp_no_player_id():
    """Joueur sans ID -> ValueError."""
    # GIVEN
    player = Player(
        id=None,
        platform_id=2,
        platform_user_id="Steam_2",
        name="TestPlayer",
    )
    service = MatchParticipationService()
    # WHEN / THEN
    with pytest.raises(ValueError, match="Le joueur doit avoir un ID valide"):
        service.get_player_mvp_participations(player)


# Tests de comptage des MVP


def test_get_mvp_count_ok():
    """La DAO renvoie le nombre de MVP -> le service le relaie."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.get_player_nb_mvp = MagicMock(return_value=5)
    # WHEN
    result = service.get_player_mvp_count(PLAYER)
    # THEN
    assert result == 5
    service.match_participation_dao.get_player_nb_mvp.assert_called_once_with(PLAYER)


def test_get_mvp_count_no_player_id():
    """Joueur sans ID -> ValueError."""
    # GIVEN
    player = Player(
        None,
        platform_id=2,
        platform_user_id="Steam_2",
        name="TestPlayer",
    )
    service = MatchParticipationService()
    # WHEN / THEN
    with pytest.raises(ValueError, match="Le joueur doit avoir un ID valide"):
        service.get_player_mvp_count(player)


# Tests de suppression


def test_delete_ok():
    """La DAO supprime la participation -> le service relaie."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.delete_match_participation = MagicMock()
    # WHEN
    service.delete_participation(PARTICIPATION_1)
    # THEN
    service.match_participation_dao.delete_match_participation.assert_called_once_with(
        PARTICIPATION_1
    )


def test_delete_no_id():
    """Participation sans ID -> ValueError."""
    # GIVEN
    participation = MatchParticipation(
        id=None,
        match_team_id=1,
        player_id=1,
        rank_id=1,
        car_id=10,
        car_name="Octane",
        mvp=True,
        start_time=0,
        end_time=300,
    )
    service = MatchParticipationService()
    # WHEN / THEN
    with pytest.raises(ValueError, match="La participation doit avoir un ID valide"):
        service.delete_participation(participation)


# Tests du taux de MVP


def test_get_mvp_rate_ok():
    """Le service calcule correctement le taux de MVP."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.get_matches_by_parameter = MagicMock(
        return_value=PARTICIPATION_LIST
    )
    service.match_participation_dao.get_player_nb_mvp = MagicMock(return_value=1)
    # WHEN
    result = service.get_player_mvp_rate(PLAYER)
    # THEN
    assert result == 50.0


def test_get_mvp_rate_no_participations():
    """Aucune participation -> None."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.get_matches_by_parameter = MagicMock(
        return_value=None
    )
    # WHEN
    result = service.get_player_mvp_rate(PLAYER)
    # THEN
    assert result is None


def test_get_mvp_rate_no_player_id():
    """Joueur sans ID -> ValueError."""
    # GIVEN
    player = Player(
        id=None,
        platform_id=2,
        platform_user_id="Steam_2",
        name="TestPlayer",
    )
    service = MatchParticipationService()
    # WHEN / THEN
    with pytest.raises(ValueError, match="Le joueur doit avoir un ID valide"):
        service.get_player_mvp_rate(player)


# Tests des statistiques de participation


def test_get_statistics_ok():
    """La participation existe -> le service renvoie les statistiques."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.get_matches_by_parameter = MagicMock(
        return_value=[PARTICIPATION_1]
    )
    # WHEN
    result = service.get_participation_statistics(1)
    # THEN
    assert result == {
        "id": 1,
        "match_team_id": 1,
        "player_id": 1,
        "rank_id": 1,
        "car_id": 10,
        "car_name": "Octane",
        "mvp": True,
        "play_time_seconds": 300,
        "start_time": 0,
        "end_time": 300,
    }


def test_get_statistics_not_found():
    """La participation n'existe pas -> None."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.get_matches_by_parameter = MagicMock(
        return_value=[]
    )
    # WHEN
    result = service.get_participation_statistics("part999")
    # THEN
    assert result is None


def test_get_statistics_no_times():
    """Participation sans temps -> play_time_seconds est None."""
    # GIVEN
    participation = MatchParticipation(
        id=1,
        match_team_id=1,
        player_id=1,
        rank_id=1,
        car_id=10,
        car_name="Octane",
        mvp=True,
        start_time=None,
        end_time=None,
    )
    service = MatchParticipationService()
    service.match_participation_dao.get_matches_by_parameter = MagicMock(
        return_value=[participation]
    )
    # WHEN
    result = service.get_participation_statistics(1)
    # THEN
    assert result["play_time_seconds"] is None


# Tests des voitures les plus utilisées


def test_get_most_used_cars_ok():
    """Le service calcule correctement les voitures les plus utilisées."""
    # GIVEN
    participations = [
        PARTICIPATION_1,  # Octane
        PARTICIPATION_2,  # Fennec
        MatchParticipation(
            id=1,
            match_team_id=1,
            player_id=1,
            rank_id=1,
            car_id=10,
            car_name="Octane",
            mvp=True,
            start_time=0,
            end_time=300,
        ),
    ]
    service = MatchParticipationService()
    service.match_participation_dao.get_matches_by_parameter = MagicMock(
        return_value=participations
    )
    # WHEN
    result = service.get_most_used_cars(PLAYER, 5)
    # THEN
    assert result == {"Octane": 2, "Fennec": 1}


def test_get_most_used_cars_with_limit():
    """Le service respecte la limite."""
    # GIVEN
    participations = [
        MatchParticipation(
            id=1,
            match_team_id=1,
            player_id=1,
            rank_id=1,
            car_id=10,
            car_name="Car1",
            mvp=True,
            start_time=0,
            end_time=300,
        ),
        MatchParticipation(
            id=2,
            match_team_id=1,
            player_id=1,
            rank_id=1,
            car_id=10,
            car_name="Car2",
            mvp=True,
            start_time=0,
            end_time=300,
        ),
        MatchParticipation(
            id="3",
            match_team_id=1,
            player_id=1,
            rank_id=1,
            car_id=10,
            car_name="Car3",
            mvp=True,
            start_time=0,
            end_time=300,
        ),
    ]
    service = MatchParticipationService()
    service.match_participation_dao.get_matches_by_parameter = MagicMock(
        return_value=participations
    )
    # WHEN
    result = service.get_most_used_cars(PLAYER, 2)
    # THEN
    assert len(result) == 2


def test_get_most_used_cars_no_participations():
    """Aucune participation -> None."""
    # GIVEN
    service = MatchParticipationService()
    service.match_participation_dao.get_matches_by_parameter = MagicMock(
        return_value=None
    )
    # WHEN
    result = service.get_most_used_cars(PLAYER)
    # THEN
    assert result is None


def test_get_most_used_cars_no_player_id():
    """Joueur sans ID -> ValueError."""
    # GIVEN
    player = Player(
        id=None,
        platform_id=2,
        platform_user_id="Steam_2",
        name="TestPlayer",
    )
    service = MatchParticipationService()
    # WHEN / THEN
    with pytest.raises(ValueError, match="Le joueur doit avoir un ID valide"):
        service.get_most_used_cars(player)


def test_get_most_used_cars_invalid_limit():
    """Limite invalide -> ValueError."""
    # GIVEN
    service = MatchParticipationService()
    # WHEN / THEN
    with pytest.raises(ValueError, match="La limite doit être supérieure à 0"):
        service.get_most_used_cars(PLAYER, 0)
