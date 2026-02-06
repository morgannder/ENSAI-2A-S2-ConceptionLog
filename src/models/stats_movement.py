class StatsMovement:
    def __init__(
        self,
        participation_id: int = 0,
        avg_speed: int = 0,
        total_distance: int = 0,
        time_supersonic_speed: float = 0.0,
        time_boost_speed: float = 0.0,
        time_slow_speed: float = 0.0,
        time_ground: float = 0.0,
        time_low_air: float = 0.0,
        time_high_air: float = 0.0,
        time_powerslide: float = 0.0,
        count_powerslide: int = 0,
        average_powerslide_duration: float = 0.0,
        average_speed_percentage: float = 0.0,
        percent_slow_speed: float = 0.0,
        percent_boost_speed: float = 0.0,
        percent_supersonic_speed: float = 0.0,
        percent_ground: float = 0.0,
        percent_low_air: float = 0.0,
        percent_high_air: float = 0.0,
    ):
        self._participation_id = participation_id
        self.avg_speed = avg_speed
        self.total_distance = total_distance
        self.time_supersonic_speed = time_supersonic_speed
        self.time_boost_speed = time_boost_speed
        self.time_slow_speed = time_slow_speed
        self.time_ground = time_ground
        self.time_low_air = time_low_air
        self.time_high_air = time_high_air
        self.time_powerslide = time_powerslide
        self.count_powerslide = count_powerslide
        self.average_powerslide_duration = average_powerslide_duration
        self.average_speed_percentage = average_speed_percentage
        self.percent_slow_speed = percent_slow_speed
        self.percent_boost_speed = percent_boost_speed
        self.percent_supersonic_speed = percent_supersonic_speed
        self.percent_ground = percent_ground
        self.percent_low_air = percent_low_air
        self.percent_high_air = percent_high_air

    @property
    def participation_id(self):
        return self._participation_id
