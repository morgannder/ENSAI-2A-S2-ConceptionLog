class Ranks:
    def __init__(self, id: int, tier: int, division: int, name: str):
        self._id = id
        self._tier = tier
        self._division = division
        self._name = name

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
