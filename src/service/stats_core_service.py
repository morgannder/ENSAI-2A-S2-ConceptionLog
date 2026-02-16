from src.dao.stats_core_dao import StatsCoreDAO
from src.models.matches import Match
from src.models.players import Player
from src.models.stats_core import StatsCore


class StatsCoreService:
    """Service pour gérer la logique métier des statistiques de jeu."""

    def __init__(self):
        self.stats_core_dao = StatsCoreDAO()

    def get_stats_core_by_rank_name(self, rank_name: str) -> float | None:
        """
        Récupère les statistiques core pour un rang donné (par nom).
        """

        return self.stats_core_dao.get_stats_core_per_rank(rank_name)

    def get_average_stats_core_by_rank_name(self, rank_name: str) -> float | None:
        """
        Récupère les statistiques core moyennes pour un rang donné (par nom).
        """

        return self.stats_core_dao.get_average_stats_core_per_rank(rank_name)

    def get_player_match_stats_core(
        self, player: Player, match: Match
    ) -> StatsCore | None:
        """
        Doc.
        """
        return self.stats_core_dao.get_player_match_stats_core(player, match)

    def get_player_average_stats_core(self, player: Player) -> dict | None:
        """
        Doc.
        """
        return self.stats_core_dao.get_player_average_stats_core(player)
