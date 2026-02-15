class Ranks:
    def __init__(self, name: str, id: int = 0, tier: int = 0, division: int = 0):
        self._name = name
        self._id = id
        self._tier = tier
        self._division = division

    @property
    def id(self):
        return self._id

    @property
    def tier(self):
        return self._tier

    @property
    def division(self):
        return self._division

    @property
    def name(self):
        return self._name
