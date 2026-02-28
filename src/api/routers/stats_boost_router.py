# src/api/routes/stats_boost_router.py
from fastapi import APIRouter, HTTPException, status

from src.api.schemas.stats_response import (
    StatsByPlayerMatchResponse,
    StatsByPlayerResponse,
    StatsByRankResponse,
    StatsResponseFactory,
    StatsType,
)
from src.dto.stats_boost_dto import StatsBoostDTO
from src.models.ranks import Ranks
from src.service.matches_service import MatchService
from src.service.players_service import PlayerService
from src.service.stats_boost_service import StatBoostService
from src.utils.enumeration import Ranks_enum


router = APIRouter(prefix="/statsboost", tags=["Boost Statistics"])

stats_boost_service = StatBoostService()
player_service = PlayerService()
match_service = MatchService()


@router.get(
    "/rank/{rank}",
    response_model=StatsByRankResponse,
    summary="Récupère les statistiques de boost moyennes par rang",
)
def get_rank_statistics(rank_name: Ranks_enum) -> StatsByRankResponse:
    """
    Récupère les statistiques de boost moyennes pour un rang donné.

    Parameters
    ----------
    rank_name : Ranks_enum
        Le nom du rang pour lequel on souhaite obtenir les statistiques.

    Returns
    -------
    StatsByRankResponse
        La réponse contenant un StatsBoostAggregatedDTO dans le champ data.

    Raises
    ------
    HTTPException
        404 si aucune donnée n'est trouvée pour le rang spécifié.
    """
    rank = Ranks(name=rank_name)

    # Service retourne directement StatsBoostAggregatedDTO
    stats_dto = stats_boost_service.get_average_stats_boost_by_rank(rank)

    if stats_dto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucune donnée trouvée pour le rang '{rank_name}'",
        )

    # Pas besoin de conversion, c'est déjà un DTO
    return StatsResponseFactory.create_rank_response(
        rank=rank_name,
        stats_type=StatsType.BOOST,
        data=stats_dto,
    )


@router.get(
    "/player/{platform_id}/averageboost",
    response_model=StatsByPlayerResponse,
    summary="Récupère les statistiques de boost moyennes d'un joueur",
)
def get_player_average_statistics(platform_id: str) -> StatsByPlayerResponse:
    """
    Récupère les statistiques de boost moyennes d'un joueur sur tous ses matchs.

    Parameters
    ----------
    platform_id : str
        L'identifiant unique du joueur sur sa plateforme de jeu.

    Returns
    -------
    StatsByPlayerResponse
        La réponse contenant un StatsBoostAggregatedDTO dans le champ data.

    Raises
    ------
    HTTPException
        404 si le joueur est introuvable ou si aucune statistique n'est trouvée.
    """
    player = player_service.get_player_by_platform_id(platform_id)

    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Joueur introuvable"
        )

    # Service retourne directement StatsBoostAggregatedDTO
    stats_dto = stats_boost_service.get_player_average_boost_stats(player)

    if stats_dto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucune statistique trouvée pour ce joueur",
        )

    # Pas besoin de conversion, c'est déjà un DTO
    return StatsResponseFactory.create_player_response(
        platform_id=platform_id, stats_type=StatsType.BOOST, data=stats_dto
    )


@router.get(
    "/player/{platform_id}/match/{match_id}",
    response_model=StatsByPlayerMatchResponse,
    summary="Récupère les statistiques de boost d'un joueur dans un match",
)
def get_player_match_statistics(
    platform_id: str, match_id: str
) -> StatsByPlayerMatchResponse:
    """
    Récupère les statistiques de boost d'un joueur pour un match spécifique.

    Parameters
    ----------
    platform_id : str
        L'identifiant unique du joueur sur sa plateforme de jeu.
    match_id : str
        L'identifiant unique du match.

    Returns
    -------
    StatsByPlayerMatchResponse
        La réponse contenant un StatsBoostDTO dans le champ data.

    Raises
    ------
    HTTPException
        404 si le joueur, le match ou les statistiques sont introuvables.
    """
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

    # Service retourne un Business Object (StatsBoost)
    stats_bo = stats_boost_service.get_player_match_boost_stats(player, match)

    if stats_bo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucune statistique trouvée pour ce joueur dans ce match",
        )

    # Conversion BO -> DTO
    stats_dto = StatsBoostDTO.from_business_object(stats_bo)

    return StatsResponseFactory.create_player_match_response(
        platform_id=platform_id,
        match_id=match_id,
        stats_type=StatsType.BOOST,
        data=stats_dto,
    )
