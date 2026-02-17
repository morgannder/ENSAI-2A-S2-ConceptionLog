from src.dao.db_connection import DBConnection
from src.dto.stats_core_dto import StatsCoreAggregatedDTO
from src.models.matches import Match
from src.models.players import Player
from src.models.ranks import Ranks
from src.models.stats_core import StatsCore
from src.utils.singleton import Singleton


class StatsCoreDAO(metaclass=Singleton):
    def __init__(self):
        self.db_connector = DBConnection()

    def get_average_stats_core_per_rank(
        self, rank: Ranks
    ) -> StatsCoreAggregatedDTO | None:
        """
        Récupère les stats globales des joueurs pour un rang donné.
        """
        rank_name = rank.name
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
                END AS rank_group,ROUND(AVG(shots), 2) AS avg_shots,
                ROUND(AVG(goals), 2) AS avg_goals,
                ROUND(AVG(saves), 2) AS avg_saves,
                ROUND(AVG(assists), 2) AS avg_assists,
                ROUND(AVG(demo_inflicted), 2) AS avg_demo_inflicted,
                ROUND(AVG(demo_taken), 2) AS avg_demo_taken,
                ROUND(AVG(score), 2) AS avg_score,
                ROUND(AVG(shooting_percentage), 2) AS avg_shooting_percentage
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

            return StatsCoreAggregatedDTO(
                shots=res["avg_shots"],
                goals=res["avg_goals"],
                saves=res["avg_saves"],
                assists=res["avg_assists"],
                score=res["avg_score"],
                shooting_percentage=res["avg_shooting_percentage"],
                demo_inflicted=res["avg_demo_inflicted"],
                demo_taken=res["avg_demo_taken"],
            )

    def get_player_match_stats_core(
        self, player: Player, match: Match
    ) -> StatsCore | None:
        query = """
                SELECT sc.*
                FROM stats_core sc
                JOIN match_participation mp ON mp.id = sc.participation_id
                JOIN match_teams mt ON mt.id = mp.match_team_id
                JOIN matches m ON m.id = mt.match_id
                JOIN players p ON p.id = mp.player_id
                WHERE m.id = ? and p.id = ?
                """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                query,
                (
                    match.id,
                    player.id,
                ),
            )
            res = cursor.fetchone()
            if not res:
                return None
            return StatsCore(
                participation_id=res["participation_id"],
                shots=res["shots"],
                goals=res["goals"],
                saves=res["saves"],
                assists=res["assists"],
                score=res["score"],
                shooting_percentage=res["shooting_percentage"],
                demo_inflicted=res["demo_inflicted"],
                demo_taken=res["demo_taken"],
            )

    def get_player_average_stats_core(
        self, player: Player
    ) -> StatsCoreAggregatedDTO | None:
        query = """
                SELECT
                    ROUND(AVG(goals), 2) AS avg_goals,
                    ROUND(AVG(saves), 2) AS avg_saves,
                    ROUND(AVG(assists), 2) AS avg_assists,
                    ROUND(AVG(demo_inflicted), 2) AS avg_demo_inflicted,
                    ROUND(AVG(demo_taken), 2) AS avg_demo_taken,
                    ROUND(AVG(score), 2) AS avg_score,
                    ROUND(AVG(shooting_percentage), 2) AS avg_shooting_percentage
                FROM stats_core sc
                JOIN match_participation mp ON sc.participation_id = mp.id
                JOIN players p on p.id = ?
                """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (player.id,))
            res = cursor.fetchone()
            if not res:
                return None
            return StatsCoreAggregatedDTO(
                shots=res["avg_shots"],
                goals=res["avg_goals"],
                saves=res["avg_saves"],
                assists=res["avg_assists"],
                score=res["avg_score"],
                shooting_percentage=res["avg_shooting_percentage"],
                demo_inflicted=res["avg_demo_inflicted"],
                demo_taken=res["avg_demo_taken"],
            )
