class Platform:
    """
    Représente une plateforme de jeu (PC, PlayStation, Xbox, etc.).
    """

    def __init__(self, id: int, name: str):
        """
        Initialise une plateforme.

        Parameters
        ----------
        id : int
            Identifiant unique de la plateforme.
        name : str
            Nom de la plateforme.
        """

        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
