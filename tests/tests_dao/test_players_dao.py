from unittest.mock import MagicMock, patch

import pytest

from src.dao.players_dao import PlayerDAO
from src.models.players import Player


# ──────────────────────────────────────────────
# Reset Singleton
# ──────────────────────────────────────────────


@pytest.fixture(autouse=True)
def reset_singleton():
    PlayerDAO._instances = {}
    yield
    PlayerDAO._instances = {}


# ──────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────


@pytest.fixture
def mock_cursor():
    return MagicMock()


@pytest.fixture
def mock_connection(mock_cursor):
    connection = MagicMock()
    connection.cursor.return_value = mock_cursor
    connection.__enter__ = MagicMock(return_value=connection)
    connection.__exit__ = MagicMock(return_value=None)
    return connection


@pytest.fixture
def player_dao(mock_connection):
    with patch("src.dao.players_dao.DBConnection") as mock_db_conn:
        mock_db_instance = MagicMock()
        mock_db_instance.connection = mock_connection
        mock_db_conn.return_value = mock_db_instance
        dao = PlayerDAO()
        yield dao


@pytest.fixture
def player_row():
    return {
        "id": "player-123",
        "platform_id": "plat-1",
        "platform_user_id": "uid_123",
        "name": "User",
    }


# ──────────────────────────────────────────────
# get_player_by_parameter
# ──────────────────────────────────────────────


class TestGetPlayerByParameter:
    def test_retourne_player_quand_trouve(self, player_dao, mock_cursor, player_row):
        mock_cursor.fetchone.return_value = player_row

        result = player_dao.get_player_by_parameter("name", "User")

        assert result is not None
        assert isinstance(result, Player)
        assert result.name == player_row["name"]
        assert result.id == player_row["id"]

    def test_retourne_none_si_non_trouve(self, player_dao, mock_cursor):
        mock_cursor.fetchone.return_value = None

        result = player_dao.get_player_by_parameter("name", "Inconnu")

        assert result is None

    def test_leve_erreur_si_colonne_invalide(self, player_dao):
        with pytest.raises(ValueError, match="Invalid column name"):
            player_dao.get_player_by_parameter("invalid_column", "value")

    def test_requete_contient_bonne_colonne(self, player_dao, mock_cursor, player_row):
        mock_cursor.fetchone.return_value = player_row

        player_dao.get_player_by_parameter("platform_user_id", "uid_123")

        call_args = mock_cursor.execute.call_args[0]
        assert "WHERE platform_user_id= ?" in call_args[0]
        assert call_args[1] == ("uid_123",)

    @pytest.mark.parametrize(
        "column", ["id", "name", "platform_id", "platform_user_id"]
    )
    def test_colonnes_autorisees_acceptees(
        self, player_dao, mock_cursor, player_row, column
    ):
        mock_cursor.fetchone.return_value = player_row

        player_dao.get_player_by_parameter(column, "test_value")

        call_args = mock_cursor.execute.call_args[0]
        assert f"WHERE {column}= ?" in call_args[0]

    def test_player_retourne_bons_attributs(self, player_dao, mock_cursor, player_row):
        mock_cursor.fetchone.return_value = player_row

        result = player_dao.get_player_by_parameter("id", "player-123")

        assert result.id == player_row["id"]
        assert result.platform_id == player_row["platform_id"]
        assert result.platform_user_id == player_row["platform_user_id"]
        assert result.name == player_row["name"]


# ──────────────────────────────────────────────
# search_players_by_name
# ──────────────────────────────────────────────


