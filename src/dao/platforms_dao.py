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
