from fastapi import APIRouter, HTTPException, status

from src.api.schemas.examples.core_examples import (
    CORE_AGGREGATED_BY_MATCH_DATA_EXAMPLE,
    CORE_AGGREGATED_BY_RANK_DATA_EXAMPLE,
    CORE_AGGREGATED_PLAYER_DATA_EXAMPLE,
)
from src.api.schemas.stats_response import (
    StatsByPlayerMatchResponse,
    StatsByPlayerResponse,
    StatsByRankResponse,
    StatsResponseFactory,
    StatsType,
)
from src.dto.stats_core_dto import StatsCoreDTO
from src.models.ranks import Ranks
from src.service.matches_service import MatchService
from src.service.players_service import PlayerService
from src.service.stats_core_service import StatsCoreService
from src.utils.enumeration import GameMode_enum, Ranks_enum


router = APIRouter(prefix="/statscore", tags=["Core Statistics"])

stats_core_service = StatsCoreService()
matches_service = MatchService()
player_service = PlayerService()


@router.get(
    "/average/{rank}",
    response_model=StatsByRankResponse,
    summary="Récupère les statistiques Core moyennes par rang",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": CORE_AGGREGATED_BY_RANK_DATA_EXAMPLE
                    }
                }
            }
        }
    },
)
def get_average_stats_core_by_rank(
    rank_name: Ranks_enum,
    game_mode: GameMode_enum | None = None,
) -> StatsByRankResponse:
    """
    Récupère les statistiques de jeu moyennes pour un rang donné.

    Parameters
    ----------
    rank_name : Ranks_enum
        Le nom du rang pour lequel on souhaite obtenir les statistiques.
    game_mode : GameMode_enum | None, optional
        Le mode de jeu sur lequel filtrer, par défaut None (tous les modes).

    Returns
    -------
    StatsByRankResponse
        La réponse contenant un StatsCoreAggregatedDTO dans le champ data.

    Raises
    ------
    HTTPException
        404 si aucune donnée n'est trouvée pour le rang spécifié.
        500 en cas d'erreur serveur.
    """
    rank = Ranks(name=rank_name)

    try:
        # Service retourne directement StatsBoostAggregatedDTO
        stats_dto = stats_core_service.get_average_stats_core_by_rank(rank, game_mode)

        if stats_dto is None:
            raise HTTPException(
                status_code=404,
                detail=f"Aucune donnée trouvée pour le rang '{rank_name}'",
            )

        # Pas besoin de conversion, c'est déjà un DTO
        return StatsResponseFactory.create_rank_response(
            game_mode=game_mode,
            rank=rank_name,
            stats_type=StatsType.CORE,
            data=stats_dto,
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur serveur lors de la récupération des statistiques core: {str(e)}",
        ) from e


@router.get(
    "/player/{player_id}/averagecore",
    response_model=StatsByPlayerResponse,
    summary="Récupère les statistiques core moyennes d'un joueur",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {"example": CORE_AGGREGATED_PLAYER_DATA_EXAMPLE}
                }
            }
        }
    },
)
def get_player_average_statistics(
    platform_id: str,
    game_mode: GameMode_enum | None = None,
) -> StatsByPlayerResponse:
    """
    Récupère les statistiques de jeu moyennes d'un joueur sur tous ses matchs.

    Parameters
    ----------
    platform_id : str
        L'identifiant unique du joueur sur sa plateforme de jeu.
    game_mode : GameMode_enum | None, optional
        Le mode de jeu sur lequel filtrer, par défaut None (tous les modes).

    Returns
    -------
    StatsByPlayerResponse
        La réponse contenant un StatsCoreAggregatedDTO dans le champ data.

    Raises
    ------
    HTTPException
        404 si le joueur est introuvable ou si aucune statistique n'est trouvée.
        500 en cas d'erreur serveur.
    """
    try:
        player = player_service.get_player_by_platform_id(platform_id)

        if player is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Joueur introuvable"
            )

        # Service retourne directement StatsBoostAggregatedDTO
        stats_dto = stats_core_service.get_player_average_stats_core(player, game_mode)

        if stats_dto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aucune statistique core trouvée pour ce joueur",
            )

        # Pas besoin de conversion, c'est déjà un DTO
        return StatsResponseFactory.create_player_response(
            game_mode=game_mode,
            platform_id=platform_id,
            stats_type=StatsType.CORE,
            data=stats_dto,
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur serveur : {str(e)}",
        ) from e


@router.get(
    "/player/{player_id}/match/{match_id}",
    response_model=StatsByPlayerMatchResponse,
    summary="Récupère les statistiques core d'un joueur dans un match",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": CORE_AGGREGATED_BY_MATCH_DATA_EXAMPLE
                    }
                }
            }
        }
    },
)
def get_player_match_statistics(
    platform_id: str,
    match_id: str,
    game_mode: GameMode_enum | None = None,
) -> StatsByPlayerMatchResponse:
    """
    Récupère les statistiques de jeu d'un joueur pour un match spécifique.

    Parameters
    ----------
    platform_id : str
        L'identifiant unique du joueur sur sa plateforme de jeu.
    match_id : str
        L'identifiant unique du match.
    game_mode : GameMode_enum | None, optional
        Le mode de jeu sur lequel filtrer, par défaut None (tous les modes).

    Returns
    -------
    StatsByPlayerMatchResponse
        La réponse contenant un StatsCoreDTO dans le champ data.

    Raises
    ------
    HTTPException
        404 si le joueur, le match ou les statistiques sont introuvables.
        500 en cas d'erreur serveur.
    """
    try:
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

        # Service retourne un Business Object (StatsPositioning)
        stats_bo = stats_core_service.get_player_match_stats_core(
            player, match, game_mode
        )

        if stats_bo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aucune statistique trouvée pour ce joueur dans ce match",
            )

        # Conversion BO -> DTO
        stats_dto = StatsCoreDTO.from_business_object(stats_bo)

        return StatsResponseFactory.create_player_match_response(
            game_mode=game_mode,
            platform_id=platform_id,
            match_id=match_id,
            stats_type=StatsType.CORE,
            data=stats_dto,
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur serveur : {str(e)}",
        ) from e
