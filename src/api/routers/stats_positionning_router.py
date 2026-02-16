from fastapi import APIRouter, HTTPException, status

from src.api.schemas.stats_response import (
    StatsByPlayerMatchResponse,
    StatsByPlayerResponse,
    StatsByRankResponse,
)
from src.models.ranks import Ranks
from src.service.matches_service import MatchService
from src.service.players_service import PlayerService
from src.service.stats_positionning_service import StatPositionningService
from src.utils.enumeration import Ranks_enum


router = APIRouter(prefix="/statspositionning", tags=["Positionning Statistics"])

stats_positionning_service = StatPositionningService()
player_service = PlayerService()
match_service = MatchService()


@router.get(
    "/rank/{rank}",
    summary="Récupère les statistiques de positionning moyennes par rang",
)
def get_rank_statistics(rank_name: Ranks_enum):
    """doc."""

    rank = Ranks(name=rank_name)
    stats = stats_positionning_service.get_rank_positionning_statistics(rank)

    if stats is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucune donnée trouvée pour le rang '{rank_name}'",
        )

    return StatsByRankResponse(rank=rank_name, data=stats)


@router.get(
    "/player/{player_id}/averagepositionning",
    summary="Récupère les statistiques de positionning moyennes d'un joueur",
)
def get_player_average_statistics(platform_id: str):
    """
    Doc.
    """
    player = player_service.get_player_by_platform_id(platform_id)

    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Joueur introuvable"
        )

    stats = stats_positionning_service.get_player_average_positionning_stats(player)

    if stats is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucune statistique trouvée pour ce joueur",
        )

    return StatsByPlayerResponse(platform_id=platform_id, data=stats)


@router.get(
    "/player/{player_id}/match/{match_id}",
    summary="Récupère les statistiques de positionning d'un joueur dans un match",
)
def get_player_match_statistics(
    platform_id: str, match_id: str
) -> StatsByPlayerMatchResponse:
    """doc."""
    player = player_service.get_player_by_platform_id(platform_id)
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Joueur introuvable"
        )

    match = match_service.get_match_by_id(match_id)
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Match introuvable"
        )

    stats = stats_positionning_service.get_player_match_positionning_stats(
        player, match
    )

    if stats is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucune statistique trouvée pour ce joueur dans ce match",
        )

    return StatsByPlayerMatchResponse(
        platform_id=platform_id, match_id=match_id, data=stats.to_dict()
    )
