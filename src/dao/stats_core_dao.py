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
        self, rank: Ranks, game_mode: str | None = None
    ) -> StatsCoreAggregatedDTO | None:
        """
        Récupère les statistiques de jeu (Core) moyennes pour un rang donné.

        Parameters
        ----------
        rank : Ranks
            Le rang pour lequel on souhaite obtenir les statistiques moyennes.
        game_mode : str | None, optional
            Le mode de jeu sur lequel filtrer, par défaut None (tous les modes).

        Returns
        -------
        StatsCoreAggregatedDTO | None
            Un DTO contenant les moyennes des statistiques de jeu pour le rang
            spécifié, ou None si aucune donnée n'est trouvée.
        """
        rank_name = rank.name
        game_mode_filter = "AND m.playlist_id = ?" if game_mode else ""

        query = f"""
            SELECT
                ROUND(AVG(sc.shots), 2) AS avg_shots,
                ROUND(AVG(sc.goals), 2) AS avg_goals,
                ROUND(AVG(sc.saves), 2) AS avg_saves,
                ROUND(AVG(sc.assists), 2) AS avg_assists,
                ROUND(AVG(sc.demo_inflicted), 2) AS avg_demo_inflicted,
                ROUND(AVG(sc.demo_taken), 2) AS avg_demo_taken,
                ROUND(AVG(sc.score), 2) AS avg_score,
                ROUND(AVG(sc.shooting_percentage), 2) AS avg_shooting_percentage
            FROM stats_core sc
            INNER JOIN match_participation mp ON sc.participation_id = mp.id
            INNER JOIN ranks r ON mp.rank_id = r.id
            INNER JOIN match_teams mt ON mt.id = mp.match_team_id
            INNER JOIN matches m ON m.id = mt.match_id
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
            {game_mode_filter}
            """

        params = (rank_name, game_mode) if game_mode else (rank_name,)

        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            res = cursor.fetchone()
            if not res or res["avg_goals"] is None:
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
        self, player: Player, match: Match, game_mode: str | None = None
    ) -> StatsCore | None:
        """
        Récupère les statistiques de jeu (Core) d'un joueur pour un match spécifique.

        Parameters
        ----------
        player : Player
            Le joueur dont on souhaite obtenir les statistiques.
        match : Match
            Le match concerné.
        game_mode : str | None, optional
            Le mode de jeu sur lequel filtrer, par défaut None (tous les modes).

        Returns
        -------
        StatsCore | None
            Un objet métier contenant les statistiques de jeu brutes du joueur
            pour ce match, ou None si aucune donnée n'est trouvée.
        """
        game_mode_filter = "AND m.playlist_id = ?" if game_mode else ""

        query = f"""
                SELECT sc.*
                FROM stats_core sc
                JOIN match_participation mp ON mp.id = sc.participation_id
                JOIN match_teams mt ON mt.id = mp.match_team_id
                JOIN matches m ON m.id = mt.match_id
                JOIN players p ON p.id = mp.player_id
                WHERE m.id = ? AND p.id = ?
                {game_mode_filter}
                """

        params = (
            (match.id, player.id, game_mode) if game_mode else (match.id, player.id)
        )

        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
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
        self, player: Player, game_mode: str | None = None
    ) -> StatsCoreAggregatedDTO | None:
        """
        Récupère les statistiques de jeu (Core) moyennes d'un joueur sur l'ensemble
        de ses matchs.

        Parameters
        ----------
        player : Player
            Le joueur dont on souhaite obtenir les statistiques moyennes.
        game_mode : str | None, optional
            Le mode de jeu sur lequel filtrer, par défaut None (tous les modes).

        Returns
        -------
        StatsCoreAggregatedDTO | None
            Un DTO contenant les moyennes des statistiques de jeu du joueur,
            ou None si aucune donnée n'est trouvée.
        """
        game_mode_filter = "AND m.playlist_id = ?" if game_mode else ""

        query = f"""
                SELECT
                    ROUND(AVG(shots), 2) AS avg_shots,
                    ROUND(AVG(goals), 2) AS avg_goals,
                    ROUND(AVG(saves), 2) AS avg_saves,
                    ROUND(AVG(assists), 2) AS avg_assists,
                    ROUND(AVG(demo_inflicted), 2) AS avg_demo_inflicted,
                    ROUND(AVG(demo_taken), 2) AS avg_demo_taken,
                    ROUND(AVG(sc.score), 2) AS avg_score,
                    ROUND(AVG(shooting_percentage), 2) AS avg_shooting_percentage
                FROM stats_core sc
                JOIN match_participation mp ON sc.participation_id = mp.id
                JOIN players p ON p.id = mp.player_id
                JOIN match_teams mt ON mt.id = mp.match_team_id
                JOIN matches m ON m.id = mt.match_id
                WHERE p.id = ?
                {game_mode_filter}
                """

        params = (player.id, game_mode) if game_mode else (player.id,)

        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            res = cursor.fetchone()
            if not res or res["avg_goals"] is None:
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
