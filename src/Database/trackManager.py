  
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

        self.databaseConnection: sqlite3.Connection = databaseConnection
        
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
            query = f"INSERT INTO {TABLENAME} VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            params = track.toTuple()
            cursor.execute(query, params)
            self.databaseConnection.commit()
    
    def getTrack(self, trackID: str) -> Track:
        
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT 1 FROM {TABLENAME} WHERE {ID} = {trackID}"
            params = (trackID, )
            cursor.execute(query, params)
            return Track(cursor.fetchone())

    def getTracks(self) -> list[Track]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME}")
            return [Track(track) for track in cursor.fetchall()]

    def updateTrack(self, track: Track):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"""UPDATE {TABLENAME}
                SET ({ID}, {NAME}, {NICKNAME}, {DESCRIPTION}, {COUNTRY}, {REGION}, {CITY}, {DATEOPENED})
                = (?, ?, ?, ?, ?, ?, ?, ?)
                WHERE {ID} = ?"""
            params = track.toTuple() + (track.id, )
            cursor.execute(query, params)
            self.databaseConnection.commit()

    def deleteTrack(self, trackID: int):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"DELETE FROM {TABLENAME} WHERE {ID} = ?"
            params = (trackID, )
            cursor.execute(query, params)
            self.databaseConnection.commit()