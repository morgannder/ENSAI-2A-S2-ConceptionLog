from ..models.platforms import Platform
from ..utils.singleton import Singleton
from .db_connection import DBConnection


class PlatformDAO(metaclass=Singleton):
    def __init__(self):
        self.db_connector = DBConnection()

    def create_platform(self, platform: Platform) -> bool:
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT 1
                    FROM platform
                    WHERE id = ?
                    """,
                (platform.id,),
            )

            res = cursor.fetchone()
            if res:
                return False

            cursor.execute(
                """
                    INSERT INTO platform (id, name)
                    VALUES (?, ?)
                    """,
                (
                    platform.id,
                    platform.name
                ),
            )

            return True

    def get_platform_by_id(self, id: int):
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT *
                    FROM platforms
                    WHERE id = ?
                    """,
                (id,),
            )
            res = cursor.fetchone()
            if not res:
                return None
            platf = Platform(id, res["namebigint"])
            return platf

    def get_platform_by_name(self, platform_name: str):
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT *
                    FROM platforms
                    WHERE namebigint = ?
                    """,
                (platform_name,),
            )
            res = cursor.fetchone()
            if not res:
                return None
            platf = Platform(res["id"], platform_name)
            return platf

    def update_platform(self):
        pass

    def delete_platform(self, platform: Platform) -> bool:
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    DELETE FROM platforms
                    WHERE name = ?
                    """,
                (platform.name,),
            )

    def get_number_player_by_platform(self, platform: Platform) -> int:
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT COUNT(DISTINTC pl.id)
                    FROM platforms p
                    JOIN players pl ON pl.platform_id = p.id
                    WHERE p.name = ?
                    """,
                (platform.name,),
            )
            res = cursor.fetchone()
            if not res:
                return 0
            return res
