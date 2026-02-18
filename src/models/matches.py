class Match:
    def __init__(
        self,
        id: str,
        playlist_id: str,
        season: int,
        duration: int,
        overtime: bool,
        date_upload: str,
    ):
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
