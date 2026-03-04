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
    Met à jour les informations d'un joueur en téléchargeant ses dernières
    parties depuis l'API Ballchasing et en les ajoutant à la base de données.

    Parameters
    ----------
    player_platform : Platform_enum, optional
        La plateforme du joueur (ex: epic, steam, psn). Doit être fourni
        conjointement avec player_id, par défaut None.
    player_id : str, optional
        L'identifiant du joueur sur sa plateforme. Doit être fourni
        conjointement avec player_platform, par défaut None.
    player_exact_pseudo : str, optional
        Le pseudo exact du joueur, par défaut None.
    game_count : int, optional
        Nombre de parties à télécharger depuis l'API Ballchasing, par défaut 1.
        Maximum 200.
    created_after : str, optional
        Date minimale de création du replay au format ISO-8601
        (YYY-MM-DDTHH:MM:SSZ), par défaut "2024-01-01T00:00:00Z".

    Returns
    -------
    bool
        True si la mise à jour a réussi, False sinon.

    Raises
    ------
    HTTPException
        400 si player_platform et player_id ne sont pas fournis ensemble,
        ou si les paramètres sont invalides.
        404 si aucune donnée n'est trouvée pour le joueur.
        500 en cas d'erreur serveur.

    Examples
    --------
        GET /api/global/player-research-update/?player_exact_pseudo=Player&game_count=1
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
    Recherche des joueurs par nom avec un filtre optionnel sur la plateforme.

    Parameters
    ----------
    pseudonym : str
        Le nom ou fragment de nom à rechercher. Longueur minimale : 3 caractères.
    platform : str, optional
        Le nom de la plateforme sur laquelle filtrer, par défaut None.
    limit : int, optional
        Le nombre maximum de résultats à retourner, par défaut 30.
    offset : int, optional
        Le décalage pour la pagination des résultats, par défaut 0.

    Returns
    -------
    dict
        Un dictionnaire contenant la requête, le filtre de plateforme et
        la liste des joueurs correspondants.

    Raises
    ------
    HTTPException
        400 si le pseudonyme fait moins de 3 caractères.
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
