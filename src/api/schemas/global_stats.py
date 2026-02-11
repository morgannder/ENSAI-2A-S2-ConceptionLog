from pydantic import BaseModel


class AverageStatsResponse(BaseModel):
    message: str
    data: dict | None
