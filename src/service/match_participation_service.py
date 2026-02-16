from src.dao.match_participation_dao import MatchParticipationDAO
from src.models.match_participation import MatchParticipation
from src.models.players import Player


class MatchParticipationService:
    """Service pour gérer les opérations métier liées aux participations de match."""

    def __init__(self):
        self.match_participation_dao = MatchParticipationDAO()

    def create_match_participation(self, participation: MatchParticipation) -> bool:
        """
        Crée une nouvelle participation de match dans la base de données.

        Parameters
        ----------
        participation : MatchParticipation
            L'objet participation à créer.

        Returns
        -------
        bool
            True si la participation a été créée, False si elle existait déjà.

        Raises
        ------
        ValueError
            Si l'ID de la participation est manquant, si le match_team_id est manquant,
            si le player_id est manquant, ou si les temps de début et de fin sont invalides
            (négatifs ou start_time > end_time).
        """
        if not participation.id:
            raise ValueError("L'ID de la participation est requis")

        if not participation.match_team_id:
            raise ValueError("Le match_team_id est requis")

        if not participation.player_id:
            raise ValueError("Le player_id est requis")

        if (
            participation.start_time < 0
            or participation.end_time < 0
            or participation.start_time > participation.end_time
        ):
            raise ValueError("Les temps de début et de fin ne conviennent pas")

        return self.match_participation_dao.create_match_participation(participation)

    def get_participation_by_id(
        self, participation_id: str
    ) -> MatchParticipation | None:
        """
        Récupère une participation par son ID.

        Parameters
        ----------
        participation_id : str
            L'identifiant unique de la participation.

        Returns
        -------
        MatchParticipation | None
            La participation trouvée, ou None si aucune participation ne correspond.
        """
        participations = self.match_participation_dao.get_matches_by_parameter(
            "id", participation_id
        )
        return participations[0] if participations else None

    def get_participations_by_team(
        self, match_team_id: str
    ) -> list[MatchParticipation] | None:
        """
        Récupère toutes les participations d'une équipe donnée.

        Parameters
        ----------
        match_team_id : str
            L'identifiant de l'équipe de match.

        Returns
        -------
        list[MatchParticipation] | None
            Liste des participations de l'équipe, ou None si aucune participation trouvée.
        """
        return self.match_participation_dao.get_matches_by_parameter(
            "match_team_id", match_team_id
        )

    def get_participations_by_player(
        self, player_id: str
    ) -> list[MatchParticipation] | None:
        """
        Récupère toutes les participations d'un joueur.

        Parameters
        ----------
        player_id : str
            L'identifiant du joueur.

        Returns
        -------
        list[MatchParticipation] | None
            Liste des participations du joueur, ou None si aucune participation trouvée.
        """
        return self.match_participation_dao.get_matches_by_parameter(
            "player_id", player_id
        )

    def get_participations_by_rank(
        self, rank_id: int
    ) -> list[MatchParticipation] | None:
        """
        Récupère toutes les participations d'un rang donné.

        Parameters
        ----------
        rank_id : int
            L'identifiant du rang.

        Returns
        -------
        list[MatchParticipation] | None
            Liste des participations de ce rang, ou None si aucune participation trouvée.
        """
        return self.match_participation_dao.get_matches_by_parameter("rank_id", rank_id)

    def get_participations_by_car(self, car_id: int) -> list[MatchParticipation] | None:
        """
        Récupère toutes les participations avec une voiture donnée.

        Parameters
        ----------
        car_id : int
            L'identifiant de la voiture.

        Returns
        -------
        list[MatchParticipation] | None
            Liste des participations avec cette voiture, ou None si aucune participation trouvée.
        """
        return self.match_participation_dao.get_matches_by_parameter("car_id", car_id)

    def get_player_recent_participations(
        self, player: Player, limit: int = 20
    ) -> list[MatchParticipation] | None:
        """
        Récupère les dernières participations d'un joueur.

        Parameters
        ----------
        player : Player
            Le joueur dont on veut récupérer les participations.
        limit : int, optional
            Nombre maximum de participations à récupérer (par défaut: 20).

        Returns
        -------
        list[MatchParticipation] | None
            Liste des participations du joueur triées par date décroissante,
            ou None si aucune participation trouvée.

        Raises
        ------
        ValueError
            Si le joueur n'a pas d'ID valide ou si limit est inférieur ou égal à 0.
        """
        if not player or not player.id:
            raise ValueError("Le joueur doit avoir un ID valide")

        if limit <= 0:
            raise ValueError("Le nombre de participations doit être supérieur à 0")

        return self.match_participation_dao.get_player_last_match_participation(
            player, limit
        )

    def get_player_mvp_participations(
        self, player: Player
    ) -> list[MatchParticipation] | None:
        """
        Récupère toutes les participations MVP d'un joueur.

        Parameters
        ----------
        player : Player
            Le joueur dont on veut récupérer les participations MVP.

        Returns
        -------
        list[MatchParticipation] | None
            Liste des participations où le joueur a été MVP,
            ou None si aucune participation MVP trouvée.

        Raises
        ------
        ValueError
            Si le joueur n'a pas d'ID valide.
        """
        if not player or not player.id:
            raise ValueError("Le joueur doit avoir un ID valide")

        return self.match_participation_dao.get_player_match_mvp(player)

    def get_player_mvp_count(self, player: Player) -> int:
        """
        Récupère le nombre de fois où un joueur a été MVP.

        Parameters
        ----------
        player : Player
            Le joueur dont on veut compter les MVPs.

        Returns
        -------
        int
            Nombre total de MVPs du joueur.

        Raises
        ------
        ValueError
            Si le joueur n'a pas d'ID valide.
        """
        if not player or not player.id:
            raise ValueError("Le joueur doit avoir un ID valide")

        return self.match_participation_dao.get_player_nb_mvp(player)

    def delete_participation(self, participation: MatchParticipation) -> None:
        """
        Supprime une participation de la base de données.

        Parameters
        ----------
        participation : MatchParticipation
            La participation à supprimer.

        Raises
        ------
        ValueError
            Si la participation n'a pas d'ID valide.
        """
        if not participation or not participation.id:
            raise ValueError("La participation doit avoir un ID valide")

        self.match_participation_dao.delete_match_participation(participation)

    def get_player_mvp_rate(self, player: Player) -> float | None:
        """
        Calcule le taux de MVP d'un joueur (pourcentage de matchs où il a été MVP).

        Parameters
        ----------
        player : Player
            Le joueur dont on veut calculer le taux de MVP.

        Returns
        -------
        float | None
            Pourcentage de MVP arrondi à 2 décimales (0-100),
            ou None si le joueur n'a aucune participation.

        Raises
        ------
        ValueError
            Si le joueur n'a pas d'ID valide.
        """
        if not player or not player.id:
            raise ValueError("Le joueur doit avoir un ID valide")

        total_participations = self.get_participations_by_player(player.id)
        if not total_participations:
            return None

        mvp_count = self.get_player_mvp_count(player)
        return round((mvp_count / len(total_participations)) * 100, 2)

    def get_participation_statistics(self, participation_id: str) -> dict | None:
        """
        Récupère des statistiques détaillées sur une participation.

        Parameters
        ----------
        participation_id : str
            L'identifiant de la participation.

        Returns
        -------
        dict | None
            Dictionnaire contenant les statistiques de la participation :
            - id : identifiant de la participation
            - match_team_id : identifiant de l'équipe
            - player_id : identifiant du joueur
            - rank_id : identifiant du rang
            - car_id : identifiant de la voiture
            - car_name : nom de la voiture
            - mvp : si le joueur a été MVP (bool)
            - play_time_seconds : temps de jeu en secondes
            - start_time : temps de début
            - end_time : temps de fin
            Retourne None si la participation n'existe pas.
        """
        participation = self.get_participation_by_id(participation_id)
        if not participation:
            return None

        play_time = None
        if participation.start_time is not None and participation.end_time is not None:
            play_time = participation.end_time - participation.start_time

        return {
            "id": participation.id,
            "match_team_id": participation.match_team_id,
            "player_id": participation.player_id,
            "rank_id": participation.rank_id,
            "car_id": participation.car_id,
            "car_name": participation.car_name,
            "mvp": participation.mvp,
            "play_time_seconds": play_time,
            "start_time": participation.start_time,
            "end_time": participation.end_time,
        }

    def get_most_used_cars(self, player: Player, limit: int = 5) -> dict | None:
        """
        Récupère les voitures les plus utilisées par un joueur.

        Parameters
        ----------
        player : Player
            Le joueur dont on veut analyser les voitures.
        limit : int, optional
            Nombre maximum de voitures à retourner (par défaut: 5).

        Returns
        -------
        dict | None
            Dictionnaire {car_name: count} trié par nombre d'utilisations décroissant,
            ou None si le joueur n'a aucune participation.

        Raises
        ------
        ValueError
            Si le joueur n'a pas d'ID valide ou si limit est inférieur ou égal à 0.

        Examples
        --------
        >>> service.get_most_used_cars(player, limit=3)
        {'Octane': 45, 'Fennec': 32, 'Dominus': 18}
        """
        if not player or not player.id:
            raise ValueError("Le joueur doit avoir un ID valide")

        if limit <= 0:
            raise ValueError("La limite doit être supérieure à 0")

        participations = self.get_participations_by_player(player.id)
        if not participations:
            return None

        car_counts = {}
        for participation in participations:
            car_name = participation.car_name
            if car_name:
                car_counts[car_name] = car_counts.get(car_name, 0) + 1

        # Trier et limiter
        sorted_cars = sorted(car_counts.items(), key=lambda x: x[1], reverse=True)[
            :limit
        ]
        return dict(sorted_cars)
