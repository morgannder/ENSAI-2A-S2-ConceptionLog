from fastapi import APIRouter, HTTPException, status

from src.service.collector.update import run_full_update
from src.service.players_service import PlayerService
from src.utils.enumeration import Platform_enum


router = APIRouter(prefix="/global", tags=["Player research"])
player_service = PlayerService()


@router.get(
    "/player-research-update/",
    response_model=None,
    summary="Update player in DB",
    description="Retourne la réussite ou l'échec de l'actualisation des parties d'un "
    "joueur dans la DB. Prend en argument au choix : "
    "\n- Une plateforme et un ID associé"
    "\n- Un pseudo exact"
    "\n- Un compteur qui correspond au nombre de match maximum que l'on peut télécharger "
    "(max 200)"
    "\n- Une date au format ISO-8601 : YYY-MM-DDTHH:MM:SSZ",
)
def update_player(
    player_platform: Platform_enum | None = None,
    player_id: str | None = None,
    player_exact_pseudo: str | None = None,
    game_count: int = 1,
    created_after: str = "2024-01-01T00:00:00Z",
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

    player_exact_pseudo: Optional[str] = None
        Le pseudo exact de l'utilisateur

    game_count: int
        Number of games requested to ballchasing API

    created_after: str = "2024-01-01T00:00:00Z"
        Date de création du replay de la partie sur Ballchasing API.
        Format : ISO-8601
        Date : YYY-MM-DDTHH:MM:SSZ
        Après le "T" dans le format -> Indique la timezone à la base UTC
        (ex : UTC+1 -> T01:00:00Z)

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
        GET /api/global/player-research-update/?player_exact_name=Player&game_count=1
        GET /api/global/player-research-update/?player_platform=epic&player_id=5273935696c041b28fc021eb9a0ef852&game_count=10

    """
    player_exact_id = None
    if player_platform is not None or player_id is not None:
        if not player_platform or not player_id:
            raise HTTPException(
                status_code=400,
                detail="Pour une recherche par ID, vous devez fournir à la fois la plateforme ET l'ID.",
            )

        player_exact_id = f"{player_platform}:{player_id}"

    elif not player_exact_pseudo:
        print(f"Loading of the {game_count} most recent matches")

    try:
        update = run_full_update(
            player_exact_pseudo, player_exact_id, game_count, created_after
        )

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


@router.get(
    "/search",
    summary="Recherche des joueurs par nom et plateforme",
    status_code=status.HTTP_200_OK,
)
def search_players(
    pseudonym: str, platform: str = None, limit: int = 30, offset: int = 0
):
    """
    longueur de pseudo minimum : 3
    """
    try:
        if len(pseudonym) < 3:
            raise ValueError("La recherche doit contenir au moins 3 caractères")

        results = player_service.search_players(pseudonym, platform, limit, offset)

        return {"query": pseudonym, "platform_filter": platform, "results": results}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
