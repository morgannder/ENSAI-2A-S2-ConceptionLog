from pydantic import BaseModel


class PlayerInfoDTO(BaseModel):
    id: int
    name: str
    platform_id: int | None = None
    platform_user_id: str | None = None


class MatchPlayersDTO(BaseModel):
    orange1: PlayerInfoDTO | None = None
    orange2: PlayerInfoDTO | None = None
    orange3: PlayerInfoDTO | None = None
    orange4: PlayerInfoDTO | None = None
    blue1: PlayerInfoDTO | None = None
    blue2: PlayerInfoDTO | None = None
    blue3: PlayerInfoDTO | None = None
    blue4: PlayerInfoDTO | None = None
