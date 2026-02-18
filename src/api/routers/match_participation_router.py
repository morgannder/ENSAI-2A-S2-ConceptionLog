from fastapi import APIRouter, HTTPException, status

from src.service.match_participation_service import MatchParticipationService
from src.service.players_service import PlayerService


router = APIRouter(prefix="/participation", tags=["Match Participation"])

participation_service = MatchParticipationService()
player_service = PlayerService()


'''@router.get("/{participation_id}", status_code=status.HTTP_200_OK)
def get_participation_statistics(participation_id: str):
    """
    Récupère les statistiques détaillées d'une participation.

    Parameters
    ----------
    participation_id : str
        L'identifiant de la participation.

    Returns
    -------
    dict
        Les statistiques de la participation.

    Raises
    ------
    HTTPException
        404 si la participation n'existe pas.
    """
    stats = participation_service.get_participation_statistics(participation_id)
    if stats is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Participation {participation_id} non trouvée",
        )
    return stats'''


@router.get(
    "/player/{platform_user_id}/recent",
    summary="Récupère les participations récentes d'un joueur",
    status_code=status.HTTP_200_OK,
)
def get_player_recent_participations(platform_user_id: str, limit: int = 20):
    """
    Récupère les participations récentes d'un joueur.

    Parameters
    ----------
    platform_user_id : str
        L'identifiant de plateforme du joueur.
    limit : int, optional
        Nombre de participations à récupérer (par défaut: 20).

    Returns
    -------
    list
        Liste des participations récentes du joueur.

    Raises
    ------
    HTTPException
        400 si le platform_user_id est invalide ou si limit est invalide.
        404 si le joueur ou ses participations n'existent pas.
    """
    try:
        player = player_service.get_player_by_platform_id(platform_user_id)
        if player is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Joueur avec platform_user_id '{platform_user_id}' non trouvé",
            )

        participations = participation_service.get_player_recent_participations(
            player, limit
        )
        if participations is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aucune participation trouvée pour le joueur '{platform_user_id}'",
            )
        return participations
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get(
    "/player/{platform_user_id}/mvp",
    summary="Récupère toutes les participations MVP d'un joueur",
    status_code=status.HTTP_200_OK,
)
def get_player_mvp_participations(platform_user_id: str):
    """
    Récupère toutes les participations MVP d'un joueur.

    Parameters
    ----------
    platform_user_id : str
        L'identifiant de plateforme du joueur.

    Returns
    -------
    list
        Liste des participations MVP du joueur.

    Raises
    ------
    HTTPException
        400 si le platform_user_id est invalide.
        404 si le joueur ou ses participations MVP n'existent pas.
    """
    try:
        player = player_service.get_player_by_platform_id(platform_user_id)
        if player is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Joueur avec platform_user_id '{platform_user_id}' non trouvé",
            )

        mvp_participations = participation_service.get_player_mvp_participations(player)
        if mvp_participations is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aucune participation MVP trouvée pour le joueur '{platform_user_id}'",
            )
        return mvp_participations
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get(
    "/player/{platform_user_id}/mvp/count",
    summary="Récupère le nombre de MVP d'un joueur",
    status_code=status.HTTP_200_OK,
)
def get_player_mvp_count(platform_user_id: str):
    """
    Récupère le nombre de MVP d'un joueur.

    Parameters
    ----------
    platform_user_id : str
        L'identifiant de plateforme du joueur.

    Returns
    -------
    dict
        Dictionnaire contenant le nombre de MVP.

    Raises
    ------
    HTTPException
        400 si le platform_user_id est invalide.
        404 si le joueur n'existe pas.
    """
    try:
        player = player_service.get_player_by_platform_id(platform_user_id)
        if player is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Joueur avec platform_user_id '{platform_user_id}' non trouvé",
            )

        mvp_count = participation_service.get_player_mvp_count(player)
        return {"platform_user_id": platform_user_id, "mvp_count": mvp_count}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get(
    "/player/{platform_user_id}/mvp/rate",
    summary="Calcule le taux de MVP d'un joueur",
    status_code=status.HTTP_200_OK,
)
def get_player_mvp_rate(platform_user_id: str):
    """
    Calcule le taux de MVP d'un joueur.

    Parameters
    ----------
    platform_user_id : str
        L'identifiant de plateforme du joueur.

    Returns
    -------
    dict
        Dictionnaire contenant le taux de MVP en pourcentage.

    Raises
    ------
    HTTPException
        400 si le platform_user_id est invalide.
        404 si le joueur n'existe pas ou n'a aucune participation.
    """
    try:
        player = player_service.get_player_by_platform_id(platform_user_id)
        if player is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Joueur avec platform_user_id '{platform_user_id}' non trouvé",
            )

        mvp_rate = participation_service.get_player_mvp_rate(player)
        if mvp_rate is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aucune participation trouvée pour le joueur '{platform_user_id}'",
            )
        return {"platform_user_id": platform_user_id, "mvp_rate": mvp_rate}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get(
    "/player/{platform_user_id}/cars",
    summary="Récupère les voitures les plus utilisées par un joueur",
    status_code=status.HTTP_200_OK,
)
def get_player_most_used_cars(platform_user_id: str, limit: int = 5):
    """
    Récupère les voitures les plus utilisées par un joueur.

    Parameters
    ----------
    platform_user_id : str
        L'identifiant de plateforme du joueur.
    limit : int, optional
        Nombre de voitures à retourner (par défaut: 5).

    Returns
    -------
    dict
        Dictionnaire {car_name: count} des voitures les plus utilisées.

    Raises
    ------
    HTTPException
        400 si le platform_user_id ou limit est invalide.
        404 si le joueur n'existe pas ou n'a aucune participation.
    """
    try:
        player = player_service.get_player_by_platform_id(platform_user_id)
        if player is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Joueur avec platform_user_id '{platform_user_id}' non trouvé",
            )

        most_used_cars = participation_service.get_most_used_cars(player, limit)
        if most_used_cars is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aucune participation trouvée pour le joueur '{platform_user_id}'",
            )
        return {"platform_user_id": platform_user_id, "most_used_cars": most_used_cars}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


