from src.dao.db_connection import DBConnection
from src.models.match_participation import MatchParticipation
from src.models.players import Player
from src.utils.singleton import Singleton


class MatchParticipationDAO(metaclass=Singleton):
    allowed_columns = {
        "id",
        "match_team_id",
        "player_id",
        "rank_id",
        "car_id",
        "car_name",
        "mvp",
        "start_time",
        "end_time",
    }

    def __init__(self):
        self.db_connector = DBConnection()

    def create_match_participation(self, match: MatchParticipation):
        """
        Crée une nouvelle participation de joueur en base de données.

        Parameters
        ----------
        match : MatchParticipation
            La participation à créer.

        Returns
        -------
        bool
            True si la participation a été créée, False si elle existait déjà.
        """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT 1
                    FROM match_participation
                    WHERE id = ?
                    """,
                (match.id,),
            )

            res = cursor.fetchone()
            if res:
                return False

            cursor.execute(
                """
                    INSERT INTO match_participation (id, match_team_id, player_id, rank_id, car_id, car_name, mvp, start_time, end_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                (
                    match.id,
                    match.match_team_id,
                    match.player_id,
                    match.rank_id,
                    match.car_id,
                    match.car_name,
                    match.mvp,
                    match.start_time,
                    match.end_time,
                ),
            )

            return True

    def get_matches_by_parameter(
        self, parameter_name: str, parameter_value
    ) -> list[MatchParticipation] | None:
        """
        Récupère les participations correspondant à un critère donné.

        Parameters
        ----------
        parameter_name : str
            Le nom de la colonne sur laquelle filtrer. Doit faire partie
            des colonnes autorisées (allowed_columns).
        parameter_value :
            La valeur recherchée pour le paramètre spécifié.

        Returns
        -------
        list[MatchParticipation] | None
            La liste des participations correspondantes, ou None si aucune
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
            FROM match_participation
            WHERE {parameter_name}= ?
            """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (parameter_value,))
            res = cursor.fetchall()
            list_match = []
            if not res:
                return None
            for val in res:
                match_part = MatchParticipation(
                    val["id"],
                    val["match_team_id"],
                    val["player_id"],
                    val["rank_id"],
                    val["car_id"],
                    val["car_name"],
                    val["mvp"],
                    val["start_time"],
                    val["end_time"],
                )
                list_match.append(match_part)
            return list_match

    def update_match_participation(self):
        """
        Met à jour une participation existante en base de données.

        Notes
        -----
        Non implémenté.
        """
        pass

    def delete_match_participation(self, match: MatchParticipation):
        """
        Supprime une participation de la base de données.

        Parameters
        ----------
        match : MatchParticipation
            La participation à supprimer.
        """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    DELETE FROM match_participation
                    WHERE id = ?
                    """,
                (match.id,),
            )

    def get_player_last_match_participation(
        self, player: Player, nb_match: int = 20
    ) -> list[MatchParticipation] | None:
        """
        Récupère les dernières participations d'un joueur, triées par date
        décroissante.

        Parameters
        ----------
        player : Player
            Le joueur dont on souhaite récupérer les participations.
        nb_match : int, optional
            Le nombre maximum de participations à retourner, par défaut 20.

        Returns
        -------
        list[MatchParticipation] | None
            La liste des dernières participations du joueur, ou None si aucune
            n'est trouvée.
        """
        query = """
            SELECT mp.*
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
            list_match = []
            if not res:
                return None
            for val in res:
                match_part = MatchParticipation(
                    val["id"],
                    val["match_team_id"],
                    val["player_id"],
                    val["rank_id"],
                    val["car_id"],
                    val["car_name"],
                    val["mvp"],
                    val["start_time"],
                    val["end_time"],
                )
                list_match.append(match_part)
            return list_match

    def get_player_match_mvp(self, player: Player) -> list[MatchParticipation] | None:
        """
        Récupère toutes les participations où le joueur a été élu MVP.

        Parameters
        ----------
        player : Player
            Le joueur dont on souhaite récupérer les participations MVP.

        Returns
        -------
        list[MatchParticipation] | None
            La liste des participations où le joueur a été MVP, ou None si
            aucune n'est trouvée.
        """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT mp.*
                    FROM match_participation mp
                    WHERE mp.player_id = ? and mvp = TRUE
                    """,
                (player.id,),
            )
            res = cursor.fetchall()
            list_match = []
            if not res:
                return None
            for val in res:
                match_part = MatchParticipation(
                    val["id"],
                    val["match_team_id"],
                    val["player_id"],
                    val["rank_id"],
                    val["car_id"],
                    val["car_name"],
                    val["mvp"],
                    val["start_time"],
                    val["end_time"],
                )
                list_match.append(match_part)
            return list_match

    def get_player_nb_mvp(self, player: Player) -> int:
        """
        Retourne le nombre de fois qu'un joueur a été élu MVP.

        Parameters
        ----------
        player : Player
            Le joueur dont on souhaite compter les MVP.

        Returns
        -------
        int
            Le nombre de participations MVP du joueur, ou 0 si aucune
            n'est trouvée.
        """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT COUNT(id)
                    FROM match_participation
                    WHERE player_id = ? and mvp = TRUE
                    """,
                (player.id,),
            )
            res = cursor.fetchone()
            if not res:
                return 0
            return res
