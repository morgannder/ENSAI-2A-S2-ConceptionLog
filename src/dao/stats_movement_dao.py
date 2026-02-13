from ..models.matches import Match
from ..models.players import Player
from ..models.ranks import Ranks
from ..models.stats_movement import StatsMovement
from ..utils.singleton import Singleton
from .db_connection import DBConnection


class StatMovementDAO(metaclass=Singleton):
    def __init__(self):
        self.db_connector = DBConnection()

    def get_average_stats_movement_per_rank(self, rank: Ranks) -> dict | None:
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
                    END AS rank_group,
                    COUNT(DISTINCT mp.player_id) AS nb_players,
                    AVG(sm.avg_speed) AS avg_avg_speed,
                    AVG(sm.total_distance) AS avg_total_distance,
                    AVG(sm.time_supersonic_speed) AS avg_time_supersonic_speed,
                    AVG(sm.time_boost_speed) AS avg_time_boost_speed,
                    AVG(sm.time_slow_speed) AS avg_time_slow_speed,
                    AVG(sm.time_ground) AS avg_time_ground,
                    AVG(sm.time_low_air) AS avg_time_low_air,
                    AVG(sm.time_high_air) AS avg_time_high_air,
                    AVG(sm.time_powerslide) AS avg_time_powerslide,
                    AVG(sm.count_powerslide) AS avg_count_powerslide,
                    AVG(sm.average_powerslide_duration) AS avg_average_powerslide_duration,
                    AVG(sm.average_speed_percentage) AS avg_average_speed_percentage,
                    AVG(sm.percent_slow_speed) AS avg_percent_slow_speed,
                    AVG(sm.percent_boost_speed) AS avg_percent_boost_speed,
                    AVG(sm.percent_supersonic_speed) AS avg_percent_supersonic_speed,
                    AVG(sm.percent_ground) AS avg_percent_ground,
                    AVG(sm.percent_low_air) AS avg_percent_low_air,
                    AVG(sm.percent_high_air) AS avg_percent_high_air
                FROM stats_movement sm
                INNER JOIN match_participation mp ON sm.participation_id = mp.id
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
                "rank_group": res["rank_group"],
                "nb_players": res["nb_players"],
                "avg_avg_speed": res["avg_avg_speed"],
                "avg_total_distance": res["avg_total_distance"],
                "avg_time_supersonic_speed": res["avg_time_supersonic_speed"],
                "avg_time_boost_speed": res["avg_time_boost_speed"],
                "avg_time_slow_speed": res["avg_time_slow_speed"],
                "avg_time_ground": res["avg_time_ground"],
                "avg_time_low_air": res["avg_time_low_air"],
                "avg_time_high_air": res["avg_time_high_air"],
                "avg_time_powerslide": res["avg_time_powerslide"],
                "avg_count_powerslide": res["avg_count_powerslide"],
                "avg_average_powerslide_duration": res[
                    "avg_average_powerslide_duration"
                ],
                "avg_average_speed_percentage": res["avg_average_speed_percentage"],
                "avg_percent_slow_speed": res["avg_percent_slow_speed"],
                "avg_percent_boost_speed": res["avg_percent_boost_speed"],
                "avg_percent_supersonic_speed": res["avg_percent_supersonic_speed"],
                "avg_percent_ground": res["avg_percent_ground"],
                "avg_percent_low_air": res["avg_percent_low_air"],
                "avg_percent_high_air": res["avg_percent_high_air"],
            }

    def get_player_match_stats_movement(
        self, player: Player, match: Match
    ) -> StatsMovement | None:
        query = """
                SELECT sm.*
                FROM stats_movement sm
                JOIN match_participation mp ON mp.id = sm.participation_id
                JOIN match_teams mt ON mt.id = mp.match_team_id
                JOIN matches m ON m.id = mt.match_id
                JOIN players p ON p.id = mp.player_id
                WHERE m.id = ? AND p.id = ?
                """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (match.id, player.id))
            res = cursor.fetchone()
            if not res:
                return None
            return StatsMovement(
                participation_id=res["participation_id"],
                avg_speed=res["avg_speed"],
                total_distance=res["total_distance"],
                time_supersonic_speed=res["time_supersonic_speed"],
                time_boost_speed=res["time_boost_speed"],
                time_slow_speed=res["time_slow_speed"],
                time_ground=res["time_ground"],
                time_low_air=res["time_low_air"],
                time_high_air=res["time_high_air"],
                time_powerslide=res["time_powerslide"],
                count_powerslide=res["count_powerslide"],
                average_powerslide_duration=res["average_powerslide_duration"],
                average_speed_percentage=res["average_speed_percentage"],
                percent_slow_speed=res["percent_slow_speed"],
                percent_boost_speed=res["percent_boost_speed"],
                percent_supersonic_speed=res["percent_supersonic_speed"],
                percent_ground=res["percent_ground"],
                percent_low_air=res["percent_low_air"],
                percent_high_air=res["percent_high_air"],
            )

    def get_player_average_stats_movement(self, player: Player) -> dict | None:
        query = """
                SELECT
                    AVG(sm.avg_speed) AS avg_avg_speed,
                    AVG(sm.total_distance) AS avg_total_distance,
                    AVG(sm.time_supersonic_speed) AS avg_time_supersonic_speed,
                    AVG(sm.time_boost_speed) AS avg_time_boost_speed,
                    AVG(sm.time_slow_speed) AS avg_time_slow_speed,
                    AVG(sm.time_ground) AS avg_time_ground,
                    AVG(sm.time_low_air) AS avg_time_low_air,
                    AVG(sm.time_high_air) AS avg_time_high_air,
                    AVG(sm.time_powerslide) AS avg_time_powerslide,
                    AVG(sm.count_powerslide) AS avg_count_powerslide,
                    AVG(sm.average_powerslide_duration) AS avg_average_powerslide_duration,
                    AVG(sm.average_speed_percentage) AS avg_average_speed_percentage,
                    AVG(sm.percent_slow_speed) AS avg_percent_slow_speed,
                    AVG(sm.percent_boost_speed) AS avg_percent_boost_speed,
                    AVG(sm.percent_supersonic_speed) AS avg_percent_supersonic_speed,
                    AVG(sm.percent_ground) AS avg_percent_ground,
                    AVG(sm.percent_low_air) AS avg_percent_low_air,
                    AVG(sm.percent_high_air) AS avg_percent_high_air
                FROM stats_movement sm
                JOIN match_participation mp ON sm.participation_id = mp.id
                JOIN players p ON mp.player_id = p.id
                WHERE p.id = ?
                """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (player.id,))
            res = cursor.fetchone()
            if not res:
                return None
            return {
                "avg_avg_speed": res["avg_avg_speed"],
                "avg_total_distance": res["avg_total_distance"],
                "avg_time_supersonic_speed": res["avg_time_supersonic_speed"],
                "avg_time_boost_speed": res["avg_time_boost_speed"],
                "avg_time_slow_speed": res["avg_time_slow_speed"],
                "avg_time_ground": res["avg_time_ground"],
                "avg_time_low_air": res["avg_time_low_air"],
                "avg_time_high_air": res["avg_time_high_air"],
                "avg_time_powerslide": res["avg_time_powerslide"],
                "avg_count_powerslide": res["avg_count_powerslide"],
                "avg_average_powerslide_duration": res[
                    "avg_average_powerslide_duration"
                ],
                "avg_average_speed_percentage": res["avg_average_speed_percentage"],
                "avg_percent_slow_speed": res["avg_percent_slow_speed"],
                "avg_percent_boost_speed": res["avg_percent_boost_speed"],
                "avg_percent_supersonic_speed": res["avg_percent_supersonic_speed"],
                "avg_percent_ground": res["avg_percent_ground"],
                "avg_percent_low_air": res["avg_percent_low_air"],
                "avg_percent_high_air": res["avg_percent_high_air"],
            }
