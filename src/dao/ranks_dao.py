from ..models.players import Player
from ..models.ranks import Ranks
from ..utils.singleton import Singleton
from .db_connection import DBConnection


class RanksDAO(metaclass=Singleton):
    allowed_columns = {"id", "name", "tier", "division"}

    def __init__(self):
        self.db_connector = DBConnection()

    def create_rank(self, rank: Ranks) -> bool:
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT 1
                    FROM ranks
                    WHERE name = ?
                    """,
                (rank.name,),
            )

            res = cursor.fetchone()
            if res:
                return False

            cursor.execute(
                """
                    INSERT INTO ranks (id, tier, division, name)
                    VALUES (?, ?, ?, ?)
                    """,
                (rank.id, rank.tier, rank.division, rank.name),
            )

            return True

    def get_rank_by_parameter(
        self, parameter_name: str, parameter_value
    ) -> list[Ranks] | None:
        if parameter_name not in self.allowed_columns:
            raise ValueError("Invalid column name")

        query = f"""
            SELECT *
            FROM ranks
            WHERE {parameter_name} = ?
        """

        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (parameter_value,))
            res = cursor.fetchall()

            if not res:
                return None

            list_rank = []
            for rank in res:
                list_rank.append(Ranks(rank["id"],
                                       rank["tier"],
                                       rank["division"],
                                       rank["name"]))
            return list_rank

    def update_rank(self, rank: Ranks):
        pass

    def delete_rank(self, rank: Ranks) -> None:
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    DELETE FROM ranks
                    WHERE name = ?
                    """,
                (rank.name,),
            )

    def get_player_rank(self, player: Player) -> Ranks | None:
        id_player = player.id
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT r.id, r.tier, r.division, r.name
                    FROM ranks r
                    JOIN match_participation mp ON mp.rank_id=r.id
                    JOIN match_teams mt ON mt.id=mp.match_team_id
                    JOIN matches m ON m.id=mt.match_id
                    JOIN players p ON p.id=mp.player_id
                    WHERE p.id = ?
                    ORDER BY m.date_upload DESC
                    LIMIT 1
                """,
                (id_player,),
            )
            res = cursor.fetchone()

            if not res:
                return None

            return Ranks(res["id"], res["tier"], res["division"], res["name"])

    def get_by_tier_division(self, rank: Ranks) -> Ranks | None:
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT *
                    FROM ranks
                    WHERE tier = ? And division =?
                    """,
                (rank.tier, rank.division,),
            )
            res = cursor.fetchone()
            if not res:
                return None
            return Ranks(
                res["id"],
                res["tier"],
                res["division"],
                res["name"],
            )
