import os
import sqlite3

from ..utils.singleton import Singleton


class DBConnection(metaclass=Singleton):
    def __init__(self, db_path=None):
        # Par défaut : fichier mydatabase.db dans src/database/
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(__file__), "..", "database", "rocket_league.db"
            )
        self.__connection = sqlite3.connect(db_path)
        self.__connection.row_factory = sqlite3.Row  # pour accéder aux colonnes par nom

    @property
    def connection(self):
        return self.__connection
