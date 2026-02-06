from db_connection import DBConnection

from models.platforms import Platform
from utils.singleton import Singleton


class PlatformDAO(metaclass=Singleton):
    def __init__(self):
        self.db_connector = DBConnection

    def create_platform(self, platform: Platform):
        pass

    def get_platform_by_id(self, id: int):
        with self.db_connector.connection as connection, connection.cursor() as cursor:
            cursor.excecute(
                """
                    SELECT *
                    FROM platforms
                    WHERE id = %(id)s
                    """,
                {"id": id},
            )
            res = cursor.fetchone()
            if not res:
                return None
            platf = Platform(id, res["namebigint"])
            return platf

    def get_platform_by_name(self, platform_name: str):
        with self.db_connector.connection as connection, connection.cursor() as cursor:
            cursor.excecute(
                """
                    SELECT *
                    FROM platforms
                    WHERE namebigint= %(platf)s
                    """,
                {"platf": platform_name},
            )
            res = cursor.fetchone()
            if not res:
                return None
            platf = Platform(res["id"], platform_name)
            return platf

    def update_platform(self):
        pass

    def delete_platform(self, platform: Platform) -> bool:
        with self.db_connector.connection as connection, connection.cursor() as cursor:
            cursor.excecute(
                """
                    DELETE FROM platforms
                    WHERE namebigint= %(platf)s
                    """,
                {"platf": platform.namebigint},
            )
