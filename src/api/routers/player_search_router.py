from fastapi import APIRouter, HTTPException

from src.service.collector.update import run_full_update


router = APIRouter(prefix="/global", tags=["Player research"])


@router.get(
    "/player-research-update/",
    response_model=None,
    summary="Récupère le pourcentage de tir moyen par rang",
    description="Retourne le pourcentage de tir moyen pour un rang donné",
)
def update_player(
    player_platform: str | None = None,
    player_id: str | None = None,
    player_exact_name: str | None = None,
    game_count: int = 1,
):
    """
    Endpoint pour mettre à jour les informations d'un joueur. Cette fonction
    télécharge les dernières parties jouées par un joueur selon son ID et sa plateforme
    ou son pseudo et les ajoute à la DB.

    PS : Soit on rempli player_id et player_platform soit on rempli player_exact_name

    Parameters
    ----------
    player_platform: Optional[str] = None
        La plateforme de l'utilisateur recherché

    player_id: Optional[str] = None
        L'id sur la plateforme de l'utilisateur

    player_exact_name: Optional[str] = None
        Le pseudo exact de l'utilisateur

    Returns
    -------
        Bool : Réussite / Echec

    Raises
    ------
        HTTPException 400: Si le nom du joueur n'est pas unique
        HTTPException 404: Si le pseudo du joueur/la plateforme/l'id du
            joueur n'existe pas
        HTTPException 500: Erreur serveur

    Examples
    --------
        GET /api/stats/shooting-percentage/rank/Gold III
        GET /api/stats/shooting-percentage/rank/Platinum II
    """
    player_exact_id = None
    if player_id is not None:
        player_exact_id = f"{player_platform}={player_id}"

    try:
        update = run_full_update(player_exact_name, player_exact_id, game_count)

        if update is None:
            raise HTTPException(
                status_code=404,
                detail="Aucune donnée trouvée pour le joueur sélectionné",
            )

        return update

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur serveur lors de la récupération des statistiques: {str(e)}",
        ) from e
