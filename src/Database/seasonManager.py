import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.season import Season

TABLENAME = "SeasonData"
SEASONNO = "SeasonNo"
NAME = "Name"
CLASS = "Class"
YEAR = "Year"
POINTSMODEL = "PointsModel"
POINTFORPOLE = "PointForPole"

class SeasonManager:

    def __init__(self, databaseConnection):

        self.databaseConnection: sqlite3.Connection = databaseConnection

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLENAME} (
                {SEASONNO} INT PRIMARY KEY,
                {NAME} SMALLTEXT,
                {CLASS} SMALLTEXT,
                {YEAR} TINYINT,
                {POINTSMODEL} TINYINT,
                {POINTFORPOLE} TINYINT
            )""")

    def insertSeason(self, season: Season):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"INSERT INTO {TABLENAME} VALUES {str(season.toTuple())}")
    
    def getSeason(self, seasonNo: int) -> Season:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME} WHERE {SEASONNO} = {seasonNo} LIMIT 1")
            return Season(cursor.fetchone())

    def getSeasons(self) -> list[Season]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME}")
            return [Season(season) for season in cursor.fetchall()]

    def getCurrentSeason(self) -> Season:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT *, max({SEASONNO}) FROM {TABLENAME}")
            return Season(cursor.fetchone())

    def updateSeason(self, season: Season):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                UPDATE {TABLENAME} 
                SET ({SEASONNO}, {NAME}, {CLASS}, {YEAR}, {POINTSMODEL}, {POINTFORPOLE}) = {str(season.toTuple())}
            """)
            self.databaseConnection.commit()