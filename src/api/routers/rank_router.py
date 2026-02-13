from fastapi import APIRouter, HTTPException

from src.service.players_service import PlayerService
from src.service.ranks_service import RanksService


router = APIRouter(prefix="/player", tags=["Rank"])

rank_service = RanksService()
player_service = PlayerService()


@router.get("/{player_id}/rank")
def get_player_rank(platform_id: str):
    """
    Récupère le rang actuel d'un joueur par son platform_id.
    """
    try:
        rank = rank_service.get_player_rank_by_platform_id(platform_id)
        player_name = player_service.get_player_by_platform_id(platform_id).name
        rank_name = "Unranked" if rank is None else rank.name

        return {
            "player_name": player_name,
            "platform_id": platform_id,
            "rank": rank_name,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except AttributeError as e:
        raise HTTPException(
            status_code=404, detail="Rang non trouvé pour ce joueur"
        ) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}") from e
