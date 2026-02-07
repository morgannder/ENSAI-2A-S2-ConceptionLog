from .db_connection import DBConnection
from ..models.matches import Match
from ..utils.singleton import Singleton


class MatchDAO(metaclass=Singleton):
    allowed_columns = {"id", "playlist_id", "season", "date_upload"}

    def __init__(self):
        self.db_connector = DBConnection

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
                                        match["date_upload"],))
            return list_match
