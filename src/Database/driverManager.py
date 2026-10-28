from discordLogger import DiscordLogger
import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.driver import Driver

TABLENAME = "DriverData"
THREECODE = "Threecode"
FIRSTNAME = "FirstName"
LASTNAME = "LastName"
NATIONALITY = "Nationality"
AGE = "Age"
QUALIPACE = "QualiPace"
RACEPACE = "RacePace"
WETPACE = "WetPace"
TYREMANAGEMENT = "TyreManagement"
AGGRESSIVENESS = "Aggressiveness"
DEFENDING = "Defending"
CONTRACTCOST = "ContractCost"
RACES = "Races"
WINS = "Wins"
PODIUMS = "Podiums"

class DriverManager:

    def __init__(self, databaseConnection):

        self.databaseConnection = databaseConnection
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLENAME} (
                {THREECODE} TINYTEXT PRIMARY KEY,
                {FIRSTNAME} SMALLTEXT,
                {LASTNAME} SMALLTEXT,
                {NATIONALITY} TINYTEXT,
                {AGE} TINYINT,
                {QUALIPACE} TINYINT,
                {RACEPACE} TINYINT,
                {WETPACE} TINYINT,
                {TYREMANAGEMENT} TINYINT,
                {AGGRESSIVENESS} TINYINT,
                {DEFENDING} TINYINT,
                {CONTRACTCOST} SMALLINT,
                {RACES} SMALLINT DEFAULT 0,
                {WINS} SMALLINT DEFAULT 0,
                {PODIUMS} SMALLINT DEFAULT 0)
            """)

    def insertDriver(self, driver: Driver):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""INSERT INTO {TABLENAME} VALUES ({driver.toTuple()})""")
            self.databaseConnection.commit()

    def updateDriver(self, driver: Driver) -> None:

        with closing(self.databaseConnection.cursor()) as cursor:
            
            cursor.execute(f"""
                UPDATE {TABLENAME}
                SET ({THREECODE}, {FIRSTNAME}, {LASTNAME}, {NATIONALITY}, {AGE}, {QUALIPACE}, {RACEPACE}, {WETPACE}, {TYREMANAGEMENT}, {AGGRESSIVENESS}, {DEFENDING}, {CONTRACTCOST}, {RACES}, {WINS}, {PODIUMS})
                = ({driver.toTuple()})
                WHERE {THREECODE} = {driver.threecode}
            """)
            self.databaseConnection.commit()

    def removeDriver(self, threecode: str):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"DELETE FROM {TABLENAME} WHERE {THREECODE} = {threecode}")
            self.databaseConnection.commit()

    def getDrivers(self) -> list[Driver]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME}")
            return [Driver(driverData) for driverData in cursor.fetchall()]

    def getDriver(self, threecode: str) -> Driver | None:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME} WHERE {THREECODE} = {threecode}")
            return Driver(cursor.fetchone())

    def getThreecodes(self) -> list[str]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT {THREECODE} FROM {TABLENAME}")
            return [row[0] for row in cursor.fetchall()]

    def ageAllDrivers(self) -> None:

        with closing(self.databaseConnection.cursor()) as cursor:
            try:
                #discLogger.info("Increasing all driver ages by 1")
                cursor.execute(f"UPDATE {TABLENAME} SET {AGE} = {AGE} + 1")
                #discLogger.info("Committing changes to database")
                self.databaseConnection.commit()
            except Exception as e:
                template = "An exception of type {0} occurred. Arguments: {1!r}"
                message = template.format(type(e).__name__, e.args)
                #discLogger.error(message)