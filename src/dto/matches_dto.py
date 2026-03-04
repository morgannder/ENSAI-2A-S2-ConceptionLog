from datetime import datetime

from pydantic import BaseModel


class MatchResponseDTO(BaseModel):
    id: str
    playlist_id: str
    season: int
    duration: int
    overtime: int
    date_upload: datetime

    class Config:
        from_attributes = True
