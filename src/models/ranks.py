class Ranks:
    """
    Représente un rang dans le système de classement de Rocket League.
    """

    def __init__(self, id: int = 0, tier: int = 0, division: int = 0, name: str = ""):
        """
        Initialise un rang.

        Parameters
        ----------
        id : int, optional
            Identifiant unique du rang en base de données, par défaut 0.
        tier : int, optional
            Niveau du rang (ex: 1-3 Bronze, 4-6 Silver, etc.), par défaut 0.
        division : int, optional
            Division au sein du tier (I, II, III, IV), par défaut 0.
        name : str, optional
            Nom complet du rang (ex: "Gold III"), par défaut "".
        """

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
            1: "Bronze I",
            2: "Bronze II",
            3: "Bronze III",
            4: "Silver I",
            5: "Silver II",
            6: "Silver III",
            7: "Gold I",
            8: "Gold II",
            9: "Gold III",
            10: "Platinum I",
            11: "Platinum II",
            12: "Platinum III",
            13: "Diamond I",
            14: "Diamond II",
            15: "Diamond III",
            16: "Champion I",
            17: "Champion II",
            18: "Champion III",
            19: "Grand Champion I",
            20: "Grand Champion II",
            21: "Grand Champion III",
            22: "Supersonic Legend",
        }
        return rank_groups.get(self.tier, "Unknown")

    @property
    def display_name(self) -> str:
        """Retourne le nom formaté (ex: 'Bronze I')"""
        return f"{self.rank_group}"
