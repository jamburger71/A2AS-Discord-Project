import logging
import sqlite3
import yaml
import os
from contextlib import closing

class DriverManager:

    def __init__(self, databaseConnection):

        self.DatabaseConnection = databaseConnection

    def insertDriver(self, driverID: int, firstName: str, lastName: str, threeLetterCode: str, nationality: str, age: int, qualiPace: int, racePace: int, wetPace: int, tyreManagement: int, aggressiveness: int, defending: int, contractCost: int, isAvailable: bool = True):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                INSERT INTO DriverData (DriverID, FirstName, LastName, ThreeLetterCode, Nationality, Age, QualiPace, RacePace, WetPace, TyreManagement, Aggressiveness, Defending, ContractCost, IsAvailable)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (driverID, firstName, lastName, threeLetterCode, nationality, age, qualiPace, racePace, wetPace, tyreManagement, aggressiveness, defending, contractCost, isAvailable))
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

    def updateDriverStats(self, driverID: int, wins: bool = False, podiums: bool = False) -> None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            if wins:
                cursor.execute("UPDATE DriverData SET Wins = Wins + 1 WHERE DriverID = ?", (driverID,))
            if podiums:
                cursor.execute("UPDATE DriverData SET Podiums = Podiums + 1 WHERE DriverID = ?", (driverID,))
            cursor.execute("UPDATE DriverData SET Races = Races + 1 WHERE DriverID = ?", (driverID,))
            self.DatabaseConnection.commit()

    def updateDriverRatings(self, driverID: int, qualiPace: int | None = None, racePace: int | None = None, wetPace: int | None = None, tyreManagement: int | None = None, aggressiveness: int | None = None, defending: int | None = None) -> None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            if qualiPace is not None:
                cursor.execute("UPDATE DriverData SET QualiPace = ? WHERE DriverID = ?", (qualiPace, driverID))
            if racePace is not None:
                cursor.execute("UPDATE DriverData SET RacePace = ? WHERE DriverID = ?", (racePace, driverID))
            if wetPace is not None:
                cursor.execute("UPDATE DriverData SET WetPace = ? WHERE DriverID = ?", (wetPace, driverID))
            if tyreManagement is not None:
                cursor.execute("UPDATE DriverData SET TyreManagement = ? WHERE DriverID = ?", (tyreManagement, driverID))
            if aggressiveness is not None:
                cursor.execute("UPDATE DriverData SET Aggressiveness = ? WHERE DriverID = ?", (aggressiveness, driverID))
            if defending is not None:
                cursor.execute("UPDATE DriverData SET Defending = ? WHERE DriverID = ?", (defending, driverID))
            self.DatabaseConnection.commit()