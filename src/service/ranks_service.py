from src.dao.players_dao import PlayerDAO
from src.dao.ranks_dao import RanksDAO
from src.models.ranks import Ranks
from src.utils.singleton import Singleton


class RanksService(metaclass=Singleton):
    """Service pour gérer la logique métier des rangs."""

    def __init__(self):
        self.ranks_dao = RanksDAO()
        self.player_dao = PlayerDAO()

    def create_rank(self, tier: str, division: str, name: str) -> Ranks | None:
        """
        Crée un nouveau rang.

        Parameters
        ----------
        tier : str
            Le tier du rang (ex: "Bronze", "Silver", "Gold").
        division : str
            La division du rang (ex: "I", "II", "III").
        name : str
            Le nom complet du rang (ex: "Bronze I Division 1").

        Returns
        -------
        Ranks | None
            Le rang créé avec son ID généré, ou None si la création a échoué.
        """
        rank = Ranks(id=None, tier=tier, division=division, name=name)

        success = self.ranks_dao.create_rank(rank)

        if success:
            return self.get_rank_by_name(name)
        return None

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

    def delete_rank(self, rank: Ranks) -> bool:
        """
        Supprime un rang.

        Parameters
        ----------
        rank : Ranks
            Le rang à supprimer.

        Returns
        -------
        bool
            True si la suppression a réussi.

        Raises
        ------
        ValueError
            Si le rang est None.
        """
        if rank is None:
            raise ValueError("Le rang ne peut pas être None")

        self.ranks_dao.delete_rank(rank)
        return True

    def rank_exists(self, name: str) -> bool:
        """
        Vérifie si un rang existe par son nom.

        Parameters
        ----------
        name : str
            Le nom complet du rang à vérifier.

        Returns
        -------
        bool
            True si le rang existe, False sinon.
        """
        return self.get_rank_by_name(name) is not None

    def get_rank_display_name(self, rank: Ranks) -> str:
        """
        Retourne le nom formaté d'un rang pour l'affichage.

        Parameters
        ----------
        rank : Ranks
            Le rang dont on veut obtenir le nom d'affichage.

        Returns
        -------
        str
            Le nom du rang formaté, ou "Non classé" si le rang est None.
        """
        if rank is None:
            return "Non classé"

        return rank.name
