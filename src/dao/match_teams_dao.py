from .db_connection import DBConnection

from ..utils.singleton import Singleton
from ..models.players import Player
from ..models.match_teams import MatchTeam


class MatchTeamDAO(metaclass=Singleton):

    allowed_columns = {"id","match_id","score","color", "time_in_side","possession_time"}

    def __init__(self):
        self.db_connector = DBConnection

    def create_match_team(self, match: MatchTeam) -> bool:
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT 1
                    FROM match_teams
                    WHERE id = ?
                    """,
                (match.id,),
            )

            res = cursor.fetchone()
            if res:
                return False

            cursor.execute(
                """
                    INSERT INTO matches (id, match_id, color, score, possession_time, time_in_side)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                (
                    match.id,
                    match.match_id,
                    match.color,
                    match.score,
                    match.possession_time,
                    match.time_in_side
                ),
            )

            return True

    def get_match_teams_by_parameter(
        self, parameter_name: str, parameter_value
    ) -> list[MatchTeam] | None:
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
            if not res:
                return None
            list_match = []
            for match in res:
                list_match.append(MatchTeam(match["id"],
                                            match["match_id"],
                                            match["color"],
                                            match["score"],
                                            match["possession_time"],
                                            match["time_in_side"]))
            return list_match

    def update(self, match: MatchTeam):
        pass

    def delete_match_teams(self, match: MatchTeam):
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    DELETE FROM match_teams
                    WHERE id = ?
                    """,
                (match.id,),
            )

    def get_player_last_match_teams(self, player: Player, nb_match: int = 20) -> list[MatchTeam] | None:
        query = """
            SELECT mt.*
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
            if not res:
                return None
            list_match = []
            for match in res:
                list_match.append(MatchTeam(match["id"],
                                            match["playlist_id"],
                                            match["season"],
                                            match["duration"],
                                            match["overtime"],
                                            match["date_upload"]))
            return list_match
