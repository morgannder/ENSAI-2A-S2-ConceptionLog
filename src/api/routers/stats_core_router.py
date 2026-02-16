from fastapi import APIRouter, HTTPException, status

from src.api.schemas.stats_response import (
    StatsByPlayerMatchResponse,
    StatsByPlayerResponse,
    StatsByRankResponse,
)
from src.service.matches_service import MatchService
from src.service.players_service import PlayerService
from src.service.stats_core_service import StatsCoreService
from src.utils.enumeration import Ranks_enum


router = APIRouter(prefix="/statscore", tags=["Core Statistics"])

stats_core_service = StatsCoreService()
matches_service = MatchService()
player_service = PlayerService()


@router.get(
    "/{rank}",
    response_model=StatsByRankResponse,
    summary="Récupère le total des statistiques Core par rang",
    description="Retourne des statistiques Core pour un rang donné",
)
def get_stats_core_by_rank(
    rank: Ranks_enum,
) -> StatsByRankResponse:
    """
    Endpoint pour récupérer les statistiques Core d'un rang.

    Parameters
    ----------
    rank: Ranks
        Le nom du rang (tier).

    Returns
    -------
        JSON contenant les statistiques core.

    Raises
    ------
        HTTPException 404: Si aucune donnée n'existe pour ce rang
        HTTPException 500: Erreur serveur
    """

    try:
        stats = stats_core_service.get_stats_core_by_rank_name(rank)

        if stats is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aucune donnée trouvée pour le rang '{rank}'",
            )

        return StatsByRankResponse(rank=rank, data=stats)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur serveur lors de la récupération des statistiques core: {str(e)}",
        ) from e


@router.get(
    "/average/{rank}",
    response_model=StatsByRankResponse,
    summary="Récupère les statistiques Core moyennes par rang",
    description="Retourne des statistiques Core moyennes pour un rang donné",
)
def get_average_stats_core_by_rank(
    rank: Ranks_enum,
) -> StatsByRankResponse:
    """
    Endpoint pour récupérer la moyenne des statistiques Core d'un rang.

    Parameters
    ----------
    rank: Ranks
        Le nom du rang (tier).

    Returns
    -------
        JSON contenant les statistiques core.

    Raises
    ------
        HTTPException 404: Si aucune donnée n'existe pour ce rang
        HTTPException 500: Erreur serveur
    """

    try:
        stats = stats_core_service.get_average_stats_core_by_rank_name(rank)

        if stats is None:
            raise HTTPException(
                status_code=404,
                detail=f"Aucune donnée trouvée pour le rang '{rank}'",
            )

        avg_percentage = stats["avg_shooting"] * 100
        avg_saves = stats["avg_saves"]
        avg_assists = stats["avg_assists"]
        avg_demo_inflicted = stats["demo_inflicted"]
        avg_demo_taken = stats["demo_taken"]

        return StatsByRankResponse(
            rank=rank,
            data={
                "players": stats["nb_players"],
                "shooting_accuracy": round(avg_percentage, 2),
                "avg_saves": round(avg_saves, 2),
                "avg_assists": round(avg_assists, 2),
                "avg_demolition_inflicted": round(avg_demo_inflicted, 2),
                "avg_demolition_taken": round(avg_demo_taken, 2),
            },
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur serveur lors de la récupération des statistiques core: {str(e)}",
        ) from e


@router.get(
    "/player/{player_id}/averagecore",
    response_model=StatsByPlayerResponse,
    summary="Récupère les statistiques core moyennes d'un joueur",
)
def get_player_average_statistics(platform_id: str) -> StatsByPlayerResponse:
    """
    Doc.
    """
    player = player_service.get_player_by_platform_id(platform_id)

    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Joueur introuvable"
        )

    stats = stats_core_service.get_player_average_stats_core(player)

    if stats is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucune statistique core trouvée pour ce joueur",
        )

    return StatsByPlayerResponse(platform_id=platform_id, data=stats)


@router.get(
    "/player/{player_id}/match/{match_id}",
    response_model=StatsByPlayerMatchResponse,
    summary="Récupère les statistiques core d'un joueur dans un match",
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

    match = matches_service.get_match_by_id(match_id)
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Match introuvable"
        )

    stats = stats_core_service.get_player_match_stats_core(player, match)

    if stats is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Erreur serveur lors de la récupération des statistiques core",
        )

    return StatsByPlayerMatchResponse(
        platform_id=platform_id, match_id=match_id, data=stats.to_dict()
    )
