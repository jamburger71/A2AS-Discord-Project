from discordLogger import DiscordLogger
import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.track import Track

TABLENAME = "TrackData"
ID = "ID"
NAME = "Name"
NICKNAME = "Nickname"
DESCRIPTION = "Description"
COUNTRY = "Country"
REGION = "Region"
CITY = "City"
DATEOPENED = "DateOpened"

class TrackManager:

    def __init__(self, databaseConnection):

        self.databaseConnection = databaseConnection
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLENAME} (
                {ID} SMALLTEXT PRIMARY KEY,
                {NAME} SMALLTEXT,
                {NICKNAME} SMALLTEXT,
                {DESCRIPTION} TEXT,
                {COUNTRY} SMALLTEXT,
                {REGION} SMALLTEXT,
                {CITY} SMALLTEXT,
                {DATEOPENED} TINYTEXT)
            """)
    
    def insertTrack(self, track: Track):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""INSERT INTO {TABLENAME} VALUES ({track.toTuple()})""")
    
    def getTrack(self, trackID: str):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                SELECT 1 FROM {TABLENAME}
                WHERE {ID} = {trackID}
            """)