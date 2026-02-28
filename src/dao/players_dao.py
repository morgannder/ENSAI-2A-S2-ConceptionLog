from src.dao.db_connection import DBConnection
from src.models.match_teams import MatchTeam
from src.models.matches import Match
from src.models.players import Player
from src.models.ranks import Ranks
from src.utils.singleton import Singleton


class PlayerDAO(metaclass=Singleton):
    allowed_columns = {"id", "name", "platform_id", "platform_user_id"}

    def __init__(self):
        self.db_connector = DBConnection()

    def create_player(self, player: Player) -> bool:
        """
        Crée un nouveau joueur en base de données.

        Parameters
        ----------
        player : Player
            Le joueur à créer.

        Returns
        -------
        bool
            True si le joueur a été créé, False s'il existait déjà.
        """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT 1
                    FROM players
                    WHERE name = ?
                    """,
                (player.name,),
            )

            res = cursor.fetchone()
            if res:
                return False

            cursor.execute(
                """
                    INSERT INTO players (id, platform_id, platform_user_id, name)
                    VALUES (?, ?, ?, ?)
                    """,
                (
                    player.id,
                    player.platform_id,
                    player.platform_user_id,
                    player.name,
                ),
            )

            return True

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

    def update_player(self, player: Player):
        """
        Met à jour un joueur existant en base de données.

        Parameters
        ----------
        player : Player
            Le joueur à mettre à jour.

        Notes
        -----
        Non implémenté.
        """
        pass

    def delete_player(self, player: Player) -> None:
        """
        Supprime un joueur de la base de données.

        Parameters
        ----------
        player : Player
            Le joueur à supprimer.
        """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    DELETE FROM players
                    WHERE name = ?
                    """,
                (player.name,),
            )

    def get_matches_count(self, player: Player) -> int:
        """
        Retourne le nombre de matchs joués par un joueur.

        Parameters
        ----------
        player : Player
            Le joueur dont on souhaite compter les matchs.

        Returns
        -------
        int
            Le nombre de matchs joués, ou 0 si aucun n'est trouvé.
        """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT COUNT(DISTINCT mp.id)
                    FROM players p
                    JOIN match_participation mp ON mp.player_id = p.id
                    WHERE p.id = ?
                    """,
                (player.id,),
            )
            res = cursor.fetchone()
            if not res:
                return 0
            return res

    def get_players_in_rank(self, rank: Ranks) -> list[Player] | None:
        """
        Récupère tous les joueurs ayant joué dans un rang donné.

        Parameters
        ----------
        rank : Ranks
            Le rang pour lequel on souhaite récupérer les joueurs.

        Returns
        -------
        list[Player] | None
            La liste des joueurs correspondants, ou None si aucun n'est trouvé.
        """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT *
                    FROM players p
                    JOIN match_participation mp ON mp.player_id = p.id
                    JOIN ranks r ON r.id = mp.rank_id
                    WHERE r.id = ?
                    """,
                (rank.id,),
            )
            res = cursor.fetchall()
            if not res:
                return None
            list_play = []
            for player in res:
                list_play.append(
                    Player(
                        player["id"],
                        player["platform_id"],
                        player["platform_user_id"],
                        player["name"],
                    )
                )
            return list_play

    def get_players_in_team(self, match_team: MatchTeam) -> list[Player] | None:
        """
        Récupère tous les joueurs d'une équipe dans un match.

        Parameters
        ----------
        match_team : MatchTeam
            L'équipe dont on souhaite récupérer les joueurs.

        Returns
        -------
        list[Player] | None
            La liste des joueurs de l'équipe, ou None si aucun n'est trouvé.
        """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT *
                    FROM players p
                    JOIN match_participation mp ON mp.player_id = p.id
                    JOIN match_teams mt ON mt.id = mp.match_team_id
                    WHERE mt.id = ?
                    """,
                (match_team.id,),
            )
        res = cursor.fetchall()
        if not res:
            return None
        list_player = []
        for player in res:
            list_player.append(
                Player(
                    player["id"],
                    player["platform_id"],
                    player["platform_user_id"],
                    player["name"],
                )
            )
        return list_player

    def get_players_in_match(self, match: Match) -> list[Player] | None:
        """
        Récupère tous les joueurs ayant participé à un match.

        Parameters
        ----------
        match : Match
            Le match dont on souhaite récupérer les joueurs.

        Returns
        -------
        list[Player] | None
            La liste des joueurs du match, ou None si aucun n'est trouvé.
        """
        connection = self.db_connector.connection
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT *
                    FROM players p
                    JOIN match_participation mp ON mp.player_id = p.id
                    JOIN match_teams mt ON mt.id = mp.match_team_id
                    JOIN matches m ON m.id = mt.match_id
                    WHERE m.id = ?
                    """,
                (match.id,),
            )
        res = cursor.fetchall()
        if not res:
            return None
        list_player = []
        for player in res:
            list_player.append(
                Player(
                    player["id"],
                    player["platform_id"],
                    player["platform_user_id"],
                    player["name"],
                )
            )
        return list_player
