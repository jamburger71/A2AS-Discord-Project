import logging
import sqlite3
import yaml
import os
from contextlib import closing

class DriverManager:

    def __init__(self, databaseConnection):

        self.DatabaseConnection = databaseConnection

    def insertDriver(self, firstName: str, lastName: str, threeLetterCode: str, nationality: str, age: int, qualiPace: int, racePace: int, wetPace: int, tyreManagement: int, aggressiveness: int, defending: int, contractCost: int, keyValManager):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            driverID = keyValManager.getNextDriverID(increment=True)
            print(f"Inserting driver with ID: {driverID}")
            cursor.execute("""
                INSERT INTO DriverData (DriverID, FirstName, LastName, ThreeLetterCode, Nationality, Age, QualiPace, RacePace, WetPace, TyreManagement, Aggressiveness, Defending, ContractCost)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (driverID, firstName, lastName, threeLetterCode, nationality, age, qualiPace, racePace, wetPace, tyreManagement, aggressiveness, defending, contractCost))
            self.DatabaseConnection.commit()

    def removeDriver(self, driverID: int | str):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            if isinstance(driverID, str):
                cursor.execute("""
                    DELETE FROM DriverData
                    WHERE ThreeLetterCode = ?
                """, (driverID,))
            else:
                cursor.execute("""
                    DELETE FROM DriverData
                    WHERE DriverID = ?
                """, (driverID,))
            self.DatabaseConnection.commit()

    def getAllDrivers(self, availableOnly: bool = False) -> list:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            if availableOnly:
                cursor.execute("SELECT * FROM DriverData WHERE IsAvailable = True")
            else:
                cursor.execute("SELECT * FROM DriverData")
            return cursor.fetchall()

    def getDriver(self, driverID: int | str) -> tuple | None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            if isinstance(driverID, str):
                cursor.execute("SELECT * FROM DriverData WHERE ThreeLetterCode = ?", (driverID,))
            else:
                cursor.execute("SELECT * FROM DriverData WHERE DriverID = ?", (driverID,))
            return cursor.fetchone()

    def getNextDriverID(self, keyValManager, increment: bool = False) -> int:

        driverID = keyValManager.getKeyVal("NextDriverID")
        if increment:
            keyValManager.updateKeyVal("NextDriverID", driverID + 1)
        print(f"Next driver ID: {driverID}")
        return driverID

    def checkDriverAvailability(self, driverID: int | str) -> bool:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            if isinstance(driverID, str):
                cursor.execute("SELECT IsAvailable FROM DriverData WHERE ThreeLetterCode = ?", (driverID,))
            else:
                cursor.execute("SELECT IsAvailable FROM DriverData WHERE DriverID = ?", (driverID,))
            result = cursor.fetchone()
            return result is not None

    def setDriverAvailability(self, driverID: int, isAvailable: bool) -> None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("UPDATE Drivers SET IsAvailable = ? WHERE DriverID = ?", (isAvailable, driverID))
            self.DatabaseConnection.commit()

    def ageAllDrivers(self) -> None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("UPDATE Drivers SET Age = Age + 1")
            self.DatabaseConnection.commit()
