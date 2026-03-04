from pydantic import BaseModel

from src.models.stats_positioning import StatsPositioning


class StatsPositioningDTO(BaseModel):
    """DTO pour les statistiques de positionnement d'un match individuel"""

    participation_id: int
    average_distance_to_ball: int
    average_distance_to_ball_possession: int
    average_distance_to_ball_no_possession: int
    average_distance_to_mates: int
    time_defensive_third: float
    time_neutral_third: float
    time_offensive_third: float
    time_defensive_half: float
    time_offensive_half: float
    time_behind_ball: float
    time_infront_ball: float
    time_most_back: float
    time_most_forward: float
    goals_against_while_last_defender: int
    time_closest_to_ball: float
    time_farthest_to_ball: float
    percent_defensive_third: float
    percent_neutral_third: float
    percent_offensive_third: float
    percent_defensive_half: float
    percent_offensive_half: float
    percent_behind_ball: float
    percent_infront_ball: float
    percent_most_back: float
    percent_most_forward: float
    percent_closest_to_ball: float
    percent_farthest_from_ball: float

    class Config:
        from_attributes = True

    @classmethod
    def from_business_object(cls, bo: StatsPositioning) -> "StatsPositioningDTO":
        """
        Convertit un Business Object StatsPositioning en DTO.

        Parameters
        ----------
        bo : StatsPositioning
            L'objet métier StatsPositioning à convertir.

        Returns
        -------
        StatsPositioningDTO
            Le DTO correspondant à l'objet métier fourni.
        """
        return cls(
            participation_id=bo._participation_id,
            average_distance_to_ball=bo.average_distance_to_ball,
            average_distance_to_ball_possession=bo.average_distance_to_ball_possession,
            average_distance_to_ball_no_possession=bo.average_distance_to_ball_no_possession,
            average_distance_to_mates=bo.average_distance_to_mates,
            time_defensive_third=bo.time_defensive_third,
            time_neutral_third=bo.time_neutral_third,
            time_offensive_third=bo.time_offensive_third,
            time_defensive_half=bo.time_defensive_half,
            time_offensive_half=bo.time_offensive_half,
            time_behind_ball=bo.time_behind_ball,
            time_infront_ball=bo.time_infront_ball,
            time_most_back=bo.time_most_back,
            time_most_forward=bo.time_most_forward,
            goals_against_while_last_defender=bo.goals_against_while_last_defender,
            time_closest_to_ball=bo.time_closest_to_ball,
            time_farthest_to_ball=bo.time_farthest_to_ball,
            percent_defensive_third=bo.percent_defensive_third,
            percent_neutral_third=bo.percent_neutral_third,
            percent_offensive_third=bo.percent_offensive_third,
            percent_defensive_half=bo.percent_defensive_half,
            percent_offensive_half=bo.percent_offensive_half,
            percent_behind_ball=bo.percent_behind_ball,
            percent_infront_ball=bo.percent_infront_ball,
            percent_most_back=bo.percent_most_back,
            percent_most_forward=bo.percent_most_forward,
            percent_closest_to_ball=bo.percent_closest_to_ball,
            percent_farthest_from_ball=bo.percent_farthest_from_ball,
        )


class StatsPositioningAggregatedDTO(BaseModel):
    """DTO pour les statistiques de positionnement agrégées (moyennes par rang ou joueur)"""

    average_distance_to_ball: float
    average_distance_to_ball_possession: float
    average_distance_to_ball_no_possession: float
    average_distance_to_mates: float
    time_defensive_third: float
    time_neutral_third: float
    time_offensive_third: float
    time_defensive_half: float
    time_offensive_half: float
    time_behind_ball: float
    time_infront_ball: float
    time_most_back: float
    time_most_forward: float
    goals_against_while_last_defender: float
    time_closest_to_ball: float
    time_farthest_to_ball: float
    percent_defensive_third: float
    percent_neutral_third: float
    percent_offensive_third: float
    percent_defensive_half: float
    percent_offensive_half: float
    percent_behind_ball: float
    percent_infront_ball: float
    percent_most_back: float
    percent_most_forward: float
    percent_closest_to_ball: float
    percent_farthest_from_ball: float

    class Config:
        from_attributes = True
