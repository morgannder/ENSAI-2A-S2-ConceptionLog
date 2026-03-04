from pydantic import BaseModel

from src.models.stats_movement import StatsMovement


class StatsMovementDTO(BaseModel):
    """DTO pour les statistiques de mouvement d'un match individuel"""

    participation_id: int
    avg_speed: int
    total_distance: int
    time_supersonic_speed: float
    time_boost_speed: float
    time_slow_speed: float
    time_ground: float
    time_low_air: float
    time_high_air: float
    time_powerslide: float
    count_powerslide: int
    avg_powerslide_duration: float
    avg_speed_percentage: float
    percent_slow_speed: float
    percent_boost_speed: float
    percent_supersonic_speed: float
    percent_ground: float
    percent_low_air: float
    percent_high_air: float

    class Config:
        from_attributes = True

    @classmethod
    def from_business_object(cls, bo: StatsMovement) -> "StatsMovementDTO":
        """
        Convertit un Business Object StatsMovement en DTO.

        Parameters
        ----------
        bo : StatsMovement
            L'objet métier StatsMovement à convertir.

        Returns
        -------
        StatsMovementDTO
            Le DTO correspondant à l'objet métier fourni.
        """
        return cls(
            participation_id=bo._participation_id,
            avg_speed=bo.avg_speed,
            total_distance=bo.total_distance,
            time_supersonic_speed=bo.time_supersonic_speed,
            time_boost_speed=bo.time_boost_speed,
            time_slow_speed=bo.time_slow_speed,
            time_ground=bo.time_ground,
            time_low_air=bo.time_low_air,
            time_high_air=bo.time_high_air,
            time_powerslide=bo.time_powerslide,
            count_powerslide=bo.count_powerslide,
            avg_powerslide_duration=bo.average_powerslide_duration,
            avg_speed_percentage=bo.average_speed_percentage,
            percent_slow_speed=bo.percent_slow_speed,
            percent_boost_speed=bo.percent_boost_speed,
            percent_supersonic_speed=bo.percent_supersonic_speed,
            percent_ground=bo.percent_ground,
            percent_low_air=bo.percent_low_air,
            percent_high_air=bo.percent_high_air,
        )


class StatsMovementAggregatedDTO(BaseModel):
    """DTO pour les statistiques de mouvement agrégées (moyennes par rang ou joueur)"""

    avg_speed: float
    total_distance: float
    time_supersonic_speed: float
    time_boost_speed: float
    time_slow_speed: float
    time_ground: float
    time_low_air: float
    time_high_air: float
    time_powerslide: float
    count_powerslide: float
    avg_powerslide_duration: float
    avg_speed_percentage: float
    percent_slow_speed: float
    percent_boost_speed: float
    percent_supersonic_speed: float
    percent_ground: float
    percent_low_air: float
    percent_high_air: float

    class Config:
        from_attributes = True
