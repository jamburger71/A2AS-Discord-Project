from discordLogger import DiscordLogger
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

        self.databaseConnection = databaseConnection
        
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
            cursor.execute(f"INSERT INTO {TABLENAME} VALUES {str(layout.toTuple())}")

    def getTrackLayout(self, layoutID: str) -> TrackLayout:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT 1 FROM {TABLENAME} WHERE {ID} = {layoutID}")
            return TrackLayout(cursor.fetchone())

    def getTrackLayoutsForTrack(self, trackID: str):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME} WHERE {TRACK} = {trackID}")
            return [TrackLayout(output) for output in cursor.fetchall()]

    def updateTrackLayout(self, layout: TrackLayout):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
            UPDATE {TABLENAME}
            SET ({ID}, {TRACK}, {NAME}, {DESCRIPTION}, {YEAR}, {LENGTH}, {CORNERS})
            = {str(layout.toTuple())}""")
            self.databaseConnection.commit()

    def deleteTrackLayout(self, layoutID: str):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"DELETE FROM {TABLENAME} WHERE {ID} = {layoutID}")
            self.databaseConnection.commit()