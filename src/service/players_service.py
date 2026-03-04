from src.dao.players_dao import PlayerDAO
from src.models.players import Player


class PlayerService:
    """Service pour gérer la logique métier des joueurs."""

    def __init__(self):
        self.player_dao = PlayerDAO()

    def get_player_by_platform_id(self, platform_id: str) -> Player | None:
        """
        Récupère un joueur par son identifiant de plateforme.

        Parameters
        ----------
        platform_id : str
            L'identifiant unique du joueur sur la plateforme.

        Returns
        -------
        Player | None
            Le joueur correspondant à l'identifiant, ou None s'il n'existe pas.

        Raises
        ------
        ValueError
            Si platform_id est None.
        """
        if platform_id is None:
            raise ValueError("Le platform_id du joueur doit être non vide")

        return self.player_dao.get_player_by_parameter("platform_user_id", platform_id)

    def search_players(
        self, name_query: str, platform: str = None, limit: int = 30, offset: int = 0
    ) -> list[dict]:
        """
        Recherche des joueurs avec validation de la limite et filtrage par plateforme.
        """
        if limit <= 0:
            raise ValueError("La limite doit être supérieure à 0")

        rows = self.player_dao.search_players_by_name(
            name_query, platform, limit, offset
        )

        if not rows:
            return []

        return [
            {
                "platform_user_id": row["platform_user_id"],
                "name": row["name"],
                "platform": row["platform_name"],
            }
            for row in rows
        ]
