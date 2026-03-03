from src.dao.match_teams_dao import MatchTeamDAO
from src.models.match_teams import MatchTeam


class MatchTeamService:
    """Service pour gérer les opérations métier liées aux équipes de match."""

    def __init__(self):
        self.match_team_dao = MatchTeamDAO()

    def get_match_team_by_id(self, team_id: str) -> MatchTeam | None:
        """
        Récupère une équipe de match par son ID.

        Parameters
        ----------
        team_id : str
            L'identifiant unique de l'équipe.

        Returns
        -------
        MatchTeam | None
            L'équipe trouvée, ou None si aucune équipe ne correspond.
        """
        teams = self.match_team_dao.get_match_teams_by_parameter("id", team_id)
        return teams[0] if teams else None

    def get_teams_by_match(self, match_id: str) -> list[MatchTeam] | None:
        """
        Récupère toutes les équipes d'un match donné.

        Parameters
        ----------
        match_id : str
            L'identifiant du match.

        Returns
        -------
        list[MatchTeam] | None
            Liste des équipes du match (généralement 2), ou None si aucune équipe trouvée.
        """
        return self.match_team_dao.get_match_teams_by_parameter("match_id", match_id)

    def get_teams_by_color(self, color: str) -> list[MatchTeam] | None:
        """
        Récupère toutes les équipes d'une couleur donnée.

        Parameters
        ----------
        color : str
            La couleur de l'équipe ('blue' ou 'orange').

        Returns
        -------
        list[MatchTeam] | None
            Liste des équipes de cette couleur, ou None si aucune équipe trouvée.

        Raises
        ------
        ValueError
            Si la couleur n'est pas 'blue' ou 'orange'.
        """
        if color not in ["blue", "orange"]:
            raise ValueError("La couleur doit être 'blue' ou 'orange'")

        return self.match_team_dao.get_match_teams_by_parameter("color", color)
