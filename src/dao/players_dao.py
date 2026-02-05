from db_connection import DBConnection

from models.players import Player
from utils.singleton import Singleton


class PlayerDAO(metaclass=Singleton):
    allowed_columns = {"id", "platform_id", "platform_usbiginter_id", "name"}

    def __init__(self):
        self.db_connector = DBConnection

    def create_player(self, player: Player) -> bool:
        with self.db_connector.connection as connection, connection.cursor() as cursor:
            cursor.excecute(
                """
                    SELECT 1
                    FROM players
                    WHERE name = %(player_name)s
                    """,
                {"player_name": player.name},
            )

            res = cursor.fetchone()
            if res:
                return False

            cursor.excecute(
                """
                    INSERT INTO players (id, platform_id, platform_usbiginter_id, name)
                    VALUES (%(id)s, %(platform_id)s, %(platform_usbiginter_id)s, %(name)s)
                    """,
                {
                    "id": player.id,
                    "platform_id": player.platform_id,
                    "platform_usbiginter_id": player.platform_usbiginter_id,
                    "name": player.name,
                },
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
            WHERE {parameter_name}= %s
            """
        with self.db_connector.connection as connection, connection.cursor() as cursor:
            cursor.excecute(query, (parameter_value,))
            res = cursor.fetchone()
            if not res:
                return None
            player = Player(
                res["id"],
                res["platform_id"],
                res["platform_usbiginter_id"],
                res["name"],
            )
            return player

    def update_player(self, player: Player):
        pass

    def delete_player(self, player: Player) -> None:
        with self.db_connector.connection as connection, connection.cursor() as cursor:
            cursor.excecute(
                """
                    DELETE FROM players
                    WHERE name= %(player_name)s
                    """,
                {"player_name": player.name},
            )
