from src.dao.db_connection import DBConnection
from src.dto.stats_positioning_dto import StatsPositioningAggregatedDTO
from src.models.matches import Match
from src.models.players import Player
from src.models.ranks import Ranks
from src.models.stats_positioning import StatsPositioning
from src.utils.singleton import Singleton


class StatPositioningDAO(metaclass=Singleton):
    def __init__(self):
        self.db_connector = DBConnection()

    def get_average_stats_positioning_per_rank(
        self, rank: Ranks
    ) -> StatsPositioningAggregatedDTO | None:
        """
        Récupère les statistiques de positionnement moyennes pour un rang donné.

        Parameters
        ----------
        rank : Ranks
            Le rang pour lequel on souhaite obtenir les statistiques moyennes.

        Returns
        -------
        StatsPositioningAggregatedDTO | None
            Un DTO contenant les moyennes des statistiques de positionnement
        """
        rank_name = rank.name
        query = query = """
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
                        ROUND(AVG(sp.average_distance_to_ball), 2) AS avg_average_distance_to_ball,
                        ROUND(AVG(sp.average_distance_to_mates), 2) AS avg_average_distance_to_mates,
                        ROUND(AVG(sp.time_defensive_third), 2) AS avg_time_defensive_third,
                        ROUND(AVG(sp.time_neutral_third), 2) AS avg_time_neutral_third,
                        ROUND(AVG(sp.time_offensive_third), 2) AS avg_time_offensive_third,
                        ROUND(AVG(sp.time_behind_ball), 2) AS avg_time_behind_ball,
                        ROUND(AVG(sp.time_infront_ball), 2) AS avg_time_infront_ball,
                        ROUND(AVG(sp.time_most_back), 2) AS avg_time_most_back,
                        ROUND(AVG(sp.time_most_forward), 2) AS avg_time_most_forward,
                        ROUND(AVG(sp.time_closest_to_ball), 2) AS avg_time_closest_to_ball,
                        ROUND(AVG(sp.time_farthest_to_ball), 2) AS avg_time_farthest_to_ball,
                        ROUND(AVG(sp.goals_against_while_last_defender), 2) AS avg_goals_against_while_last_defender,
                        ROUND(AVG(sp.percent_defensive_third), 2) AS avg_percent_defensive_third,
                        ROUND(AVG(sp.percent_offensive_third), 2) AS avg_percent_offensive_third,
                        ROUND(AVG(sp.percent_neutral_third), 2) AS avg_percent_neutral_third,
                        ROUND(AVG(sp.percent_defensive_half), 2) AS avg_percent_defensive_half,
                        ROUND(AVG(sp.percent_offensive_half), 2) AS avg_percent_offensive_half,
                        ROUND(AVG(sp.percent_behind_ball), 2) AS avg_percent_behind_ball,
                        ROUND(AVG(sp.percent_infront_ball), 2) AS avg_percent_infront_ball,
                        ROUND(AVG(sp.percent_most_back), 2) AS avg_percent_most_back,
                        ROUND(AVG(sp.percent_most_forward), 2) AS avg_percent_most_forward,
                        ROUND(AVG(sp.percent_closest_to_ball), 2) AS avg_percent_closest_to_ball,
                        ROUND(AVG(sp.percent_farthest_from_ball), 2) AS avg_percent_farthest_from_ball
                    FROM stats_positioning sp
                    INNER JOIN match_participation mp ON sp.participation_id = mp.id
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
        # ROUND(AVG(sp.average_distance_to_ball_possession), 2) AS avg_distance_to_ball_possession,
        # ROUND(AVG(sp.average_distance_to_ball_no_possession), 2) AS avg_distance_to_ball_no_possession,
        # ROUND(AVG(sp.time_defensive_half), 2) AS avg_time_defensive_half,
        # ROUNG(AVG(sp.time_offensive_half),2) AS avg_time_offensive_half,
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (rank_name,))
            res = cursor.fetchone()
            if not res:
                return None

            return StatsPositioningAggregatedDTO(
                average_distance_to_ball=res["avg_average_distance_to_ball"],
                # average_distance_to_ball_possession=res["avg_average_distance_to_ball_possession"],
                # average_distance_to_ball_no_possession=res["average_distance_to_ball_no_possession"],
                average_distance_to_mates=res["avg_average_distance_to_mates"],
                time_defensive_third=res["avg_time_defensive_third"],
                time_neutral_third=res["avg_time_neutral_third"],
                time_offensive_third=res["avg_time_offensive_third"],
                # time_defensive_half=res["time_defensive_half"],
                # time_offensive_half=res["time_offensive_half"],
                time_behind_ball=res["avg_time_behind_ball"],
                time_infront_ball=res["avg_time_infront_ball"],
                time_most_back=res["avg_time_most_back"],
                time_most_forward=res["avg_time_most_forward"],
                goals_against_while_last_defender=res[
                    "avg_goals_against_while_last_defender"
                ],
                time_closest_to_ball=res["avg_time_closest_to_ball"],
                time_farthest_to_ball=res["avg_time_farthest_to_ball"],
                percent_defensive_third=res["avg_percent_defensive_third"],
                percent_neutral_third=res["avg_percent_neutral_third"],
                percent_offensive_third=res["avg_percent_offensive_third"],
                percent_defensive_half=res["avg_percent_defensive_half"],
                percent_offensive_half=res["avg_percent_offensive_half"],
                percent_behind_ball=res["avg_percent_behind_ball"],
                percent_infront_ball=res["avg_percent_infront_ball"],
                percent_most_back=res["avg_percent_most_back"],
                percent_most_forward=res["avg_percent_most_forward"],
                percent_closest_to_ball=res["avg_percent_closest_to_ball"],
                percent_farthest_from_ball=res["avg_percent_farthest_from_ball"],
            )

    def get_player_match_stats_positioning(
        self, player: Player, match: Match
    ) -> StatsPositioning | None:
        """
        Récupère les statistiques de positionnement d'un joueur pour un match
        spécifique.

        Parameters
        ----------
        player : Player
            Le joueur dont on souhaite obtenir les statistiques.
        match : Match
            Le match concerné.

        Returns
        -------
        StatsPositioning | None
            Un objet métier contenant les statistiques de positionnement brutes
            du joueur pour ce match, ou None si aucune donnée n'est trouvée.
        """
        query = """
                SELECT sp.*
                FROM stats_positioning sp
                JOIN match_participation mp ON mp.id = sp.participation_id
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
            return StatsPositioning(
                participation_id=res["participation_id"],
                average_distance_to_ball=res["average_distance_to_ball"],
                # average_distance_to_ball_possession=res[
                #    "average_distance_to_ball_possession"
                # ],
                # average_distance_to_ball_no_possession=res[
                #    "average_distance_to_ball_no_possession"
                # ],
                average_distance_to_mates=res["average_distance_to_mates"],
                time_defensive_third=res["time_defensive_third"],
                time_neutral_third=res["time_neutral_third"],
                time_offensive_third=res["time_offensive_third"],
                # time_defensive_half=res["time_defensive_half"],
                # time_offensive_half=res["time_offensive_half"],
                time_behind_ball=res["time_behind_ball"],
                time_infront_ball=res["time_infront_ball"],
                time_most_back=res["time_most_back"],
                time_most_forward=res["time_most_forward"],
                goals_against_while_last_defender=res[
                    "goals_against_while_last_defender"
                ],
                time_closest_to_ball=res["time_closest_to_ball"],
                time_farthest_to_ball=res["time_farthest_to_ball"],
                percent_defensive_third=res["percent_defensive_third"],
                percent_neutral_third=res["percent_neutral_third"],
                percent_offensive_third=res["percent_offensive_third"],
                percent_defensive_half=res["percent_defensive_half"],
                percent_offensive_half=res["percent_offensive_half"],
                percent_behind_ball=res["percent_behind_ball"],
                percent_infront_ball=res["percent_infront_ball"],
                percent_most_back=res["percent_most_back"],
                percent_most_forward=res["percent_most_forward"],
                percent_closest_to_ball=res["percent_closest_to_ball"],
                percent_farthest_from_ball=res["percent_farthest_from_ball"],
            )

    def get_player_average_stats_positioning(
        self, player: Player
    ) -> StatsPositioningAggregatedDTO | None:
        """
        Récupère les statistiques de positionnement moyennes d'un joueur sur
        l'ensemble de ses matchs.

        Parameters
        ----------
        player : Player
            Le joueur dont on souhaite obtenir les statistiques moyennes.

        Returns
        -------
        StatsPositioningAggregatedDTO | None
            Un DTO contenant les moyennes des statistiques de positionnement
            du joueur, ou None si aucune donnée n'est trouvée.
        """
        query = """
                SELECT
                    AVG(sp.average_distance_to_ball) AS avg_average_distance_to_ball,
                    AVG(sp.average_distance_to_mates) AS avg_average_distance_to_mates,
                    AVG(sp.time_defensive_third) AS avg_time_defensive_third,
                    AVG(sp.time_neutral_third) AS avg_time_neutral_third,
                    AVG(sp.time_offensive_third) AS avg_time_offensive_third,
                    AVG(sp.time_behind_ball) AS avg_time_behind_ball,
                    AVG(sp.time_infront_ball) AS avg_time_infront_ball,
                    AVG(sp.time_most_back) AS avg_time_most_back,
                    AVG(sp.time_most_forward) AS avg_time_most_forward,
                    AVG(sp.time_closest_to_ball) AS avg_time_closest_to_ball,
                    AVG(sp.time_farthest_to_ball) AS avg_time_farthest_to_ball,
                    AVG(sp.goals_against_while_last_defender) AS avg_goals_against_while_last_defender,
                    AVG(sp.percent_defensive_third) AS avg_percent_defensive_third,
                    AVG(sp.percent_offensive_third) AS avg_percent_offensive_third,
                    AVG(sp.percent_neutral_third) AS avg_percent_neutral_third,
                    AVG(sp.percent_defensive_half) AS avg_percent_defensive_half,
                    AVG(sp.percent_offensive_half) AS avg_percent_offensive_half,
                    AVG(sp.percent_behind_ball) AS avg_percent_behind_ball,
                    AVG(sp.percent_infront_ball) AS avg_percent_infront_ball,
                    AVG(sp.percent_most_back) AS avg_percent_most_back,
                    AVG(sp.percent_most_forward) AS avg_percent_most_forward,
                    AVG(sp.percent_closest_to_ball) AS avg_percent_closest_to_ball,
                    AVG(sp.percent_farthest_from_ball) AS avg_percent_farthest_from_ball
                FROM stats_positioning sp
                JOIN match_participation mp ON sp.participation_id = mp.id
                JOIN players p ON mp.player_id = p.id
                WHERE p.id = ?
                """
        # ROUND(AVG(sp.average_distance_to_ball_possession), 2) AS avg_distance_to_ball_possession,
        # ROUND(AVG(sp.average_distance_to_ball_no_possession), 2) AS avg_distance_to_ball_no_possession,
        # ROUND(AVG(sp.time_defensive_half), 2) AS avg_time_defensive_half,
        # ROUNG(AVG(sp.time_offensive_half),2) AS avg_time_offensive_half,
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (player.id,))
            res = cursor.fetchone()
            if not res:
                return None
            return StatsPositioningAggregatedDTO(
                average_distance_to_ball=res["avg_average_distance_to_ball"],
                # average_distance_to_ball_possession=res["avg_average_distance_to_ball_possession"],
                # average_distance_to_ball_no_possession=res["average_distance_to_ball_no_possession"],
                average_distance_to_mates=res["avg_average_distance_to_mates"],
                time_defensive_third=res["avg_time_defensive_third"],
                time_neutral_third=res["avg_time_neutral_third"],
                time_offensive_third=res["avg_time_offensive_third"],
                # time_defensive_half=res["time_defensive_half"],
                # time_offensive_half=res["time_offensive_half"],
                time_behind_ball=res["avg_time_behind_ball"],
                time_infront_ball=res["avg_time_infront_ball"],
                time_most_back=res["avg_time_most_back"],
                time_most_forward=res["avg_time_most_forward"],
                goals_against_while_last_defender=res[
                    "avg_goals_against_while_last_defender"
                ],
                time_closest_to_ball=res["avg_time_closest_to_ball"],
                time_farthest_to_ball=res["avg_time_farthest_to_ball"],
                percent_defensive_third=res["avg_percent_defensive_third"],
                percent_neutral_third=res["avg_percent_neutral_third"],
                percent_offensive_third=res["avg_percent_offensive_third"],
                percent_defensive_half=res["avg_percent_defensive_half"],
                percent_offensive_half=res["avg_percent_offensive_half"],
                percent_behind_ball=res["avg_percent_behind_ball"],
                percent_infront_ball=res["avg_percent_infront_ball"],
                percent_most_back=res["avg_percent_most_back"],
                percent_most_forward=res["avg_percent_most_forward"],
                percent_closest_to_ball=res["avg_percent_closest_to_ball"],
                percent_farthest_from_ball=res["avg_percent_farthest_from_ball"],
            )
