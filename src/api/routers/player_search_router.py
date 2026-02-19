from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from src.service.collector.update import run_full_update
from src.service.players_service import PlayerService
from src.utils.enumeration import Platform_enum


router = APIRouter(prefix="/global", tags=["Player research"])
player_service = PlayerService()


@router.get(
    "/player-research-update/",
    summary="Update player in DB",
    description="Retourne un flux d'actualisation des parties d'un joueur dans la DB "
    "avec barre de progression. Prend en argument au choix : "
    "\n- Une plateforme et un ID associé"
    "\n- Un pseudo exact"
    "\n- Un compteur (max 200)"
    "\n- Une date au format ISO-8601 : YYY-MM-DDTHH:MM:SSZ",
)
def update_player(
    player_platform: Platform_enum | None = None,
    player_id: str | None = None,
    player_exact_pseudo: str | None = None,
    game_count: int = 1,
    created_after: str = "2024-01-01T00:00:00Z",
):
    player_exact_id = None

    if player_platform is not None or player_id is not None:
        if not player_platform or not player_id:
            raise HTTPException(
                status_code=400,
                detail="Pour une recherche par ID, vous devez fournir à la fois la plateforme ET l'ID.",
            )
        player_exact_id = f"{player_platform.value if hasattr(player_platform, 'value') else player_platform}:{player_id}"
        player_exact_pseudo = None

    elif not player_exact_pseudo:
        raise HTTPException(
            status_code=400,
            detail="Veuillez fournir soit le couple (Plateforme + ID), soit un Pseudo exact.",
        )

    try:
        # On utilise StreamingResponse car run_full_update utilise 'yield'
        return StreamingResponse(
            run_full_update(
                player_exact_pseudo, player_exact_id, game_count, created_after
            ),
            media_type="application/x-ndjson",
        )

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
