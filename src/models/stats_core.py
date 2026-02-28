class StatsCore:
    """
    Représente les statistiques de jeu d'un joueur pour une participation
    à un match.
    """

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
        """
        Initialise les statistiques de jeu.

        Parameters
        ----------
        participation_id : int, optional
            Identifiant de la participation au match, par défaut 0.
        shots : int, optional
            Nombre de tirs effectués, par défaut 0.
        goals : int, optional
            Nombre de buts marqués, par défaut 0.
        saves : int, optional
            Nombre d'arrêts effectués, par défaut 0.
        assists : int, optional
            Nombre de passes décisives, par défaut 0.
        score : int, optional
            Score total obtenu dans le match, par défaut 0.
        shooting_percentage : int, optional
            Pourcentage de tirs convertis en buts, par défaut 0.
        demo_inflicted : int, optional
            Nombre de démolitions infligées à l'adversaire, par défaut 0.
        demo_taken : int, optional
            Nombre de démolitions subies, par défaut 0.
        """

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