class TestSearchPlayersByName:
    def test_retourne_liste_joueurs(self, player_dao, mock_cursor):
        mock_cursor.fetchall.return_value = [
            {"platform_user_id": "uid_1", "name": "User", "platform_name": "Steam"},
            {"platform_user_id": "uid_2", "name": "UserRL", "platform_name": "Epic"},
        ]

        result = player_dao.search_players_by_name("User")

        assert len(result) == 2
        assert result[0]["name"] == "User"
        assert result[1]["name"] == "UserRL"

    def test_retourne_liste_vide_si_aucun_resultat(self, player_dao, mock_cursor):
        mock_cursor.fetchall.return_value = []

        result = player_dao.search_players_by_name("Inconnu")

        assert result == []

    def test_params_sans_filtre_plateforme(self, player_dao, mock_cursor):
        mock_cursor.fetchall.return_value = []

        player_dao.search_players_by_name("User", limit=10, offset=5)

        params = mock_cursor.execute.call_args[0][1]
        assert "%User%" in params
        assert "User" in params
        assert 10 in params
        assert 5 in params

    def test_params_avec_filtre_plateforme(self, player_dao, mock_cursor):
        mock_cursor.fetchall.return_value = []

        player_dao.search_players_by_name(
            "User", platform_filter="Steam", limit=10, offset=0
        )

        params = mock_cursor.execute.call_args[0][1]
        assert "%User%" in params
        assert "Steam" in params
        assert 10 in params

    def test_requete_contient_clause_plateforme_si_filtre(
        self, player_dao, mock_cursor
    ):
        mock_cursor.fetchall.return_value = []

        player_dao.search_players_by_name("User", platform_filter="Steam")

        query = mock_cursor.execute.call_args[0][0]
        assert "AND plat.name = ?" in query

    def test_requete_sans_clause_plateforme_si_pas_filtre(
        self, player_dao, mock_cursor
    ):
        mock_cursor.fetchall.return_value = []

        player_dao.search_players_by_name("User")

        query = mock_cursor.execute.call_args[0][0]
        assert "AND plat.name = ?" not in query

    def test_valeurs_par_defaut_limit_offset(self, player_dao, mock_cursor):
        mock_cursor.fetchall.return_value = []

        player_dao.search_players_by_name("User")

        params = mock_cursor.execute.call_args[0][1]
        assert 30 in params
        assert 0 in params


# ──────────────────────────────────────────────
# get_players_in_match
# ──────────────────────────────────────────────


class TestGetPlayersInMatch:
    def test_retourne_liste_joueurs_avec_couleur(self, player_dao, mock_cursor):
        mock_cursor.fetchone.return_value = {"id": "match-abc"}
        mock_cursor.fetchall.return_value = [
            {
                "id": "player-1",
                "platform_id": "plat-1",
                "platform_user_id": "uid_1",
                "name": "User1",
                "color": "Blue",
            },
            {
                "id": "player-2",
                "platform_id": "plat-1",
                "platform_user_id": "uid_2",
                "name": "User2",
                "color": "Orange",
            },
        ]

        result = player_dao.get_players_in_match("match-abc")

        assert result is not None
        assert len(result) == 2
        assert isinstance(result[0]["player"], Player)
        assert result[0]["color"] == "blue"
        assert result[1]["color"] == "orange"

    def test_retourne_none_si_aucun_joueur(self, player_dao, mock_cursor):
        mock_cursor.fetchone.return_value = {"id": "match-abc"}
        mock_cursor.fetchall.return_value = None

        result = player_dao.get_players_in_match("match-abc")

        assert result is None

    def test_retourne_none_si_liste_vide(self, player_dao, mock_cursor):
        mock_cursor.fetchone.return_value = {"id": "match-abc"}
        mock_cursor.fetchall.return_value = []

        result = player_dao.get_players_in_match("match-abc")

        assert result is None

    def test_couleur_mise_en_minuscule(self, player_dao, mock_cursor):
        mock_cursor.fetchone.return_value = {"id": "match-abc"}
        mock_cursor.fetchall.return_value = [
            {
                "id": "player-1",
                "platform_id": "plat-1",
                "platform_user_id": "uid_1",
                "name": "User1",
                "color": "BLUE",
            },
        ]

        result = player_dao.get_players_in_match("match-abc")

        assert result[0]["color"] == "blue"

    def test_couleur_none_retourne_chaine_vide(self, player_dao, mock_cursor):
        mock_cursor.fetchone.return_value = {"id": "match-abc"}
        mock_cursor.fetchall.return_value = [
            {
                "id": "player-1",
                "platform_id": "plat-1",
                "platform_user_id": "uid_1",
                "name": "User1",
                "color": None,
            },
        ]

        result = player_dao.get_players_in_match("match-abc")

        assert result[0]["color"] == ""


# ──────────────────────────────────────────────
# Singleton
# ──────────────────────────────────────────────


class TestPlayerDAOSingleton:
    def test_singleton_pattern(self):
        with patch("src.dao.players_dao.DBConnection"):
            instance1 = PlayerDAO()
            instance2 = PlayerDAO()
            assert instance1 is instance2
