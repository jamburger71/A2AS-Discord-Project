from discordLogger import DiscordLogger
import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.driver import Driver

TABLENAME = "DriverData"
ID = "ID"
ISACTIVE = "IsActive"
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

class DriverManager:

    def __init__(self, databaseConnection):

        self.databaseConnection = databaseConnection
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLENAME} (
                {ID} INT PRIMARY KEY,
                {ISACTIVE} TINYINT,
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
                {CONTRACTCOST} SMALLINT
            )""")

    def insertDriver(self, driver: Driver):

        with closing(self.databaseConnection.cursor()) as cursor:
            
            query = f"INSERT INTO {TABLENAME} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            params = driver.toTuple()
            cursor.execute(query, params)
            self.databaseConnection.commit()

    def updateDriver(self, driver: Driver) -> None:

        with closing(self.databaseConnection.cursor()) as cursor:
            
            query = f"""
                UPDATE {TABLENAME}
                SET ({ID}, {ISACTIVE}, {FIRSTNAME}, {LASTNAME}, {NATIONALITY}, {AGE}, {QUALIPACE}, {RACEPACE}, {WETPACE}, {TYREMANAGEMENT}, {AGGRESSIVENESS}, {DEFENDING}, {CONTRACTCOST})
                = (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                WHERE {ID} = ?
            """
            params = driver.toTuple() + (driver.ID, )
            cursor.execute(query, params)
            self.databaseConnection.commit()

    def removeDriver(self, driverID: int):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"DELETE FROM {TABLENAME} WHERE {ID} = ?"
            params = (driverID, )
            cursor.execute(query, params)
            self.databaseConnection.commit()

    def getDrivers(self) -> list[Driver]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME}")
            return [Driver.new(driverData) for driverData in cursor.fetchall()]

    def getActiveDrivers(self, getInactive: bool = False) -> list[Driver]:

        activeState = 0 if getInactive else 1
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {ISACTIVE} = ?"
            params = (activeState, )
            cursor.execute(query, params)
            return [Driver.new(driverData) for driverData in cursor.fetchall()]

    def getDriver(self, driverID) -> Driver | None:

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {ID} = ?"
            params = (driverID, )
            cursor.execute(query, params)
            return Driver.new(cursor.fetchone())

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

    def deactivateDriver(self, driverID):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"UPDATE {TABLENAME} SET {ISACTIVE} = 0 WHERE {ID} = {driverID}")