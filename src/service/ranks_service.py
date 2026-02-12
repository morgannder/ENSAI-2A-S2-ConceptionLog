from ..dao.ranks_dao import RanksDAO
from ..models.players import Player
from ..models.ranks import Ranks
from ..utils.singleton import Singleton


class RanksService(metaclass=Singleton):
    """Service pour gérer la logique métier des rangs."""

    def __init__(self):
        self.ranks_dao = RanksDAO()

    def create_rank(self, tier: str, division: str, name: str) -> Ranks | None:
        """
        Crée un nouveau rang.
        """
        rank = Ranks(id=None, tier=tier, division=division, name=name)

        success = self.ranks_dao.create_rank(rank)

        if success:
            return self.get_rank_by_name(name)
        return None

    def get_rank_by_id(self, rank_id: int) -> Ranks | None:
        """
        Récupère un rang par son ID.
        """
        return self.ranks_dao.get_rank_by_parameter("id", rank_id)

    def get_rank_by_name(self, name: str) -> Ranks | None:
        """
        Récupère un rang par son nom.
        """
        return self.ranks_dao.get_rank_by_parameter("name", name)

    def get_current_rank_for_player(self, player: Player) -> Ranks | None:
        """
        Récupère le rang actuel d'un joueur (basé sur son match le plus récent).
        """
        if player is None:
            raise ValueError("Le joueur ne peut pas être None")

        return self.ranks_dao.get_rank_by_player(player)

    def delete_rank(self, rank: Ranks) -> bool:
        """
        Supprime un rang.
        """
        if rank is None:
            raise ValueError("Le rang ne peut pas être None")

        self.ranks_dao.delete_rank(rank)
        return True

    def rank_exists(self, name: str) -> bool:
        """
        Vérifie si un rang existe par son nom.
        """
        return self.get_rank_by_name(name) is not None

    def get_rank_display_name(self, rank: Ranks) -> str:
        """
        Retourne le nom formaté d'un rang pour l'affichage.
        """
        if rank is None:
            return "Non classé"

        return f"{rank.tier.capitalize()} {rank.division}"

    def compare_ranks(self, rank1: Ranks, rank2: Ranks) -> int:
        """
        Compare deux rangs
        """
        tier = {
            "IRON": 0,
            "BRONZE": 1,
            "SILVER": 2,
            "GOLD": 3,
            "PLATINUM": 4,
            "DIAMOND": 5,
            "MASTER": 6,
            "GRANDMASTER": 7,
            "CHALLENGER": 8,
        }

        division = {"IV": 0, "III": 1, "II": 2, "I": 3}

        tier1 = tier.get(rank1.tier.upper(), 0)
        tier2 = tier.get(rank2.tier.upper(), 0)

        if tier1 != tier2:
            if tier1 < tier2:
                return -1
            return 1

        div1 = division.get(rank1.division.upper(), 0)
        div2 = division.get(rank2.division.upper(), 0)

        if div1 < div2:
            return -1
        elif div1 > div2:
            return 1
        return 0
