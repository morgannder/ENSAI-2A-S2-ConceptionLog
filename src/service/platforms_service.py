from src.dao.platforms_dao import PlatformDAO
from src.models.platforms import Platform


class PlatformService:
    """Service pour gérer la logique métier des plateformes."""

    def __init__(self):
        self.platform_dao = PlatformDAO()

    def get_platform_by_id(self, platform_id: int) -> Platform | None:
        """
        Récupère une plateforme par son ID.

        Parameters
        ----------
        platform_id : int
            L'identifiant unique de la plateforme.

        Returns
        -------
        Platform | None
            La plateforme correspondante, ou None si elle n'existe pas.

        Raises
        ------
        ValueError
            Si platform_id est None ou négatif.
        """
        if platform_id is None or platform_id < 0:
            raise ValueError("L'ID de la plateforme doit être un entier positif")

        return self.platform_dao.get_platform_by_id(platform_id)

    def get_platform_by_name(self, name: str) -> Platform | None:
        """
        Récupère une plateforme par son nom.

        Parameters
        ----------
        name : str
            Le nom de la plateforme à rechercher.

        Returns
        -------
        Platform | None
            La plateforme correspondante, ou None si elle n'existe pas.

        Raises
        ------
        ValueError
            Si le nom est vide ou None.
        """
        if not name or not name.strip():
            raise ValueError("Le nom de la plateforme ne peut pas être vide")

        return self.platform_dao.get_platform_by_name(name.strip().upper())

    def delete_platform(self, platform: Platform) -> bool:
        """
        Supprime une plateforme.

        Parameters
        ----------
        platform : Platform
            La plateforme à supprimer.

        Returns
        -------
        bool
            True si la suppression a réussi, False sinon.

        Raises
        ------
        ValueError
            Si la plateforme est None.
        """
        if platform is None:
            raise ValueError("La plateforme ne peut pas être None")

        return self.platform_dao.delete_platform(platform)

    def delete_platform_by_name(self, name: str) -> bool:
        """
        Supprime une plateforme par son nom.

        Parameters
        ----------
        name : str
            Le nom de la plateforme à supprimer.

        Returns
        -------
        bool
            True si la plateforme a été trouvée et supprimée, False sinon.
        """
        platform = self.get_platform_by_name(name)
        if platform is None:
            return False

        return self.delete_platform(platform)

    def platform_exists(self, name: str) -> bool:
        """
        Vérifie si une plateforme existe par son nom.

        Parameters
        ----------
        name : str
            Le nom de la plateforme à vérifier.

        Returns
        -------
        bool
            True si la plateforme existe, False sinon ou si le nom est invalide.
        """
        try:
            return self.get_platform_by_name(name) is not None
        except ValueError:
            return False

    def platform_exists_by_id(self, platform_id: int) -> bool:
        """
        Vérifie si une plateforme existe par son ID.

        Parameters
        ----------
        platform_id : int
            L'identifiant de la plateforme à vérifier.

        Returns
        -------
        bool
            True si la plateforme existe, False sinon ou si l'ID est invalide.
        """
        try:
            return self.get_platform_by_id(platform_id) is not None
        except ValueError:
            return False

    def normalize_platform_name(self, name: str) -> str:
        """
        Normalise un nom de plateforme en le convertissant en majuscules.

        Parameters
        ----------
        name : str
            Le nom de la plateforme à normaliser.

        Returns
        -------
        str
            Le nom normalisé en majuscules et sans espaces superflus,
            ou une chaîne vide si le nom est vide ou None.
        """
        if not name:
            return ""

        return name.strip().upper()
