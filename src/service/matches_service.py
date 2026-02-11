from src.dao.matches_dao import MatchDAO
from src.models.players import Player


class MatchService:
    """doc."""

    def __init__(self):
        self.match_dao = MatchDAO

    def get_player_last_matches(self, player: Player, nb_match: int = 20):
        pass
