from src.dao.db_connection import DBConnection
from src.models.matches import Match
from src.models.players import Player
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

    def create_match(self, match: Match) -> bool:
        """
        Crée un nouveau match en base de données.

        Parameters
        ----------
        match : Match
            Le match à créer.

        Returns
        -------
        bool
            True si le match a été créé, False s'il existait déjà.
        """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT 1
                    FROM matches
                    WHERE id = ?
                    """,
                (match.id,),
            )

            res = cursor.fetchone()
            if res:
                return False

            cursor.execute(
                """
                    INSERT INTO matches (id, playlist_id, season, duration, overtime, date_upload)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                (
                    match.id,
                    match.playlist_id,
                    match.season,
                    match.duration,
                    match.overtime,
                    match.date_upload,
                ),
            )

            return True

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

    def update_match(self, match: Match):
        """
        Met à jour un match existant en base de données.

        Parameters
        ----------
        match : Match
            Le match à mettre à jour.

        Notes
        -----
        Non implémenté.
        """
        pass

    def delete_match(self, match: Match):
        """
        Supprime un match de la base de données.

        Parameters
        ----------
        match : Match
            Le match à supprimer.
        """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    DELETE FROM matches
                    WHERE id = ?
                    """,
                (match.id,),
            )

    def get_20_recent_matches(self, nb_match=20) -> list[Match] | None:
        """
        Récupère les matchs les plus récents, triés par date décroissante.

        Parameters
        ----------
        nb_match : int, optional
            Le nombre maximum de matchs à retourner, par défaut 20.

        Returns
        -------
        list[Match] | None
            La liste des matchs les plus récents, ou None si aucun
            n'est trouvé.
        """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT *
                    FROM matches
                    ORDER BY date_upload DESC
                    LIMIT ?
                    """,
                (nb_match,),
            )
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

    def get_player_last_matches(
        self, player: Player, nb_match: int = 20
    ) -> list[Match] | None:
        """
        Récupère les derniers matchs d'un joueur, triés par date décroissante.

        Parameters
        ----------
        player : Player
            Le joueur dont on souhaite récupérer les matchs.
        nb_match : int, optional
            Le nombre maximum de matchs à retourner, par défaut 20.

        Returns
        -------
        list[Match] | None
            La liste des derniers matchs du joueur, ou None si aucun
            n'est trouvé.
        """
        query = """
            SELECT m.*
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
