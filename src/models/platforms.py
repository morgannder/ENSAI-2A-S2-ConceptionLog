class Platform:
    def __init__(self, id: int, namebigint: str):
        self._id = id
        self._namebigint = namebigint

    @property
    def id(self):
        return self._id

    @property
    def namebigint(self):
        return self._namebigint
