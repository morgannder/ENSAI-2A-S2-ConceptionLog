from src.dao.db_connection import DBConnection
from src.models.platforms import Platform
from src.utils.singleton import Singleton


class PlatformDAO(metaclass=Singleton):
    def __init__(self):
        self.db_connector = DBConnection()

    def get_platform_by_id(self, id: int):
        """
        Récupère une plateforme par son identifiant.

        Parameters
        ----------
        id : int
            L'identifiant unique de la plateforme.

        Returns
        -------
        Platform | None
            La plateforme correspondante, ou None si elle n'existe pas.
        """
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
        """
        Récupère une plateforme par son nom.

        Parameters
        ----------
        platform_name : str
            Le nom de la plateforme recherchée.

        Returns
        -------
        Platform | None
            La plateforme correspondante, ou None si elle n'existe pas.
        """
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
