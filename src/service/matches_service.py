from src.dao.matches_dao import MatchDAO
from src.models.matches import Match
from src.models.players import Player


class MatchService:
    """Service pour gérer les opérations métier liées aux matchs."""

    def __init__(self):
        self.match_dao = MatchDAO()

    def create_match(self, match: Match) -> bool:
        """
        Crée un nouveau match dans la base de données.

        Parameters
        ----------
        match : Match
            L'objet match à créer

        Returns
        -------
        bool
            True si le match a été créé, False s'il existait déjà

        Raises
        ------
        ValueError
            Si les données du match sont invalides
        """
        if not match.id:
            raise ValueError("L'ID du match est requis")

        if not match.playlist_id:
            raise ValueError("Le playlist_id est requis")

        return self.match_dao.create_match(match)

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

    def get_recent_matches(self, limit: int = 20) -> list[Match] | None:
        """
        Récupère les matchs les plus récents.

        Parameters
        ----------
        limit : int, optional
            Nombre de matchs à récupérer (par défaut: 20)

        Returns
        -------
        Optional[list[Match]]
            Liste des matchs récents ou None

        Raises
        ------
        ValueError
            Si limit est inférieur ou égal à 0
        """
        if limit <= 0:
            raise ValueError("Le nombre de matchs doit être strictement supérieur à 0")

        return self.match_dao.get_20_recent_matches(limit)

    def get_player_matches(self, player: Player, limit: int = 20) -> list[Match] | None:
        """
        Récupère les derniers matchs d'un joueur.

        Parameters
        ----------
        player : Player
            Le joueur dont on veut récupérer les matchs
        limit : int, optional
            Nombre de matchs à récupérer (par défaut: 20)

        Returns
        -------
        Optional[list[Match]]
            Liste des matchs du joueur ou None

        Raises
        ------
        ValueError
            Si le joueur n'a pas d'ID ou si limit est invalide
        """
        if not player or not player.id:
            raise ValueError("Le joueur doit avoir un ID valide")

        if limit <= 0:
            raise ValueError("Le nombre de matchs doit être supérieur à 0")

        return self.match_dao.get_player_last_matches(player, limit)

    def delete_match(self, match: Match) -> None:
        """
        Supprime un match de la base de données.

        Parameters
        ----------
        match : Match
            Le match à supprimer

        Raises
        ------
        ValueError
            Si le match n'a pas d'ID
        """
        if not match or not match.id:
            raise ValueError("Le match doit avoir un ID valide")

        self.match_dao.delete_match(match)

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
