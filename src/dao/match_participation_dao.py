from ..models.match_participation import MatchParticipation
from ..utils.singleton import Singleton
from .db_connection import DBConnection


class MatchParticipationDAO(metaclass=Singleton):
    def __init__(self):
        self.db_connector = DBConnection()

    def get_matches_by_parameter(
        self, parameter_name: str, parameter_value
    ) -> list[MatchParticipation] | None:
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
