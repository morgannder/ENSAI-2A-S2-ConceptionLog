from src.dao.db_connection import DBConnection
from src.models.match_teams import MatchTeam
from src.utils.singleton import Singleton


class MatchTeamDAO(metaclass=Singleton):
    allowed_columns = {
        "id",
        "match_id",
        "score",
        "color",
        "time_in_side",
        "possession_time",
    }

    def __init__(self):
        self.db_connector = DBConnection

    def get_match_teams_by_parameter(
        self, parameter_name: str, parameter_value
    ) -> list[MatchTeam] | None:
        """
        Récupère les équipes correspondant à un critère donné.

        Parameters
        ----------
        parameter_name : str
            Le nom de la colonne sur laquelle filtrer. Doit faire partie
            des colonnes autorisées (allowed_columns).
        parameter_value :
            La valeur recherchée pour le paramètre spécifié.

        Returns
        -------
        list[MatchTeam] | None
            La liste des équipes correspondantes, ou None si aucune
            n'est trouvée.

        Raises
        ------
        ValueError
            Si parameter_name ne fait pas partie des colonnes autorisées.
        """
        if parameter_name not in self.allowed_columns:
            raise ValueError("Invalid column name")

        query = f"""
            SELECT *
            FROM match_teams
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
                    MatchTeam(
                        match["id"],
                        match["match_id"],
                        match["color"],
                        match["score"],
                        match["possession_time"],
                        match["time_in_side"],
                    )
                )
            return list_match
