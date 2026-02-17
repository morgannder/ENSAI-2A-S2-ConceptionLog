from pydantic import BaseModel

from src.models.stats_boost import StatsBoost


class StatsBoostDTO(BaseModel):
    """DTO pour les statistiques boost d'un match individuel"""

    participation_id: int
    boost_per_minute: float
    boost_consumed_per_minute: float
    average_amount: float
    amount_collected: int
    amount_stolen: int
    amount_collected_big: int
    amount_stolen_big: int
    amount_collected_small: int
    amount_stolen_small: int
    count_collected_big: int
    count_stolen_big: int
    count_collected_small: int
    count_stolen_small: int
    amount_overfill: int
    amount_overfill_stolen: int
    amount_used_while_supersonic: int
    time_zero_boost: float
    percent_zero_boost: float
    time_full_boost: float
    percent_full_boost: float
    time_boost_0_25: float
    time_boost_25_50: float
    time_boost_50_75: float
    time_boost_75_100: float
    percent_boost_0_25: float
    percent_boost_25_50: float
    percent_boost_50_75: float
    percent_boost_75_100: float

    class Config:
        from_attributes = True

    @classmethod
    def from_business_object(cls, bo: StatsBoost) -> "StatsBoostDTO":
        """Convertit un Business Object StatsBoost en DTO"""
        return cls(
            participation_id=bo._participation_id,
            boost_per_minute=bo.boost_per_minute,
            boost_consumed_per_minute=bo.boost_consumed_per_minute,
            average_amount=bo.average_amount,
            amount_collected=bo.amount_collected,
            amount_stolen=bo.amount_stolen,
            amount_collected_big=bo.amount_collected_big,
            amount_stolen_big=bo.amount_stolen_big,
            amount_collected_small=bo.amount_collected_small,
            amount_stolen_small=bo.amount_stolen_small,
            count_collected_big=bo.count_collected_big,
            count_stolen_big=bo.count_stolen_big,
            count_collected_small=bo.count_collected_small,
            count_stolen_small=bo.count_stolen_small,
            amount_overfill=bo.amount_overfill,
            amount_overfill_stolen=bo.amount_overfill_stolen,
            amount_used_while_supersonic=bo.amount_used_while_supersonic,
            time_zero_boost=bo.time_zero_boost,
            percent_zero_boost=bo.percent_zero_boost,
            time_full_boost=bo.time_full_boost,
            percent_full_boost=bo.percent_full_boost,
            time_boost_0_25=bo.time_boost_0_25,
            time_boost_25_50=bo.time_boost_25_50,
            time_boost_50_75=bo.time_boost_50_75,
            time_boost_75_100=bo.time_boost_75_100,
            percent_boost_0_25=bo.percent_boost_0_25,
            percent_boost_25_50=bo.percent_boost_25_50,
            percent_boost_50_75=bo.percent_boost_50_75,
            percent_boost_75_100=bo.percent_boost_75_100,
        )


class StatsBoostAggregatedDTO(BaseModel):
    """DTO pour les statistiques boost agrégées (moyennes par rang ou joueur)"""

    boost_per_minute: float
    boost_consumed_per_minute: float
    average_amount: float
    amount_collected: float
    amount_stolen: float
    amount_collected_big: float
    amount_stolen_big: float
    amount_collected_small: float
    amount_stolen_small: float
    count_collected_big: float
    count_stolen_big: float
    count_collected_small: float
    count_stolen_small: float
    amount_overfill: float
    amount_overfill_stolen: float
    amount_used_while_supersonic: float
    time_zero_boost: float
    percent_zero_boost: float
    time_full_boost: float
    percent_full_boost: float
    time_boost_0_25: float
    time_boost_25_50: float
    time_boost_50_75: float
    time_boost_75_100: float
    percent_boost_0_25: float
    percent_boost_25_50: float
    percent_boost_50_75: float
    percent_boost_75_100: float

    class Config:
        from_attributes = True
