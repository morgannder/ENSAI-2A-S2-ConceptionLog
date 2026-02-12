from src.dao.db_connection import DBConnection
from src.utils.singleton import Singleton


class StatsCoreDAO(metaclass=Singleton):
    def __init__(self):
        self.db_connector = DBConnection()

    def get_average_stats_per_rank(self, rank_name: str) -> dict | None:
        """
        Récupère les stats globales des joueurs pour un rang donné.
        """
        query = """
            SELECT
                CASE
                    WHEN r.tier BETWEEN 1 AND 3 THEN 'Bronze'
                    WHEN r.tier BETWEEN 4 AND 6 THEN 'Silver'
                    WHEN r.tier BETWEEN 7 AND 9 THEN 'Gold'
                    WHEN r.tier BETWEEN 10 AND 12 THEN 'Platinum'
                    WHEN r.tier BETWEEN 13 AND 15 THEN 'Diamond'
                    WHEN r.tier BETWEEN 16 AND 18 THEN 'Champion'
                    WHEN r.tier BETWEEN 19 AND 21 THEN 'Grand Champion'
                    WHEN r.tier = 22 THEN 'Supersonic Legend'
                    ELSE 'Unknown'
                END AS rank_group,
                COUNT(*) AS nb_players,
                AVG(saves) AS avg_saves,
                AVG(assists) AS avg_assists,
                AVG(demo_inflicted) AS avg_demo_inflicted,
                AVG(demo_taken) AS avg_demo_taken,
                SUM(sc.goals) * 1.0 / NULLIF(SUM(sc.shots), 0) AS avg_shooting
            FROM stats_core sc
            INNER JOIN match_participation mp ON sc.participation_id = mp.id
            INNER JOIN ranks r ON mp.rank_id = r.id
            WHERE CASE
                WHEN r.tier BETWEEN 1 AND 3 THEN 'Bronze'
                WHEN r.tier BETWEEN 4 AND 6 THEN 'Silver'
                WHEN r.tier BETWEEN 7 AND 9 THEN 'Gold'
                WHEN r.tier BETWEEN 10 AND 12 THEN 'Platinum'
                WHEN r.tier BETWEEN 13 AND 15 THEN 'Diamond'
                WHEN r.tier BETWEEN 16 AND 18 THEN 'Champion'
                WHEN r.tier BETWEEN 19 AND 21 THEN 'Grand Champion'
                WHEN r.tier = 22 THEN 'Supersonic Legend'
                ELSE 'Unknown'
            END = ?
            GROUP BY rank_group
            """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (rank_name,))
            res = cursor.fetchone()
            if not res:
                return None

            return {
                "avg_shooting": res["avg_shooting"],
                "nb_players": res["nb_players"],
                "avg_saves": res["avg_saves"],
                "demo_taken": res["avg_demo_taken"],
                "avg_assists": res["avg_assists"],
                "demo_inflicted": res["avg_demo_inflicted"],
            }