'''@router.get("/team/{match_team_id}", status_code=status.HTTP_200_OK)
def get_participations_by_team(match_team_id: str):
    """
    Récupère toutes les participations d'une équipe.

    Parameters
    ----------
    match_team_id : str
        L'identifiant de l'équipe de match.

    Returns
    -------
    list
        Liste des participations de l'équipe.

    Raises
    ------
    HTTPException
        404 si aucune participation n'est trouvée pour l'équipe.
    """
    participations = participation_service.get_participations_by_team(match_team_id)
    if participations is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucune participation trouvée pour l'équipe {match_team_id}",
        )
    return participations'''


'''@router.get("/rank/{rank_id}", status_code=status.HTTP_200_OK)
def get_participations_by_rank(rank_id: int):
    """
    Récupère toutes les participations d'un rang.

    Parameters
    ----------
    rank_id : int
        L'identifiant du rang.

    Returns
    -------
    list
        Liste des participations du rang.

    Raises
    ------
    HTTPException
        404 si aucune participation n'est trouvée pour le rang.
    """
    participations = participation_service.get_participations_by_rank(rank_id)
    if participations is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucune participation trouvée pour le rang {rank_id}",
        )
    return participations'''


'''@router.get("/car/{car_id}", status_code=status.HTTP_200_OK)
def get_participations_by_car(car_id: int):
    """
    Récupère toutes les participations avec une voiture donnée.

    Parameters
    ----------
    car_id : int
        L'identifiant de la voiture.

    Returns
    -------
    list
        Liste des participations avec cette voiture.

    Raises
    ------
    HTTPException
        404 si aucune participation n'est trouvée pour la voiture.
    """
    participations = participation_service.get_participations_by_car(car_id)
    if participations is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucune participation trouvée pour la voiture {car_id}",
        )
    return participations'''
