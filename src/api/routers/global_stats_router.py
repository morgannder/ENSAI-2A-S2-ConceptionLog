from fastapi import APIRouter, HTTPException

from src.api.schemas.global_stats import AverageStatsResponse
from src.service.stats_core_service import StatsCoreService
from src.utils.enumeration import Ranks


router = APIRouter(prefix="/global", tags=["Global Statistics"])

stats_service = StatsCoreService()


@router.get(
    "/stats/{rank}",
    response_model=AverageStatsResponse,
    summary="Récupère des statistiques globales par rang",
    description="Retourne des statistiques globales pour un rang donné",
)
def get_average_stats_by_rank(
    rank: Ranks,
) -> AverageStatsResponse:
    """
    Endpoint pour récupérer la moyenne des statistiques d'un rang.

    Parameters
    ----------
    rank: Ranks
        Le nom du rang (tier).

    Returns
    -------
        JSON contenant les statistiques.

    Raises
    ------
        HTTPException 404: Si aucune donnée n'existe pour ce rang
        HTTPException 500: Erreur serveur
    """

    try:
        stats = stats_service.get_average_stats_by_rank_name(rank)

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

        return AverageStatsResponse(
            message="Statistiques globales récupérées avec succès",
            data={
                "rank name": rank,
                "number of matches": stats["nb_matches"],
                "shooting accuracy": round(avg_percentage, 2),
                "average saves": round(avg_saves, 2),
                "average assists": round(avg_assists, 2),
                "average demolition_inflicted": round(avg_demo_inflicted, 2),
                "average demolition_taken": round(avg_demo_taken, 2),
            },
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur serveur lors de la récupération des statistiques: {str(e)}",
        ) from e
