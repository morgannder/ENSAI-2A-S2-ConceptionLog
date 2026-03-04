from src.dao.stats_core_dao import StatsCoreDAO
from src.dto.stats_core_dto import StatsCoreAggregatedDTO
from src.models.matches import Match
from src.models.players import Player
from src.models.ranks import Ranks
from src.models.stats_core import StatsCore


class StatsCoreService:
    """Service pour gérer la logique métier des statistiques de jeu principales."""

    def __init__(self):
        self.stats_core_dao = StatsCoreDAO()

    def get_average_stats_core_by_rank(
        self, rank: Ranks, game_mode: str | None = None
    ) -> StatsCoreAggregatedDTO | None:
        """
        Récupère les statistiques core moyennes pour un rang donné.

        Parameters
        ----------
        rank : Ranks
            Le rang pour lequel on veut obtenir les statistiques core.
        game_mode : str | None, optional
            Le mode de jeu sur lequel filtrer, par défaut None (tous les modes).

        Returns
        -------
        StatsCoreAggregatedDTO | None
            Les statistiques core moyennes pour ce rang,
            ou None si aucune donnée n'est disponible.
        """
        return self.stats_core_dao.get_average_stats_core_per_rank(rank, game_mode)

    def get_player_match_stats_core(
        self, player: Player, match: Match, game_mode: str | None = None
    ) -> StatsCore | None:
        """
        Récupère les statistiques core d'un joueur pour un match spécifique.

        Parameters
        ----------
        player : Player
            Le joueur dont on veut récupérer les statistiques.
        match : Match
            Le match pour lequel on veut obtenir les statistiques.
        game_mode : str | None, optional
            Le mode de jeu sur lequel filtrer, par défaut None (tous les modes).

        Returns
        -------
        StatsCore | None
            Les statistiques core du joueur pour ce match,
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

        return self.stats_core_dao.get_player_match_stats_core(player, match, game_mode)

    def get_player_average_stats_core(
        self, player: Player, game_mode: str | None = None
    ) -> StatsCoreAggregatedDTO | None:
        """
        Récupère les statistiques core moyennes d'un joueur sur tous ses matchs.

        Parameters
        ----------
        player : Player
            Le joueur dont on veut récupérer les statistiques moyennes.
        game_mode : str | None, optional
            Le mode de jeu sur lequel filtrer, par défaut None (tous les modes).

        Returns
        -------
        StatsCoreAggregatedDTO | None
            Les statistiques core moyennes du joueur,
            ou None si le joueur n'a aucune statistique disponible.

        Raises
        ------
        ValueError
            Si le joueur n'a pas d'ID valide.
        """
        if not player or not player.id:
            raise ValueError("Le joueur doit avoir un ID valide")

        return self.stats_core_dao.get_player_average_stats_core(player, game_mode)
