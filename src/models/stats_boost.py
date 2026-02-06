class StatsBoost:
    def __init__(
        self,
        participation_id: int = 0,
        boost_per_minute: float = 0.0,
        boost_consumed_per_minute: float = 0.0,
        average_amount: float = 0.0,
        amount_collected: int = 0,
        amount_stolen: int = 0,
        amount_collected_big: int = 0,
        amount_stolen_big: int = 0,
        amount_collected_small: int = 0,
        amount_stolen_small: int = 0,
        count_collected_big: int = 0,
        count_stolen_big: int = 0,
        count_collected_small: int = 0,
        count_stolen_small: int = 0,
        amount_overfill: int = 0,
        amount_overfill_stolen: int = 0,
        amount_used_while_supersonic: int = 0,
        time_zero_boost: float = 0.0,
        percent_zero_boost: float = 0.0,
        time_full_boost: float = 0.0,
        percent_full_boost: float = 0.0,
        time_boost_0_25: float = 0.0,
        time_boost_25_50: float = 0.0,
        time_boost_50_75: float = 0.0,
        time_boost_75_100: float = 0.0,
        percent_boost_0_25: float = 0.0,
        percent_boost_25_50: float = 0.0,
        percent_boost_50_75: float = 0.0,
        percent_boost_75_100: float = 0.0,
    ):
        self._participation_id = participation_id

        self.boost_per_minute = boost_per_minute
        self.boost_consumed_per_minute = boost_consumed_per_minute
        self.average_amount = average_amount
        self.amount_collected = amount_collected
        self.amount_stolen = amount_stolen
        self.amount_collected_big = amount_collected_big
        self.amount_stolen_big = amount_stolen_big
        self.amount_collected_small = amount_collected_small
        self.amount_stolen_small = amount_stolen_small
        self.count_collected_big = count_collected_big
        self.count_stolen_big = count_stolen_big
        self.count_collected_small = count_collected_small
        self.count_stolen_small = count_stolen_small
        self.amount_overfill = amount_overfill
        self.amount_overfill_stolen = amount_overfill_stolen
        self.amount_used_while_supersonic = amount_used_while_supersonic
        self.time_zero_boost = time_zero_boost
        self.percent_zero_boost = percent_zero_boost
        self.time_full_boost = time_full_boost
        self.percent_full_boost = percent_full_boost
        self.time_boost_0_25 = time_boost_0_25
        self.time_boost_25_50 = time_boost_25_50
        self.time_boost_50_75 = time_boost_50_75
        self.time_boost_75_100 = time_boost_75_100
        self.percent_boost_0_25 = percent_boost_0_25
        self.percent_boost_25_50 = percent_boost_25_50
        self.percent_boost_50_75 = percent_boost_50_75
        self.percent_boost_75_100 = percent_boost_75_100

    @property
    def participation_id(self) -> int:
        return self._participation_id
