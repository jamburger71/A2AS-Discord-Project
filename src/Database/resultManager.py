from discord.search import SearchAuthorType

import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.result import Result
from Classes.driver import Driver
from Classes.event import Event

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

        self.databaseConnection = databaseConnection

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.commit(f"""
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
            cursor.execute(f"INSERT INTO {TABLENAME} VALUES {str(result.toTuple())}")

    def getRoundResultForDriver(self, driverID: int, roundNo: int, seasonNo: int) -> Result:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                SELECT 1 FROM {TABLENAME}
                WHERE {DRIVER} = {driverID}
                AND {ROUNDNO} = {roundNo}
                AND {SEASONNO} = {seasonNo}
            """)
            return Result(cursor.fetchone())

    def getSeasonResultsForDriver(self, driverID: int, seasonNo: int) -> list[Result]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                SELECT * FROM {TABLENAME}
                WHERE {DRIVER} = {driverID}
                AND {SEASONNO} = {seasonNo}
            """)
        return [Result(result) for result in cursor.fetchall()]

    def getAllResultsForDriver(self, driverID: int) -> list[Result]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME} WHERE {DRIVER} = {driverID}")
            return [Result(result) for result in cursor.fetchall()]
    
    def getRoundResultsForTeam(self, teamID: int, roundNo: int, seasonNo: int) -> list[Result]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                SELECT * FROM {TABLENAME}
                WHERE {TEAM} = {teamID}
                AND {ROUNDNO} = {roundNo}
                AND {SEASONNO} = {seasonNo}
            """)
            return [Result(result) for result in cursor.fetchall()]

    def getSeasonResultsForTeam(self, teamID: int, seasonNo: int) -> list[Result]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                SELECT * FROM {TABLENAME}
                WHERE {TEAM} = {teamID}
                AND {SEASONNO} = {seasonNo}
            """)
            return [Result(result) for result in cursor.fetchall()]

    def getAllResultsForTeam(self, teamID: int) -> list[Result]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME} WHERE {TEAM} = {teamID}")
            return [Result(result) for result in cursor.fetchall()]

    def getResultsForEvent(self, seasonNo: int, roundNo: int) -> list[Result]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                SELECT * FROM {TABLENAME}
                WHERE {ROUNDNO} = {roundNo}
                AND {SEASONNO} = {seasonNo}
                ORDER BY {RACEPOSITION}
            """)
            return [Result(result) for result in cursor.fetchall()]