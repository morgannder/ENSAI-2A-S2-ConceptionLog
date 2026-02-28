from src.dao.db_connection import DBConnection
from src.models.match_teams import MatchTeam
from src.models.players import Player
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

    def create_match_team(self, match: MatchTeam) -> bool:
        """
        Crée une nouvelle équipe de match en base de données.

        Parameters
        ----------
        match : MatchTeam
            L'équipe à créer.

        Returns
        -------
        bool
            True si l'équipe a été créée, False si elle existait déjà.
        """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT 1
                    FROM match_teams
                    WHERE id = ?
                    """,
                (match.id,),
            )

            res = cursor.fetchone()
            if res:
                return False

            cursor.execute(
                """
                    INSERT INTO match_teams (id, match_id, color, score, possession_time, time_in_side)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                (
                    match.id,
                    match.match_id,
                    match.color,
                    match.score,
                    match.possession_time,
                    match.time_in_side,
                ),
            )

            return True

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

    def update(self, match: MatchTeam):
        """
        Met à jour une équipe existante en base de données.

        Parameters
        ----------
        match : MatchTeam
            L'équipe à mettre à jour.

        Notes
        -----
        Non implémenté.
        """
        pass

    def delete_match_teams(self, match: MatchTeam):
        """
        Supprime une équipe de la base de données.

        Parameters
        ----------
        match : MatchTeam
            L'équipe à supprimer.
        """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    DELETE FROM match_teams
                    WHERE id = ?
                    """,
                (match.id,),
            )

    def get_player_last_match_teams(
        self, player: Player, nb_match: int = 20
    ) -> list[MatchTeam] | None:
        """
        Récupère les équipes des derniers matchs d'un joueur, triées par date
        décroissante.

        Parameters
        ----------
        player : Player
            Le joueur dont on souhaite récupérer les équipes.
        nb_match : int, optional
            Le nombre maximum d'équipes à retourner, par défaut 20.

        Returns
        -------
        list[MatchTeam] | None
            La liste des équipes des derniers matchs du joueur, ou None si
            aucune n'est trouvée.
        """
        query = """
            SELECT mt.*
            FROM matches m
            JOIN match_teams mt ON mt.match_id = m.id
            JOIN match_participation mp ON mp.match_team_id = mt.id
            JOIN players p ON p.id = mp.player_id
            WHERE p.id = ?
            ORDER BY m.date_upload DESC
            LIMIT ?
            """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                query,
                (
                    player.id,
                    nb_match,
                ),
            )
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
