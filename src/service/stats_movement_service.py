from src.dao.stats_movement_dao import StatMovementDAO
from src.models.matches import Match
from src.models.players import Player
from src.models.ranks import Ranks
from src.models.stats_movement import StatsMovement


class StatMovementService:
    """Service pour gérer les opérations métier liées aux statistiques de mouvement."""

    def __init__(self):
        self.stats_movement_dao = StatMovementDAO()

    def get_rank_movement_statistics(self, rank: Ranks) -> dict | None:
        """
        Récupère les statistiques moyennes de mouvement pour un rang donné.

        Parameters
        ----------
        rank : Ranks
            Le rang pour lequel on veut obtenir les statistiques de mouvement.

        Returns
        -------
        dict | None
            Dictionnaire contenant les statistiques moyennes de mouvement pour ce rang,
            ou None si aucune statistique n'est disponible.

        Notes
        -----
        Les statistiques de mouvement incluent typiquement la distance parcourue,
        le temps passé à différentes vitesses, les sauts, rotations, et autres
        métriques de mobilité pour tous les joueurs de ce rang.
        """
        return self.stats_movement_dao.get_average_stats_movement_per_rank(rank)

    def get_player_match_movement_stats(
        self, player: Player, match: Match
    ) -> StatsMovement | None:
        """
        Récupère les statistiques de mouvement d'un joueur pour un match spécifique.

        Parameters
        ----------
        player : Player
            Le joueur dont on veut récupérer les statistiques de mouvement.
        match : Match
            Le match pour lequel on veut obtenir les statistiques.

        Returns
        -------
        StatsMovement | None
            Les statistiques de mouvement du joueur pour ce match,
            ou None si aucune donnée n'est disponible.

        Raises
        ------
        ValueError
            Si le joueur ou le match n'a pas d'ID valide.

        Notes
        -----
        Les statistiques incluent la distance parcourue, le temps passé à vitesse
        supersonique, le temps passé au sol/en l'air, et autres métriques de mobilité.
        """
        if not player or not player.id:
            raise ValueError("Le joueur doit avoir un ID valide")

        if not match or not match.id:
            raise ValueError("Le match doit avoir un ID valide")

        return self.stats_movement_dao.get_player_match_stats_movement(player, match)

    def get_player_average_movement_stats(self, player: Player) -> dict | None:
        """
        Récupère les statistiques moyennes de mouvement d'un joueur sur tous ses matchs.

        Parameters
        ----------
        player : Player
            Le joueur dont on veut récupérer les statistiques moyennes de mouvement.

        Returns
        -------
        dict | None
            Dictionnaire contenant les statistiques moyennes de mouvement du joueur,
            ou None si le joueur n'a aucune statistique disponible.

        Raises
        ------
        ValueError
            Si le joueur n'a pas d'ID valide.
        """
        if not player or not player.id:
            raise ValueError("Le joueur doit avoir un ID valide")

        return self.stats_movement_dao.get_player_average_stats_movement(player)
