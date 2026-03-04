class MatchParticipation:
    """
    Représente la participation d'un joueur à un match.
    """

    def __init__(
        self,
        id: int,
        match_team_id: int,
        player_id: int,
        rank_id: int,
        car_id: int,
        car_name: str,
        mvp: bool,
        start_time: float,
        end_time: float,
    ):
        """
        Initialise une participation de joueur à un match.

        Parameters
        ----------
        id : int
            Identifiant unique de la participation.
        match_team_id : int
            Identifiant de l'équipe dans le match.
        player_id : int
            Identifiant du joueur.
        rank_id : int
            Identifiant du rang du joueur au moment du match.
        car_id : int
            Identifiant de la voiture utilisée par le joueur.
        car_name : str
            Nom de la voiture utilisée par le joueur.
        mvp : bool
            Indique si le joueur a été élu MVP du match.
        start_time : float
            Timestamp de début de participation au match.
        end_time : float
            Timestamp de fin de participation au match.
        """

        self._id = id
        self._match_team_id = match_team_id
        self._player_id = player_id
        self._rank_id = rank_id
        self._car_id = car_id
        self._car_name = car_name
        self._mvp = mvp
        self._start_time = start_time
        self._end_time = end_time

    @property
    def id(self) -> int:
        return self._id

    @property
    def match_team_id(self) -> int:
        return self._match_team_id

    @property
    def player_id(self) -> int:
        return self._player_id

    @property
    def rank_id(self) -> int:
        return self._rank_id

    @property
    def car_id(self) -> int:
        return self._car_id

    @property
    def car_name(self) -> str:
        return self._car_name

    @property
    def start_time(self) -> float:
        return self._start_time

    @property
    def end_time(self) -> float:
        return self._end_time

    @property
    def mvp(self) -> bool:
        return self._mvp
