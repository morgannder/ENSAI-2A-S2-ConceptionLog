from src.dao.players_dao import PlayerDAO
from src.dao.ranks_dao import RanksDAO
from src.dto.ranks_dto import PlayerRankDTO
from src.utils.singleton import Singleton


class RanksService(metaclass=Singleton):
    """Service pour gérer la logique métier des rangs."""

    def __init__(self):
        self.ranks_dao = RanksDAO()
        self.player_dao = PlayerDAO()

    def get_player_rank_by_platform_id(self, platform_id: str) -> PlayerRankDTO | None:
        """
        Récupère le rang actuel d'un joueur (basé sur son match le plus récent).

        Parameters
        ----------
        platform_id : str
            L'identifiant de plateforme du joueur (ex: Steam ID).

        Returns
        -------
        PlayerRankDTO | None
            Un dictionnaire contenant les informations du rang :
            - tier : le tier du rang (int)
            - division : la division du rang (int)
            - name : le nom d'affichage (ex: "Bronze I")
            - full_name : le nom complet (ex: "Bronze I Division 1")
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

        return PlayerRankDTO(
            tier=rank.tier,
            division=rank.division,
            name=rank.display_name,
            full_name=rank.name,
        )
