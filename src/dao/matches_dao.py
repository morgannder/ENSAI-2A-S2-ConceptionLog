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
