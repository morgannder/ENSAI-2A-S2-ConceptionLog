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
