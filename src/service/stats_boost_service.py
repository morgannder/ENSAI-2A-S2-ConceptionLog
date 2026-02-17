from src.dao.stats_boost_dao import StatBoostDAO
from src.dto.stats_boost_dto import StatsBoostAggregatedDTO
from src.models.matches import Match
from src.models.players import Player
from src.models.ranks import Ranks
from src.models.stats_boost import StatsBoost


class StatBoostService:
    """Service pour gérer les opérations métier liées aux statistiques de boost."""

    def __init__(self):
        self.stats_boost_dao = StatBoostDAO()

    def get_average_stats_boost_by_rank(
        self, rank: Ranks
    ) -> StatsBoostAggregatedDTO | None:
        """
        Récupère les statistiques moyennes de boost pour un rang donné.

        Parameters
        ----------
        rank : Ranks
            Le rang pour lequel on veut obtenir les statistiques de boost.

        Returns
        -------
        StatsBoostAggregatedDTO | None
            DTO contenant les statistiques moyennes de boost pour ce rang,
            ou None si aucune statistique n'est disponible.

        Notes
        -----
        Les statistiques incluent typiquement les moyennes de boost collecté,
        boost utilisé, et autres métriques liées au boost pour tous les joueurs
        de ce rang.
        """
        return self.stats_boost_dao.get_average_stats_boost_per_rank(rank)

    def get_player_match_boost_stats(
        self, player: Player, match: Match
    ) -> StatsBoost | None:
        """
        Récupère les statistiques de boost d'un joueur pour un match spécifique.

        Parameters
        ----------
        player : Player
            Le joueur dont on veut récupérer les statistiques de boost.
        match : Match
            Le match pour lequel on veut obtenir les statistiques.

        Returns
        -------
        StatsBoost | None
            Business Object contenant les statistiques de boost du joueur pour ce match,
            ou None si aucune donnée n'est disponible.

        Raises
        ------
        ValueError
            Si le joueur ou le match n'a pas d'ID valide.
        """
        if not player or not player.id:
            raise ValueError("Le joueur doit avoir un ID valide")

        if not match or not match.id:
            raise ValueError("Le match doit avoir un ID valide")

        return self.stats_boost_dao.get_player_match_stats_boost(player, match)

    def get_player_average_boost_stats(
        self, player: Player
    ) -> StatsBoostAggregatedDTO | None:
        """
        Récupère les statistiques moyennes de boost d'un joueur sur tous ses matchs.

        Parameters
        ----------
        player : Player
            Le joueur dont on veut récupérer les statistiques moyennes de boost.

        Returns
        -------
        StatsBoostAggregatedDTO | None
            DTO contenant les statistiques moyennes de boost du joueur,
            ou None si le joueur n'a aucune statistique disponible.

        Raises
        ------
        ValueError
            Si le joueur n'a pas d'ID valide.
        """
        if not player or not player.id:
            raise ValueError("Le joueur doit avoir un ID valide")

        return self.stats_boost_dao.get_player_average_stats_boost(player)
