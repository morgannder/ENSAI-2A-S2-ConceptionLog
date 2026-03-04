from pydantic import BaseModel


class MatchTeamResponseDTO(BaseModel):
    id: int
    match_id: str
    color: str
    score: int
    possession_time: float
    time_in_side: float
