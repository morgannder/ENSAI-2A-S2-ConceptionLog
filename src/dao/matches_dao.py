from .db_connection import DBConnection
from ..models.matches import Match
from ..utils.singleton import Singleton
from ..models.players import Player


class MatchDAO(metaclass=Singleton):
    allowed_columns = {"id", "playlist_id", "season", "date_upload", "overtime", "duration"}

    def __init__(self):
        self.db_connector = DBConnection

    def create_match(self, match: Match) -> bool:
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT 1
                    FROM matches
                    WHERE id = ?
                    """,
                (match.id,),
            )

            res = cursor.fetchone()
            if res:
                return False

            cursor.execute(
                """
                    INSERT INTO matches (id, playlist_id, season, duration, overtime, date_upload)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                (
                    match.id,
                    match.playlist_id,
                    match.season,
                    match.duration,
                    match.overtime,
                    match.date_upload
                ),
            )

            return True

    def get_match_by_parameter(
        self, parameter_name: str, parameter_value
    ) -> list[Match] | None:
        if parameter_name not in self.allowed_columns:
            raise ValueError("Invalid column name")

        query = f"""
            SELECT *
            FROM matches
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
                list_match.append(Match(match["id"],
                                        match["playlist_id"],
                                        match["season"],
                                        match["duration"],
                                        match["overtime"],
                                        match["date_upload"]))
            return list_match

    def update_match(self, match: Match):
        pass

    def delete_match(self, match: Match):
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    DELETE FROM matches
                    WHERE id = ?
                    """,
                (match.id,),
            )

    def get_20_recent_matches(self, nb_match=20) -> list[Match] | None:
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT *
                    FROM matches
                    ORDER BY date_upload DESC
                    LIMIT ?
                    """,
                    (nb_match,),
            )
        res = cursor.fetchall()
        if not res:
            return None
        list_match = []
        for match in res:
            list_match.append(Match(match["id"],
                                    match["playlist_id"],
                                    match["season"],
                                    match["duration"],
                                    match["overtime"],
                                    match["date_upload"]))
        return list_match

    def get_player_last_matches(self, player: Player, nb_match: int = 20) -> list[Match] | None:
        query = """
            SELECT m.*
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
                list_match.append(Match(match["id"],
                                        match["playlist_id"],
                                        match["season"],
                                        match["duration"],
                                        match["overtime"],
                                        match["date_upload"]))
            return list_match
