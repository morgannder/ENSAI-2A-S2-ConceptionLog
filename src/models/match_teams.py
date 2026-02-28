class MatchTeam:
    """
    Représente une équipe dans un match.
    """

    def __init__(
        self,
        id: int,
        match_id: str,
        color: bool,
        score: int,
        possession_time: float,
        time_in_side: float,
    ):
        """
        Initialise une équipe dans un match.

        Parameters
        ----------
        id : int
            Identifiant unique de l'équipe dans le match.
        match_id : str
            Identifiant du match auquel appartient l'équipe.
        color : bool
            Couleur de l'équipe (True pour bleu, False pour orange).
        score : int
            Score final de l'équipe dans le match.
        possession_time : float
            Temps de possession du ballon en secondes.
        time_in_side : float
            Temps passé dans son propre camp en secondes.
        """

        self._id = id
        self._match_id = match_id
        self._color = color
        self._score = score
        self._possession_time = possession_time
        self._time_in_side = time_in_side

    @property
    def id(self) -> int:
        return self._id

    @property
    def match_id(self) -> str:
        return self._match_id

    @property
    def color(self) -> bool:
        return self._color

    @property
    def score(self) -> int:
        return self._score

    @property
    def possession_time(self) -> float:
        return self._possession_time

    @property
    def time_in_side(self) -> float:
        return self._time_in_side
