from fastapi import APIRouter, HTTPException, Path

from src.api.schemas.global_stats import AverageStatsResponse
from src.service.stats_core_service import StatsCoreService


router = APIRouter(prefix="/global", tags=["Global Statistics"])

stats_service = StatsCoreService()


@router.get(
    "/average-stats/rank/{rank_name}",
    response_model=AverageStatsResponse,
    summary="Récupère le pourcentage de tir moyen par rang",
    description="Retourne le pourcentage de tir moyen pour un rang donné",
)
def get_average_stats_by_rank(
    rank_name: str = Path(
        ...,
        description="Le nom du rang (tier p division q)",
        examples="Gold III Division I",
    ),
):
    """
    Endpoint pour récupérer la moyenne des statistiques d'un rang.

    Parameters
    ----------
    rank_name: str
        Le nom du rang (passé dans l'URL)

    Returns
    -------
        JSON avec le pourcentage moyen ou une erreur

    Raises
    ------
        HTTPException 400: Si le nom du rang est invalide
        HTTPException 404: Si aucune donnée n'existe pour ce rang
        HTTPException 500: Erreur serveur

    Examples
    --------
        GET /api/stats/shooting-percentage/rank/Gold III
        GET /api/stats/shooting-percentage/rank/Platinum II
    """
    try:
        stats = stats_service.get_average_stats_by_rank_name(rank_name)

        if stats is None:
            raise HTTPException(
                status_code=404,
                detail=f"Aucune donnée trouvée pour le rang '{rank_name}'",
            )
        avg_percentage = stats["avg_shooting"] * 100
        avg_saves = stats["avg_saves"] * 100
        avg_assists = stats["avg_assists"] * 100
        avg_demo_inflicted = stats["demo_inflicted"] * 100
        avg_demo_taken = stats["demo_taken"] * 100

        return AverageStatsResponse(
            success=True,
            message="Statistiques globales récupérées avec succès",
            data={
                "rank_name": rank_name,
                "number_matches": stats["nb_matches"],
                "shooting_accuracy": round(avg_percentage, 2),
                "average_saves": round(avg_saves, 2),
                "average_assists": round(avg_assists, 2),
                "average_demolition_inflicted": round(avg_demo_inflicted, 2),
                "average_demolition_taken": round(avg_demo_taken, 2),
            },
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur serveur lors de la récupération des statistiques: {str(e)}",
        ) from e
