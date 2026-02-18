class Ranks:
    def __init__(self, id: int = 0, tier: int = 0, division: int = 0, name: str = ""):
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

    @property
    def rank_group(self) -> str:
        """Retourne le groupe de rang (Bronze, Silver, etc.)"""
        rank_groups = {
            1: "Bronze",
            2: "Bronze",
            3: "Bronze",
            4: "Silver",
            5: "Silver",
            6: "Silver",
            7: "Gold",
            8: "Gold",
            9: "Gold",
            10: "Platinum",
            11: "Platinum",
            12: "Platinum",
            13: "Diamond",
            14: "Diamond",
            15: "Diamond",
            16: "Champion",
            17: "Champion",
            18: "Champion",
            19: "Grand Champion",
            20: "Grand Champion",
            21: "Grand Champion",
            22: "Supersonic Legend",
        }
        return rank_groups.get(self.tier, "Unknown")

    @property
    def division_roman(self) -> str:
        """Retourne la division en chiffres romains"""
        divisions = {1: "I", 2: "II", 3: "III", 4: "IV"}
        return divisions.get(self.division, "")

    @property
    def display_name(self) -> str:
        """Retourne le nom formaté (ex: 'Bronze I')"""
        return f"{self.rank_group} {self.division_roman}"
