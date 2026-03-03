from src.dao.matches_dao import MatchDAO
from src.dao.players_dao import PlayerDAO
from src.dto.match_players_dto import MatchPlayersDTO, PlayerInfoDTO
from src.models.matches import Match


class MatchService:
    """Service pour gérer les opérations métier liées aux matchs."""

    def __init__(self):
        self.match_dao = MatchDAO()
        self.players_dao = PlayerDAO()

    def get_match_by_id(self, match_id: str) -> Match | None:
        """
        Récupère un match par son ID.

        Parameters
        ----------
        match_id : str
            L'ID du match

        Returns
        -------
        Optional[Match]
            Le match trouvé ou None
        """
        matches = self.match_dao.get_match_by_parameter("id", match_id)
        return matches[0] if matches else None

    def get_matches_by_season(self, season: int) -> list[Match] | None:
        """
        Récupère tous les matchs d'une saison donnée.

        Parameters
        ----------
        season : int
            Le numéro de saison

        Returns
        -------
        Optional[list[Match]]
            Liste des matchs de la saison ou None
        """
        return self.match_dao.get_match_by_parameter("season", season)

    def get_matches_by_playlist(self, playlist_id: int) -> list[Match] | None:
        """
        Récupère tous les matchs d'une playlist donnée.

        Parameters
        ----------
        playlist_id : int
            L'ID de la playlist

        Returns
        -------
        Optional[list[Match]]
            Liste des matchs de la playlist ou None
        """
        return self.match_dao.get_match_by_parameter("playlist_id", playlist_id)

    def get_overtime_matches(self, overtime: bool = True) -> list[Match] | None:
        """
        Récupère tous les matchs allés en overtime ou pas.

        parameters
        ----------
        overtime : bool
            indique si le match est allé en overtime (overtime = 1) ou pas

        Returns
        -------
        Optional[list[Match]]
            Liste des matchs en overtime ou None
        """
        overtime = 1 if overtime is True else 0
        return self.match_dao.get_match_by_parameter("overtime", overtime)

    def get_match_statistics(self, match_id: str) -> dict | None:
        """
        Récupère des statistiques sur un match.

        Parameters
        ----------
        match_id : str
            L'ID du match

        Returns
        -------
        Optional[dict]
            Dictionnaire contenant les statistiques du match ou None
        """
        match = self.get_match_by_id(match_id)
        if not match:
            return None

        return {
            "id": match.id,
            "playlist_id": match.playlist_id,
            "season": match.season,
            "duration": match.duration,
            "overtime": match.overtime,
            "date_upload": match.date_upload,
        }

    def get_match_players(self, match_id: str) -> MatchPlayersDTO | None:
        players_data = self.players_dao.get_players_in_match(match_id)

        if not players_data:
            return None

        dto_data = {}
        orange_count = 1
        blue_count = 1

        for data in players_data:
            color = data["color"]
            player = data["player"]

            player_info = PlayerInfoDTO(
                id=player.id,
                name=player.name,
                platform_id=player.platform_id,
                platform_user_id=player.platform_user_id,
            )

            if color == "orange" and orange_count <= 4:
                dto_data[f"orange{orange_count}"] = player_info
                orange_count += 1
            elif color == "blue" and blue_count <= 4:
                dto_data[f"blue{blue_count}"] = player_info
                blue_count += 1

        return MatchPlayersDTO(**dto_data)
