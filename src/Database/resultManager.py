import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.result import Result

TABLENAME = "ResultData"
SEASONNO = "SeasonNo"
ROUNDNO = "RoundNo"
DRIVER = "Driver"
TEAM = "Team"
QUALIPOSITION = "QualiPosition"
QUALILAP = "QualiLap"
RACEPOSITION = "RacePosition"
RACEGAP = "RaceGap"
RACESTOPS = "RaceStops"
RACEFINISHSTATUS = "RaceFinishStatus"

class ResultManager:

    def __init__(self, databaseConnection):

        self.databaseConnection: sqlite3.Connection = databaseConnection

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLENAME} (
                {SEASONNO} INT NOT NULL,
                {ROUNDNO} INT NOT NULL,
                {DRIVER} INT NOT NULL,
                {TEAM} INT,
                {QUALIPOSITION} TINYINT,
                {QUALILAP} REAL,
                {RACEPOSITION} TINYINT,
                {RACEGAP} REAL,
                {RACESTOPS} TINYINT,
                {RACEFINISHSTATUS} TINYINT
            )""")

    def insertResult(self, result: Result):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"INSERT INTO {TABLENAME} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            params = result.toTuple()
            cursor.execute(query, params)

    def getRoundResultForDriver(self, driverID: int, roundNo: int, seasonNo: int) -> Result:

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {DRIVER} = ? AND {ROUNDNO} = ? AND {SEASONNO} = ?"
            params = (driverID, roundNo, seasonNo)
            cursor.execute(query, params)
            return Result(cursor.fetchone())

    def getSeasonResultsForDriver(self, driverID: int, seasonNo: int) -> list[Result]:

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {DRIVER} = ? AND {SEASONNO} = ?"
            params = (driverID, seasonNo)
            cursor.execute(query, params)
        return [Result(result) for result in cursor.fetchall()]

    def getAllResultsForDriver(self, driverID: int) -> list[Result]:

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {DRIVER} = ?"
            params = (driverID, )
            cursor.execute(query, params)
            return [Result(result) for result in cursor.fetchall()]
    
    def getRoundResultsForTeam(self, teamID: int, roundNo: int, seasonNo: int) -> list[Result]:

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {TEAM} = ? AND {ROUNDNO} = ? AND {SEASONNO} = ?"
            params = (teamID, roundNo, seasonNo)
            cursor.execute(query, params)
            return [Result(result) for result in cursor.fetchall()]

    def getSeasonResultsForTeam(self, teamID: int, seasonNo: int) -> list[Result]:

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {TEAM} = ? AND {SEASONNO} = ?"
            params = (teamID, seasonNo)
            cursor.execute(query, params)
            return [Result(result) for result in cursor.fetchall()]

    def getAllResultsForTeam(self, teamID: int) -> list[Result]:

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {TEAM} = ?"
            params = (teamID, )
            cursor.execute(query, params)
            return [Result(result) for result in cursor.fetchall()]

    def getResultsForEvent(self, seasonNo: int, roundNo: int) -> list[Result]:

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {ROUNDNO} = ? AND {SEASONNO} = ?"
            params = (roundNo, seasonNo)
            cursor.execute(query, params)
            return [Result(result) for result in cursor.fetchall()]

    def getResultsForSeason(self, seasonNo: int) -> list[Result]:

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {SEASONNO} = ?"
            params = (seasonNo, )
            cursor.execute(query, params)
            return [Result(result) for result in cursor.fetchall()]

    def getResults(self) -> list[Result]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME}")
            return [Result(result) for result in cursor.fetchall()]

    def updateResult(self, driverID, seasonNo, roundNo):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"""UPDATE {TABLENAME}
                SET ({SEASONNO}, {ROUNDNO}, {DRIVER}, {TEAM}, {QUALIPOSITION}, {QUALILAP}, {RACEPOSITION}, {RACEGAP}, {RACESTOPS}, {RACEFINISHSTATUS})
                = (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                WHERE {DRIVER} = ? AND {SEASONNO} = ? AND {ROUNDNO} = ?
            """
            params = (driverID, seasonNo, roundNo)
            cursor.execute(query, params)
            self.databaseConnection.commit()

    def deleteResult(self, driverID, seasonNo, roundNo):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"DELETE FROM {TABLENAME} WHERE {DRIVER} = ? AND {SEASONNO} = ? AND {ROUNDNO} = ?"
            params = (driverID, seasonNo, roundNo)
            cursor.execute(query, params)
            self.databaseConnection.commit()
