from src.dao.players_dao import PlayerDAO
from src.models.players import Player


class PlayerService:
    """Service pour gérer la logique métier des joueurs."""

    def __init__(self):
        self.player_dao = PlayerDAO()

    def create_player(
        self, platform_id: str, platform_user_id: str, name: str
    ) -> Player | None:
        """
        Crée un nouveau joueur.

        Parameters
        ----------
        platform_id : str
            L'identifiant de la plateforme (ex: "1" pour Steam).
        platform_user_id : str
            L'identifiant unique du joueur sur la plateforme (ex: Steam ID).
        name : str
            Le nom du joueur.

        Returns
        -------
        Player | None
            Le joueur créé avec son ID généré, ou None si la création a échoué.

        Raises
        ------
        ValueError
            Si le nom est vide ou si les identifiants de plateforme sont manquants.
        """
        if not name or not name.strip():
            raise ValueError("Le nom du joueur ne peut pas être vide")

        if not platform_id or not platform_user_id:
            raise ValueError("Les identifiants de plateforme sont requis")

        # Créer l'objet Player (l'ID sera généré si nécessaire)
        player = Player(
            id=None,
            platform_id=platform_id,
            platform_user_id=platform_user_id,
            name=name.strip(),
        )

        success = self.player_dao.create_player(player)

        if success:
            # Récupérer le joueur créé pour avoir l'ID généré
            return self.get_player_by_name(name)
        return None

    def get_player_by_platform_id(self, platform_id: str) -> Player | None:
        """
        Récupère un joueur par son identifiant de plateforme.

        Parameters
        ----------
        platform_id : str
            L'identifiant unique du joueur sur la plateforme.

        Returns
        -------
        Player | None
            Le joueur correspondant à l'identifiant, ou None s'il n'existe pas.

        Raises
        ------
        ValueError
            Si platform_id est None.
        """
        if platform_id is None:
            raise ValueError("Le platform_id du joueur doit être non vide")

        return self.player_dao.get_player_by_parameter("platform_user_id", platform_id)

    def get_player_by_name(self, name: str) -> Player | None:
        """
        Récupère un joueur par son nom.

        Parameters
        ----------
        name : str
            Le nom du joueur à rechercher.

        Returns
        -------
        Player | None
            Le joueur correspondant au nom, ou None s'il n'existe pas.

        Raises
        ------
        ValueError
            Si le nom est vide ou None.
        """
        if not name or not name.strip():
            raise ValueError("Le nom ne peut pas être vide")

        return self.player_dao.get_player_by_parameter("name", name.strip())

    def delete_player(self, player: Player) -> bool:
        """
        Supprime un joueur.

        Parameters
        ----------
        player : Player
            Le joueur à supprimer.

        Returns
        -------
        bool
            True si la suppression a réussi.

        Raises
        ------
        ValueError
            Si le joueur est None.
        """
        if player is None:
            raise ValueError("Le joueur ne peut pas être None")

        self.player_dao.delete_player(player)
        return True

    def delete_player_by_name(self, name: str) -> bool:
        """
        Supprime un joueur par son nom.

        Parameters
        ----------
        name : str
            Le nom du joueur à supprimer.

        Returns
        -------
        bool
            True si le joueur a été trouvé et supprimé, False sinon.
        """
        player = self.get_player_by_name(name)
        if player is None:
            return False

        return self.delete_player(player)

    def player_exists(self, name: str) -> bool:
        """
        Vérifie si un joueur existe par son nom.

        Parameters
        ----------
        name : str
            Le nom du joueur à vérifier.

        Returns
        -------
        bool
            True si le joueur existe, False sinon.
        """
        return self.get_player_by_name(name) is not None

    def player_exists_by_platform_id(self, platform_id: str) -> bool:
        """
        Vérifie si un joueur existe par son identifiant de plateforme.

        Parameters
        ----------
        platform_id : str
            L'identifiant de plateforme à vérifier.

        Returns
        -------
        bool
            True si le joueur existe, False sinon ou si platform_id est invalide.
        """
        try:
            return self.get_player_by_platform_id(platform_id) is not None
        except ValueError:
            return False

    def get_or_create_player(
        self, platform_id: str, platform_user_id: str, name: str
    ) -> Player:
        """
        Récupère un joueur existant ou le crée s'il n'existe pas.

        Parameters
        ----------
        platform_id : str
            L'identifiant de la plateforme.
        platform_user_id : str
            L'identifiant unique du joueur sur la plateforme.
        name : str
            Le nom du joueur.

        Returns
        -------
        Player
            Le joueur existant ou nouvellement créé.

        Raises
        ------
        RuntimeError
            Si la création du joueur échoue et qu'il n'existe toujours pas.
        """
        # Vérifier si le joueur existe déjà
        existing_player = self.get_player_by_name(name)
        if existing_player:
            return existing_player

        # Créer le joueur s'il n'existe pas
        new_player = self.create_player(platform_id, platform_user_id, name)
        if new_player is None:
            existing_player = self.get_player_by_name(name)
            if existing_player:
                return existing_player
            raise RuntimeError(f"Impossible de créer ou récupérer le joueur {name}")

        return new_player

    def validate_player_name(self, name: str) -> tuple[bool, str]:
        """
        Valide un nom de joueur selon les règles métier.

        Parameters
        ----------
        name : str
            Le nom du joueur à valider.

        Returns
        -------
        tuple[bool, str]
            Un tuple contenant :
            - bool : True si le nom est valide, False sinon
            - str : Un message d'erreur si invalide, chaîne vide si valide

        Notes
        -----
        Règles de validation :
        - Le nom ne peut pas être vide
        - Le nom doit contenir au moins 3 caractères
        - Le nom ne peut pas dépasser 50 caractères
        """
        if not name or not name.strip():
            return False, "Le nom ne peut pas être vide"

        name = name.strip()

        if len(name) < 3:
            return False, "Le nom doit contenir au moins 3 caractères"

        if len(name) > 50:
            return False, "Le nom ne peut pas dépasser 50 caractères"

        return True, ""

    def get_player_display_info(self, player: Player) -> str:
        """
        Retourne une représentation formatée du joueur pour l'affichage.

        Parameters
        ----------
        player : Player
            Le joueur dont on veut obtenir les informations d'affichage.

        Returns
        -------
        str
            Une chaîne formatée contenant le nom, l'ID et la plateforme du joueur,
            ou "Joueur inconnu" si le joueur est None.
        """
        if player is None:
            return "Joueur inconnu"

        return f"{player.name} (ID: {player.id}, Platform: {player.platform_id})"

    def search_players_by_name_partial(self, partial_name: str) -> list[Player]:
        """
        Recherche des joueurs dont le nom contient une chaîne donnée.

        Parameters
        ----------
        partial_name : str
            La chaîne partielle à rechercher dans les noms de joueurs.

        Returns
        -------
        list[Player]
            La liste des joueurs correspondants.

        Raises
        ------
        NotImplementedError
            Cette méthode n'est pas encore implémentée dans la DAO.

        Notes
        -----
        Cette méthode nécessiterait une nouvelle méthode dans la DAO.
        TODO: Implémenter dans la DAO une méthode search_by_partial_name.
        """
        # TODO: Implémenter dans la DAO une méthode search_by_partial_name
        raise NotImplementedError(
            "La recherche partielle n'est pas encore implémentée dans la DAO"
        )
