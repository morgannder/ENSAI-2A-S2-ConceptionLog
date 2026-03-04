from pydantic import BaseModel


class RanksDTO(BaseModel):
    """DTO pour les informations sur le rang d'un joueur"""

    player_name: str
    platform_id: str
    rank: str
    full_rank: str | None


class PlayerRankDTO(BaseModel):
    """DTO pour le rang retourné par get_player_rank_by_platform_id"""

    tier: int
    division: int
    name: str
    full_name: str
