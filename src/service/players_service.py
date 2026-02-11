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

    def get_player_by_id(self, player_id: int) -> Player | None:
        """
        Récupère un joueur par son ID.
        """
        if player_id is None or player_id < 0:
            raise ValueError("L'ID du joueur doit être un entier positif")

        return self.player_dao.get_player_by_parameter("id", player_id)

    def get_player_by_name(self, name: str) -> Player | None:
        """
        Récupère un joueur par son nom.
        """
        if not name or not name.strip():
            raise ValueError("Le nom ne peut pas être vide")

        return self.player_dao.get_player_by_parameter("name", name.strip())

    def delete_player(self, player: Player) -> bool:
        """
        Supprime un joueur.
        """
        if player is None:
            raise ValueError("Le joueur ne peut pas être None")

        self.player_dao.delete_player(player)
        return True

    def delete_player_by_name(self, name: str) -> bool:
        """
        Supprime un joueur par son nom.
        """
        player = self.get_player_by_name(name)
        if player is None:
            return False

        return self.delete_player(player)

    def player_exists(self, name: str) -> bool:
        """
        Vérifie si un joueur existe par son nom.
        """
        return self.get_player_by_name(name) is not None

    def player_exists_by_id(self, player_id: int) -> bool:
        """
        Vérifie si un joueur existe par son ID.
        """
        try:
            return self.get_player_by_id(player_id) is not None
        except ValueError:
            return False

    def get_or_create_player(
        self, platform_id: str, platform_user_id: str, name: str
    ) -> Player:
        """
        Récupère un joueur existant ou le crée s'il n'existe pas.
        """
        # Vérifier si le joueur existe déjà
        existing_player = self.get_player_by_name(name)
        if existing_player:
            return existing_player

        # Créer le joueur s'il n'existe pas
        new_player = self.create_player(platform_id, platform_user_id, name)
        if new_player is None:
            # Si la création échoue, réessayer de récupérer (race condition possible)
            existing_player = self.get_player_by_name(name)
            if existing_player:
                return existing_player
            raise RuntimeError(f"Impossible de créer ou récupérer le joueur {name}")

        return new_player

    def validate_player_name(self, name: str) -> tuple[bool, str]:
        """
        Valide un nom de joueur selon les règles métier.
        """
        if not name or not name.strip():
            return False, "Le nom ne peut pas être vide"

        name = name.strip()

        if len(name) < 3:
            return False, "Le nom doit contenir au moins 3 caractères"

        if len(name) > 50:
            return False, "Le nom ne peut pas dépasser 50 caractères"

        # Ajouter d'autres règles si nécessaire
        # Par exemple : caractères autorisés, pas de caractères spéciaux, etc.

        return True, ""

    def get_player_display_info(self, player: Player) -> str:
        """
        Retourne une représentation formatée du joueur pour l'affichage.
        """
        if player is None:
            return "Joueur inconnu"

        return f"{player.name} (ID: {player.id}, Platform: {player.platform_id})"

    def search_players_by_name_partial(self, partial_name: str) -> list[Player]:
        """
        Recherche des joueurs dont le nom contient une chaîne donnée.
        Note: Cette méthode nécessiterait une nouvelle méthode dans la DAO.
        Pour l'instant, retourne une liste vide ou lève une exception.
        """
        # TODO: Implémenter dans la DAO une méthode search_by_partial_name
        raise NotImplementedError(
            "La recherche partielle n'est pas encore implémentée dans la DAO"
        )
