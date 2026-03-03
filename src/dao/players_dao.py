from src.dao.db_connection import DBConnection
from src.models.players import Player
from src.utils.singleton import Singleton


class PlayerDAO(metaclass=Singleton):
    allowed_columns = {"id", "name", "platform_id", "platform_user_id"}

    def __init__(self):
        self.db_connector = DBConnection()

    def get_player_by_parameter(
        self, parameter_name: str, parameter_value
    ) -> Player | None:
        """
        Récupère un joueur correspondant à un critère donné.

        Parameters
        ----------
        parameter_name : str
            Le nom de la colonne sur laquelle filtrer. Doit faire partie
            des colonnes autorisées (allowed_columns).
        parameter_value :
            La valeur recherchée pour le paramètre spécifié.

        Returns
        -------
        Player | None
            Le joueur correspondant, ou None s'il n'existe pas.

        Raises
        ------
        ValueError
            Si parameter_name ne fait pas partie des colonnes autorisées.
        """
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

    def search_players_by_name(
        self,
        name_query: str,
        platform_filter: str = None,
        limit: int = 30,
        offset: int = 0,
    ) -> list:
        """
        Recherche des joueurs par nom avec un filtre optionnel sur la plateforme.

        Parameters
        ----------
        name_query : str
            Le nom ou fragment de nom à rechercher.
        platform_filter : str, optional
            Le nom de la plateforme sur laquelle filtrer, par défaut None.
        limit : int, optional
            Le nombre maximum de résultats à retourner, par défaut 30.
        offset : int, optional
            Le décalage pour la pagination des résultats, par défaut 0.

        Returns
        -------
        list
            La liste des joueurs correspondants sous forme de lignes brutes,
            chacune contenant le platform_user_id, le nom et la plateforme.
        """
        platform_clause = "AND plat.name = ?" if platform_filter else ""

        query = f"""
            SELECT p.platform_user_id, p.name, plat.name AS platform_name
            FROM players p
            JOIN platforms plat ON p.platform_id = plat.id
            WHERE p.name LIKE ? {platform_clause}
            ORDER BY
                CASE WHEN p.name = ? THEN 0 ELSE 1 END,
                p.name ASC
            LIMIT ? OFFSET ?
        """

        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()

            params = [f"%{name_query}%"]
            if platform_filter:
                params.append(platform_filter)
            params.extend([name_query, limit, offset])

            cursor.execute(query, tuple(params))
            return cursor.fetchall()

    def get_players_in_match(self, match_id: int) -> list[dict] | None:
        """
        Récupère tous les joueurs ayant participé à un match, associés à leur couleur d'équipe.
        """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT *
                FROM matches m
                JOIN match_teams mt on mt.match_id = m.id
                WHERE mt.id = ?
                """,
                (match_id,),
            )

            res1 = cursor.fetchone()
            id = res1["id"]
            cursor.execute(
                """
                SELECT p.*, mt.color
                FROM players p
                JOIN match_participation mp ON mp.player_id = p.id
                JOIN match_teams mt ON mt.id = mp.match_team_id
                JOIN matches m on m.id = mt.match_id
                WHERE m.id = ?
                """,
                (id,),
            )
            res2 = cursor.fetchall()

        if not res2:
            return None

        list_player_data = []
        for row in res2:
            player_obj = Player(
                row["id"],
                row["platform_id"],
                row["platform_user_id"],
                row["name"],
            )

            list_player_data.append(
                {
                    "player": player_obj,
                    "color": row["color"].lower() if row["color"] else "",
                }
            )

        return list_player_data
