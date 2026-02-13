from ..models.matches import Match
from ..models.players import Player
from ..models.ranks import Ranks
from ..models.stats_boost import StatsBoost
from ..utils.singleton import Singleton
from .db_connection import DBConnection


class StatBoostDAO(metaclass=Singleton):
    def __init__(self):
        self.db_connector = DBConnection()

    def get_average_stats_boost_per_rank(self, rank: Ranks) -> dict | None:
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
                    AVG(sb.boost_per_minute) AS avg_boost_per_minute,
                    AVG(sb.boost_consumed_per_minute) AS avg_boost_consumed_per_minute,
                    AVG(sb.average_amount) AS avg_average_amount,
                    AVG(sb.amount_collected) AS avg_amount_collected,
                    AVG(sb.amount_stolen) AS avg_amount_stolen,
                    AVG(sb.amount_collected_big) AS avg_amount_collected_big,
                    AVG(sb.amount_stolen_big) AS avg_amount_stolen_big,
                    AVG(sb.amount_collected_small) AS avg_amount_collected_small,
                    AVG(sb.amount_stolen_small) AS avg_amount_stolen_small,
                    AVG(sb.count_collected_big) AS avg_count_collected_big,
                    AVG(sb.count_stolen_big) AS avg_count_stolen_big,
                    AVG(sb.count_collected_small) AS avg_count_collected_small,
                    AVG(sb.count_stolen_small) AS avg_count_stolen_small,
                    AVG(sb.amount_overfill) AS avg_amount_overfill,
                    AVG(sb.amount_overfill_stolen) AS avg_amount_overfill_stolen,
                    AVG(sb.amount_used_while_supersonic) AS avg_amount_used_while_supersonic,
                    AVG(sb.time_zero_boost) AS avg_time_zero_boost,
                    AVG(sb.percent_zero_boost) AS avg_percent_zero_boost,
                    AVG(sb.time_full_boost) AS avg_time_full_boost,
                    AVG(sb.percent_full_boost) AS avg_percent_full_boost,
                    AVG(sb.time_boost_0_25) AS avg_time_boost_0_25,
                    AVG(sb.time_boost_25_50) AS avg_time_boost_25_50,
                    AVG(sb.time_boost_50_75) AS avg_time_boost_50_75,
                    AVG(sb.time_boost_75_100) AS avg_time_boost_75_100,
                    AVG(sb.percent_boost_0_25) AS avg_percent_boost_0_25,
                    AVG(sb.percent_boost_25_50) AS avg_percent_boost_25_50,
                    AVG(sb.percent_boost_50_75) AS avg_percent_boost_50_75,
                    AVG(sb.percent_boost_75_100) AS avg_percent_boost_75_100,
                    AVG(sb.amount_collected) * 1.0 / NULLIF(AVG(sb.boost_consumed_per_minute), 0) AS boost_efficiency_ratio
                FROM stats_boost sb
                INNER JOIN match_participation mp ON sb.participation_id = mp.id
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
                "avg_boost_per_minute": res["avg_boost_per_minute"],
                "avg_boost_consumed_per_minute": res["avg_boost_consumed_per_minute"],
                "avg_average_amount": res["avg_average_amount"],
                "avg_amount_collected": res["avg_amount_collected"],
                "avg_amount_stolen": res["avg_amount_stolen"],
                "avg_amount_collected_big": res["avg_amount_collected_big"],
                "avg_amount_stolen_big": res["avg_amount_stolen_big"],
                "avg_amount_collected_small": res["avg_amount_collected_small"],
                "avg_amount_stolen_small": res["avg_amount_stolen_small"],
                "avg_count_collected_big": res["avg_count_collected_big"],
                "avg_count_stolen_big": res["avg_count_stolen_big"],
                "avg_count_collected_small": res["avg_count_collected_small"],
                "avg_count_stolen_small": res["avg_count_stolen_small"],
                "avg_amount_overfill": res["avg_amount_overfill"],
                "avg_amount_overfill_stolen": res["avg_amount_overfill_stolen"],
                "avg_amount_used_while_supersonic": res[
                    "avg_amount_used_while_supersonic"
                ],
                "avg_time_zero_boost": res["avg_time_zero_boost"],
                "avg_percent_zero_boost": res["avg_percent_zero_boost"],
                "avg_time_full_boost": res["avg_time_full_boost"],
                "avg_percent_full_boost": res["avg_percent_full_boost"],
                "avg_time_boost_0_25": res["avg_time_boost_0_25"],
                "avg_time_boost_25_50": res["avg_time_boost_25_50"],
                "avg_time_boost_50_75": res["avg_time_boost_50_75"],
                "avg_time_boost_75_100": res["avg_time_boost_75_100"],
                "avg_percent_boost_0_25": res["avg_percent_boost_0_25"],
                "avg_percent_boost_25_50": res["avg_percent_boost_25_50"],
                "avg_percent_boost_50_75": res["avg_percent_boost_50_75"],
                "avg_percent_boost_75_100": res["avg_percent_boost_75_100"],
                "boost_efficiency_ratio": res["boost_efficiency_ratio"],
            }

    def get_player_match_stats_boost(
        self, player: Player, match: Match
    ) -> StatsBoost | None:
        query = """
                SELECT sb.*
                FROM stats_boost sb
                JOIN match_participation mp ON mp.id = sb.participation_id
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
            return StatsBoost(
                participation_id=res["participation_id"],
                boost_per_minute=res["boost_per_minute"],
                boost_consumed_per_minute=res["boost_consumed_per_minute"],
                average_amount=res["average_amount"],
                amount_collected=res["amount_collected"],
                amount_stolen=res["amount_stolen"],
                amount_collected_big=res["amount_collected_big"],
                amount_stolen_big=res["amount_stolen_big"],
                amount_collected_small=res["amount_collected_small"],
                amount_stolen_small=res["amount_stolen_small"],
                count_collected_big=res["count_collected_big"],
                count_stolen_big=res["count_stolen_big"],
                count_collected_small=res["count_collected_small"],
                count_stolen_small=res["count_stolen_small"],
                amount_overfill=res["amount_overfill"],
                amount_overfill_stolen=res["amount_overfill_stolen"],
                amount_used_while_supersonic=res["amount_used_while_supersonic"],
                time_zero_boost=res["time_zero_boost"],
                percent_zero_boost=res["percent_zero_boost"],
                time_full_boost=res["time_full_boost"],
                percent_full_boost=res["percent_full_boost"],
                time_boost_0_25=res["time_boost_0_25"],
                time_boost_25_50=res["time_boost_25_50"],
                time_boost_50_75=res["time_boost_50_75"],
                time_boost_75_100=res["time_boost_75_100"],
                percent_boost_0_25=res["percent_boost_0_25"],
                percent_boost_25_50=res["percent_boost_25_50"],
                percent_boost_50_75=res["percent_boost_50_75"],
                percent_boost_75_100=res["percent_boost_75_100"],
            )

    def get_player_average_stats_boost(self, player: Player) -> dict | None:
        query = """
                SELECT
                    AVG(sb.boost_per_minute) AS avg_boost_per_minute,
                    AVG(sb.boost_consumed_per_minute) AS avg_boost_consumed_per_minute,
                    AVG(sb.average_amount) AS avg_average_amount,
                    AVG(sb.amount_collected) AS avg_amount_collected,
                    AVG(sb.amount_stolen) AS avg_amount_stolen,
                    AVG(sb.amount_collected_big) AS avg_amount_collected_big,
                    AVG(sb.amount_stolen_big) AS avg_amount_stolen_big,
                    AVG(sb.amount_collected_small) AS avg_amount_collected_small,
                    AVG(sb.amount_stolen_small) AS avg_amount_stolen_small,
                    AVG(sb.count_collected_big) AS avg_count_collected_big,
                    AVG(sb.count_stolen_big) AS avg_count_stolen_big,
                    AVG(sb.count_collected_small) AS avg_count_collected_small,
                    AVG(sb.count_stolen_small) AS avg_count_stolen_small,
                    AVG(sb.amount_overfill) AS avg_amount_overfill,
                    AVG(sb.amount_overfill_stolen) AS avg_amount_overfill_stolen,
                    AVG(sb.amount_used_while_supersonic) AS avg_amount_used_while_supersonic,
                    AVG(sb.time_zero_boost) AS avg_time_zero_boost,
                    AVG(sb.percent_zero_boost) AS avg_percent_zero_boost,
                    AVG(sb.time_full_boost) AS avg_time_full_boost,
                    AVG(sb.percent_full_boost) AS avg_percent_full_boost,
                    AVG(sb.time_boost_0_25) AS avg_time_boost_0_25,
                    AVG(sb.time_boost_25_50) AS avg_time_boost_25_50,
                    AVG(sb.time_boost_50_75) AS avg_time_boost_50_75,
                    AVG(sb.time_boost_75_100) AS avg_time_boost_75_100,
                    AVG(sb.percent_boost_0_25) AS avg_percent_boost_0_25,
                    AVG(sb.percent_boost_25_50) AS avg_percent_boost_25_50,
                    AVG(sb.percent_boost_50_75) AS avg_percent_boost_50_75,
                    AVG(sb.percent_boost_75_100) AS avg_percent_boost_75_100,
                    AVG(sb.amount_collected) * 1.0 / NULLIF(AVG(sb.boost_consumed_per_minute), 0) AS boost_efficiency_ratio
                FROM stats_boost sb
                JOIN match_participation mp ON sb.participation_id = mp.id
                JOIN players p on p.id = ?
                """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (player.id,))
            res = cursor.fetchone()
            if not res:
                return None
            return {
                "avg_boost_per_minute": res["avg_boost_per_minute"],
                "avg_boost_consumed_per_minute": res["avg_boost_consumed_per_minute"],
                "avg_average_amount": res["avg_average_amount"],
                "avg_amount_collected": res["avg_amount_collected"],
                "avg_amount_stolen": res["avg_amount_stolen"],
                "avg_amount_collected_big": res["avg_amount_collected_big"],
                "avg_amount_stolen_big": res["avg_amount_stolen_big"],
                "avg_amount_collected_small": res["avg_amount_collected_small"],
                "avg_amount_stolen_small": res["avg_amount_stolen_small"],
                "avg_count_collected_big": res["avg_count_collected_big"],
                "avg_count_stolen_big": res["avg_count_stolen_big"],
                "avg_count_collected_small": res["avg_count_collected_small"],
                "avg_count_stolen_small": res["avg_count_stolen_small"],
                "avg_amount_overfill": res["avg_amount_overfill"],
                "avg_amount_overfill_stolen": res["avg_amount_overfill_stolen"],
                "avg_amount_used_while_supersonic": res[
                    "avg_amount_used_while_supersonic"
                ],
                "avg_time_zero_boost": res["avg_time_zero_boost"],
                "avg_percent_zero_boost": res["avg_percent_zero_boost"],
                "avg_time_full_boost": res["avg_time_full_boost"],
                "avg_percent_full_boost": res["avg_percent_full_boost"],
                "avg_time_boost_0_25": res["avg_time_boost_0_25"],
                "avg_time_boost_25_50": res["avg_time_boost_25_50"],
                "avg_time_boost_50_75": res["avg_time_boost_50_75"],
                "avg_time_boost_75_100": res["avg_time_boost_75_100"],
                "avg_percent_boost_0_25": res["avg_percent_boost_0_25"],
                "avg_percent_boost_25_50": res["avg_percent_boost_25_50"],
                "avg_percent_boost_50_75": res["avg_percent_boost_50_75"],
                "avg_percent_boost_75_100": res["avg_percent_boost_75_100"],
                "boost_efficiency_ratio": res["boost_efficiency_ratio"],
            }
