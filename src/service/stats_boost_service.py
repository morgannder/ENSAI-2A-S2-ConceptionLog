from src.dao.stats_boost_dao import StatBoostDAO
from src.models.matches import Match
from src.models.players import Player
from src.models.ranks import Ranks
from src.models.stats_boost import StatsBoost


class StatBoostService:
    """Doc."""

    def __init__(self):
        self.stats_boost_dao = StatBoostDAO()

    def get_rank_boost_statistics(self, rank: Ranks) -> dict | None:
        """
        Doc.
        """
        return self.stats_boost_dao.get_average_stats_boost_per_rank(rank)

    def get_player_match_boost_stats(
        self, player: Player, match: Match
    ) -> StatsBoost | None:
        """
        Doc.
        """
        return self.stats_boost_dao.get_player_match_stats_boost(player, match)

    def get_player_average_boost_stats(self, player: Player) -> dict | None:
        """
        Doc.
        """
        return self.stats_boost_dao.get_player_average_stats_boost(player)
