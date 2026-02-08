from pydantic import BaseModel


class AverageStatsResponse(BaseModel):
    success: bool
    message: str
    data: dict | None
