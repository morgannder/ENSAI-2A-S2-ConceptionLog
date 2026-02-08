from src.dao.db_connection import DBConnection
from src.utils.singleton import Singleton


class StatsCoreDAO(metaclass=Singleton):
    def __init__(self):
        self.db_connector = DBConnection()

    def get_average_stats_per_rank(self, rank_name: str) -> float | None:
        """
        Récupère le pourcentage de tir moyen pour un rang donné.
        """
        connection = self.db_connector.connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                COUNT(*) AS nb_matches,
                AVG(saves) AS avg_saves,
                AVG(assists) AS avg_assists,
                AVG(demo_inflicted) AS avg_demo_inflicted,
                AVG(demo_taken) AS avg_demo_taken,
                SUM(sc.goals) * 1.0 / NULLIF(SUM(sc.shots), 0) AS avg_shooting
                FROM stats_core sc
                INNER JOIN match_participation mp ON sc.participation_id = mp.id
                INNER JOIN ranks r ON mp.rank_id = r.id
                WHERE r.name = ?
                GROUP BY r.name
                """,
                (rank_name.title(),),
            )
            res = cursor.fetchone()

            if not res:
                return None

            return {
                "avg_shooting": res["avg_shooting"],
                "nb_matches": res["nb_matches"],
                "avg_saves": res["avg_saves"],
                "demo_taken": res["avg_demo_taken"],
                "avg_assists": res["avg_assists"],
                "demo_inflicted": res["avg_demo_inflicted"],
            }

        finally:
            cursor.close()
