import os
import sqlite3

from src.utils.singleton import Singleton


class DBConnection(metaclass=Singleton):
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(__file__), "..", "database", "rocket_league.db"
            )

        self.__connection = sqlite3.connect(
            db_path,
            check_same_thread=False,  # ✅ Permet multi-threading
            timeout=10.0,  # ✅ Timeout de 10 secondes
        )
        self.__connection.row_factory = sqlite3.Row

    @property
    def connection(self):
        return self.__connection
