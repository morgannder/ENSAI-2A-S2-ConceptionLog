from datetime import datetime
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


class MatchResponse(BaseModel):
    id: str
    playlist_id: str
    season: int
    duration: int
    overtime: int
    date_upload: datetime

    class Config:
        from_attributes = True


class MatchTeamResponse(BaseModel):
    id: int
    match_id: str
    color: str
    score: int
    possession_time: float
    time_in_side: float


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
    game_mode: str | None = None
    rank: str
    stats_type: StatsType
    data: StatsDataDTO | None = None


class StatsByPlayerMatchResponse(BaseModel):
    game_mode: str | None = None
    platform_id: str
    match_id: str
    stats_type: StatsType
    data: StatsDataDTO | None = None


class StatsByPlayerResponse(BaseModel):
    game_mode: str | None = None
    platform_id: str
    stats_type: StatsType
    data: StatsDataDTO | None = None


# Factory pour créer les réponses
class StatsResponseFactory:
    @staticmethod
    def create_rank_response(
        game_mode: str,
        rank: str,
        stats_type: StatsType,
        data: StatsDataDTO,
    ) -> StatsByRankResponse:
        """Crée une réponse de statistiques par rang."""
        return StatsByRankResponse(
            game_mode=game_mode, rank=rank, stats_type=stats_type, data=data
        )

    @staticmethod
    def create_player_match_response(
        game_mode: str,
        platform_id: str,
        match_id: str,
        stats_type: StatsType,
        data: StatsDataDTO,
    ) -> StatsByPlayerMatchResponse:
        """Crée une réponse de statistiques par joueur et match."""
        return StatsByPlayerMatchResponse(
            game_mode=game_mode,
            platform_id=platform_id,
            match_id=match_id,
            stats_type=stats_type,
            data=data,
        )

    @staticmethod
    def create_player_response(
        game_mode: str,
        platform_id: str,
        stats_type: StatsType,
        data: StatsDataDTO,
    ) -> StatsByPlayerResponse:
        """Crée une réponse de statistiques par joueur."""
        return StatsByPlayerResponse(
            game_mode=game_mode,
            platform_id=platform_id,
            stats_type=stats_type,
            data=data,
        )
