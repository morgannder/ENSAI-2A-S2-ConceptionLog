class Match:
    """
    Représente un match Rocket League.
    """

    def __init__(
        self,
        id: str,
        playlist_id: str,
        season: int,
        duration: int,
        overtime: bool,
        date_upload: str,
    ):
        """
        Initialise un match.

        Parameters
        ----------
        id : str
            Identifiant unique du match.
        playlist_id : str
            Identifiant de la playlist (mode de jeu) du match.
        season : int
            Numéro de la saison durant laquelle le match a été joué.
        duration : int
            Durée du match en secondes.
        overtime : bool
            Indique si le match s'est terminé en prolongation.
        date_upload : str
            Date d'upload du replay du match.
        """

        self._id = id
        self._playlist_id = playlist_id
        self._season = season
        self._duration = duration
        self._overtime = overtime
        self._date_upload = date_upload

    @property
    def id(self) -> str:
        return self._id

    @property
    def playlist_id(self) -> str:
        return self._playlist_id

    @property
    def season(self) -> int:
        return self._season

    @property
    def date_upload(self) -> str:
        return self._date_upload

    @property
    def duration(self) -> int:
        return self._duration

    @property
    def overtime(self) -> bool:
        return self._overtime
