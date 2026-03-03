from src.dao.players_dao import PlayerDAO
from src.dao.ranks_dao import RanksDAO
from src.models.ranks import Ranks
from src.utils.singleton import Singleton


class RanksService(metaclass=Singleton):
    """Service pour gérer la logique métier des rangs."""

    def __init__(self):
        self.ranks_dao = RanksDAO()
        self.player_dao = PlayerDAO()

    def get_rank_by_id(self, rank_id: int) -> Ranks | None:
        """
        Récupère un rang par son ID.

        Parameters
        ----------
        rank_id : int
            L'identifiant unique du rang.

        Returns
        -------
        Ranks | None
            Le rang correspondant à l'ID, ou None s'il n'existe pas.
        """
        return self.ranks_dao.get_rank_by_parameter("id", rank_id)

    def get_rank_by_name(self, name: str) -> Ranks | None:
        """
        Récupère un rang par son nom.

        Parameters
        ----------
        name : str
            Le nom complet du rang (ex: "Bronze I Division 1").

        Returns
        -------
        Ranks | None
            Le rang correspondant au nom, ou None s'il n'existe pas.
        """
        return self.ranks_dao.get_rank_by_parameter("name", name)

    def get_player_rank_by_platform_id(self, platform_id: str) -> dict | None:
        """
        Récupère le rang actuel d'un joueur (basé sur son match le plus récent).

        Parameters
        ----------
        platform_id : str
            L'identifiant de plateforme du joueur (ex: Steam ID).

        Returns
        -------
        dict | None
            Un dictionnaire contenant les informations du rang :
            - tier : le tier du rang (int)
            - division : la division du rang (int)
            - name : le nom d'affichage (ex: "Bronze I")
            - full_name : le nom complet depuis la base de données
            Retourne None si le joueur n'existe pas ou n'a pas de rang.

        Raises
        ------
        ValueError
            Si platform_id est None.
        """
        if platform_id is None:
            raise ValueError("Veuillez insérer un identifiant.")

        player = self.player_dao.get_player_by_parameter(
            "platform_user_id", platform_id
        )

        if player is None:
            return None

        rank = self.ranks_dao.get_player_rank(player)

        if rank is None:
            return None

        return {
            "tier": rank.tier,
            "division": rank.division,
            "name": rank.display_name,  # "Bronze I" via property
            "full_name": rank.name,  # "Bronze I Division 1" depuis la DB
        }
