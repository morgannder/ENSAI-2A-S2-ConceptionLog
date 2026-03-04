from pydantic import BaseModel

from src.models.stats_core import StatsCore


class StatsCoreDTO(BaseModel):
    """DTO pour les statistiques core d'un match individuel"""

    participation_id: int
    shots: int
    goals: int
    saves: int
    assists: int
    score: int
    shooting_percentage: float
    demo_inflicted: int
    demo_taken: int

    class Config:
        from_attributes = True

    @classmethod
    def from_business_object(cls, bo: StatsCore) -> "StatsCoreDTO":
        """
        Convertit un Business Object StatsCore en DTO.

        Parameters
        ----------
        bo : StatsCore
            L'objet métier StatsCore à convertir.

        Returns
        -------
        StatsCoreDTO
            Le DTO correspondant à l'objet métier fourni.
        """
        return cls(
            participation_id=bo._participation_id,
            shots=bo.shots,
            goals=bo.goals,
            saves=bo.saves,
            assists=bo.assists,
            score=bo.score,
            shooting_percentage=bo.shooting_percentage,
            demo_inflicted=bo.demo_inflicted,
            demo_taken=bo.demo_taken,
        )


class StatsCoreAggregatedDTO(BaseModel):
    """DTO pour les statistiques core agrégées (moyennes par rang ou joueur)"""

    shots: float
    goals: float
    saves: float
    assists: float
    score: float
    shooting_percentage: float
    demo_inflicted: float
    demo_taken: float

    class Config:
        from_attributes = True
