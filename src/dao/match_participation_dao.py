from ..models.match_participation import MatchParticipation
from ..utils.singleton import Singleton
from .db_connection import DBConnection
from ..models.players import Player


class MatchParticipationDAO(metaclass=Singleton):

    allowed_columns = {"id", "match_team_id", "playerd_id", "rank_id",
                       "car_id", "car_name", "mvp", "start_time", "end_time"}

    def __init__(self):
        self.db_connector = DBConnection()

    def create_match_participation(self, match: MatchParticipation):
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT 1
                    FROM match_participation
                    WHERE id = ?
                    """,
                (match.id,),
            )

            res = cursor.fetchone()
            if res:
                return False

            cursor.execute(
                """
                    INSERT INTO match_participation (id, match_team_id, player_id, rank_id, car_id, car_name, mvp, strat_time, end_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                (
                    match.id,
                    match.match_team_id,
                    match.player_id,
                    match.rank_id,
                    match.car_id,
                    match.car_name,
                    match.mvp,
                    match.start_time,
                    match.end_time
                ),
            )

            return True

    def get_matches_by_parameter(
        self, parameter_name: str, parameter_value
    ) -> list[MatchParticipation] | None:
        if parameter_name not in self.allowed_columns:
            raise ValueError("Invalid column name")
        query = f"""
            SELECT *
            FROM match_participation
            WHERE {parameter_name}= ?
            """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (parameter_value,))
            res = cursor.fetchall()
            list_match = []
            if not res:
                return None
            for val in res:
                match_part = MatchParticipation(
                    val["id"],
                    val["match_tema_id"],
                    val["player_id"],
                    val["rank_id"],
                    val["car_id"],
                    val["car_name"],
                    val["mvp"],
                    val["start_time"],
                    val["end_time"],
                )
                list_match.append(match_part)
            return list_match

    def update_match_participation(self):
        pass

    def delete_match_participation(self, match: MatchParticipation):
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    DELETE FROM match_participation
                    WHERE id = ?
                    """,
                (match.id,),
            )

    def get_player_last_match_participation(self, player: Player, nb_match: int = 20) -> list[MatchParticipation] | None:
        query = """
            SELECT mp.*
            FROM matches m
            JOIN match_teams mt ON mt.match_id = m.id
            JOIN match_participation mp ON mp.match_team_id = mt.id
            JOIN players p ON p.id = mp.player_id
            WHERE p.id = ?
            ORDER BY m.date_upload DESC
            LIMIT ?
            """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (player.id, nb_match,))
            res = cursor.fetchall()
            list_match = []
            if not res:
                return None
            for val in res:
                match_part = MatchParticipation(
                    val["id"],
                    val["match_tema_id"],
                    val["player_id"],
                    val["rank_id"],
                    val["car_id"],
                    val["car_name"],
                    val["mvp"],
                    val["start_time"],
                    val["end_time"],
                )
                list_match.append(match_part)
            return list_match

    def get_player_match_mvp(self, player: Player) -> list[MatchParticipation] | None:
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT mp.*
                    FROM match_participation mp
                    WHERE mp.player_id = ? and mvp = TRUE
                    """,
                (player.id,),
            )
            res = cursor.fetchall()
            list_match = []
            if not res:
                return None
            for val in res:
                match_part = MatchParticipation(
                    val["id"],
                    val["match_tema_id"],
                    val["player_id"],
                    val["rank_id"],
                    val["car_id"],
                    val["car_name"],
                    val["mvp"],
                    val["start_time"],
                    val["end_time"],
                )
                list_match.append(match_part)
            return list_match

    def get_player_nb_mvp(self, player: Player) -> int:
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT COUNT(id)
                    FROM match_participation
                    WHERE player_id = ? and mvp = TRUE
                    """,
                (player.id,),
            )
            res = cursor.fetchone
            if not res:
                return 0
            return res
