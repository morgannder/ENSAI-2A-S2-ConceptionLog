from src.dao.stats_core_dao import StatsCoreDAO
from src.models.matches import Match
from src.models.players import Player
from src.models.stats_core import StatsCore


class StatsCoreService:
    """Service pour gérer la logique métier des statistiques de jeu principales."""

    def __init__(self):
        self.stats_core_dao = StatsCoreDAO()

    def get_sum_stats_core_by_rank_name(self, rank_name: str) -> float | None:
        """
        Récupère les statistiques core pour un rang donné (par nom).

        Parameters
        ----------
        rank_name : str
            Le nom du rang (ex: "Bronze I", "Silver II", "Gold III").

        Returns
        -------
        float | None
            Les statistiques core pour ce rang, ou None si aucune donnée n'est disponible.

        Notes
        -----
        Cette méthode retourne les statistiques brutes (non moyennées) pour le rang.
        """
        return self.stats_core_dao.get_sum_stats_core_per_rank(rank_name)

    def get_average_stats_core_by_rank_name(self, rank_name: str) -> float | None:
        """
        Récupère les statistiques core moyennes pour un rang donné (par nom).

        Parameters
        ----------
        rank_name : str
            Le nom du rang (ex: "Bronze I", "Silver II", "Gold III").

        Returns
        -------
        float | None
            Les statistiques core moyennes pour ce rang,
            ou None si aucune donnée n'est disponible.

        Notes
        -----
        Cette méthode retourne la moyenne des statistiques core pour tous les joueurs
        du rang spécifié.
        """
        return self.stats_core_dao.get_average_stats_core_per_rank(rank_name)

    def get_player_match_stats_core(
        self, player: Player, match: Match
    ) -> StatsCore | None:
        """
        Récupère les statistiques core d'un joueur pour un match spécifique.

        Parameters
        ----------
        player : Player
            Le joueur dont on veut récupérer les statistiques.
        match : Match
            Le match pour lequel on veut obtenir les statistiques.

        Returns
        -------
        StatsCore | None
            Les statistiques core du joueur pour ce match,
            ou None si aucune donnée n'est disponible.

        Raises
        ------
        ValueError
            Si le joueur ou le match n'a pas d'ID valide.

        Notes
        -----
        Les statistiques core incluent typiquement les buts, passes décisives,
        sauvetages, tirs, et autres métriques de base du jeu.
        """
        if not player or not player.id:
            raise ValueError("Le joueur doit avoir un ID valide")

        if not match or not match.id:
            raise ValueError("Le match doit avoir un ID valide")

        return self.stats_core_dao.get_player_match_stats_core(player, match)

    def get_player_average_stats_core(self, player: Player) -> dict | None:
        """
        Récupère les statistiques core moyennes d'un joueur sur tous ses matchs.

        Parameters
        ----------
        player : Player
            Le joueur dont on veut récupérer les statistiques moyennes.

        Returns
        -------
        dict | None
            Dictionnaire contenant les statistiques core moyennes du joueur,
            ou None si le joueur n'a aucune statistique disponible.

        Raises
        ------
        ValueError
            Si le joueur n'a pas d'ID valide.

        """
        if not player or not player.id:
            raise ValueError("Le joueur doit avoir un ID valide")

        return self.stats_core_dao.get_player_average_stats_core(player)
