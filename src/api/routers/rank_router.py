from fastapi import APIRouter, HTTPException

from src.service.players_service import PlayerService
from src.service.ranks_service import RanksService


router = APIRouter(prefix="/player", tags=["Rank"])

rank_service = RanksService()
player_service = PlayerService()


@router.get(
    "/player/{platform_id}/rank",
    summary="Récupère le rang d'un joueur",
)
def get_player_rank(platform_id: str):
    """
    Récupère le rang actuel d'un joueur par son platform_id.
    """
    try:
        player = player_service.get_player_by_platform_id(platform_id)

        if player is None:
            raise HTTPException(
                status_code=404,
                detail=f"Joueur non trouvé avec platform_id: {platform_id}",
            )

        rank_info = rank_service.get_player_rank_by_platform_id(platform_id)

        if rank_info is None:
            return {
                "player_name": player.name,
                "platform_id": platform_id,
                "rank": "Unranked",
            }

        return {
            "player_name": player.name,
            "platform_id": platform_id,
            "rank": rank_info["name"],  # "Bronze I"
            "full_rank": rank_info["full_name"],  # "Bronze I Division 1"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}") from e
