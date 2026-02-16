from src.dao.stats_positionning_dao import StatPositionningDAO
from src.models.matches import Match
from src.models.players import Player
from src.models.ranks import Ranks
from src.models.stats_positionning import StatsPositionning


class StatPositionningService:
    """Doc."""

    def __init__(self):
        self.stats_positionning_dao = StatPositionningDAO()

    def get_rank_positionning_statistics(self, rank: Ranks) -> dict | None:
        """
        Doc.
        """
        return self.stats_positionning_dao.get_average_stats_positionning_per_rank(rank)

    def get_player_match_positionning_stats(
        self, player: Player, match: Match
    ) -> StatsPositionning | None:
        """
        Doc.
        """
        return self.stats_positionning_dao.get_player_match_stats_positionning(
            player, match
        )

    def get_player_average_positionning_stats(self, player: Player) -> dict | None:
        """
        Doc.
        """
        return self.stats_positionning_dao.get_player_average_stats_positionning(player)
