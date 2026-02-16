class StatsCore:
    def __init__(
        self,
        participation_id: int = 0,
        shots: int = 0,
        goals: int = 0,
        saves: int = 0,
        assists: int = 0,
        score: int = 0,
        shooting_percentage: int = 0,
        demo_inflicted: int = 0,
        demo_taken: int = 0,
    ):
        self._participation_id = participation_id

        self.shots = shots
        self.goals = goals
        self.saves = saves
        self.assists = assists
        self.score = score
        self.shooting_percentage = shooting_percentage
        self.demo_inflicted = demo_inflicted
        self.demo_taken = demo_taken

    @property
    def participation_id(self) -> int:
        return self._participation_id

    def to_dict(self) -> dict:
        """Convertit StatsCore en dictionnaire pour l'API."""
        return {
            "participation_id": self._participation_id,
            "shots": self.shots,
            "goals": self.goals,
            "saves": self.saves,
            "assists": self.assists,
            "score": self.score,
            "shooting_percentage": self.shooting_percentage,
            "demo_inflicted": self.demo_inflicted,
            "demo_taken": self.demo_taken,
        }
