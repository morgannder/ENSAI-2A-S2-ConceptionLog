from src.dao.db_connection import DBConnection
from src.models.platforms import Platform
from src.utils.singleton import Singleton


class PlatformDAO(metaclass=Singleton):
    def __init__(self):
        self.db_connector = DBConnection()

    def create_platform(self, platform: Platform) -> bool:
        """
        Crée une nouvelle plateforme en base de données.

        Parameters
        ----------
        platform : Platform
            La plateforme à créer.

        Returns
        -------
        bool
            True si la plateforme a été créée, False si elle existait déjà.
        """
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
                (platform.id, platform.name),
            )

            return True

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

    def update_platform(self):
        pass

    def delete_platform(self, platform: Platform) -> bool:
        """
        Supprime une plateforme de la base de données.

        Parameters
        ----------
        platform : Platform
            La plateforme à supprimer.
        """
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
        """
        Retourne le nombre de joueurs inscrits sur une plateforme donnée.

        Parameters
        ----------
        platform : Platform
            La plateforme dont on souhaite compter les joueurs.

        Returns
        -------
        int
            Le nombre de joueurs sur la plateforme, ou 0 si aucun n'est trouvé.
        """
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
