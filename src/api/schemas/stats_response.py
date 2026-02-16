from enum import Enum

from pydantic import BaseModel


class StatsType(str, Enum):
    CORE = "core"
    BOOST = "boost"
    MOVEMENT = "movement"
    POSITIONING = "positioning"


class StatsByRankResponse(BaseModel):
    rank: str
    stats_type: StatsType
    data: dict = None


class StatsByPlayerMatchResponse(BaseModel):
    platform_id: str
    match_id: str
    stats_type: StatsType
    data: dict = None


class StatsByPlayerResponse(BaseModel):
    platform_id: str
    stats_type: StatsType
    data: dict = None


# Factory pour créer les réponses
class StatsResponseFactory:
    @staticmethod
    def create_rank_response(
        rank: str, stats_type: StatsType, data: dict
    ) -> StatsByRankResponse:
        """Crée une réponse de statistiques par rang."""
        return StatsByRankResponse(rank=rank, stats_type=stats_type, data=data)

    @staticmethod
    def create_player_match_response(
        platform_id: str, match_id: str, stats_type: StatsType, data: dict
    ) -> StatsByPlayerMatchResponse:
        """Crée une réponse de statistiques par joueur et match."""
        return StatsByPlayerMatchResponse(
            platform_id=platform_id, match_id=match_id, stats_type=stats_type, data=data
        )

    @staticmethod
    def create_player_response(
        platform_id: str, stats_type: StatsType, data: dict
    ) -> StatsByPlayerResponse:
        """Crée une réponse de statistiques par joueur."""
        return StatsByPlayerResponse(
            platform_id=platform_id, stats_type=stats_type, data=data
        )


"""from pydantic import BaseModel


class StatsByRankResponse(BaseModel):
    rank: str
    data: dict = None


# faire une factory pour match les 4 types avec un type


class StatsByPlayerMatchResponse(BaseModel):
    platform_id: str
    match_id: str
    data: dict = None


class StatsByPlayerResponse(BaseModel):
    platform_id: str
    data: dict = None
"""
