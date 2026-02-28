from enum import Enum

from pydantic import BaseModel

from src.dto.stats_boost_dto import StatsBoostAggregatedDTO, StatsBoostDTO
from src.dto.stats_core_dto import StatsCoreAggregatedDTO, StatsCoreDTO
from src.dto.stats_movement_dto import (
    StatsMovementAggregatedDTO,
    StatsMovementDTO,
)
from src.dto.stats_positioning_dto import (
    StatsPositioningAggregatedDTO,
    StatsPositioningDTO,
)


class StatsType(str, Enum):
    CORE = "core"
    BOOST = "boost"
    MOVEMENT = "movement"
    POSITIONING = "positioning"


# Union de tous les DTOs (individuels et agrégés) avec "|"
StatsDataDTO = (
    StatsCoreDTO
    | StatsCoreAggregatedDTO
    | StatsBoostDTO
    | StatsBoostAggregatedDTO
    | StatsMovementDTO
    | StatsMovementAggregatedDTO
    | StatsPositioningDTO
    | StatsPositioningAggregatedDTO
)


class StatsByRankResponse(BaseModel):
    rank: str
    stats_type: StatsType
    data: StatsDataDTO | None = None


class StatsByPlayerMatchResponse(BaseModel):
    platform_id: str
    match_id: str
    stats_type: StatsType
    data: StatsDataDTO | None = None


class StatsByPlayerResponse(BaseModel):
    platform_id: str
    stats_type: StatsType
    data: StatsDataDTO | None = None


# Factory pour créer les réponses
class StatsResponseFactory:
    @staticmethod
    def create_rank_response(
        rank: str,
        stats_type: StatsType,
        data: StatsDataDTO,
    ) -> StatsByRankResponse:
        """Crée une réponse de statistiques par rang."""
        return StatsByRankResponse(rank=rank, stats_type=stats_type, data=data)

    @staticmethod
    def create_player_match_response(
        platform_id: str,
        match_id: str,
        stats_type: StatsType,
        data: StatsDataDTO,
    ) -> StatsByPlayerMatchResponse:
        """Crée une réponse de statistiques par joueur et match."""
        return StatsByPlayerMatchResponse(
            platform_id=platform_id, match_id=match_id, stats_type=stats_type, data=data
        )

    @staticmethod
    def create_player_response(
        platform_id: str,
        stats_type: StatsType,
        data: StatsDataDTO,
    ) -> StatsByPlayerResponse:
        """Crée une réponse de statistiques par joueur."""
        return StatsByPlayerResponse(
            platform_id=platform_id, stats_type=stats_type, data=data
        )
