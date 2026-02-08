from src.dao.platforms_dao import PlatformDAO
from src.models.platforms import Platform


class PlatformService:
    """Service pour gérer la logique métier des plateformes."""

    def __init__(self):
        self.platform_dao = PlatformDAO()

    def get_platform_by_id(self, platform_id: int) -> Platform | None:
        """
        Récupère une plateforme par son ID.
        """
        if platform_id is None or platform_id < 0:
            raise ValueError("L'ID de la plateforme doit être un entier positif")

        return self.platform_dao.get_platform_by_id(platform_id)

    def get_platform_by_name(self, name: str) -> Platform | None:
        """
        Récupère une plateforme par son nom.
        """
        if not name or not name.strip():
            raise ValueError("Le nom de la plateforme ne peut pas être vide")

        return self.platform_dao.get_platform_by_name(name.strip().upper())

    def delete_platform(self, platform: Platform) -> bool:
        """
        Supprime une plateforme.
        """
        if platform is None:
            raise ValueError("La plateforme ne peut pas être None")

        return self.platform_dao.delete_platform(platform)

    def delete_platform_by_name(self, name: str) -> bool:
        """
        Supprime une plateforme par son nom.

        """
        platform = self.get_platform_by_name(name)
        if platform is None:
            return False

        return self.delete_platform(platform)

    def platform_exists(self, name: str) -> bool:
        """
        Vérifie si une plateforme existe par son nom.
        """
        try:
            return self.get_platform_by_name(name) is not None
        except ValueError:
            return False

    def platform_exists_by_id(self, platform_id: int) -> bool:
        """
        Vérifie si une plateforme existe par son ID.
        """
        try:
            return self.get_platform_by_id(platform_id) is not None
        except ValueError:
            return False

    def normalize_platform_name(self, name: str) -> str:
        """
        Normalise un nom de plateforme.
        """
        if not name:
            return ""

        return name.strip().upper()
