from src.dao.stats_core_dao import StatsCoreDAO


class StatsCoreService:
    """Service pour gérer la logique métier des statistiques de jeu."""

    def __init__(self):
        self.stats_core_dao = StatsCoreDAO()

    def get_average_stats_by_rank_name(self, rank_name: str) -> float | None:
        """
        Récupère le pourcentage de tir moyen pour un rang donné (par nom).
        """
        if not rank_name or not rank_name.strip():
            raise ValueError("Le nom du rang ne peut pas être vide")

        return self.stats_core_dao.get_average_stats_per_rank(rank_name.strip())
