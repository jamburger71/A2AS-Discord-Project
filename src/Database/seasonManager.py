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
            query = f"INSERT INTO {TABLENAME} VALUES (?, ?, ?, ?, ?, ?)"
            params = season.toTuple()
            cursor.execute(query, params)
            self.databaseConnection.commit()
    
    def getSeason(self, seasonNo: int) -> Season:

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {SEASONNO} = ?"
            params = (seasonNo, )
            cursor.execute(query, params)
            return Season(cursor.fetchone())

    def getSeasons(self) -> list[Season]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME}")
            return [Season(season) for season in cursor.fetchall()]

    def updateSeason(self, season: Season):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"""
                UPDATE {TABLENAME} 
                SET ({SEASONNO}, {NAME}, {CLASS}, {YEAR}, {POINTSMODEL}, {POINTFORPOLE})
                = (?, ?, ?, ?, ?, ?)
                WHERE {SEASONNO} = ?
            """
            params = season.toTuple() + (season.seasonNo, )
            cursor.execute(query, params)
            self.databaseConnection.commit()

        def deleteSeason(self, seasonNo: int):

            with closing(self.databaseConnection.cursor()) as cursor:
                query = f"DELETE FROM {TABLENAME} WHERE {SEASONNO} = ?"
                params = (seasonNo, )
                cursor.execute(query, params)
                self.databaseConnection.commit()