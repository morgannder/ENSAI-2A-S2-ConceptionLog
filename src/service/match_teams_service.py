from src.dao.match_teams_dao import MatchTeamDAO
from src.models.match_teams import MatchTeam
from src.models.players import Player


class MatchTeamService:
    """Service pour gérer les opérations métier liées aux équipes de match."""

    def __init__(self):
        self.match_team_dao = MatchTeamDAO()

    def create_match_team(self, match_team: MatchTeam) -> bool:
        """
        Crée une nouvelle équipe de match dans la base de données.

        Parameters
        ----------
        match_team : MatchTeam
            L'objet équipe de match à créer

        Returns
        -------
        bool
            True si l'équipe a été créée, False si elle existait déjà

        Raises
        ------
        ValueError
            Si les données de l'équipe sont invalides
        """
        if not match_team.id:
            raise ValueError("L'ID de l'équipe est requis")

        if not match_team.match_id:
            raise ValueError("Le match_id est requis")

        if match_team.score is None or match_team.score < 0:
            raise ValueError("Le score doit être un entier positif ou nul")

        if match_team.color not in ["blue", "orange"]:
            raise ValueError("La couleur doit être 'blue' ou 'orange'")

        if match_team.possession_time < 0:
            raise ValueError("'possession_time' doit être positif")

        if match_team.time_in_side < 0:
            raise ValueError("'time_in_side' doit être positif")

        return self.match_team_dao.create_match_team(match_team)

    def get_match_team_by_id(self, team_id: str) -> MatchTeam | None:
        """
        Récupère une équipe de match par son ID.

        Parameters
        ----------
        team_id : str
            L'ID de l'équipe

        Returns
        -------
        MatchTeam | None
            L'équipe trouvée ou None
        """
        teams = self.match_team_dao.get_match_teams_by_parameter("id", team_id)
        return teams[0] if teams else None

    def get_teams_by_match(self, match_id: str) -> list[MatchTeam] | None:
        """
        Récupère toutes les équipes d'un match donné.

        Parameters
        ----------
        match_id : str
            L'ID du match

        Returns
        -------
        list[MatchTeam] | None
            Liste des équipes du match (généralement 2) ou None
        """
        return self.match_team_dao.get_match_teams_by_parameter("match_id", match_id)

    def get_teams_by_color(self, color: str) -> list[MatchTeam] | None:
        """
        Récupère toutes les équipes d'une couleur donnée.

        Parameters
        ----------
        color : str
            La couleur de l'équipe ('blue' ou 'orange')

        Returns
        -------
        list[MatchTeam] | None
            Liste des équipes de cette couleur ou None

        Raises
        ------
        ValueError
            Si la couleur n'est pas valide
        """
        if color not in ["blue", "orange"]:
            raise ValueError("La couleur doit être 'blue' ou 'orange'")

        return self.match_team_dao.get_match_teams_by_parameter("color", color)

    def get_teams_by_score(self, score: int) -> list[MatchTeam] | None:
        """
        Récupère toutes les équipes ayant marqué un score donné.

        Parameters
        ----------
        score : int
            Le score recherché

        Returns
        -------
        list[MatchTeam] | None
            Liste des équipes avec ce score ou None

        Raises
        ------
        ValueError
            Si le score est négatif
        """
        if score < 0:
            raise ValueError("Le score ne peut pas être négatif")

        return self.match_team_dao.get_match_teams_by_parameter("score", score)

    def get_player_teams(
        self, player: Player, limit: int = 20
    ) -> list[MatchTeam] | None:
        """
        Récupère les dernières équipes auxquelles un joueur a participé.

        Parameters
        ----------
        player : Player
            Le joueur dont on veut récupérer les équipes
        limit : int, optional
            Nombre d'équipes à récupérer (par défaut: 20)

        Returns
        -------
        list[MatchTeam] | None
            Liste des équipes du joueur ou None

        Raises
        ------
        ValueError
            Si le joueur n'a pas d'ID ou si limit est invalide
        """
        if not player or not player.id:
            raise ValueError("Le joueur doit avoir un ID valide")

        if limit <= 0:
            raise ValueError("Le nombre d'équipes doit être supérieur à 0")

        return self.match_team_dao.get_player_last_match_teams(player, limit)

    def delete_match_team(self, match_team: MatchTeam) -> None:
        """
        Supprime une équipe de match de la base de données.

        Parameters
        ----------
        match_team : MatchTeam
            L'équipe à supprimer

        Raises
        ------
        ValueError
            Si l'équipe n'a pas d'ID
        """
        if not match_team or not match_team.id:
            raise ValueError("L'équipe doit avoir un ID valide")

        self.match_team_dao.delete_match_teams(match_team)

    def get_match_winner(self, match_id: str) -> MatchTeam | None:
        """
        Récupère l'équipe gagnante d'un match.

        Parameters
        ----------
        match_id : str
            L'ID du match

        Returns
        -------
        MatchTeam | None
            L'équipe gagnante ou None si match nul ou introuvable
        """
        teams = self.get_teams_by_match(match_id)
        if not teams or len(teams) != 2:
            return None

        # Tri par score décroissant selon le score
        sorted_teams = sorted(teams, key=lambda t: t.score, reverse=True)

        # Cas d'égalité (en match custom, on peut désactiver l'overtime)
        if sorted_teams[0].score == sorted_teams[1].score:
            return None

        return sorted_teams[0]

    def get_team_statistics(self, team_id: str) -> dict | None:
        """
        Récupère des statistiques sur une équipe.

        Parameters
        ----------
        team_id : str
            L'ID de l'équipe

        Returns
        -------
        dict | None
            Dictionnaire contenant les statistiques de l'équipe ou None
        """
        team = self.get_match_team_by_id(team_id)
        if not team:
            return None

        return {
            "id": team.id,
            "match_id": team.match_id,
            "color": team.color,
            "score": team.score,
            "possession_time": team.possession_time,
            "time_in_side": team.time_in_side,
            "possession_percentage": (
                round((team.possession_time / 300) * 100, 2)
                if team.possession_time
                else None
            ),  # En supposant un match de 5min
        }
