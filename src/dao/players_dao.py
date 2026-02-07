from ..models.players import Player
from ..models.ranks import Ranks
from ..models.matches import Match
from ..models.match_teams import MatchTeam
from ..utils.singleton import Singleton
from .db_connection import DBConnection


class PlayerDAO(metaclass=Singleton):
    allowed_columns = {"id", "name", "platform_id"}

    def __init__(self):
        self.db_connector = DBConnection()

    def create_player(self, player: Player) -> bool:
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

    def update_player(self, player: Player):
        pass

    def delete_player(self, player: Player) -> None:
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
                list_play.append(Player(player["id"],
                                        player["platform_id"],
                                        player["platform_user_id"],
                                        player["name"]))
            return list_play

    def get_players_in_team(self, match_team: MatchTeam) -> list[Player] | None:
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
            list_player.append(Player(player["id"],
                                      player["platform_id"],
                                      player["platform_user_id"],
                                      player["name"]))
        return list_player

    def get_players_in_match(self, match: Match) -> list[Player] | None:
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
            list_player.append(Player(player["id"],
                                      player["platform_id"],
                                      player["platform_user_id"],
                                      player["name"]))
        return list_player
