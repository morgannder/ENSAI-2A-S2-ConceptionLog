from src.dao.db_connection import DBConnection
from src.models.matches import Match
from src.utils.singleton import Singleton


class MatchDAO(metaclass=Singleton):
    allowed_columns = {
        "id",
        "playlist_id",
        "season",
        "date_upload",
        "overtime",
        "duration",
    }

    def __init__(self):
        self.db_connector = DBConnection()

    def get_match_by_parameter(
        self, parameter_name: str, parameter_value
    ) -> list[Match] | None:
        """
        Récupère les matchs correspondant à un critère donné.

        Parameters
        ----------
        parameter_name : str
            Le nom de la colonne sur laquelle filtrer. Doit faire partie
            des colonnes autorisées (allowed_columns).
        parameter_value :
            La valeur recherchée pour le paramètre spécifié.

        Returns
        -------
        list[Match] | None
            La liste des matchs correspondants, ou None si aucun n'est trouvé.

        Raises
        ------
        ValueError
            Si parameter_name ne fait pas partie des colonnes autorisées.
        """
        if parameter_name not in self.allowed_columns:
            raise ValueError("Invalid column name")

        query = f"""
            SELECT *
            FROM matches
            WHERE {parameter_name}= ?
            """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (parameter_value,))
            res = cursor.fetchall()
            if not res:
                return None
            list_match = []
            for match in res:
                list_match.append(
                    Match(
                        match["id"],
                        match["playlist_id"],
                        match["season"],
                        match["duration"],
                        match["overtime"],
                        match["date_upload"],
                    )
                )
            return list_match

    def get_match_by_match_team_id(self, match_team_id: int) -> Match | None:
        """
        Récupère le match pour un match_team_id donnée

        Parameters
        ----------
        match_team_id: int
            L'id du match_team

        Returns
        -------
        Match | None
            Le match correspondant, ou None si aucun n'est trouvé.

        Raises
        ------
        ValueError
            Si match_team_id n'est pas un entier'.
        """
        if not isinstance(match_team_id, int):
            raise TypeError("Match_team_id has to be an integer")
        query = """
            SELECT m.*
            FROM matches m
            JOIN match_teams mt ON mt.match_id = m.id
            WHERE mt.id = ?
            """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (match_team_id,))
            res = cursor.fetchone()
            if not res:
                return None
            return Match(
                res["id"],
                res["playlist_id"],
                res["season"],
                res["duration"],
                res["overtime"],
                res["date_upload"],
            )
