from db_connection import DBConnection

from utils.singleton import Singleton


class PlatformDAO(metaclass=Singleton):
    def __init__(self):
        self.db_connector = DBConnection
