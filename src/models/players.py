class Player:
    """
    Représente un joueur Rocket League.
    """

    def __init__(self, id: int, platform_id: int, platform_user_id: str, name: str):
        """
        Initialise un joueur.

        Parameters
        ----------
        id : int
            Identifiant unique du joueur en base de données.
        platform_id : int
            Identifiant de la plateforme sur laquelle joue le joueur.
        platform_user_id : str
            Identifiant du joueur sur sa plateforme de jeu.
        name : str
            Nom d'affichage du joueur.
        """

        self._id = id
        self._platform_id = platform_id
        self._platform_user_id = platform_user_id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def platform_id(self):
        return self._platform_id

    @property
    def platform_user_id(self):
        return self._platform_user_id

    @property
    def name(self):
        return self._name
