from discordLogger import DiscordLogger
import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.trackLayout import TrackLayout

class CarManager:

    def __init__(self, databaseConnection):

        self.databaseConnection = databaseConnection
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS TrackLayoutData (
                ID SMALLTEXT PRIMARY KEY,
                Name SMALLTEXT,
                Description SMALLTEXT,
                Year TINYTEXT,
                Length SMALLTEXT,
                Corners SMALLINT)
            """)