from src.dao.stats_positioning_dao import StatPositioningDAO
from src.dto.stats_positioning_dto import StatsPositioningAggregatedDTO
from src.models.matches import Match
from src.models.players import Player
from src.models.ranks import Ranks
from src.models.stats_positioning import StatsPositioning


class StatPositionningService:
    """Service pour gérer les opérations métier liées aux statistiques de positionnement."""

    def __init__(self):
        self.stats_positioning_dao = StatPositioningDAO()

    def get_average_stats_positioning_by_rank(
        self, rank: Ranks
    ) -> StatsPositioningAggregatedDTO | None:
        """
        Récupère les statistiques moyennes de positionnement pour un rang donné.

        Parameters
        ----------
        rank : Ranks
            Le rang pour lequel on veut obtenir les statistiques de positionnement.

        Returns
        -------
        dict | None
            Dictionnaire contenant les statistiques moyennes de positionnement pour ce rang,
            ou None si aucune statistique n'est disponible.

        Notes
        -----
        Les statistiques de positionnement incluent typiquement le temps passé en zone
        offensive, défensive, neutre, la position moyenne sur le terrain, et autres
        métriques de placement tactique pour tous les joueurs de ce rang.
        """
        return self.stats_positioning_dao.get_average_stats_positioning_per_rank(rank)

    def get_player_match_positioning_stats(
        self, player: Player, match: Match
    ) -> StatsPositioning | None:
        """
        Récupère les statistiques de positionnement d'un joueur pour un match spécifique.

        Parameters
        ----------
        player : Player
            Le joueur dont on veut récupérer les statistiques de positionnement.
        match : Match
            Le match pour lequel on veut obtenir les statistiques.

        Returns
        -------
        StatsPositionning | None
            Les statistiques de positionnement du joueur pour ce match,
            ou None si aucune donnée n'est disponible.

        Raises
        ------
        ValueError
            Si le joueur ou le match n'a pas d'ID valide.

        Notes
        -----
        Les statistiques incluent le temps passé dans chaque tiers du terrain
        (offensif, neutre, défensif), la position moyenne, et autres métriques
        de placement tactique durant le match.
        """
        if not player or not player.id:
            raise ValueError("Le joueur doit avoir un ID valide")

        if not match or not match.id:
            raise ValueError("Le match doit avoir un ID valide")

        return self.stats_positioning_dao.get_player_match_stats_positioning(
            player, match
        )

    def get_player_average_positioning_stats(
        self, player: Player
    ) -> StatsPositioningAggregatedDTO | None:
        """
        Récupère les statistiques moyennes de positionnement d'un joueur sur tous ses matchs.

        Parameters
        ----------
        player : Player
            Le joueur dont on veut récupérer les statistiques moyennes de positionnement.

        Returns
        -------
        dict | None
            Dictionnaire contenant les statistiques moyennes de positionnement du joueur,
            ou None si le joueur n'a aucune statistique disponible.

        Raises
        ------
        ValueError
            Si le joueur n'a pas d'ID valide.
        """
        if not player or not player.id:
            raise ValueError("Le joueur doit avoir un ID valide")

        return self.stats_positioning_dao.get_player_average_stats_positioning(player)
