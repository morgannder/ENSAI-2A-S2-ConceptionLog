from src.dao.stats_movement_dao import StatMovementDAO
from src.models.matches import Match
from src.models.players import Player
from src.models.ranks import Ranks
from src.models.stats_movement import StatsMovement


class StatMovementService:
    """Doc."""

    def __init__(self):
        self.stats_movement_dao = StatMovementDAO()

    def get_rank_movement_statistics(self, rank: Ranks) -> dict | None:
        """
        Doc.
        """
        return self.stats_movement_dao.get_average_stats_movement_per_rank(rank)

    def get_player_match_movement_stats(
        self, player: Player, match: Match
    ) -> StatsMovement | None:
        """
        Doc.
        """
        return self.stats_movement_dao.get_player_match_stats_movement(player, match)

    def get_player_average_movement_stats(self, player: Player) -> dict | None:
        """
        Doc.
        """
        return self.stats_movement_dao.get_player_average_stats_movement(player)
