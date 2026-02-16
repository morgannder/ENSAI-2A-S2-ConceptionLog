from pydantic import BaseModel


class StatsByRankResponse(BaseModel):
    rank: str
    data: dict = None


class StatsByPlayerMatchResponse(BaseModel):
    platform_id: str
    match_id: str
    data: dict = None


class StatsByPlayerResponse(BaseModel):
    platform_id: str
    data: dict = None
