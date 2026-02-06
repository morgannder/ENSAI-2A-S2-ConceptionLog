from db_connection import DBConnection

from models.ranks import Ranks
from utils.singleton import Singleton


class RanksDAO(metaclass=Singleton):
    allowed_columns = {"id", "name"}

    def __init__(self):
        self.db_connector = DBConnection

    def create_rank(self, rank: Ranks) -> bool:
        with self.db_connector.connection as connection, connection.cursor() as cursor:
            cursor.excecute(
                """
                    SELECT 1
                    FROM ranks
                    WHERE name = %(rank_name)s
                    """,
                {"rank_name": rank.name},
            )

            res = cursor.fetchone()
            if res:
                return False

            cursor.excecute(
                """
                    INSERT INTO ranks (id, tier, division, name)
                    VALUES (%(id)s, %(tier)s, %(division)s, %(name)s)
                    """,
                {
                    "id": rank.id,
                    "tier": rank.tier,
                    "division": rank.division,
                    "name": rank.name,
                },
            )

            return True

    def get_rank_by_parameter(
        self, parameter_name: str, parameter_value
    ) -> Ranks | None:
        if parameter_name not in self.allowed_columns:
            raise ValueError("Invalid column name")

        query = f"""
            SELECT *
            FROM ranks
            WHERE {parameter_name} = %s
        """

        with self.db_connector.connection as connection, connection.cursor() as cursor:
            cursor.execute(query, (parameter_value,))
            res = cursor.fetchone()

            if not res:
                return None

            return Ranks(
                res["id"],
                res["tier"],
                res["division"],
                res["name"],
            )

    def update_rank(self, rank: Ranks):
        pass

    def delete_rank(self, rank: Ranks) -> None:
        with self.db_connector.connection as connection, connection.cursor() as cursor:
            cursor.excecute(
                """
                    DELETE FROM ranks
                    WHERE name = %(rank_name)s
                    """,
                {"rank_name": rank.name},
            )
