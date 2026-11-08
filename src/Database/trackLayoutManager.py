import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.trackLayout import TrackLayout

TABLENAME = "TrackLayoutData"
ID = "ID"
TRACK = "Track"
NAME = "Name"
DESCRIPTION = "Description"
YEAR = "Year"
LENGTH = "Length"
CORNERS = "Corners"


class TrackLayoutManager:

    def __init__(self, databaseConnection):

        self.databaseConnection: sqlite3.Connection = databaseConnection
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLENAME} (
                {ID} SMALLTEXT PRIMARY KEY,
                {TRACK} SMALLTEXT,
                {NAME} SMALLTEXT,
                {DESCRIPTION} SMALLTEXT,
                {YEAR} TINYTEXT,
                {LENGTH} REAL,
                {CORNERS} SMALLINT)
            """)
            
    def insertTrackLayout(self, layout: TrackLayout):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"INSERT INTO {TABLENAME} VALUES (?, ?, ?, ?, ?, ?, ?)"
            params = layout.toTuple()
            cursor.execute(query, params)
            self.databaseConnection.commit()

    def getTrackLayout(self, layoutID: str) -> TrackLayout:

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {ID} = ?"
            params = (layoutID, )
            cursor.execute(query, params)
            return TrackLayout(cursor.fetchone())

    def getTrackLayoutsForTrack(self, trackID: str):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {TRACK} = ?"
            params = (trackID, )
            cursor.execute(query, params)
            return [TrackLayout(output) for output in cursor.fetchall()]

    def updateTrackLayout(self, layout: TrackLayout):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"""
                UPDATE {TABLENAME}
                SET ({ID}, {TRACK}, {NAME}, {DESCRIPTION}, {YEAR}, {LENGTH}, {CORNERS})
                = (?, ?, ?, ?, ?, ?, ?)"""
            params = layout.toTuple() + (layout.id, )
            self.databaseConnection.commit()

    def deleteTrackLayout(self, layoutID: str):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"DELETE FROM {TABLENAME} WHERE {ID} = ?"
            params = (layoutID, )
            cursor.execute(query, params)
            self.databaseConnection.commit()