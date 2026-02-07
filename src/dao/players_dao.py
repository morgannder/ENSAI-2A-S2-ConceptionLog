from ..models.players import Player
from ..utils.singleton import Singleton
from .db_connection import DBConnection


class PlayerDAO(metaclass=Singleton):
    allowed_columns = {"id", "name"}

    def __init__(self):
        self.db_connector = DBConnection()

    def create_player(self, player: Player) -> bool:
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT 1
                    FROM players
                    WHERE name = ?
                    """,
                (player.name,),
            )

            res = cursor.fetchone()
            if res:
                return False

            cursor.execute(
                """
                    INSERT INTO players (id, platform_id, platform_user_id, name)
                    VALUES (?, ?, ?, ?)
                    """,
                (
                    player.id,
                    player.platform_id,
                    player.platform_user_id,
                    player.name,
                ),
            )

            return True

    def get_player_by_parameter(
        self, parameter_name: str, parameter_value
    ) -> Player | None:
        if parameter_name not in self.allowed_columns:
            raise ValueError("Invalid column name")

        query = f"""
            SELECT *
            FROM players
            WHERE {parameter_name}= ?
            """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (parameter_value,))
            res = cursor.fetchone()
            if not res:
                return None
            player = Player(
                res["id"],
                res["platform_id"],
                res["platform_user_id"],
                res["name"],
            )
            return player

    def update_player(self, player: Player):
        pass

    def delete_player(self, player: Player) -> None:
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    DELETE FROM players
                    WHERE name = ?
                    """,
                (player.name,),
            )
